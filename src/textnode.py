# static site generator
# 5/6/2024
# Brian Morris

# text node
# representation of a unit of text in a document
# used for construction of trees of relationship between text units

from enum import Enum, auto

class TextNode:
    # text type
    # intended to inscribe enum values for parent and leaf nodes
    # used to represent block types, and inline text types, respectively
    class TextType(Enum):
        pass
    
    # default constructor
    # requires enum value for type of text
    # can be empty of text, children, or properties
    def __init__(self, text_type, text=None, children=None, props=None):
        self.text_type = text_type
        self.text = text
        self.children = children
        self.props = props
    
    def __eq__(self, other):
        result = self.text == other.text
        result = result and self.text_type == other.text_type
        result = result and self.children == other.children
        return result and self.props == other.props

    def __repr__(self):
        representation = f"Text Type: {self.text_type}"
        
        if self.text == None:
            representation += "\nValue: None"
        else:
            representation += f"\nValue: {self.text}"

        children_print = "\nChildren: "
        if self.children == None:
            representation += f"{children_print}None"
        else:
            children_print += "["
            for child in self.children:
                children_print += f"\nCHILD: <\n{child} >"
            representation += f"{children_print}\n]"
        
        if self.props == None:
            representation += "\nProps: None"
        else:
            representation += "\nProps:\n"
            for prop in self.props:
                representation += f"{prop} = {self.props[prop]}\n"
            representation = representation[:-1]
        
        return representation
    
    # to html
    # returns html code reprentation of the text tree structure
    # is to be used by parent node, and leaf nodes
    def to_html(self):
        raise NotImplementedError
    
    # type to html
    # convert text_type to an appropriate html tag
    # unimplemented since there are different types for leaf and parent
    def type_to_html(self):
        raise NotImplementedError