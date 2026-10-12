# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright 2026 ValeLMS contributors
"""Installer/preflight contracts using synthetic keys and in-memory S3 only."""
import contextlib
import copy
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'deploy/installer'))
import policy


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


setup = module('guided_setup', 'deploy/setup.py')
preflight = module('setup_preflight', 'deploy/preflight.py')


class FakeStorage:
    def __init__(self, fail=False, cors=True):
        self.objects, self.uploads, self.calls = {}, {}, []
        self.fail, self.cors = fail, cors

    def client(self, settings, role):
        store = self

        class Client:
            def __getattr__(self, operation):
                def call(*positional, **args):
                    store.calls.append((role, operation, args))
                    bucket, key = args.get('Bucket'), args.get('Key')
                    if operation == 'head_bucket':
                        return {}
                    if operation == 'create_multipart_upload':
                        upload = str(len(store.calls))
                        store.uploads[upload] = (bucket, key)
                        return {'UploadId': upload}
                    if operation == 'generate_presigned_url':
                        return 'https://storage.example.invalid/synthetic-part'
                    if operation == 'list_parts':
                        return {'Parts': [{'Size': len(store.payload), 'ETag': 'synthetic-etag'}]}
                    if operation == 'complete_multipart_upload':
                        store.objects[bucket, key] = store.payload
                        del store.uploads[args['UploadId']]
                        return {}
                    if operation == 'abort_multipart_upload':
                        del store.uploads[args['UploadId']]
                        return {}
                    if operation == 'put_object':
                        if store.fail:
                            raise RuntimeError('sensitive-storage-details')
                        store.objects[bucket, key] = args['Body']
                        return {}
                    if operation == 'head_object':
                        return {'ContentLength': len(store.objects[bucket, key])}
                    if operation == 'get_object':
                        body = store.objects[bucket, key]
                        return {'Body': io.BytesIO(body[:8] if args.get('Range') else body)}
                    if operation == 'delete_object':
                        store.objects.pop((bucket, key), None)
                        return {}
                    raise AssertionError(operation)
                return call
        return Client()

    def http(self, url, data=None, method=None, **kwargs):
        headers = {'Access-Control-Allow-Origin': 'https://moodle.example.invalid',
            'Access-Control-Allow-Methods': 'PUT', 'Access-Control-Allow-Headers': 'content-type',
            'Access-Control-Expose-Headers': 'ETag' if self.cors else '', 'ETag': 'synthetic-etag'}
        if method == 'PUT':
            self.payload = data
        return 200, headers, b''


class InstallationUX(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=Path.home())
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.settings = json.loads((ROOT / 'deploy/operator-policy.json.example').read_text())
        for role in policy.STORAGE_ROLES:
            for key in ('access', 'secret'):
                path = self.root / f'{role}-{key}'
                setup.write_new(path, 'synthetic-not-a-real-credential')
                self.settings['storage_files'][role][key] = str(path)

    def test_policy_valid_r2_s3_and_invalid(self):
        self.assertEqual(policy.validate(self.settings)['storage_backend'], 's3-compatible')
        r2 = copy.deepcopy(self.settings)
        r2.update(storage_backend='r2', endpoint='https://' + '0' * 32 + '.r2.cloudflarestorage.com')
        policy.validate(r2)
        for delta in [{'endpoint': 'http://storage.example.invalid'}, {'endpoint': 'https://user:pass@example.invalid'},
                      {'endpoint': 'https://storage.example.invalid/path'}, {'endpoint': 'https://storage.example.invalid?key=secret'},
                      {'raw_bucket': self.settings['processed_bucket']}, {'storage_backend': 'filesystem'},
                      {'allowed_hosts': 'localhost\nINJECT=1'}, {'storage_addressing_style': 'unsafe'},
                      {'allowed_hosts': None}, {'storage_region': None}, {'storage_files': []}]:
            with self.subTest(delta=delta), self.assertRaises(ValueError):
                policy.validate({**self.settings, **delta})

    def test_guided_config_secret_modes_and_existing_refusal(self):
        answers = iter(['s3-compatible', 'https://moodle.example.invalid', 'https://video.example.invalid',
            'https://media.example.invalid', 'https://storage.example.invalid', 'videolesson-private-raw',
            'videolesson-private-processed'])
        dest = self.root / 'new'
        path = setup.configure(dest, lambda prompt: next(answers), lambda prompt: 'synthetic-only')
        config = policy.load(path)
        self.assertEqual(config['storage_region'], 'us-east-1')
        self.assertEqual(config['storage_addressing_style'], 'path')
        original = path.read_bytes()
        self.assertEqual(len(list(dest.iterdir())), 9, 'policy plus eight generated role credential files')
        with self.assertRaises(ValueError):
            setup.configure(dest)
        self.assertEqual(path.read_bytes(), original)
        if os.name == 'posix':
            self.assertEqual(dest.stat().st_mode & 0o777, 0o700)
            self.assertTrue(all(p.stat().st_mode & 0o777 == 0o600 for p in dest.iterdir()))

    @unittest.skipUnless(os.name == 'posix', 'POSIX permissions/symlinks')
    def test_unsafe_secret_modes_and_symlinks(self):
        path = Path(self.settings['storage_files']['api']['secret'])
        path.chmod(0o644)
        with self.assertRaises(ValueError):
            policy.validate(self.settings)
        path.chmod(0o600)
        link = self.root / 'link'
        link.symlink_to(path)
        with self.assertRaises(ValueError):
            policy.protected_file(link)
        with self.assertRaises(ValueError):
            setup.configure(link)

    def test_scoped_write_probe_complete_and_cleanup(self):
        storage = FakeStorage()
        self.assertTrue(preflight.storage_probe(self.settings, storage.client, storage.http))
        self.assertEqual(storage.objects, {})
        self.assertEqual(storage.uploads, {})
        roles = {(r, op) for r, op, args in storage.calls}
        self.assertIn(('gateway', 'get_object'), roles)
        self.assertIn(('worker', 'put_object'), roles)
        self.assertIn(('janitor', 'delete_object'), roles)
        self.assertTrue(all(args.get('Key', 'valelms-preflight/').startswith('valelms-preflight/')
                            for _, _, args in storage.calls))

    def test_probe_failures_cleanup_exact_own_keys(self):
        for settings in ({'fail': True}, {'cors': False}):
            storage = FakeStorage(**settings)
            with self.assertRaises(Exception):
                preflight.storage_probe(self.settings, storage.client, storage.http)
            self.assertEqual(storage.objects, {})
            self.assertEqual(storage.uploads, {})

    def test_signed_capabilities_without_credential_output(self):
        handoff = self.root / 'connection.json'
        setup.write_new(handoff, json.dumps({'endpoint': 'https://video.example.invalid', 'tenant': 'synthetic-tenant',
            'keyid': 'installation-1', 'key': 'synthetic-key-not-real'}))
        ready = dict(protocol_version=2, service_version='0.5.0-rc2', schema_versions=[1, 2, 3, 4, 5],
            max_duration_seconds=21600, schema_ready=True, storage_config_valid=True,
            raw_reachable=True, processed_reachable=True, redis_ready=True, worker_capacity_ready=True)
        for delta, expected in [({}, True), ({'protocol_version': 1}, False), ({'raw_reachable': False}, False),
                                ({'worker_capacity_ready': False}, False), ({'max_duration_seconds': 43200}, False)]:
            def http(url, **kwargs):
                self.assertEqual(url, 'https://video.example.invalid/v2/rpc')
                self.assertNotIn('key', json.loads(kwargs['data']))
                self.assertIn('X-VL-Signature', kwargs['headers'])
                return 200, {}, json.dumps({'data': {**ready, **delta}}).encode()
            self.assertEqual(preflight.capabilities(handoff, http), expected)

    def test_preflight_offline_does_not_network_or_change_state(self):
        config = self.root / 'policy.json'
        setup.write_new(config, json.dumps(self.settings))
        before = {p.name: p.read_bytes() for p in self.root.iterdir()}
        with patch.object(preflight, 'request', side_effect=AssertionError('network forbidden')), \
             patch.object(preflight.socket, 'getaddrinfo', side_effect=AssertionError('network forbidden')), \
             patch.object(preflight.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0)), \
             contextlib.redirect_stdout(io.StringIO()) as output:
            preflight.main(['--config', str(config), '--staging', str(self.root)])
        self.assertEqual({p.name: p.read_bytes() for p in self.root.iterdir()}, before)
        self.assertIn('PENDING', output.getvalue())
        self.assertNotIn('synthetic-not-a-real-credential', output.getvalue())

    @unittest.skipUnless(sys.platform == 'linux' and os.geteuid() == 0, 'root Linux configuration generation')
    def test_real_compose_preparer_guard_and_rerun(self):
        config = self.root / 'policy.json'
        setup.write_new(config, json.dumps(self.settings))
        directory = self.root / 'runtime'
        # Generic S3 secrets may contain interpolation characters; preserve exact bytes.
        canary = 'synthetic-$UNSET_CANARY#quoted"value'
        Path(self.settings['storage_files']['api']['secret']).write_text(canary)
        command = [sys.executable, str(ROOT / 'deploy/docker/prepare.py'),
                   '--directory', str(directory), '--config', str(config)]
        first = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        self.assertNotIn('synthetic-not-a-real-credential', first.stdout + first.stderr)
        state = json.loads((directory / 'installation.json').read_text())
        self.assertEqual(len(state['rpc']), 64)
        for role in ('api', 'gateway', 'worker', 'janitor'):
            env = dict(line.split('=', 1) for line in (directory / (role + '.env')).read_text().splitlines())
            self.assertEqual(env['STORAGE_BACKEND'], 's3-compatible')
            self.assertEqual(env['STORAGE_REGION'], 'us-east-1')
            self.assertEqual(env['RAW_BUCKET'], self.settings['raw_bucket'])
            self.assertEqual(env['R2_SECRET_KEY'], canary if role == 'api' else 'synthetic-not-a-real-credential')
            self.assertEqual((directory / (role + '.env')).stat().st_mode & 0o777, 0o600)
        rendered = subprocess.run(['docker', 'compose', '-f', str(ROOT / 'deploy/docker/compose.yaml'),
            'config', '--format', 'json'], env={**os.environ, 'VIDEO_CONFIG': str(directory)},
            capture_output=True, text=True)
        self.assertEqual(rendered.returncode, 0, 'Compose configuration did not parse')
        # Compose serializes literal dollars as $$ so its rendered model is reusable.
        rendered_secret = json.loads(rendered.stdout)['services']['api']['environment']['R2_SECRET_KEY']
        self.assertEqual(rendered_secret, canary.replace('$', '$$'))
        self.assertEqual((ROOT / 'deploy/docker/compose.yaml').read_text().count('format: raw'), 6)
        before = {p.name: p.read_bytes() for p in directory.iterdir() if p.is_file()}
        self.assertEqual(len(before), 12, 'existing preparer generates twelve runtime files')
        again = subprocess.run(command, capture_output=True, text=True)
        self.assertNotEqual(again.returncode, 0)
        self.assertEqual({p.name: p.read_bytes() for p in directory.iterdir() if p.is_file()}, before)

    def test_signed_readiness_auth_failure_and_sanitized_output(self):
        config = self.root / 'policy.json'
        setup.write_new(config, json.dumps(self.settings))
        with patch.object(preflight.socket, 'getaddrinfo', side_effect=RuntimeError('sensitive-address')), \
             patch.object(preflight, 'request', side_effect=RuntimeError('sensitive-token-or-error')), \
             patch.object(preflight.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0)), \
             contextlib.redirect_stdout(io.StringIO()) as output:
            result = preflight.main(['--config', str(config), '--staging', str(self.root), '--online',
                '--handoff', str(self.root / 'missing')])
        self.assertEqual(result, 1)
        self.assertNotIn('sensitive-', output.getvalue())
        self.assertIn('FAIL', output.getvalue())

    def test_compose_version_contract(self):
        for value, expected in [('2.29.1', False), ('2.30.0', True), ('v5.6.0', True), ('unrecognized', False)]:
            with patch.object(preflight.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, value)):
                self.assertEqual(bool(preflight.compose_supported()), expected)

    @unittest.skipUnless(sys.platform == 'linux', 'Linux mountinfo')
    def test_staging_rejects_ram_and_shared_permissions(self):
        original = Path.read_text
        for filesystem, expected in [('ext4', True), ('tmpfs', False), ('ramfs', False)]:
            def read(path, *args, **kwargs):
                if str(path) == '/proc/self/mountinfo':
                    return '1 0 0:1 / / rw - ' + filesystem + ' root rw\n'
                return original(path, *args, **kwargs)
            with patch.object(Path, 'read_text', read), \
                 patch.object(preflight.shutil, 'disk_usage', return_value=type('Disk', (), {'free': 2 * 1024**3})()):
                self.assertEqual(preflight.staging_ready(self.root), expected)
        self.root.chmod(0o755)
        self.assertFalse(preflight.staging_ready(self.root))
        self.root.chmod(0o700)


if __name__ == '__main__':
    unittest.main()
