from leafnode import LeafNode

import re

class TextNode:
    
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

    @staticmethod
    def text_to_html(text):
        text_lines = text.split("\n")
        temp = []
        # for each line, add a list of inline text nodes
        for line in text_lines:
            line_node = TextNode(line, "text")
            temp.append(line_node.seperate_inline())
        #flatten temp
        result = []
        for group in temp:
            result.extend(group)
        return result

    def seperate_inline(self):
        result = []
        result.append(self) # result is 1 node long
        
        delimiter_types = {
            "bold" : "**",
            "italic" : "*",
            "code" : "`"
        }

        for t_type in delimiter_types:
            temp = []
            # temp is the new layer of nodes
            for node in result:
                temp.extend(node.seperate_delimiter(t_type, delimiter_types[t_type]))
            # temp has a list of node_lists created by seperate_delimiter
            result = temp.copy()

        new_result = []
        for node in result:
            temp = node.seperate_images()
            for item in temp:
                new_group = item.seperate_links()
                for new_item in new_group:
                    if new_item.text != "":
                        new_result.append(new_item)

        return new_result

    def seperate_images(self):
        result = []
        image_group = re.findall(r"!\[(.*?)\]\((.*?)\)", self.text)
        if len(image_group) != 0:
            for item in image_group:
                substrings = self.text.split(f"![{item[0]}]({item[1]})", 1)
                counter = 0
                for substring in substrings:
                    result.append(TextNode(substring, self.text_type))
                    counter += 1
                    if counter % 2 != 0:
                        result.append(TextNode(f"{item[0]}", "image", item[1]))
            return result
        else:
            return [self]

    def seperate_links(self):
        result = []
        link_group = re.findall(r"\[(.*?)\]\((.*?)\)", self.text)
        if len(link_group) != 0:
            for item in link_group:
                substrings = self.text.split(f"[{item[0]}]({item[1]})", 1)
                counter = 0
                for substring in substrings:
                    result.append(TextNode(substring, self.text_type))
                    counter += 1
                    if counter % 2 != 0:
                        result.append(TextNode(f"{item[0]}", "link", item[1]))
            return result
        else:
            return [self]

    def seperate_delimiter(self, t_type, delimiter):
        result = []
        normalword = ""
        foundword = ""
        counter = 0
        inside_delimiter = False

        while counter < len(self.text):
            if counter == len(self.text) - len(delimiter) and self.text[counter:counter + len(delimiter)] == delimiter and not inside_delimiter:
                normalword += delimiter #the last few characters are a delimiter AND it's not a closing delimiter
                counter += len(delimiter)
            elif self.text[counter:counter + len(delimiter)] == delimiter:
                counter += len(delimiter)
                inside_delimiter = not inside_delimiter
                # check if we have just skipped over a closing delimiter
                if not inside_delimiter:
                    # check if these words even have content
                    if normalword and not normalword.isspace():
                        # append all text before opening delimiter
                        result.append(TextNode(normalword, self.text_type))
                        normalword = ""
                    if foundword and not foundword.isspace():
                        # append all text inside delimiters
                        result.append(TextNode(foundword, t_type))
                        foundword = ""
            else:
                if inside_delimiter:
                    # we crossed an opening delimiter before
                    foundword += self.text[counter]
                else:
                    # we are outside a pair of delimiters
                    normalword += self.text[counter]
                counter += 1

        if foundword and not foundword.isspace():
            if normalword and not normalword.isspace():
                result.append(TextNode(f"{normalword}{delimiter}{foundword}", self.text_type))
            else:
                result.append(TextNode(f"{delimiter}{foundword}", self.text_type))
        elif normalword and not normalword.isspace():
            result.append(TextNode(normalword, self.text_type))

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