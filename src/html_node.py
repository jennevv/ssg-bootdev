from typing import override


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str | None] | None = None,
    ):
        self.tag: str | None = tag
        self.value: str | None = value
        self.children: list["HTMLNode | LeafNode | ParentNode"] | None = children
        self.props: dict[str, str | None] | None = props

    def to_html(self) -> str | None:
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if self.props:
            return "".join([f' {key}="{value}"' for key, value in self.props.items()])
        return ""

    @override
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str | None,
        props: dict[str, str | None] | None = None,
    ):
        super().__init__(tag, value, None, props)

    @override
    def to_html(self) -> str:
        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()}>"
        elif self.value is None:
            raise ValueError("A LeafNode must have a value.")
        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list["HTMLNode | LeafNode | ParentNode"],
        props: dict[str, str | None] | None = None,
    ):
        super().__init__(tag, None, children, props)

    @override
    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("A ParentNode must have a tag.")
        if self.children is None:
            raise ValueError("A ParentNode must have children.")

        html = f"<{self.tag}>"
        for child in self.children:
            html += f"{child.to_html()}"
        html += f"</{self.tag}>"

        return html
