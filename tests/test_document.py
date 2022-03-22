import unittest
from pathlib import Path
from src.document_metrics import Document


class TestDocument(unittest.TestCase):
    test_assets_path: Path = Path(__file__).parent / 'assets'

    @staticmethod
    def doc_path(doc_name: str):
        return TestDocument.test_assets_path / doc_name

    def test_entire_file_read(self):
        document = Document(self.doc_path('doc_multiple_lines.txt'))
        actual = document.read()
        expected = "Let me begin by saying thanks to all you who've traveled, from far and wide, to brave the cold today.\n" \
                   "We all made this journey for a reason. It's humbling, but in my heart I know you didn't come here just for " \
                   "me, you came here because you believe in what this country can be.\nIn the face of war, you believe there " \
                   "can be peace. In the face of despair, you believe there can be hope."
        self.assertEqual(expected, actual)

    def test_empty_file_read(self):
        document = Document(self.doc_path('doc_empty.txt'))
        actual = document.read()
        expected = ""
        self.assertEqual(expected, actual)

    def test_file_does_not_exist(self):
        document = Document(self.doc_path('bogus.txt'))
        actual = document.exists()
        self.assertFalse(actual)

    def test_file_does_exist(self):
        document = Document(self.doc_path('doc_empty.txt'))
        actual = document.exists()
        self.assertTrue(actual)

    def test_extraction_of_filename_from_document_path(self):
        filename = 'doc_empty.txt'
        document = Document(self.doc_path(filename))
        actual = document.name()
        expected = filename
        self.assertEqual(expected, actual)
