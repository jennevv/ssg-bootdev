import unittest

from src.link_extraction import extract_markdown_images, extract_markdown_links


class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image_link(self):
        text = "![This](image.png) is an image link."
        result = extract_markdown_images(text)
        self.assertEqual(result, [("This", "image.png")])


class TestExtractMarkdownLinks(unittest.TestCase):
    pass
