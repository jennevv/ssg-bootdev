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

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props:
            return "".join([f' {key}="{value}"' for key, value in self.props.items()])
        return ""

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        value: str,
        props: Optional[dict[str, str]] = None,
    ):
        super().__init__(tag, value, None, props)

    def to_html(self):
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
        children: HTMLNode,
        props: Optional[dict[str, str]] = None,
    ):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("A ParentNode must have a tag.")
        if self.children is None:
            raise ValueError("A ParentNode must have children.")

        html = f"<{self.tag}>"
        for child in self.children:
            html += f"{child.to_html()}"
        html += f"</{self.tag}>"

        return html
