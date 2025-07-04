from .block_type import md_block_to_block_type, BlockType
from .markdown_to_blocks import markdown_to_blocks
from .html_node import LeafNode, ParentNode, HTMLNode


def markdown_to_html_node(md: str) -> HTMLNode:
    md_blocks = markdown_to_blocks(md)
    for block in md_blocks:
        block_type = md_block_to_blck_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                LeafNode(tag="p", value=block)
