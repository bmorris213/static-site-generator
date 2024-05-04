from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        # parent nodes have no value, and must have children
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.children == None:
            raise ValueError("Parent Nodes require children")
        if self.tag == None:
            raise ValueError("Parent nodes require a tag")
        htmlresult = f"<{self.tag}>"
        for child in self.children:
            htmlresult += f"{child.to_html()}"
        htmlresult += f"<\{self.tag}>"
        return htmlresult
        