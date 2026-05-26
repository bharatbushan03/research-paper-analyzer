import unittest
import os
from load_paper import load_pdf
from text_splitter import split_text

class TestPaperAnalyzer(unittest.TestCase):
    def test_split_text(self):
        text = "This is a test. " * 100
        chunks = split_text(text)
        self.assertIsInstance(chunks, list)
        self.assertGreater(len(chunks), 0)
        self.assertLessEqual(len(chunks[0]), 800)

    def test_load_pdf_missing_file(self):
        with self.assertRaises(Exception):
            load_pdf("non_existent_file.pdf")

if __name__ == "__main__":
    unittest.main()
