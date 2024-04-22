from leafnode import LeafNode

from enum import Enum

class TextType(Enum):
    text = 0
    bold = 1
    italic = 2
    code = 3
    link = 4
    image = 5

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        if text_type not in list(TextType):
            raise Exception("text type enum of an invalid type")
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return self.text == other.text and \
            self.text_type == other.text_type and \
            self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
    def to_html(self):
        if self.text_type == TextType.text:
            return LeafNode(None, self.text)
        elif self.text_type == TextType.bold:
            return LeafNode("b", self.text)
        elif self.text_type == TextType.italic:
            return LeafNode("i", self.text)
        elif self.text_type == TextType.code:
            return LeafNode("code", self.text)
        elif self.text_type == TextType.link:
            return LeafNode("a", self.text, {"href":self.url})
        elif self.text_type == TextType.image:
            return LeafNode("img", "", {"src":self.url, "alt":self.text})
        else:
            raise Exception(f"text type ({self.text_type}) of text node is invalid")