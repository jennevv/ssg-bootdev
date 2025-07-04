from typing import Callable
from .link_extraction import extract_markdown_images, extract_markdown_links
from .text_node import TextNode, TextType


def check_delimiter_text_type_match(delimiter: str, text_type: TextType) -> None:
    match text_type:
        case TextType.BOLD:
            if delimiter != "**":
                raise ValueError(
                    f"Incorrect delimiter {delimiter} for text_type {text_type}."
                )
        case TextType.ITALIC:
            if delimiter != "*" and delimiter != "_":
                raise ValueError(
                    f"Incorrect delimiter {delimiter} for text_type {text_type}."
                )
        case TextType.CODE:
            if delimiter != "`":
                raise ValueError(
                    f"Incorrect delimiter {delimiter} for text_type {text_type}."
                )
        case _:
            raise NotImplementedError("Text type {text_type} is not implemented.")


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    check_delimiter_text_type_match(delimiter, text_type)

    size_delim = len(delimiter)
    nodes: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.extend([node])
            continue

        text: str = node.text
        first = text.find(delimiter)

        if first == -1:
            nodes.extend([node])
            continue
        elif first != 0:
            nodes.append(TextNode(text[:first], TextType.TEXT))

        second = text.find(delimiter, first + size_delim)

        while second != -1:
            delim_node = TextNode(text[first + size_delim : second], text_type)
            nodes.append(delim_node)

            first = text.find(delimiter, second + size_delim)

            if first != -1:
                regular_node = TextNode(
                    text[second + size_delim : first], TextType.TEXT
                )
                nodes.append(regular_node)
            else:
                regular_node = TextNode(text[second + size_delim :], TextType.TEXT)
                nodes.append(regular_node)
                break

            second = text.find(delimiter, first + size_delim)

    return nodes


def splitter(
    old_nodes: list[TextNode],
    str_format: str,
    extract_func: Callable[[str], list[tuple[str, str]]],
    text_type: TextType,
) -> list[TextNode]:
    nodes: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.extend([node])
            continue

        text = node.text
        items = extract_func(text)

        if items == []:
            nodes.append(node)
        else:
            for i, item in enumerate(items):
                if i == 0:
                    split = text.split(str_format.format(item[0], item[1]), maxsplit=1)
                else:
                    split = split[1].split(
                        str_format.format(item[0], item[1]), maxsplit=1
                    )

                if split[0] != "":
                    nodes.append(TextNode(text=split[0], text_type=TextType.TEXT))

                nodes.append(TextNode(text=item[0], text_type=text_type, url=item[1]))

                if i + 1 == len(items) and split[1] != "":
                    nodes.append(TextNode(text=split[1], text_type=TextType.TEXT))

    return nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    str_format = "![{}]({})"
    nodes = splitter(old_nodes, str_format, extract_markdown_images, TextType.IMAGE)
    return nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    str_format = "[{}]({})"
    nodes = splitter(old_nodes, str_format, extract_markdown_links, TextType.LINK)
    return nodes
