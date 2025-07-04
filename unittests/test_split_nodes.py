import unittest

from src.split_text_node import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)
from src.text_node import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_text_with_code_node(self):
        node = TextNode("This is some text.", TextType.CODE)
        split_node = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(
            split_node,
            [TextNode("This is some text.", TextType.CODE)],
        )

    def test_text_with_code(self):
        node = TextNode("This is some text with code: `y = x`.", TextType.TEXT)
        split_node = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(
            split_node,
            [
                TextNode("This is some text with code: ", TextType.TEXT),
                TextNode("y = x", TextType.CODE),
                TextNode(".", TextType.TEXT),
            ],
        )

    def test_text_with_two_code_nodes(self):
        node1 = TextNode("This is some text with code: `y = x`.", TextType.TEXT)
        node2 = TextNode("This is some text with code: `x = y`.", TextType.TEXT)
        split_node = split_nodes_delimiter([node1, node2], "`", TextType.CODE)

        self.assertEqual(
            split_node,
            [
                TextNode("This is some text with code: ", TextType.TEXT),
                TextNode("y = x", TextType.CODE),
                TextNode(".", TextType.TEXT),
                TextNode("This is some text with code: ", TextType.TEXT),
                TextNode("x = y", TextType.CODE),
                TextNode(".", TextType.TEXT),
            ],
        )

    def test_text_with_bold(self):
        node = TextNode("This is some **bold text**.", TextType.TEXT)
        split_node = split_nodes_delimiter([node], "**", TextType.BOLD)

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
        split_node = split_nodes_delimiter([node], "*", TextType.ITALIC)

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
            _ = split_nodes_delimiter([node], "`", TextType.ITALIC)

    def test_not_implemented_text_style(self):
        node = TextNode("This is some text.", TextType.TEXT)
        with self.assertRaises(NotImplementedError):
            _ = split_nodes_delimiter([node], " ", TextType.IMAGE)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_image_at_start_string(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_link_at_start_string(self):
        node = TextNode(
            "[link](www.boot.dev) and another [second link](www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "www.google.com"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](www.boot.dev) and another [second link](www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "www.google.com"),
            ],
            new_nodes,
        )
