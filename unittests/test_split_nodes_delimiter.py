import unittest

from src.split_text_node import split_nodes_delimiter
from src.textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_text_with_code(self):
        node = TextNode("This is some text with code: `y = x`.", TextType.TEXT)
        split_node = split_nodes_delimiter(node, "`", TextType.CODE)

        self.assertEqual(
            split_node,
            [
                TextNode("This is some text with code: ", TextType.TEXT),
                TextNode("y = x", TextType.CODE),
                TextNode(".", TextType.TEXT),
            ],
        )

    def test_text_with_bold(self):
        node = TextNode("This is some **bold text**.", TextType.TEXT)
        split_node = split_nodes_delimiter(node, "**", TextType.BOLD)

        self.assertEqual(
            split_node,
            [
                TextNode("This is some ", TextType.TEXT),
                TextNode("bold text", TextType.BOLD),
                TextNode(".", TextType.TEXT),
            ],
        )

    def test_text_with_italic(self):
        node = TextNode("This is some *italic text*.", TextType.TEXT)
        split_node = split_nodes_delimiter(node, "*", TextType.ITALIC)

        self.assertEqual(
            split_node,
            [
                TextNode("This is some ", TextType.TEXT),
                TextNode("italic text", TextType.ITALIC),
                TextNode(".", TextType.TEXT),
            ],
        )

    def test_wrong_delimiter(self):
        node = TextNode("This is some *italic text*.", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_node = split_nodes_delimiter(node, "`", TextType.ITALIC)

    def test_not_implemented_text_style(self):
        node = TextNode("This is some text.", TextType.TEXT)
        with self.assertRaises(NotImplementedError):
            split_nodes_delimiter(node, " ", TextType.IMAGE)
