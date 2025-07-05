from .text_node import TextNode, TextType
from .split_text_node import split_nodes_delimiter, split_nodes_image, split_nodes_link


def text_to_text_nodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text=text, text_type=TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, delimiter="**", text_type=TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, delimiter="_", text_type=TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, delimiter="`", text_type=TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
