import unittest

from textnode import TextNode
from textnode import TextType

class TestTextNode(unittest.TestCase):
    def test_text_to_html(self):
        node = TextNode("This is a text node", TextType.bold)
        node2 = TextNode("This is a text node", TextType.italic)
        leaf = node.to_html()
        print(leaf)
        print(node2.to_html())


if __name__ == "__main__":
    unittest.main()
