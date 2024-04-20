import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node_children = ("one", "two", "three", "four")
        node_properties = {"first":"https://your.mom", "second":"blank"}
        node = HTMLNode("a", "breakfast club", node_children, node_properties)
        print(node)
        node2 = HTMLNode()
        print(node2)

if __name__ == "__main__":
    unittest.main()