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
        if self.tag == None:
            print ("Tag: None")
        else:
            print(f"Tag: {self.tag}")
        if self.value == None:
            print ("Value: None")
        else:
            print(f"Value: {self.value}")

        children_print = "Children: "
        if self.children == None:
            print(f"{children_print}None")
        else:
            for child in self.children:
                children_print += f"{child}, "
            print(f"{children_print[:-2]}")
        
        if self.props == None:
            print("Props: None")
        else:
            print(f"Props: {self.props_to_html()}")