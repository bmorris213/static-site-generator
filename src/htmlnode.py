class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        newstring = ""
        if self.props == None:
            return None
        for key in self.props:
            newstring += f" {key}=\"{self.props[key]}\""
        return newstring
    
    def __repr__(self):
        representation = ""
        if self.tag == None:
            representation += "\nTag: None"
        else:
            representation += f"\nTag: {self.tag}"
        if self.value == None:
            representation += "\nValue: None"
        else:
            representation += f"\nValue: {self.value}"

        children_print = "\nChildren: "
        if self.children == None:
            representation += f"{children_print}None"
        else:
            children_print += "("
            for child in self.children:
                children_print += f"{child}, "
            representation += f"{children_print[:-2]})"
        
        if self.props == None:
            representation += "\nProps: None"
        else:
            representation += f"\nProps: {{{self.props_to_html()}}}"
        
        return representation