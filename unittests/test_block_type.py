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
        md = "####### Header 7"
        self.assertNotEqual(md_block_to_block_type(md), BlockType.HEADING)
