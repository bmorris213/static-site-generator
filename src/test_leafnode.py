import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_html(self):
        node = LeafNode("This is a node", "p")
        print (node.to_html())
        node2 = LeafNode("this is raw test lmao")
        print (node2.to_html())
        node3 = LeafNode("Click this link for free sex", "a" , {"href":"https//free.sex.not_a_scam.org"})
        print (node3.to_html())

if __name__ == "__main__":
    unittest.main()