import unittest

from src.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode(
            "<a>",
            "some text",
            [],
            {"href": "https://www.google.com", "target": "_blank"},
        )
        expected_string = "HTMLNode(<a>, some text, [], {'href': 'https://www.google.com', 'target': '_blank'})"
        self.assertEqual(node.__repr__(), expected_string)

    def test_to_html(self):
        node = HTMLNode("<a>", "text", [])
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_value_and_children_none(self):
        with self.assertRaises(ValueError):
            HTMLNode()

    def test_props_to_html(self):
        node = HTMLNode(
            "<a>",
            "some text",
            [],
            {"href": "https://www.google.com", "target": "_blank"},
        )

        self.assertEqual(
            node.props_to_html(), 'href="https://www.google.com" target="_blank"'
        )

        node2 = HTMLNode("<a>", "some text")

        self.assertEqual(node2.props_to_html(), "")
