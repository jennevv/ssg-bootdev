import re

from .text_node import TextNode, TextType
from .block_type import md_block_to_block_type, BlockType, heading_level
from .markdown_to_blocks import markdown_to_blocks
from .html_node import LeafNode, ParentNode, HTMLNode
from .text_to_text_nodes import text_to_text_nodes
from .text_node_to_html_node import text_node_to_html_node


def markdown_to_html_node(md: str) -> HTMLNode:
    md_blocks = markdown_to_blocks(md)
    html_nodes: list[ParentNode] = []
    for block in md_blocks:
        block_type = md_block_to_block_type(block)
        children = text_to_children(block, block_type)
        match block_type:
            case BlockType.PARAGRAPH:
                parent = ParentNode(tag="p", children=children)
            case BlockType.HEADING:
                level = heading_level(block)
                parent = ParentNode(tag=f"h{level}", children=children)
            case BlockType.CODE:
                parent = ParentNode(
                    "pre", children=[ParentNode(tag="code", children=children)]
                )
            case BlockType.QUOTE:
                parent = ParentNode(tag="blockquote", children=children)
            case BlockType.UNORDERED_LIST:
                parent = ParentNode(tag="ul", children=children)
            case BlockType.ORDERED_LIST:
                parent = ParentNode(tag="ol", children=children)

        html_nodes.append(parent)

    div_node = ParentNode(tag="div", children=html_nodes)
    return div_node


def text_to_children(text: str, block_type: BlockType) -> list[LeafNode | ParentNode]:
    match block_type:
        case BlockType.CODE:
            code_text = format_code_text(text)
            code_text_node = TextNode(code_text, TextType.TEXT)
            code_html_nodes = [text_node_to_html_node(code_text_node)]
            return code_html_nodes
        case BlockType.UNORDERED_LIST:
            formatted_text = format_unordered_list_text(text)
            list_items = formatted_text.split("\n")
            list_item_text_nodes = list(map(text_to_text_nodes, list_items))
            parent_list_html_nodes = []
            for item in list_item_text_nodes:
                html_nodes = list(map(text_node_to_html_node, item))
                parent = ParentNode("li", html_nodes)
                parent_list_html_nodes.append(parent)
            return parent_list_html_nodes
        case BlockType.ORDERED_LIST:
            formatted_text = format_ordered_list_text(text)
            list_items = formatted_text.split("\n")
            list_item_text_nodes = list(map(text_to_text_nodes, list_items))
            parent_list_html_nodes: list[ParentNode] = []
            for item in list_item_text_nodes:
                html_nodes = list(map(text_node_to_html_node, item))
                parent = ParentNode("li", html_nodes)
                parent_list_html_nodes.append(parent)
            return parent_list_html_nodes
        case BlockType.QUOTE:
            formatted_text = format_quote_text(text)
            paragraphs: list[str] = []
            last_idx = 0
            for idx, line in enumerate(formatted_text.splitlines()):
                if line == "":
                    paragraphs.append(
                        " ".join(formatted_text.splitlines()[last_idx:idx])
                    )
                    last_idx = idx + 1
            paragraphs.append(" ".join(formatted_text.splitlines()[last_idx:]))

            parent_html_nodes: list[ParentNode] = []
            for paragraph in paragraphs:
                children = text_to_text_nodes(paragraph)
                children = list(map(text_node_to_html_node, children))
                parent_html_nodes.append(ParentNode("p", children))
            return parent_html_nodes

        case BlockType.HEADING:
            formatted_text = format_heading_text(text)
            heading_text_nodes = text_to_text_nodes(formatted_text)
            heading_html_nodes = list(map(text_node_to_html_node, heading_text_nodes))
            return heading_html_nodes

        case BlockType.PARAGRAPH:
            formatted_text = format_text(text)
            paragraph_text_nodes = text_to_text_nodes(formatted_text)
            paragraph_html_nodes = list(
                map(text_node_to_html_node, paragraph_text_nodes)
            )
            return paragraph_html_nodes


def format_text(text: str) -> str:
    list_of_lines = text.splitlines()
    formatted_text = " ".join(list_of_lines)
    return formatted_text


def format_code_text(text: str) -> str:
    list_of_lines = text.splitlines()
    formatted_text = "\n".join(list_of_lines[1:-1])
    formatted_text += "\n"
    return formatted_text


def format_unordered_list_text(text: str) -> str:
    list_of_lines = text.splitlines()
    list_of_lines = [re.sub(r"^(\- )", "", line) for line in list_of_lines]
    formatted_text = "\n".join(list_of_lines)
    return formatted_text


def format_ordered_list_text(text: str) -> str:
    list_of_lines = text.splitlines()
    list_of_lines = [re.sub(r"^(\d\. )", "", line) for line in list_of_lines]
    formatted_text = "\n".join(list_of_lines)
    return formatted_text


def format_quote_text(text: str) -> str:
    formatted_text = "\n".join(
        [line.strip() for line in text.replace(">", "").splitlines()]
    )
    return formatted_text


def format_heading_text(text: str) -> str:
    return text.replace("#", "")[1:]
