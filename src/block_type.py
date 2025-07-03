import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def md_block_to_block_type(md_block: str) -> BlockType:
    if contains_heading(md_block):
        return BlockType("heading")
    elif contains_code(md_block):
        return BlockType("code")
    elif contains_quote(md_block):
        return BlockType("quote")
    elif contains_unordered_list(md_block):
        return BlockType("UNORDERED_LIST")
    elif contains_ordered_list(md_block):
        return BlockType("ordered_list")
    else:
        return BlockType("paragraph")


def contains_heading(md_block: str) -> bool:
    return bool(re.match("^(#{1,6}) .*", md_block))


def contains_code(md_block: str) -> bool:
    return bool(re.match("^(```)|(```)$", md_block))


def contains_quote(md_block: str) -> bool:
    split_over_lines = md_block.split("\n")
    starts_with_char = list(
        filter(lambda x: bool(re.match(r"(^|(?<=\n))>", x)), md_block)
    )
    return len(starts_with_char) == len(split_over_lines)


def contains_unordered_list(md_block: str) -> bool:
    split_over_lines = md_block.split("\n")
    starts_with_char = list(
        filter(lambda x: bool(re.match(r"(^|(?<=\n))- ", x)), md_block)
    )
    return len(starts_with_char) == len(split_over_lines)


def contains_ordered_list(md_block: str) -> bool:
    split_over_lines = md_block.split("\n")
    starts_with_char = list(
        filter(lambda x: bool(re.match(r"(^|(?<=\n))\d\. ", x)), md_block)
    )
    return len(starts_with_char) == len(split_over_lines)
