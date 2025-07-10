import unittest
from src.generate_page import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = """#     This is the title   
Here is the rest of the text

with different paragraphs
"""
        title = extract_title(md)
        self.assertEqual(title, "This is the title")

    def test_title_not_on_first_line(self):
        md = """

# This is the title   
Here is the rest of the text

with different paragraphs
"""
        title = extract_title(md)
        self.assertEqual(title, "This is the title")

    def test_wrong_heading_syntax(self):
        md = "#Title"
        with self.assertRaises(ValueError):
            _ = extract_title(md)

    def test_no_heading(self):
        md = "just some text"
        with self.assertRaises(ValueError):
            _ = extract_title(md)

    def test_higher_level_heading(self):
        md = "## Not the Title\n# Title"
        title = extract_title(md)
        self.assertEqual(title, "Title")
        md = "## Title"
        with self.assertRaises(ValueError):
            _ = extract_title(title)
