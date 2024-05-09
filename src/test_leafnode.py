import unittest

from leafnode import LeafNode

# test suite    expected tests: 6
#   eq              expected tests: 2
#   repr            expected tests: 1
#   props_to_html   expected tests: 1
#   type_to_html    expected tests: 1
#   to_html         expected tests: 1
class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode(LeafNode.TextType.NORMAL, "This is a node")
        node2 = LeafNode(LeafNode.TextType.NORMAL, "This is a node")
        self.assertTrue(node == node2)

        node = LeafNode(LeafNode.TextType.NORMAL, "This is a node")
        node2 = LeafNode(LeafNode.TextType.BOLD, "This is another node")
        self.assertFalse(node == node2)
    
    def test_rep(self):
        node = LeafNode(LeafNode.TextType.ITALIC, "This is some italic text")
        
        result = repr(node)

        expected_output = "Text Type: TextType.ITALIC"
        expected_output += "\nValue: This is some italic text"
        expected_output += "\nChildren: None"
        expected_output += "\nProps: None"

        self.assertEqual(result, expected_output)

    def test_props_to_html(self):
        node = LeafNode(LeafNode.TextType.IMAGE, "", {"alt":"This is an image","href":"https//www.yahoo.com"})
        node2 = LeafNode(LeafNode.TextType.LINK, "This is a link", {"href":"https//www.google.com"})

        result = node.props_to_html()
        result += f"\n{node2.props_to_html()}"

        expected_output = " alt=\"This is an image\" href=\"https//www.yahoo.com\""
        expected_output += "\n href=\"https//www.google.com\""

        self.assertEqual(result, expected_output)
    
    def test_type_to_html(self):
        node = LeafNode(LeafNode.TextType.NORMAL, "This is a node")
        node2 = LeafNode(LeafNode.TextType.BOLD, "This is another node")
        node3 = LeafNode(LeafNode.TextType.IMAGE, "", {"alt":"This is an image","href":"https//www.yahoo.com"})

        result = f"{node.type_to_html()}"
        result += f"\n{node2.type_to_html()}"
        result += f"\n{node3.type_to_html()}"

        expected_output = "None\nb\nimg"

        self.assertEqual(result, expected_output)
    
    def test_to_html(self):
        node = LeafNode(LeafNode.TextType.NORMAL, "This is a node")
        node2 = LeafNode(LeafNode.TextType.BOLD, "This is another node")
        node3 = LeafNode(LeafNode.TextType.IMAGE, "", {"alt":"This is an image","href":"https//www.yahoo.com"})

        result = f"{node.to_html()}"
        result += f"\n{node2.to_html()}"
        result += f"\n{node3.to_html()}"

        expected_output = "This is a node"
        expected_output += "\n<b>This is another node</b>"
        expected_output += "\n<img alt=\"This is an image\" href=\"https//www.yahoo.com\"></img>"
        
        self.assertEqual(result, expected_output)

if __name__ == "__main__":
    unittest.main()