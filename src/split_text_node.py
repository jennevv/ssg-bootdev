from .link_extraction import extract_markdown_images, extract_markdown_links
from .textnode import TextNode, TextType


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


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    nodes: list[TextNode] = []

    for node in old_nodes:
        text = node.text
        images: list[tuple[str, str]] = extract_markdown_images(text)

        if images == []:
            nodes.append(node)
        else:
            for i, image in enumerate(images):
                if i == 0:
                    split = text.split(f"![{image[0]}]({image[1]})", maxsplit=1)
                    nodes.append(TextNode(text=split[0], text_type=TextType.TEXT))
                    nodes.append(
                        TextNode(text=image[0], text_type=TextType.IMAGE, url=image[1])
                    )
                else:
                    prev_split: list[str] = split
                    split = prev_split[1].split(
                        f"![{image[0]}]({image[1]})", maxsplit=1
                    )
                    nodes.append(TextNode(text=split[0], text_type=TextType.TEXT))
                    nodes.append(
                        TextNode(text=image[0], text_type=TextType.IMAGE, url=image[1])
                    )

                if i + 1 == len(images) and split[1] != "":
                    nodes.append(TextNode(text=split[1], text_type=TextType.TEXT))

    return nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    nodes: list[TextNode] = []

    for node in old_nodes:
        text = node.text
        links: list[tuple[str, str]] = extract_markdown_links(text)

        if links == []:
            nodes.append(node)

        else:
            for i, link in enumerate(links):
                if i == 0:
                    split = text.split(f"[{link[0]}]({link[1]})", maxsplit=1)
                    nodes.append(TextNode(text=split[0], text_type=TextType.TEXT))
                    nodes.append(
                        TextNode(text=link[0], text_type=TextType.LINK, url=link[1])
                    )
                else:
                    prev_split: list[str] = split
                    split = prev_split[1].split(f"[{link[0]}]({link[1]})", maxsplit=1)
                    nodes.append(TextNode(text=split[0], text_type=TextType.TEXT))
                    nodes.append(
                        TextNode(text=link[0], text_type=TextType.LINK, url=link[1])
                    )

                if i + 1 == len(links) and split[1] != "":
                    nodes.append(TextNode(text=split[1], text_type=TextType.TEXT))

    return nodes
