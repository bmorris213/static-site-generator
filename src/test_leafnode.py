import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_html(self):
        node = LeafNode("p", "This is a node")
        print (node.to_html())
        node2 = LeafNode(None, "this is raw test lmao")
        print (node2.to_html())
        node3 = LeafNode("a", "Click this link", {"href":"https//not_a_scam.org"})
        print (node3.to_html())

if __name__ == "__main__":
    unittest.main()