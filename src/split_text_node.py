from .textnode import TextNode, TextType


def split_nodes_delimiter(node, delimiter, text_type):
    check_delimiter_text_type_match(delimiter, text_type)

    size_delim = len(delimiter)
    nodes = []
    text = node.text
    first = text.find(delimiter)

    if first == -1:
        return [node]
    elif first != 0:
        nodes.append(TextNode(text[:first], TextType.TEXT))

    second = text.find(delimiter, first + size_delim)

    while second != -1:
        delim_node = TextNode(text[first + size_delim : second], text_type)
        nodes.append(delim_node)

        first = text.find(delimiter, second + size_delim)

        if first != -1:
            regular_node = TextNode(text[second + size_delim : first], TextType.TEXT)
            nodes.append(regular_node)
        else:
            regular_node = TextNode(text[second + size_delim :], TextType.TEXT)
            nodes.append(regular_node)
            break

        second = text.find(delimiter, first + size_delim)

    return nodes


def check_delimiter_text_type_match(delimiter, text_type) -> None:
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
