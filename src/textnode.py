from leafnode import LeafNode

from enum import Enum

class TextNode:
    text_type_delimiters = {
        "text" : "",
        "bold" : "**",
        "italic" : "*",
        "code": "`"
    }
    
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return self.text == other.text and \
            self.text_type == other.text_type and \
            self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
    def split_delimiter(self, t_type):
        if t_type not in self.text_type_delimiters.keys():
            # trying to split up using a type that has no delimiter
            return list(self)
        delimiter = self.text_type_delimiters[t_type]
        result = []
        temp = ""
        foundword = ""
        inside_delimiter = False
        delimiter_length = len(delimiter)
        current_index = 0

        while current_index < len(self.text):
            if self.text[current_index:current_index + delimiter_length] == delimiter:
                inside_delimiter = not inside_delimiter
                current_index += delimiter_length
                if not inside_delimiter:
                    result.append(TextNode(temp, "text"))
                    result.append(TextNode(foundword, t_type))
                    temp = ""
                    foundword = ""
                continue
            elif self.text[current_index] != delimiter[0]:
                if inside_delimiter:
                    foundword += self.text[current_index]
                else:
                    temp += self.text[current_index]
            current_index += 1
        
        if temp:
            result.append(TextNode(temp, "text"))
        if foundword:
            # end of word found without a closing delimiter
            result.append(TextNode(f"{delimiter}{foundword}", "text"))
        return result

    def to_html(self):
        if self.text_type == "text":
            return LeafNode(None, self.text)
        elif self.text_type == "bold":
            return LeafNode("b", self.text)
        elif self.text_type == "italic":
            return LeafNode("i", self.text)
        elif self.text_type == "code":
            return LeafNode("code", self.text)
        elif self.text_type == "link":
            return LeafNode("a", self.text, {"href":self.url})
        elif self.text_type == "image":
            return LeafNode("img", "", {"src":self.url, "alt":self.text})
        else:
            raise Exception(f"text type ({self.text_type}) of text node is invalid")