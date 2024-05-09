# static site generator
# 5/6/2024
# Brian Morris

# parent node
# represents blocks of formatted text
# can be nested, where root represents the entire document

from textnode import TextNode
from enum import Enum, auto

class ParentNode(TextNode):
    # different types of block formatting for text
    class TextType(TextNode.TextType):
        NORMAL = auto()
        ROOT = auto()
        QUOTE = auto()
        CODE = auto()
        PREFORMAT = auto()
        ORDERED_LIST = auto()
        UNORDERED_LIST = auto()
        HEADING1 = auto()
        HEADING2 = auto()
        HEADING3 = auto()
        HEADING4 = auto()
        HEADING5 = auto()
        HEADING6 = auto()
    
    # parent nodes must have children, but cannot have text or props
    def __init__(self, text_type, children):
        super().__init__(text_type, None, children, None)

    # overwrite super
    # generates html code for a block of text
    def to_html(self, recur_level=None):
        if self.children == None or len(self.children) == 0:
            raise ValueError("Parent nodes must have children")
        
        children_text = ""
        # recursion level is an internal factor storing level of nested parents
        if recur_level == None:
            recur_level = 0
        
        # notes about additional issues:
        #   lists need <li></li> on each item

        tag = self.type_to_html()

        for child in self.children:
            children_text += "\n"
            # a nested parent needs not have extra tabs
            # the parent's recursion level will take care of that
            if type(child) == ParentNode:
                children_text += child.to_html(recur_level + 1)
            else:
                # only leaf nodes need be indented
                for i in range(recur_level):
                    children_text += "\t"
                # children leaf nodes which are ul or ol need to be wrapped in <li>
                if tag == "ul" or tag == "ol":
                    children_text += "<li>"
                children_text += child.to_html()
                if tag == "ul" or tag == "ol":
                    children_text += "</li>"
        children_text += "\n"

        return f"<{tag}>{children_text}</{tag}>"

    # overwrite super
    # generates a tag for a block of text based on type
    def type_to_html(self):
        if self.text_type == ParentNode.TextType.NORMAL:
            return "p"
        elif self.text_type == ParentNode.TextType.ROOT:
            return "div"
        elif self.text_type == ParentNode.TextType.QUOTE:
            return "blockquote"
        elif self.text_type == ParentNode.TextType.CODE:
            return "code"
        elif self.text_type == ParentNode.TextType.PREFORMAT:
            return "pre"
        elif self.text_type == ParentNode.TextType.ORDERED_LIST:
            return "ol"
        elif self.text_type == ParentNode.TextType.UNORDERED_LIST:
            return "ul"
        elif self.text_type == ParentNode.TextType.HEADING_1:
            return "h1"
        elif self.text_type == ParentNode.TextType.HEADING_2:
            return "h2"
        elif self.text_type == ParentNode.TextType.HEADING_3:
            return "h3"
        elif self.text_type == ParentNode.TextType.HEADING_4:
            return "h4"
        elif self.text_type == ParentNode.TextType.HEADING_5:
            return "h5"
        elif self.text_type == ParentNode.TextType.HEADING_6:
            return "h6"
        else:
            raise ValueError(f"Parent node has invalid type of {self.text_type}")