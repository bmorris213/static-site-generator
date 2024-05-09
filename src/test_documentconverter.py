import unittest

from documentconverter import DocumentConverter
from leafnode import LeafNode
from parentnode import ParentNode

# test suite    expected tests: 4
#   read_markdown               expected tests: 1
#   split_markdown              expected tests: 1
#   split_line_delimiter        expected tests: 1
#   extract_markdown_reference  expected tests: 1
class TestDocumentConverter(unittest.TestCase):
    def test_read_markdown(self):
        test_document = "This is the *first line* of text"
        test_document += "\n#with a heading of level 1\n\n##level 2\n####### and level6"
        test_document += "\n```\nand a code block\nwith **bold text**\nand a [link](https//www.google.com)"
        test_document += "\n> With some quotes too\n> \n> like `this one`\n\n\n"
        test_document += "\n1. and an ordered\n2.list\n3.3.with more\n5.weird cased"

        result = DocumentConverter.read_markdown(test_document)

        node_list = [LeafNode(LeafNode.TextType.NORMAL, "This is the ") , LeafNode(LeafNode.TextType.ITALIC, "first line"), LeafNode(LeafNode.TextType.NORMAL, " of text")]
        parent_list = [ParentNode(ParentNode.TextType.NORMAL, node_list)]
        node_list = [LeafNode(LeafNode.TextType.NORMAL, "with a heading of level 1")]
        parent_list.append(ParentNode(ParentNode.TextType.HEADING1, node_list))
        node_list = [LeafNode(LeafNode.TextType.NORMAL, "level 2")]
        parent_list.append(ParentNode(ParentNode.TextType.HEADING2, node_list))
        node_list = [LeafNode(LeafNode.TextType.NORMAL, "# and level6")]
        parent_list.append(ParentNode(ParentNode.TextType.HEADING6, node_list))
        node_list = [LeafNode(LeafNode.TextType.NORMAL, "and a code block"), LeafNode(LeafNode.TextType.NORMAL, "with "), LeafNode(LeafNode.TextType.BOLD, "bold text")]
        node_list.extend([LeafNode(LeafNode.TextType.NORMAL, "and a "), LeafNode(LeafNode.TextType.LINK, "link", {"href":"https//www.google.com"})])
        parent_list.append(ParentNode(ParentNode.TextType.CODE, node_list))
        node_list = [LeafNode(LeafNode.TextType.NORMAL, "With some quotes too"), LeafNode(LeafNode.TextType.NORMAL, "like "), LeafNode(LeafNode.TextType.CODE, "this one")]
        parent_list.append(ParentNode(ParentNode.TextType.QUOTE, node_list))
        node_list = [LeafNode(LeafNode.TextType.NORMAL, " and an ordered"), LeafNode(LeafNode.TextType.NORMAL, "list"), LeafNode(LeafNode.TextType.NORMAL, "3.with more")]
        parent_list.append(ParentNode(ParentNode.TextType.ORDERED_LIST, node_list))
        node_list = [LeafNode(LeafNode.TextType.NORMAL, "5.weird cased")]
        parent_list.append(ParentNode(ParentNode.TextType.NORMAL, node_list))

        expected_output = ParentNode(ParentNode.TextType.ROOT, parent_list)

        self.assertEqual(result, expected_output)
    
    def test_split_markdown(self):
        test_document = "This is the *first line* of text"
        test_document += "\n#with a heading of level 1\n\n##level 2\n####### and level6"
        test_document += "\n```\nand a code block\nwith **bold text**\nand a [link](https//www.google.com)"
        test_document += "\n> With some quotes too\n> \n> like `this one`\n\n\n"
        test_document += "\n1. and an ordered\n2.list\n3.3.with more\n5.weird cased"

        result = DocumentConverter.split_markdown(test_document)

        expected_output = [(ParentNode.TextType.NORMAL, ["This is the *first line* of text"])]
        expected_output.append((ParentNode.TextType.HEADING1, ["with a heading of level 1"]))
        expected_output.append((ParentNode.TextType.HEADING2, ["level 2"]))
        expected_output.append((ParentNode.TextType.HEADING6, ["# and level6"]))
        expected_output.append((ParentNode.TextType.CODE, ["and a code block", "with **bold text**", "and a [link](https//www.google.com)"]))
        expected_output.append((ParentNode.TextType.QUOTE, ["With some quotes too","like `this one`"]))
        expected_output.append((ParentNode.TextType.ORDERED_LIST, [" and an ordered","list","3.with more"]))
        expected_output.append((ParentNode.TextType.NORMAL, ["5.weird cased"]))

        self.assertEqual(result, expected_output)

    def test_split_line_delimiter(self):
        test_string = "This is *italic with **bold inside** it*"

        result = DocumentConverter.split_line_delimiter(test_string, DocumentConverter.markdown_delimiters, LeafNode.TextType.NORMAL)

        expected_output = [(LeafNode.TextType.NORMAL, "This is ")]
        expected_output.append((LeafNode.TextType.ITALIC, "italic with "))
        expected_output.append((LeafNode.TextType.BOLD, "bold inside"))
        expected_output.append((LeafNode.TextType.ITALIC, " it"))

        self.assertEqual(result, expected_output)
    
    def test_extract_markdown_reference(self):
        test_string = "This is ![an image](https://google.com), and this is [a link](https://yahoo.com)"

        result = DocumentConverter.extract_markdown_references(test_string, LeafNode.TextType.NORMAL)
        
        expected_output = [(LeafNode.TextType.NORMAL, "This is ", None)]
        expected_output.append((LeafNode.TextType.IMAGE, "an image", "https://google.com"))
        expected_output.append((LeafNode.TextType.NORMAL, ", and this is ", None))
        expected_output.append((LeafNode.TextType.LINK, "a link", "https://yahoo.com"))

        self.assertEqual(result, expected_output)

if __name__ == "__main__":
    unittest.main()