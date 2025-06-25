import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode(
            "<a>",
            "some text",
            [],
            {"href": "https://www.google.com", "target": "_blank"},
        )
        expected_string = "HTMLNode(<a>, some text, [], {'href': 'https://www.google.com', 'target': '_blank'})"
        self.assertEqual(node.__repr__(), expected_string)

    def test_to_html(self):
        node = HTMLNode("<a>", "text", [])
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        node = HTMLNode(
            "<a>",
            "some text",
            [],
            {"href": "https://www.google.com", "target": "_blank"},
        )

        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

        node2 = HTMLNode("<a>", "some text")

        self.assertEqual(node2.props_to_html(), "")


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "www.boots.dev", "target": "_blank"})
        self.assertEqual(
            node.to_html(), '<a href="www.boots.dev" target="_blank">Click me!</a>'
        )

    def test_leaf_to_html_header(self):
        node = LeafNode("h1", "header 1")
        self.assertEqual(node.to_html(), "<h1>header 1</h1>")

    def test_leaf_to_html_code(self):
        node = LeafNode("code", "y = x")
        self.assertEqual(node.to_html(), "<code>y = x</code>")

    def test_to_html_img(self):
        node = LeafNode(
            "img",
            None,
            {
                "src": "img_girl.jpg",
                "alt": "Girl in a jacket",
                "width": "500",
                "height": "600",
            },
        )
        self.assertEqual(
            node.to_html(),
            '<img src="img_girl.jpg" alt="Girl in a jacket" width="500" height="600">',
        )

    def test_leaf_to_html_value_is_none(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_tag_is_none(self):
        node = LeafNode(None, "some text")
        self.assertEqual(node.to_html(), "some text")


class TestParentNode(unittest.TestCase):
    def test_to_html_with_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchild(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("b", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(), "<div><span>child1</span><b>child2</b></div>"
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node1a = LeafNode("b", "grandchild1a")
        grandchild_node2a = LeafNode("b", "grandchild2a")
        grandchild_node1b = LeafNode("b", "grandchild1b")
        grandchild_node2b = LeafNode("b", "grandchild2b")
        child_node1 = ParentNode("span", [grandchild_node1a, grandchild_node1b])
        child_node2 = ParentNode("span", [grandchild_node2a, grandchild_node2b])
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild1a</b><b>grandchild1b</b></span><span><b>grandchild2a</b><b>grandchild2b</b></span></div>",
        )

    def test_to_html_with_nested_parents(self):
        parent_node1 = ParentNode("div", [])
        parent_node2 = ParentNode("div", [parent_node1])
        parent_node1.children = [parent_node2]
        with self.assertRaises(RecursionError):
            parent_node1.to_html()
