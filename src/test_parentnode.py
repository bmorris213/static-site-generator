import unittest

from leafnode import LeafNode
from parentnode import ParentNode

# test suite    expected tests: 5
#   eq              expected tests: 2
#   repr            expected tests: 1
#   type_to_html    expected tests: 1
#   to_html         expected tests: 1
class TestParentNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode(LeafNode.TextType.NORMAL, "This is a node")
        node2 = LeafNode(LeafNode.TextType.NORMAL, "This is a node")

        parentnode = ParentNode(ParentNode.TextType.ROOT, [node, node2])
        parentnode2 = ParentNode(ParentNode.TextType.ROOT, [node, node2])

        self.assertTrue(parentnode == parentnode2)

        node = LeafNode(LeafNode.TextType.NORMAL, "This is a node")
        node2 = LeafNode(LeafNode.TextType.BOLD, "This is another node")

        parentnode = ParentNode(ParentNode.TextType.ROOT, [node, node2])
        parentnode2 = ParentNode(ParentNode.TextType.NORMAL, [node, node2])

        self.assertFalse(parentnode == parentnode2)
    
    def test_rep(self):
        node = LeafNode(LeafNode.TextType.NORMAL, "This is a node")
        node2 = LeafNode(LeafNode.TextType.NORMAL, "This is a node")
        node3 = LeafNode(LeafNode.TextType.ITALIC, "This is some italic text")

        parentnode = ParentNode(ParentNode.TextType.ROOT, [node, node2, node3])

        result = repr(parentnode)

        expected_output = "Text Type: TextType.ROOT"
        expected_output += "\nValue: None\nChildren: ["
        expected_output += "\nCHILD: <"
        expected_output += "\nText Type: TextType.NORMAL\nValue: This is a node\nChildren: None\nProps: None >"
        expected_output += "\nCHILD: <"
        expected_output += "\nText Type: TextType.NORMAL\nValue: This is a node\nChildren: None\nProps: None >"
        expected_output += "\nCHILD: <"
        expected_output += "\nText Type: TextType.ITALIC\nValue: This is some italic text\nChildren: None\nProps: None >"
        expected_output += "\n]"
        expected_output += "\nProps: None"

        self.assertEqual(result, expected_output)

    def test_type_to_html(self):
        node = LeafNode(LeafNode.TextType.NORMAL, "This is a node")
        node2 = LeafNode(LeafNode.TextType.BOLD, "This is another node")
        node3 = LeafNode(LeafNode.TextType.IMAGE, "", {"alt":"This is an image","href":"https//www.yahoo.com"})

        parentnode = ParentNode(ParentNode.TextType.ROOT, [node, node3])
        parentnode2 = ParentNode(ParentNode.TextType.CODE, [node, node2])
        parentnode3 = ParentNode(ParentNode.TextType.NORMAL, [node2, node3])
        
        result = f"{parentnode.type_to_html()}\n{parentnode2.type_to_html()}\n{parentnode3.type_to_html()}"

        expected_output = "div\ncode\np"

        self.assertEqual(result, expected_output)

    def test_to_html(self):
        node = LeafNode(LeafNode.TextType.NORMAL, "This is a node")
        node2 = LeafNode(LeafNode.TextType.BOLD, "This is another node")
        node3 = LeafNode(LeafNode.TextType.IMAGE, "", {"alt":"This is an image","href":"https//www.yahoo.com"})
        
        parentnode = ParentNode(ParentNode.TextType.QUOTE, [node, node3])
        parentnode2 = ParentNode(ParentNode.TextType.CODE, [node, node2])
        parentnode3 = ParentNode(ParentNode.TextType.NORMAL, [node2, node3])
        
        rootnode = ParentNode(ParentNode.TextType.ROOT, [parentnode, parentnode2, parentnode3])
        
        result = f"{rootnode.to_html()}"

        expected_output = "<div>\n<blockquote>\n\tThis is a node"
        expected_output += "\n\t<img alt=\"This is an image\" href=\"https//www.yahoo.com\"></img>"
        expected_output += "\n</blockquote>\n<code>\n\tThis is a node\n\t<b>This is another node</b>"
        expected_output += "\n</code>\n<p>"
        expected_output += "\n\t<b>This is another node</b>\n\t<img alt=\"This is an image\" href=\"https//www.yahoo.com\"></img>"
        expected_output += "\n</p>\n</div>"

        self.assertEqual(result, expected_output)

if __name__ == "__main__":
    unittest.main()