# static site generator
# 5/6/2024
# Brian Morris

# leaf node
# representation of lines of text at the ends of a tree
# should be used for the smallest units of text in a document

from textnode import TextNode
from enum import Enum, auto

class LeafNode(TextNode):
    # different types of line formatting for text
    class TextType(TextNode.TextType):
        NORMAL = auto()
        BOLD = auto()
        ITALIC = auto()
        CODE = auto()
        IMAGE = auto()
        LINK = auto()
    
    # leaf nodes have no children and must have a text value
    def __init__(self, text_type, text, props=None):
        super().__init__(text_type, text, None, props)

    # overwrite super
    # generates html code for a line
    def to_html(self):
        if self.text == None:
            raise ValueError("Leaf Nodes require a value")

        if self.text_type == LeafNode.TextType.NORMAL:
            return self.text

        tag = self.type_to_html()

        result = f"<{tag}"

        if self.props != None:
            result += self.props_to_html()
        
        result += f">{self.text}</{tag}>"
        return result
    
    # overwrite super
    # generates html tag for each text type
    def type_to_html(self):
        if self.text_type == LeafNode.TextType.NORMAL:
            return None
        elif self.text_type == LeafNode.TextType.BOLD:
            return "b"
        elif self.text_type == LeafNode.TextType.ITALIC:
            return "i"
        elif self.text_type == LeafNode.TextType.CODE:
            return "code"
        elif self.text_type == LeafNode.TextType.IMAGE:
            return "img"
        elif self.text_type == LeafNode.TextType.LINK:
            return "a"
        else:
            raise ValueError(f"text type of {self.text_type} is invalid html for leaf node")
    
    # props to html
    # returns html code representation of props
    def props_to_html(self):
        if self.props == None:
            return None

        newstring = ""

        for key in self.props:
            newstring += f" {key}=\"{self.props[key]}\""
        return newstring
        