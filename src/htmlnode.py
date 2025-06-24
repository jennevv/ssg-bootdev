from typing import Optional


class HTMLNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[list["HTMLNode"]] = None,
        props: Optional[dict[str, str]] = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

        if value is None and children is None:
            raise ValueError("value and children cannot be None at the same time.")

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props:
            return f'href="{self.props["href"]}" target="{self.props["target"]}"'
        return ""

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
