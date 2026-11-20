import importlib.util
import json
from pathlib import Path
import struct
import tempfile
import unittest

SCRIPT = Path(__file__).with_name('publish-frozen-sendmux.py')


class FrozenCrateTests(unittest.TestCase):
    def test_registry_errors_or_ambiguous_success_are_refused(self):
        spec = importlib.util.spec_from_file_location('frozen_sendmux', SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        success = b'{"warnings":{"invalid_categories":[],"invalid_badges":[],"other":[]}}'
        self.assertEqual(module.validate_response(success)['warnings']['other'], [])
        self.assertEqual(module.validate_response(b'{}'), {})
        for response in (b'{"errors":[{"detail":"rejected"}]}', b'[]', b'not JSON'):
            with self.subTest(response=response), self.assertRaises(ValueError):
                module.validate_response(response)

    def test_frozen_bytes_are_preserved_and_changed_bytes_refused(self):
        spec = importlib.util.spec_from_file_location('frozen_sendmux', SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        archive = module.ARCHIVE.read_bytes()
        body = module.prepare_upload(module.ARCHIVE)
        length = struct.unpack_from('<I', body)[0]
        metadata = json.loads(body[4:4 + length])
        self.assertEqual((metadata['name'], metadata['vers']), ('sendmux', '1.0.0'))
        self.assertEqual(metadata['deps'][0]['version_req'], '=1.0.0')
        self.assertEqual(struct.unpack_from('<I', body, 4 + length)[0], 11593)
        self.assertEqual(body[8 + length:], archive)
        with tempfile.TemporaryDirectory() as directory:
            changed = Path(directory) / 'sendmux-1.0.0.crate'
            changed.write_bytes(archive[:-1] + bytes([archive[-1] ^ 1]))
            with self.assertRaisesRegex(ValueError, 'SHA-256'):
                module.prepare_upload(changed)
            changed.write_bytes(archive[:-1])
            with self.assertRaisesRegex(ValueError, 'size'):
                module.prepare_upload(changed)


if __name__ == '__main__':
    unittest.main()
