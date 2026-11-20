"""Validate the approved sendmux archive; upload only with --publish and an OIDC token."""

import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import struct
import tarfile
import tomllib
import urllib.error
import urllib.request

ARCHIVE = Path(__file__).resolve().parents[1] / 'release-pointers/cratesio/sendmux/sendmux-1.0.0.crate'
CHECKSUM = '0382c47cd5ae1b8afa20ecd59cf8e5218424f80786429603535a73b1d8dad802'
USER_AGENT = 'qubrics-sdk-release/1.0 (https://github.com/qubrics/qubrics-sdk)'


def prepare_upload(archive_path):
    archive_bytes = archive_path.read_bytes()
    if len(archive_bytes) != 11593:
        raise ValueError('Approved sendmux archive size differs')
    if hashlib.sha256(archive_bytes).hexdigest() != CHECKSUM:
        raise ValueError('Approved sendmux archive SHA-256 differs')
    with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode='r:gz') as archive:
        package = tomllib.loads(archive.extractfile('sendmux-1.0.0/Cargo.toml').read().decode())['package']
        readme = archive.extractfile('sendmux-1.0.0/README.md').read().decode()
    # The registry envelope carries the frozen archive unchanged; cargo publish would repack source.
    dependency = dict(name='qubrics', version_req='=1.0.0', features=[], optional=False, default_features=True, target=None, kind='normal', registry=None, explicit_name_in_toml=None)
    metadata = dict(name=package['name'], vers=package['version'], deps=[dependency], features={}, authors=package.get('authors', []), description=package['description'], documentation=package.get('documentation'), homepage=package.get('homepage'), readme=readme, readme_file='README.md', keywords=package.get('keywords', []), categories=package.get('categories', []), license=package['license'], license_file=package.get('license-file'), repository=package['repository'], badges={}, links=package.get('links'), rust_version=package['rust-version'])
    encoded = json.dumps(metadata, separators=(',', ':')).encode()
    return struct.pack('<I', len(encoded)) + encoded + struct.pack('<I', len(archive_bytes)) + archive_bytes


def validate_response(raw):
    response = json.loads(raw)
    if not isinstance(response, dict) or 'errors' in response:
        raise ValueError('Registry rejected publication or returned an invalid response; stop for public readback')
    return response


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--publish', action='store_true')
    args = parser.parse_args()
    body = prepare_upload(ARCHIVE)
    print(f'sendmux 1.0.0: 11593 bytes, SHA-256 {CHECKSUM}', flush=True)
    if not args.publish:
        return
    index = urllib.request.Request('https://index.crates.io/se/nd/sendmux', headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(index, timeout=20) as response:
        versions = [json.loads(line) for line in response.read().splitlines() if line]
    if any(version['vers'] == '1.0.0' for version in versions):
        raise RuntimeError('sendmux 1.0.0 already exists; no upload attempted')
    request = urllib.request.Request('https://crates.io/api/v1/crates/new', data=body, method='PUT', headers={'Authorization': os.environ['CARGO_REGISTRY_TOKEN'], 'Content-Type': 'application/octet-stream', 'User-Agent': USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            print(json.dumps(validate_response(response.read())))
    except urllib.error.HTTPError as error:
        raise RuntimeError(f'Publication HTTP {error.code}: {error.read().decode()}; stop and read public state before any retry') from None


if __name__ == '__main__':
    main()
