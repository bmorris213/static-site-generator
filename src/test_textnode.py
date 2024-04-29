import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_text_to_html(self):
        #it breaks up bold first... because of ordering OOPS
        test_text = "This is **text** with an *italic* word and a `code block` and an ![image](https://google.com.png) and a [link](https://boot.dev)"
        node_group = TextNode.text_to_html(test_text)
        for node in node_group:
            print(node.to_html())

if __name__ == "__main__":
    unittest.main()
