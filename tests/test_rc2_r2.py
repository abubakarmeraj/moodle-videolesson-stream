# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright 2026 ValeLMS contributors
"""Dedicated R2 client/SigV4 contracts with botocore stubs, not live cloud tests."""
import importlib
from unittest.mock import patch
import unittest
from urllib.parse import urlsplit, parse_qs
from botocore.stub import Stubber
from test_os1_baseline import configuration


class R2(unittest.TestCase):
    def setUp(self):
        self.cfg = configuration(R2_ACCESS_KEY='synthetic-access', R2_SECRET_KEY='synthetic-secret')
        self.storage = importlib.import_module('service.storage')

    def test_r2_sigv4_exact_part_url(self):
        with patch.object(self.storage, 'config', self.cfg):
            with patch.dict('os.environ', {'R2_ACCESS_KEY': 'synthetic-access', 'R2_SECRET_KEY': 'synthetic-secret'}, clear=True):
                client = self.storage.client()
        url = client.generate_presigned_url('upload_part', Params={'Bucket': self.cfg.RAW,
            'Key': 'assigned/source', 'UploadId': 'upload-identity', 'PartNumber': 2}, ExpiresIn=60)
        parsed = urlsplit(url)
        query = parse_qs(parsed.query)
        self.assertEqual(parsed.hostname, '0' * 32 + '.r2.cloudflarestorage.com')
        self.assertEqual(parsed.path, '/' + self.cfg.RAW + '/assigned/source')
        self.assertEqual(query['X-Amz-Algorithm'], ['AWS4-HMAC-SHA256'])
        self.assertEqual(query['X-Amz-Expires'], ['60'])
        self.assertEqual(query['partNumber'], ['2'])
        self.assertEqual(query['uploadId'], ['upload-identity'])
        self.assertIn('/auto/s3/aws4_request', query['X-Amz-Credential'][0])
        # URL deliberately never logged or persisted.

    def test_multipart_head_range_delete_bucket_contract(self):
        with patch.object(self.storage, 'config', self.cfg), patch.dict('os.environ', {
                'R2_ACCESS_KEY': 'synthetic-access', 'R2_SECRET_KEY': 'synthetic-secret'}, clear=True):
            client = self.storage.client()
        raw, processed = self.cfg.RAW, self.cfg.PROCESSED
        with Stubber(client) as stub:
            stub.add_response('create_multipart_upload', {'UploadId':'u'}, {'Bucket':raw,'Key':'assigned/source'})
            stub.add_response('complete_multipart_upload', {'ETag':'"done"'}, {'Bucket':raw,'Key':'assigned/source',
                'UploadId':'u','MultipartUpload':{'Parts':[{'PartNumber':1,'ETag':'"part"'}]}})
            stub.add_response('head_object', {'ContentLength':123,'Metadata':{'upload':'u'}}, {'Bucket':raw,'Key':'assigned/source'})
            stub.add_response('get_object', {'ContentLength':10}, {'Bucket':processed,'Key':'assigned/segment.ts','Range':'bytes=0-9'})
            stub.add_response('delete_object', {}, {'Bucket':raw,'Key':'assigned/source'})
            self.assertEqual(client.create_multipart_upload(Bucket=raw,Key='assigned/source')['UploadId'],'u')
            client.complete_multipart_upload(Bucket=raw,Key='assigned/source',UploadId='u',
                MultipartUpload={'Parts':[{'PartNumber':1,'ETag':'"part"'}]})
            self.assertEqual(client.head_object(Bucket=raw,Key='assigned/source')['ContentLength'],123)
            client.get_object(Bucket=processed,Key='assigned/segment.ts',Range='bytes=0-9')
            client.delete_object(Bucket=raw,Key='assigned/source')
            stub.assert_no_pending_responses()
