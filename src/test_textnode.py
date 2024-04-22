import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_text_to_html(self):
        node = TextNode("This is a **text** node with **bold text** and *italic* text **ending** without being **bold", "bold")
        splitnodes = node.split_delimiter("bold") # fix t_type vs delimiter class types lmao it took away the italic *s
        for item in splitnodes:
            print(item.to_html())

if __name__ == "__main__":
    unittest.main()
