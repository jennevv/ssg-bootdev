import unittest

from src.text_node import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_ineq_text_type(self):
        node = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_ineq_url(self):
        node = TextNode("This is a text node", TextType.LINK, "www.boots.dev")
        node2 = TextNode("This is a text node", TextType.LINK, "www.boots.com")
        self.assertNotEqual(node, node2)

    def test_ineq_text(self):
        node = TextNode("This is a text node", TextType.LINK, "www.boots.dev")
        node2 = TextNode("This is a node", TextType.LINK, "www.boots.dev")
        self.assertNotEqual(node, node2)

    def test_ineq_multiple(self):
        node = TextNode("This is a text node", TextType.CODE, "www.boots.com")
        node2 = TextNode("This is a node", TextType.LINK, "www.boots.dev")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node.__repr__(), "TextNode(This is a text node, italic, None)")

    def test_url_is_none(self):
        node = TextNode("string", TextType.ITALIC, None)
        self.assertEqual(node.url, None)

    def test_url_is_not_none(self):
        node = TextNode("string", TextType.LINK, "www.boots.dev")
        self.assertEqual(node.url, "www.boots.dev")


if __name__ == "__main__":
    unittest.main()
