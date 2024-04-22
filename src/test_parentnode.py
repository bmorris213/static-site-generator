import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_repr(self):
        node = ParentNode (
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                ParentNode(
                    "p",
                    [
                        LeafNode("i", "Italic text"),
                        LeafNode("u", "Underline text")
                    ]
                )
            ]
        )

        print (node.to_html())

if __name__ == "__main__":
    unittest.main()