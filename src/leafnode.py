from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        # leaf nodes have no children, and must have a value
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        htmlresult = "<"
        htmlresult += self.tag
        if self.props != None:
            htmlresult += self.props_to_html()
        htmlresult += ">"
        htmlresult += self.value
        htmlresult += f"<\\{self.tag}>"
        return htmlresult
