import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_text_to_html(self):
        #it breaks up bold first... because of ordering OOPS
        #also inline text_type AND block block_types need to be classified
        #   <Code blocks should be surrounded by a <code> tag nested inside a <pre> tag.
        #   and list item should be surrounded by a <ul> or <ol>tag.
        # there are currently no /n how do I add them back in?? hmm
        # ordered list has no <ol> and still has 1. and etc etc
        test_text = "This is a test text"
        test_text += "\n> And these are quotes"
        test_text += "\n> with **bold** words"
        test_text += "\n# this is a heading with *italic*\n## and heading level 2\n### and three\n###### and six!"
        test_text += "\n```\nWhile this is code!\nit has an ![image](https://google.com.png)\n```"
        test_text += "\n1. and\n2. an\n3. ordered\n4. list!"
        test_text += "\n* unordered\n- list\n* anyone?"
        test_text += "\nwith also a `code block` and a [link](https://boot.dev)"
        parent_node = TextNode.process_doc(test_text)
        print(parent_node.to_html())

if __name__ == "__main__":
    unittest.main()
