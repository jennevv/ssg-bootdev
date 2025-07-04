import unittest

from src.block_type import md_block_to_block_type, BlockType


class TestBlockType(unittest.TestCase):
    def test_valid_heading(self):
        md = "# Header 1"
        self.assertEqual(md_block_to_block_type(md), BlockType.HEADING)
        md = "## Header 2"
        self.assertEqual(md_block_to_block_type(md), BlockType.HEADING)
        md = "### Header 3"
        self.assertEqual(md_block_to_block_type(md), BlockType.HEADING)
        md = "#### Header 4"
        self.assertEqual(md_block_to_block_type(md), BlockType.HEADING)
        md = "##### Header 5"
        self.assertEqual(md_block_to_block_type(md), BlockType.HEADING)
        md = "###### Header 6"
        self.assertEqual(md_block_to_block_type(md), BlockType.HEADING)

    def test_invalid_heading(self):
        md = "#Header 1"
        self.assertEqual(md_block_to_block_type(md), BlockType.PARAGRAPH)
        md = "####### Header 7"
        self.assertEqual(md_block_to_block_type(md), BlockType.PARAGRAPH)
        md = " # Header 1"
        self.assertEqual(md_block_to_block_type(md), BlockType.PARAGRAPH)
        md = "Header 1 #"
        self.assertEqual(md_block_to_block_type(md), BlockType.PARAGRAPH)

    def test_valid_code(self):
        md = "``````"
        self.assertEqual(md_block_to_block_type(md), BlockType.CODE)
        md = """```
        this should be a code block
        ```"""
        self.assertEqual(md_block_to_block_type(md), BlockType.CODE)
        md = """``` ###
        this should be a code block

        - asdfasf
        - asdfa
        some more code 

        ```"""
        self.assertEqual(md_block_to_block_type(md), BlockType.CODE)
        md = """```this should be a code block

        some more code 

        ```"""
        self.assertEqual(md_block_to_block_type(md), BlockType.CODE)

    def test_invalid_code(self):
        md = "``\n ```"
        self.assertEqual(md_block_to_block_type(md), BlockType.PARAGRAPH)
        md = "`\n`"
        self.assertEqual(md_block_to_block_type(md), BlockType.PARAGRAPH)
        md = " ```\n```"
        self.assertEqual(md_block_to_block_type(md), BlockType.PARAGRAPH)
        md = "`````"
        self.assertEqual(md_block_to_block_type(md), BlockType.PARAGRAPH)
        md = "```\n``` "
        self.assertEqual(md_block_to_block_type(md), BlockType.PARAGRAPH)

    def test_valid_quote(self):
        md = """>\n> this is a quote block\n>- Genevieve\n> """
        self.assertEqual(md_block_to_block_type(md), BlockType.QUOTE)
        md = """>>>>>\n> this is a quote block\n>- Genevieve>"""
        self.assertEqual(md_block_to_block_type(md), BlockType.QUOTE)

    def test_invalid_quote(self):
        md = """
                > this is a quote
            """
        self.assertEqual(md_block_to_block_type(md), BlockType.PARAGRAPH)

    def test_valid_unordered_list(self):
        md = "- item 1\n- item 2\n- item 3"
        self.assertEqual(md_block_to_block_type(md), BlockType.UNORDERED_LIST)
        md = "- item 1"
        self.assertEqual(md_block_to_block_type(md), BlockType.UNORDERED_LIST)
        md = "- \n- \n- "
        self.assertEqual(md_block_to_block_type(md), BlockType.UNORDERED_LIST)
        md = "- "
        self.assertEqual(md_block_to_block_type(md), BlockType.UNORDERED_LIST)

    def test_invalid_unordered_list(self):
        md = "-"
        self.assertEqual(md_block_to_block_type(md), BlockType.PARAGRAPH)
        md = """-
        -
        -"""
        self.assertEqual(md_block_to_block_type(md), BlockType.PARAGRAPH)
        md = "-item"
        self.assertEqual(md_block_to_block_type(md), BlockType.PARAGRAPH)
        md = """-Item
        -
        -"""
        self.assertEqual(md_block_to_block_type(md), BlockType.PARAGRAPH)
        md = """- Item 1
        - Item 2

        - Item 3"""
        self.assertEqual(md_block_to_block_type(md), BlockType.PARAGRAPH)

    def test_valid_ordered_list(self):
        md = "1. item 1\n1. item 2\n1. item 3"
        self.assertEqual(md_block_to_block_type(md), BlockType.ORDERED_LIST)
        md = "1. item 1"
        self.assertEqual(md_block_to_block_type(md), BlockType.ORDERED_LIST)
        md = "1. \n1. \n1. "
        self.assertEqual(md_block_to_block_type(md), BlockType.ORDERED_LIST)
        md = "1. "
        self.assertEqual(md_block_to_block_type(md), BlockType.ORDERED_LIST)

    def test_invalid_ordered_list(self):
        md = "1."
        self.assertEqual(md_block_to_block_type(md), BlockType.PARAGRAPH)
        md = """1.
        1.
        1."""
        self.assertEqual(md_block_to_block_type(md), BlockType.PARAGRAPH)
        md = "1.item"
        self.assertEqual(md_block_to_block_type(md), BlockType.PARAGRAPH)
        md = """1.Item
        1.
        1."""
        self.assertEqual(md_block_to_block_type(md), BlockType.PARAGRAPH)
        md = """1. Item 1
        1. Item 2

        1. Item 3"""
        self.assertEqual(md_block_to_block_type(md), BlockType.PARAGRAPH)
