# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright 2026 ValeLMS contributors
"""Opt-in preflight integration against a NEW disposable local MinIO, no media/LMS.

Requires existing cached MinIO/mc images; never pulls, edits or stops other stacks.
"""
import importlib.util
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('preflight', ROOT / 'deploy/preflight.py')
preflight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preflight)
MINIO = 'quay.io/minio/minio:RELEASE.2025-04-22T22-12-26Z'
MC = 'quay.io/minio/mc:RELEASE.2025-04-16T18-13-26Z'


def run(command, **kwargs):
    result = subprocess.run(command, capture_output=True, timeout=90, **kwargs)
    if result.returncode:
        raise RuntimeError('Disposable storage command failed (sensitive output withheld)')
    return result.stdout


def main():
    if sys.platform != 'linux':
        raise RuntimeError('Run inside the independent Linux test environment')
    suffix = secrets.token_hex(6)
    name = 'valelms-install-ux-' + suffix
    created = False
    with tempfile.TemporaryDirectory(prefix='valelms-install-ux-', dir=Path.home()) as directory:
        work = Path(directory)
        certs = work / 'certs'
        certs.mkdir(mode=0o700)
        run(['openssl', 'req', '-x509', '-newkey', 'rsa:2048', '-nodes', '-days', '1',
             '-keyout', str(certs / 'private.key'), '-out', str(certs / 'public.crt'),
             '-subj', '/CN=localhost', '-addext', 'subjectAltName=DNS:localhost,IP:127.0.0.1'])
        admin_access, admin_secret = 'probe' + suffix, secrets.token_hex(32)
        private_env = work / 'storage.env'
        private_env.write_text('MINIO_ROOT_USER=' + admin_access + '\nMINIO_ROOT_PASSWORD=' + admin_secret + '\n' +
            'MINIO_API_CORS_ALLOW_ORIGIN=https://moodle.example.invalid\n')
        private_env.chmod(0o600)
        mcenv = work / 'mc.env'
        mcenv.write_text(f'MC_HOST_probe=https://{admin_access}:{admin_secret}@localhost:31230\n')
        mcenv.chmod(0o600)

        def mc(*args):
            return run(['docker', 'run', '--rm', '--pull=never', '--network', 'host', '--env-file', str(mcenv),
                '-v', str(certs / 'public.crt') + ':/root/.mc/certs/CAs/probe.crt:ro',
                '-v', str(work) + ':/probe:ro', MC, *args])

        try:
            run(['docker', 'run', '-d', '--pull=never', '--name', name, '--label', 'valelms.install-ux=' + suffix,
                '-p', '127.0.0.1:31230:9000', '--env-file', str(private_env),
                '-v', str(certs) + ':/certs:ro', '--tmpfs', '/data:size=64m', MINIO,
                'server', '/data', '--certs-dir', '/certs', '--address', ':9000'])
            created = True
            for attempt in range(20):
                try:
                    mc('ready', 'probe')
                    break
                except RuntimeError:
                    if attempt == 19:
                        raise
                    time.sleep(1)
            raw, processed = 'videolesson-test-raw', 'videolesson-test-processed'
            mc('mb', 'probe/' + raw)
            mc('mb', 'probe/' + processed)
            settings = dict(storage_backend='s3-compatible', endpoint='https://localhost:31230',
                storage_region='us-east-1', storage_addressing_style='path',
                storage_ca_bundle=str(certs / 'public.crt'), moodle_origin='https://moodle.example.invalid',
                service_origin='https://video.example.invalid', gateway_origin='https://media.example.invalid',
                allowed_hosts='video.example.invalid,media.example.invalid', raw_bucket=raw,
                processed_bucket=processed, storage_files={})
            for role in preflight.policy.STORAGE_ROLES:
                access, secret = 'role' + role + suffix, secrets.token_hex(32)
                settings['storage_files'][role] = {}
                for key, value in [('access', access), ('secret', secret)]:
                    path = work / (role + '-' + key)
                    path.write_text(value)
                    path.chmod(0o600)
                    settings['storage_files'][role][key] = str(path)
                bucket_resources = ['arn:aws:s3:::' + b for b in ((processed,) if role == 'gateway' else (raw, processed))]
                statements = [dict(Effect='Allow', Action=['s3:ListBucket'], Resource=bucket_resources)]
                actions = {
                    'api': {raw: ['s3:GetObject', 's3:PutObject', 's3:DeleteObject', 's3:AbortMultipartUpload', 's3:ListMultipartUploadParts']},
                    'worker': {raw: ['s3:GetObject'], processed: ['s3:PutObject', 's3:GetObject']},
                    'gateway': {processed: ['s3:GetObject']},
                    'janitor': {raw: ['s3:DeleteObject'], processed: ['s3:DeleteObject']},
                }
                for bucket, operations in actions[role].items():
                    statements.append(dict(Effect='Allow', Action=operations, Resource=['arn:aws:s3:::' + bucket + '/*']))
                path = work / (role + '.json')
                path.write_text(json.dumps({'Version': '2012-10-17', 'Statement': statements}))
                mc('admin', 'user', 'add', 'probe', access, secret)
                mc('admin', 'policy', 'create', 'probe', role, '/probe/' + path.name)
                mc('admin', 'policy', 'attach', 'probe', role, '--user', access)
            preflight.policy.validate(settings)
            assert preflight.storage_probe(settings)
            assert not mc('ls', '--recursive', '--json', 'probe/' + raw).strip()
            assert not mc('ls', '--recursive', '--json', 'probe/' + processed).strip()
            assert not mc('ls', '--incomplete', '--recursive', '--json', 'probe/' + raw).strip()
            untrusted = False
            try:
                preflight.request(settings['endpoint'] + '/minio/health/ready')
            except Exception:
                untrusted = True
            assert untrusted  # Default trust must not accept the private test certificate.
            # Independent permission negative: gateway can never read a raw object.
            denied = False
            try:
                preflight.s3_client(settings, 'gateway').head_bucket(Bucket=raw)
            except Exception:
                denied = True
            assert denied
            report = {'result': 'PASS', 'scope': 'new disposable local storage only, no media/LMS',
                'provider': MINIO, 'tls': 'verified private one-day test certificate',
                'role_credentials': 'distinct synthetic least-privilege identities',
                'multipart_presigned_put_list_complete_abort': 'PASS', 'cors_options_etag': 'PASS',
                'raw_processed_head_read_write_range_cleanup': 'PASS', 'gateway_raw_denied': True,
                'untrusted_certificate_rejected': True, 'objects_and_incomplete_uploads_remaining': 0,
                'existing_stacks_changed': False}
            path = ROOT / '.lab/evidence/development/installation-ux/STORAGE-PROBE.json'
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(report, indent=2) + '\n')
            print(json.dumps(report, indent=2))
        finally:
            if created:
                # Exact newly-created random name only; no volume, bucket or other stack pruning.
                run(['docker', 'rm', '-f', name])


if __name__ == '__main__':
    try:
        main()
    except Exception:
        print('STORAGE_PROBE_TEST=FAIL; sensitive subprocess/storage output withheld')
        sys.exit(1)
