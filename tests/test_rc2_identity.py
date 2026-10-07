# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright 2026 ValeLMS contributors
import sys
from pathlib import Path
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from check_identity import validate


class Identity(unittest.TestCase):
    def test_distinct_component_contract(self):
        self.assertEqual(validate()['result'], 'PASS')

    def test_invalid_activity_name_is_rejected(self):
        original = Path.read_text
        def invalid(path, *args, **kwargs):
            text = original(path, *args, **kwargs)
            if path.name == 'version.php':
                return text.replace('mod_videolessonstream', 'mod_videolesson_stream')
            return text
        with patch.object(Path, 'read_text', invalid), self.assertRaisesRegex(ValueError, 'Invalid Moodle activity'):
            validate()
