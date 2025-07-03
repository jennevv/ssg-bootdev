def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks]
    blocks = list(filter(lambda x: x != "", blocks))

    return blocks
