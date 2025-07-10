import unittest

from src.markdown_to_html_node import markdown_to_html_node


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
This is text that _should_ remain
the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quote(self):
        md = ">This is a **quote**\n>spread over multiple _lines_>\n>I guess"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote><p>This is a <b>quote</b> spread over multiple <i>lines</i> I guess</p></blockquote></div>",
        )

    def test_quote_multiple_paragraphs(self):
        md = ">This is a **quote**\n>spread over multiple _lines_\n>\n>I guess"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote><p>This is a <b>quote</b> spread over multiple <i>lines</i></p><p>I guess</p></blockquote></div>",
        )

    def test_unordered_list(self):
        md = "\n- **item** 1\n- item 2\n- item 3"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li><b>item</b> 1</li><li>item 2</li><li>item 3</li></ul></div>",
        )

    def test_ordered_list(self):
        md = "\n1. item 1\n2. item 2\n3. item 3"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><ol><li>item 1</li><li>item 2</li><li>item 3</li></ol></div>"
        )

    def test_heading(self):
        md = "# Heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Heading</h1></div>")
