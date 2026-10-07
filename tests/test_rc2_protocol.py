# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright 2026 ValeLMS contributors
"""Protocol-2 canonicalization/replay boundaries plus explicit protocol-1 aliases."""
import base64
from contextlib import contextmanager
import hashlib
import hmac
import importlib
import json
import time
import unittest
from unittest.mock import patch
from starlette.datastructures import Headers
from test_os1_baseline import configuration


class Protocol(unittest.TestCase):
    def setUp(self):
        self.cfg = configuration(SERVICE_ROLE='api', SERVICE_KEY_ID='test-key',
                                 SERVICE_AUTH_KEY='a' * 32, GRANT_KEY='g' * 32)
        self.security = importlib.import_module('service.security')
        self.nonces = set()
        outer = self
        class Cursor:
            def execute(self, sql, args):
                if sql.startswith('INSERT'):
                    key = tuple(args[:2])
                    if key in outer.nonces:
                        raise RuntimeError('duplicate')
                    outer.nonces.add(key)
        @contextmanager
        def transaction():
            yield Cursor()
        self.patches = [patch.object(self.security, 'config', self.cfg),
                        patch.object(self.security, 'transaction', transaction)]
        for p in self.patches: p.start()
        self.addCleanup(lambda: [p.stop() for p in reversed(self.patches)])
        self.body = b'{"op":"capabilities"}'

    def headers(self, path='/v2/rpc', nonce='b' * 64):
        timestamp = str(int(time.time()))
        canonical = '\n'.join(['POST', path, 'test-key', timestamp, nonce,
                                hashlib.sha256(self.body).hexdigest()])
        signature = hmac.new(self.cfg.AUTH_KEY.encode(), canonical.encode(), hashlib.sha256).hexdigest()
        prefix = 'x-vl-' if path == '/v2/rpc' else 'x-cf-'
        return Headers({prefix + k: v for k, v in zip(('key', 'time', 'nonce', 'signature'),
                                                    ('test-key', timestamp, nonce, signature))})

    def test_new_and_legacy_canonical_auth(self):
        self.security.authenticate(self.headers(), self.body, '/v2/rpc')
        self.security.authenticate(self.headers('/v1/rpc', 'c' * 64), self.body, '/v1/rpc')

    def test_replay_rejected_across_protocols(self):
        self.security.authenticate(self.headers(), self.body, '/v2/rpc')
        with self.assertRaises(self.security.Rejected) as error:
            self.security.authenticate(self.headers('/v1/rpc'), self.body, '/v1/rpc')
        self.assertEqual(error.exception.code, 'service_replay')

    def test_wrong_path_body_family_and_duplicates(self):
        h = self.headers()
        wrong_signature = dict(h)
        wrong_signature['x-vl-signature'] = '0' * 64
        mixed = dict(h) | {'x-cf-key': 'test-key'}
        duplicates = Headers(raw=h.raw + [(b'x-vl-key', b'test-key')])
        for headers, body, path in [(h, self.body, '/v1/rpc'), (h, b'changed', '/v2/rpc'),
                (self.headers('/v1/rpc'), self.body, '/v2/rpc'),
                (wrong_signature, self.body, '/v2/rpc'), (mixed, self.body, '/v2/rpc'),
                (duplicates, self.body, '/v2/rpc')]:
            with self.subTest(path=path), self.assertRaises(self.security.Rejected):
                self.security.authenticate(headers, body, path)

    def test_legacy_disabled(self):
        with patch.object(self.cfg, 'ALLOW_LEGACY_PROTOCOL', False):
            with self.assertRaises(self.security.Rejected):
                self.security.authenticate(self.headers('/v1/rpc'), self.body, '/v1/rpc')

    def token(self, audience, **overrides):
        payload = {'aud': audience, 'tenant': self.cfg.TENANT,
                   'video': '11111111-1111-4111-8111-111111111111',
                   'revision': 1, 'sub': 'd' * 64, 'session': 'e' * 64,
                   'iat': int(time.time()), 'exp': int(time.time()) + 30} | overrides
        data = base64.urlsafe_b64encode(json.dumps(payload).encode()).rstrip(b'=')
        return data.decode() + '.' + hmac.new(self.cfg.GRANT_KEY.encode(), data, hashlib.sha256).hexdigest()

    def test_audience_transition_and_expiry(self):
        for audience in ('videolesson-stream-media', 'codefortex-media'):
            self.assertEqual(self.security.verify_grant(self.token(audience))['aud'], audience)
        with patch.object(self.cfg, 'ALLOW_LEGACY_PROTOCOL', False):
            with self.assertRaises(self.security.Rejected):
                self.security.verify_grant(self.token('codefortex-media'))
        for token in (self.token('wrong'), self.token('videolesson-stream-media', exp=0),
                      self.token('videolesson-stream-media', tenant='another-tenant')):
            with self.assertRaises(self.security.Rejected): self.security.verify_grant(token)

    def test_new_grant_emits_only_neutral_audience(self):
        token, expires = self.security.grant({'tenant': self.cfg.TENANT,
            'uuid': '11111111-1111-4111-8111-111111111111', 'revision': 1}, 'd' * 64, 'e' * 64)
        self.assertEqual(self.security.verify_grant(token)['aud'], 'videolesson-stream-media')
