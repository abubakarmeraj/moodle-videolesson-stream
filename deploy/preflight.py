#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright 2026 ValeLMS contributors
"""Non-destructive setup checks. Network and scoped synthetic writes are opt-in."""
import argparse
import hashlib
import hmac
import json
import os
from pathlib import Path
import platform
import re
import secrets
import shutil
import socket
import ssl
import subprocess
import sys
import time
from urllib.parse import urlsplit
import urllib.request

sys.path.insert(0, str(Path(__file__).resolve().parent / 'installer'))
import policy


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # Never forward a signature/bearer token to another endpoint.


def request(url, data=None, method=None, headers=None, ca=None):
    parsed = urlsplit(url)
    policy.origin(parsed.scheme + '://' + parsed.netloc)
    context = ssl.create_default_context(cafile=ca)
    opener = urllib.request.build_opener(NoRedirect(), urllib.request.HTTPSHandler(context=context))
    with opener.open(urllib.request.Request(url, data=data, method=method, headers=headers or {}), timeout=20) as response:
        return response.status, response.headers, response.read(65537)


def s3_client(settings, role):
    # Use the SAME pinned dependencies/options as the runtime. No extra dependency.
    import boto3
    from botocore.config import Config
    files = settings['storage_files'][role]
    return boto3.client('s3', endpoint_url=settings['endpoint'],
        aws_access_key_id=policy.protected_file(files['access']).strip(),
        aws_secret_access_key=policy.protected_file(files['secret']).strip(),
        region_name=settings.get('storage_region', 'auto' if settings['storage_backend'] == 'r2' else 'us-east-1'),
        verify=settings.get('storage_ca_bundle', True),
        config=Config(signature_version='s3v4', connect_timeout=5, read_timeout=20,
            retries={'max_attempts': 2, 'mode': 'standard'},
            s3={'addressing_style': settings.get('storage_addressing_style', 'path')},
            request_checksum_calculation='when_required', response_checksum_validation='when_required'))


def storage_probe(settings, client=s3_client, http=request):
    """Only randomly named synthetic objects; never change IAM/CORS/buckets."""
    clients = {role: client(settings, role) for role in policy.STORAGE_ROLES}
    raw, processed = settings['raw_bucket'], settings['processed_bucket']
    key = 'valelms-preflight/' + secrets.token_hex(24)
    payload = b'ValeLMS synthetic storage permission probe\n'
    pending = []
    clean = True
    try:
        for role in clients:
            for bucket in ((processed,) if role == 'gateway' else (raw, processed)):
                clients[role].head_bucket(Bucket=bucket)
        api = clients['api']
        upload = api.create_multipart_upload(Bucket=raw, Key=key)['UploadId']
        pending.append(upload)
        url = api.generate_presigned_url('upload_part', Params={
            'Bucket': raw, 'Key': key, 'UploadId': upload, 'PartNumber': 1}, ExpiresIn=60)
        status, headers, _ = http(url, method='OPTIONS', headers={'Origin': settings['moodle_origin'],
            'Access-Control-Request-Method': 'PUT', 'Access-Control-Request-Headers': 'content-type'},
            ca=settings.get('storage_ca_bundle'))
        if (status not in (200, 204) or headers.get('Access-Control-Allow-Origin') != settings['moodle_origin'] or
                'PUT' not in headers.get('Access-Control-Allow-Methods', '').upper() or
                not any(h.strip().lower() in ('content-type', '*') for h in
                        headers.get('Access-Control-Allow-Headers', '').split(','))):
            raise ValueError('cors_preflight')
        status, headers, _ = http(url, data=payload, method='PUT',
            headers={'Origin': settings['moodle_origin'], 'Content-Type': 'application/octet-stream'},
            ca=settings.get('storage_ca_bundle'))
        etag = headers.get('ETag')
        if (status != 200 or not etag or headers.get('Access-Control-Allow-Origin') != settings['moodle_origin'] or
                'etag' not in [h.strip().lower() for h in headers.get('Access-Control-Expose-Headers', '').split(',')]):
            raise ValueError('cors_receipt')
        parts = api.list_parts(Bucket=raw, Key=key, UploadId=upload)['Parts']
        if len(parts) != 1 or parts[0]['Size'] != len(payload):
            raise ValueError('multipart_receipt')
        api.complete_multipart_upload(Bucket=raw, Key=key, UploadId=upload,
            MultipartUpload={'Parts': [{'PartNumber': 1, 'ETag': etag}]})
        pending.remove(upload)
        if clients['worker'].get_object(Bucket=raw, Key=key)['Body'].read() != payload:
            raise ValueError('raw_read')
        if api.head_object(Bucket=raw, Key=key)['ContentLength'] != len(payload):
            raise ValueError('raw_size')
        worker = clients['worker']
        worker.put_object(Bucket=processed, Key=key, Body=payload)
        if worker.head_object(Bucket=processed, Key=key)['ContentLength'] != len(payload):
            raise ValueError('processed_size')
        if clients['gateway'].get_object(Bucket=processed, Key=key, Range='bytes=0-7')['Body'].read() != payload[:8]:
            raise ValueError('range_read')
        if clients['gateway'].get_object(Bucket=processed, Key=key)['Body'].read() != payload:
            raise ValueError('processed_read')
        abandoned = api.create_multipart_upload(Bucket=raw, Key=key)['UploadId']
        pending.append(abandoned)
        api.abort_multipart_upload(Bucket=raw, Key=key, UploadId=abandoned)
        pending.remove(abandoned)
    finally:
        # Only exact keys/upload IDs created by THIS invocation, even after a failed PUT.
        for upload in pending:
            try:
                clients['api'].abort_multipart_upload(Bucket=raw, Key=key, UploadId=upload)
            except Exception:
                clean = False
        for bucket in (raw, processed):
            try:
                clients['janitor'].delete_object(Bucket=bucket, Key=key)
            except Exception:
                clean = False
        if not clean:
            raise ValueError('probe_cleanup_failed')
    return True


def capabilities(handoff, http=request):
    data = json.loads(policy.protected_file(handoff, group_read=True))
    policy.origin(data['endpoint'])
    body = json.dumps({'tenant': data['tenant'], 'op': 'capabilities'}, separators=(',', ':')).encode()
    timestamp, nonce = str(int(time.time())), secrets.token_hex(32)
    canonical = '\n'.join(['POST', '/v2/rpc', data['keyid'], timestamp, nonce, hashlib.sha256(body).hexdigest()])
    signature = hmac.new(data['key'].encode(), canonical.encode(), hashlib.sha256).hexdigest()
    status, _, result = http(data['endpoint'] + '/v2/rpc', data=body, headers={'Content-Type': 'application/json',
        'X-VL-Key': data['keyid'], 'X-VL-Time': timestamp, 'X-VL-Nonce': nonce, 'X-VL-Signature': signature})
    response = json.loads(result)['data']
    return (status == 200 and response.get('protocol_version') == 2 and response.get('service_version') == '0.5.0' and
        type(response.get('max_duration_seconds')) is int and 60 <= response['max_duration_seconds'] <= 21600 and
        response.get('schema_versions') == [1, 2, 3, 4, 5] and all(response.get(k) is True for k in
        ('schema_ready', 'storage_config_valid', 'raw_reachable', 'processed_reachable', 'redis_ready', 'worker_capacity_ready')))


def compose_supported():
    result = subprocess.run(['docker', 'compose', 'version', '--short'], capture_output=True, text=True, timeout=15)
    version = re.match(r'v?(\d+)\.(\d+)', result.stdout or '')
    return result.returncode == 0 and version and tuple(map(int, version.groups())) >= (2, 30)


def staging_ready(path):
    if not path.is_dir() or path.is_symlink() or path.stat().st_mode & 0o077:
        return False
    resolved = path.resolve()
    mounts = []
    for line in Path('/proc/self/mountinfo').read_text().splitlines():
        before, after = line.split(' - ', 1)
        mount = Path(before.split()[4].replace('\\040', ' '))
        if resolved.is_relative_to(mount):
            mounts.append((len(mount.parts), after.split()[0]))
    if not mounts or max(mounts)[1] in ('tmpfs', 'ramfs'):
        return False
    return shutil.disk_usage(path).free >= 1024**3


def ports_available(api, gateway):
    if api == gateway or any(not 1024 <= p <= 65535 for p in (api, gateway)):
        return False
    sockets = []
    try:
        for port in (api, gateway):
            sock = socket.socket()
            sockets.append(sock)
            sock.bind(('127.0.0.1', port))
        return True
    except OSError:
        return False
    finally:
        for sock in sockets:
            sock.close()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--staging', type=Path, required=True)
    parser.add_argument('--online', action='store_true', help='DNS/TLS/health checks of explicit operator origins')
    parser.add_argument('--handoff', type=Path, help='Protected connection file for authenticated readiness')
    parser.add_argument('--storage-probe', action='store_true', help='Explicitly create/delete tiny synthetic objects and multipart uploads')
    parser.add_argument('--check-ports', action='store_true', help='Before first startup, check selected loopback bindings are unused')
    parser.add_argument('--api-port', type=int, default=28090)
    parser.add_argument('--gateway-port', type=int, default=28091)
    args = parser.parse_args(argv)
    if (args.storage_probe or args.handoff) and not args.online:
        parser.error('--storage-probe/--handoff require --online')
    results = []

    def check(name, operation, guidance):
        try:
            passed = bool(operation())
        except Exception:
            passed = False  # Never print SDK/TLS/HTTP bodies, endpoint URLs or credentials.
        results.append({'check': name, 'result': 'PASS' if passed else 'FAIL',
                        'guidance': '' if passed else guidance})
        return passed

    check('Linux architecture', lambda: sys.platform == 'linux' and platform.machine() in ('x86_64', 'aarch64'),
          'Use supported Ubuntu 24.04 amd64/arm64; other hosts require separate qualification.')
    check('Host resources', lambda: (os.cpu_count() or 0) >= 2 and
          os.sysconf('SC_PHYS_PAGES') * os.sysconf('SC_PAGE_SIZE') >= 4 * 1024**3,
          'Plan at least 2 CPUs/4 GiB for a small smoke; shared Moodle and large jobs require more headroom.')
    check('Docker daemon', lambda: subprocess.run(['docker', 'info'], capture_output=True, timeout=15).returncode == 0,
          'Install/start Docker Engine; grant appropriate operator access. Preflight does not start it.')
    check('Compose plugin >= 2.30', compose_supported,
          'Install Compose >= 2.30 (including v5) for raw env-file secret preservation; do not print compose config output.')
    if args.check_ports:
        check('Unused API/gateway loopback ports', lambda: ports_available(args.api_port, args.gateway_port),
              'Select distinct unused ports via VIDEO_API_PORT/VIDEO_GATEWAY_PORT; pass the same values to preflight and update HTTPS upstreams. Do not stop another stack. Omit --check-ports after startup.')
    check('Private staging disk', lambda: staging_ready(args.staging),
          'Provide mode-0700 disk-backed (not tmpfs/ramfs) staging with at least 1 GiB free for a short smoke. This is NOT large-video admission.')
    try:
        settings = policy.load(args.config)
        results.append({'check': 'Protected operator configuration', 'result': 'PASS', 'guidance': ''})
    except Exception:
        results.append({'check': 'Protected operator configuration', 'result': 'FAIL',
            'guidance': 'Use setup.py or validated HTTPS policy with distinct buckets, role key files and private permissions.'})
        settings = None
    if settings and args.online:
        for name in ('moodle_origin', 'service_origin', 'gateway_origin', 'endpoint'):
            url = urlsplit(settings[name])

            def tls(url=url):
                socket.getaddrinfo(url.hostname, url.port or 443)
                context = ssl.create_default_context(cafile=settings.get('storage_ca_bundle') if name == 'endpoint' else None)
                with socket.create_connection((url.hostname, url.port or 443), timeout=10) as sock:
                    with context.wrap_socket(sock, server_hostname=url.hostname):
                        return True
            check(name + ' DNS and trusted TLS', tls, 'Correct DNS, certificate chain and routing from THIS host; also test from Moodle and browser hosts.')
        for name in ('service_origin', 'gateway_origin'):
            check(name + ' health', lambda name=name: json.loads(request(settings[name] + '/health')[2]).get('ready') is True,
                  'Build/start the correct Compose roles and trusted HTTPS proxy. Health is not storage write readiness.')
        if args.handoff:
            check('Authenticated protocol/schema/storage/Redis/capacity', lambda: capabilities(args.handoff),
                  'Use matched service 0.5.0/protocol 2, migrations 001-005, protected handoff, role permissions and a fresh worker heartbeat. Run Moodle Test Connection.')
        else:
            results.append({'check': 'Authenticated readiness', 'result': 'PENDING', 'guidance': 'After startup add --handoff runtime/moodle-connection.json and --online.'})
        if args.storage_probe:
            check('Role storage multipart/read/write/range/CORS/cleanup', lambda: storage_probe(settings),
                  'Install locked service dependencies in the operator venv. Check role IAM, BOTH buckets, writable volumes, exact-origin CORS/ETag and cleanup. HEAD alone is insufficient. Never print signed URLs.')
        else:
            results.append({'check': 'Storage write probe', 'result': 'PENDING', 'guidance': 'Use --storage-probe explicitly; creates/deletes only tiny random synthetic objects.'})
    else:
        results.append({'check': 'Network/storage/readiness', 'result': 'PENDING', 'guidance': 'Local-only run; use --online after endpoint setup and --storage-probe to test actual writes.'})
    results.append({'check': 'Browser and Moodle-host verification', 'result': 'PENDING',
        'guidance': 'This host cannot prove another browser/PHP host reachability. Test Connection, then a short native browser upload/playback/completion are still required.'})
    print(json.dumps({'checks': results, 'scope': 'installation preflight, NOT complete media qualification'}, indent=2))
    return 1 if any(r['result'] == 'FAIL' for r in results) else 0


if __name__ == '__main__':
    sys.exit(main())
