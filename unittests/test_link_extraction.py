import unittest

from src.link_extraction import extract_markdown_images, extract_markdown_links


class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image_link(self):
        text = "![This](image.png) is an image link."
        result = extract_markdown_images(text)
        self.assertEqual(result, [("This", "image.png")])

    def test_double_image_link(self):
        text = "![This](image.png) is an ![image](another_image.png) link."
        result = extract_markdown_images(text)
        self.assertEqual(
            result, [("This", "image.png"), ("image", "another_image.png")]
        )

    def test_multiple_words_in_alter(self):
        text = "This is an ![image link](image.png)."
        result = extract_markdown_images(text)
        self.assertEqual(result, [("image link", "image.png")])

    def test_markdown_link(self):
        text = "[This](www.google.com) is not an image link."
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_double_markdown_link(self):
        text = "[This](www.google.com) is not an [image](www.boot.dev) link."
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_unclosed_image_link(self):
        text = "![This](www.google.com is not a correct image link."
        result = extract_markdown_images(text)
        self.assertEqual(result, [])
        text = "!This](www.google.com) is not a correct image link."
        result = extract_markdown_images(text)
        self.assertEqual(result, [])
        text = "![This(www.google.com) is not a correct image link."
        result = extract_markdown_images(text)
        self.assertEqual(result, [])
        text = "![This]www.google.com) is not a correct image link."
        result = extract_markdown_images(text)
        self.assertEqual(result, [])
        text = "![Thiswww.google.com) is not a correct image link."
        result = extract_markdown_images(text)
        self.assertEqual(result, [])
        text = "!This](www.google.com is not a correct image link."
        result = extract_markdown_images(text)
        self.assertEqual(result, [])


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_image_link(self):
        text = "![This](image.png) is an image link."
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_double_image_link(self):
        text = "![This](image.png) is an ![image](another_image.png) link."
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_markdown_link(self):
        text = "[This](www.google.com) is not an image link."
        result = extract_markdown_links(text)
        self.assertEqual(result, [("This", "www.google.com")])

    def test_multiple_words_in_alter(self):
        text = "[This is](www.google.com) not an image link."
        result = extract_markdown_links(text)
        self.assertEqual(result, [("This is", "www.google.com")])

    def test_double_markdown_link(self):
        text = "[This](www.google.com) is not an [image](www.boot.dev) link."
        result = extract_markdown_links(text)
        self.assertEqual(
            result, [("This", "www.google.com"), ("image", "www.boot.dev")]
        )

    def test_unclosed_markdown_link(self):
        text = "[This](www.google.com is not a correct image link."
        result = extract_markdown_links(text)
        self.assertEqual(result, [])
        text = "This](www.google.com) is not a correct image link."
        result = extract_markdown_links(text)
        self.assertEqual(result, [])
        text = "[This(www.google.com) is not a correct image link."
        result = extract_markdown_links(text)
        self.assertEqual(result, [])
        text = "[This]www.google.com) is not a correct image link."
        result = extract_markdown_links(text)
        self.assertEqual(result, [])
        text = "[Thiswww.google.com) is not a correct image link."
        result = extract_markdown_links(text)
        self.assertEqual(result, [])
        text = "This](www.google.com is not a correct image link."
        result = extract_markdown_links(text)
        self.assertEqual(result, [])
