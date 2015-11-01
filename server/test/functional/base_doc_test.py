import unittest

import app
app.test_mode = True

from app.server import config


class ApiDocTestCase(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def assertApiDoc(self, results: str, expected: str):
        expected = self.__fixup_indentation(expected).rstrip(' ')
        self.assertEqual(expected % {'app_name': config.App.NAME}, results)

    def __fixup_indentation(self, text_block: str, indentation_level=1) -> str:
        return '\n'.join([line[(indentation_level * 4):] for line in text_block.splitlines()])
