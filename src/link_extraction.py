import re


def extract_markdown_images(text: str) -> list[tuple[str]]:
    image = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return image


def extract_markdown_links(text: str) -> list[tuple[str]]:
    link = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return link
