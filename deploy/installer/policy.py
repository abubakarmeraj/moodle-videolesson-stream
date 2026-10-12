# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright 2026 ValeLMS contributors
"""Shared operator-policy validation. Never put an input value in an error."""
import json
import os
from pathlib import Path
import re
import stat
from urllib.parse import urlsplit

STORAGE_ROLES = ('api', 'gateway', 'worker', 'janitor')


def origin(value):
    if not isinstance(value, str) or re.search(r'[\s\\]', value):
        raise ValueError('Use an HTTPS origin without whitespace or a path')
    url = urlsplit(value)
    if (url.scheme != 'https' or not url.hostname or url.username or url.password or
            url.path or url.query or url.fragment or not url.netloc or url.port == 0):
        raise ValueError('Use a trusted HTTPS origin without a path, userinfo, query or fragment')
    return value


def protected_file(path, group_read=False):
    if not isinstance(path, (str, Path)):
        raise ValueError('Provide a protected file path')
    path = Path(path)
    if not path.is_absolute() or any(p.is_symlink() for p in [path, *path.parents]):
        raise ValueError('Use an absolute, non-symlink protected file')
    info = path.stat()
    if not stat.S_ISREG(info.st_mode) or not 0 < info.st_size <= 16384:
        raise ValueError('Protected file must be a small non-empty regular file')
    if os.name == 'posix':
        forbidden = 0o027 if group_read else 0o077
        if info.st_mode & forbidden or info.st_uid not in (0, os.geteuid()):
            raise ValueError('Protected file needs a trusted owner and mode 0600 (handoff may use 0640)')
        for parent in path.parents:
            if parent.stat().st_mode & 0o022 or parent.stat().st_uid not in (0, os.geteuid()):
                raise ValueError('Protected file parents must not be group/world writable')
    return path.read_text()


def validate(policy):
    if not isinstance(policy, dict):
        raise ValueError('Policy must be a JSON object')
    backend = policy.get('storage_backend')
    if backend not in ('r2', 's3-compatible'):
        raise ValueError('Choose r2 or s3-compatible storage')
    for key in ('endpoint', 'moodle_origin', 'service_origin', 'gateway_origin'):
        origin(policy.get(key))
    if backend == 'r2' and not re.fullmatch(r'https://[a-f0-9]{32}\.r2\.cloudflarestorage\.com', policy['endpoint']):
        raise ValueError('R2 requires its account HTTPS endpoint')
    for key in ('raw_bucket', 'processed_bucket'):
        name = policy.get(key, '')
        if not isinstance(name, str) or not re.fullmatch(r'[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]', name):
            raise ValueError('Use valid explicit private bucket names')
    if policy['raw_bucket'] == policy['processed_bucket']:
        raise ValueError('Raw and processed buckets must be different')
    if policy.get('storage_addressing_style', 'path') not in ('path', 'virtual'):
        raise ValueError('Addressing style must be path or virtual')
    region = policy.get('storage_region', 'auto' if backend == 'r2' else 'us-east-1')
    if not isinstance(region, str) or not re.fullmatch(r'[a-zA-Z0-9-]{1,64}', region):
        raise ValueError('Provide a valid storage region')
    hosts = policy.get('allowed_hosts', '')
    if not isinstance(hosts, str) or not re.fullmatch(r'[a-zA-Z0-9.,:-]+', hosts):
        raise ValueError('Provide a comma-separated explicit service host allowlist')
    for key in ('service_origin', 'gateway_origin'):
        if urlsplit(policy[key]).hostname not in hosts.split(','):
            raise ValueError('Service and gateway hostnames must be in allowed_hosts')
    storage_files = policy.get('storage_files')
    if not isinstance(storage_files, dict):
        raise ValueError('Provide protected files for each storage role')
    for role in STORAGE_ROLES:
        files = storage_files.get(role, {})
        if not isinstance(files, dict):
            raise ValueError('Role credential paths must be an object')
        for key in ('access', 'secret'):
            value = protected_file(files.get(key, ''))
            if not value.strip() or re.search(r'[\r\n\x00]', value.strip()):
                raise ValueError('Storage credentials must be non-empty single-line values')
    if policy.get('storage_ca_bundle'):
        path = Path(policy['storage_ca_bundle'])
        if not path.is_absolute() or not path.is_file():
            raise ValueError('Private CA bundle must be an absolute existing file')
    return policy


def load(path):
    return validate(json.loads(protected_file(path)))
