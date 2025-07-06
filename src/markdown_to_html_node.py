from src.text_node import TextNode, TextType
from .block_type import md_block_to_block_type, BlockType, heading_level
from .markdown_to_blocks import markdown_to_blocks
from .html_node import LeafNode, ParentNode, HTMLNode
from .text_to_text_nodes import text_to_text_nodes
from .text_node_to_html_node import text_node_to_html_node


def markdown_to_html_node(md: str) -> HTMLNode:
    md_blocks = markdown_to_blocks(md)
    html_nodes = []
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
                parent = ParentNode(tag="col", children=children)
            case BlockType.ORDERED_LIST:
                parent = ParentNode(tag="p", children=children)

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
            formatted_text = format_list_text(text)
            list_items = formatted_text.split("\n")
            list_item_text_nodes = list(map(text_to_text_nodes, list_items))
            list_item_html_nodes = [
                ParentNode("li", children=[item_text_node])
                for item_text_node in list_item_text_nodes
            ]
            return list_item_html_nodes
        case BlockType.ORDERED_LIST:
            formatted_text = format_list_text(text)
            list_items = formatted_text.split("\n")
            list_item_text_nodes = list(map(text_to_text_nodes, list_items))
            list_item_html_nodes = [
                ParentNode("li", children=[item_text_node])
                for item_text_node in list_item_text_nodes
            ]
            return list_item_html_nodes
        case _:
            formatted_text = format_text(text)
            text_nodes = text_to_text_nodes(formatted_text)
            html_nodes = list(map(text_node_to_html_node, text_nodes))
            return html_nodes


def format_text(text: str) -> str:
    list_of_lines = text.splitlines()
    list_of_lines = [line.strip() for line in list_of_lines]
    formatted_text = " ".join(list_of_lines)
    return formatted_text


def format_code_text(text: str) -> str:
    list_of_lines = text.splitlines()
    list_of_lines = [line.strip() for line in list_of_lines]
    formatted_text = "\n".join(list_of_lines[1:-1])
    formatted_text += "\n"
    return formatted_text


def format_list_text(text: str) -> str:
    list_of_lines = text.splitlines()
    list_of_lines = [line.strip() for line in list_of_lines]
    formatted_text = "\n".join(list_of_lines)
    return formatted_text
