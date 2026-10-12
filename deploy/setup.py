#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright 2026 ValeLMS contributors
"""Guided Compose configuration; no package/service/bucket/Moodle mutations."""
import argparse
import getpass
import json
import os
from pathlib import Path
import subprocess
import sys
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent / 'installer'))
import policy


def write_new(path, text):
    with open(path, 'x', opener=lambda name, flags: os.open(name, flags, 0o600)) as file:
        file.write(text)


def configure(directory, ask=input, secret=getpass.getpass, supplied=None):
    directory = Path(directory).absolute()
    if directory.exists() or any(p.is_symlink() for p in [directory, *directory.parents]):
        raise ValueError('Configuration already exists or is a symlink; reuse it, never regenerate credentials')
    if not directory.parent.is_dir() or (os.name == 'posix' and directory.parent.stat().st_mode & 0o022):
        raise ValueError('Choose an existing root-owned private parent, not a shared writable directory')
    if os.name == 'posix' and any(p.stat().st_uid not in (0, os.geteuid()) or p.stat().st_mode & 0o022
                                for p in directory.parents):
        raise ValueError('Configuration parents must be trusted and not group/world writable')
    if supplied:
        settings = policy.load(supplied)
    else:
        settings = {'storage_backend': ask('Storage backend [s3-compatible/r2]: ').strip() or 's3-compatible'}
        for key, prompt in [('moodle_origin', 'Moodle HTTPS origin'), ('service_origin', 'Video API HTTPS origin'),
                            ('gateway_origin', 'Media gateway HTTPS origin'), ('endpoint', 'Browser-reachable S3 HTTPS origin')]:
            settings[key] = policy.origin(ask(prompt + ': ').strip())
        for key in ('raw_bucket', 'processed_bucket'):
            settings[key] = ask(key.replace('_', ' ').capitalize() + ': ').strip()
        settings['storage_region'] = 'auto' if settings['storage_backend'] == 'r2' else 'us-east-1'
        settings['storage_addressing_style'] = 'path'
        settings['allowed_hosts'] = ','.join(dict.fromkeys(['localhost', '127.0.0.1'] +
            [urlsplit(settings[k]).hostname for k in ('service_origin', 'gateway_origin')]))
        settings['storage_files'] = {}
    directory.mkdir(mode=0o700)
    if not supplied:
        for role in policy.STORAGE_ROLES:
            settings['storage_files'][role] = {}
            for key in ('access', 'secret'):
                value = secret(f'{role} storage {key} (hidden): ').strip()
                if not value or any(c in value for c in '\r\n\x00'):
                    raise ValueError('Credential must be a non-empty single-line value; incomplete directory retained')
                path = directory / f'{role}-{key}'
                write_new(path, value)
                settings['storage_files'][role][key] = str(path)
    policy.validate(settings)
    write_new(directory / 'policy.json', json.dumps(settings, indent=2) + '\n')
    return directory / 'policy.json'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, required=True, help='NEW root-only configuration directory')
    parser.add_argument('--config', type=Path, help='Existing protected operator policy instead of guided prompts')
    args = parser.parse_args()
    if sys.platform != 'linux' or os.geteuid() != 0:
        parser.error('Run with sudo on the Linux service host')
    try:
        path = configure(args.directory, supplied=args.config)
        subprocess.run([sys.executable, str(Path(__file__).parent / 'docker/prepare.py'),
                        '--directory', str(path.parent / 'runtime'), '--config', str(path)], check=True)
    except (ValueError, OSError, subprocess.CalledProcessError):
        print('SETUP_FAILED: check inputs/permissions; existing state was not overwritten. Retain any incomplete new directory privately.')
        return 1
    print('CONFIG_CREATED: private policy and runtime generated. No services started or storage permissions changed.')
    print('Next: preflight, build Compose, configure trusted HTTPS, then Test Connection. See docs/quick-start.md.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
