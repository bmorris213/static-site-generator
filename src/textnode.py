from leafnode import LeafNode
from parentnode import ParentNode

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
    def process_doc(doc):
        blocks = TextNode.split_doc(doc)
        node_group = []

        for block in blocks:
            node_group.append(TextNode.block_to_html(block[0], block[1]))
        
        result = ParentNode("div", node_group)

        return result

    @staticmethod
    def split_doc(doc):
        text_lines = doc.split("\n")

        block_type = "paragraph"
        blocks = []
        new_block = []
        counter = 0

        for line in text_lines:
            # test for exiting ordered list
            if counter != 0 and line[0:len(str(counter))] != f"{counter}.":
                counter = 0

            # test to see if the new type of block is not the old type

            if line == "":
                continue
            elif block_type == "code_block":
                if line == "```":
                    if len(new_block) != 0:
                        blocks.append((new_block, "code_block"))
                        new_block = []
                    block_type = "paragraph"
                    continue
                new_block.append(line)
            elif line == "```":
                if len(new_block) != 0:
                    blocks.append((new_block, block_type))
                    new_block = []
                block_type = "code_block"
                continue
            elif line[0] == "*" or line[0] == "-":
                if block_type != "unordered_list":
                    if len(new_block) != 0:
                        blocks.append((new_block,block_type))
                        new_block = []
                    block_type = "unordered_list"
                new_block.append(line)
            elif line[0] == "#":
                if len(new_block) != 0:
                    blocks.append((new_block,block_type))
                    new_block = []
                block_type = "heading"

                new_block.append(line)
                #always add new_block for a heading
                blocks.append((new_block,block_type))
                new_block = []
            elif line[0] == ">":
                if block_type != "quote":
                    if len(new_block) != 0:
                        blocks.append((new_block,block_type))
                        new_block = []
                    block_type = "quote"
                new_block.append(line)
            elif line[0:1] == "1." or counter != 0:
                if block_type != "ordered_list":
                    if len(new_block) != 0:
                        blocks.append((new_block,block_type))
                        new_block = []
                    block_type = "ordered_list"
                counter += 1
                if line[0:len(str(counter))] == f"{counter}.":
                    new_block.append(line)
            else:
                if block_type != "paragraph":
                    if len(new_block) != 0:
                        blocks.append((new_block,block_type))
                        new_block = []
                    block_type = "paragraph"
                new_block.append(line)
        
        if len(blocks) == 0:
            if len(new_block) == 0:
                raise Exception("block to split results in length 0")
            else:
                blocks.append((new_block,"paragraph"))
        
        return blocks     

    @staticmethod
    def block_to_html(block, block_type):
        temp = []
        heading_level = 0

        for line in block:
            node_group = []
            if block_type == "quote" or block_type == "unordered_list":
                # this line has a # followed by a space
                node_group = TextNode(line[2:], "text").seperate_inline()
            elif block_type == "heading":
                # this line has a number of "#" up to 6
                heading_level = 0
                while heading_level != 6 and line[heading_level] == '#':
                    heading_level += 1
                node_group = TextNode(line[heading_level + 1:], "text").seperate_inline()
            elif block_type == "code_block" or block_type == "paragraph":
                node_group = TextNode(line, "text").seperate_inline()
            elif block_type == "ordered_list":
                number_substring = ""
                for character in line:
                    if character.isnumeric():
                        number_substring.append(character)
                    else:
                        break
                node_group = TextNode(line[number_substring.int():], "text").seperate_inline()
            else:
                raise Exception("invalid block type")
            node_group[0].text = f"{node_group[0].text}"
            temp.extend(node_group)
        
        # add tag and return block
        tag = ""
        if block_type == "quote":
            tag = "blockquote"
        elif block_type == "code_block":
            tag = "code"
        elif block_type == "paragraph":
            tag = "p"
        elif block_type == "unordered_list":
            tag = "ul"
        elif block_type == "ordered_list":
            tag = "ol"
        elif block_type == "heading":
            tag = f"h{heading_level}"

        children = []
        for child in temp:
            if type(child) == TextNode:
                children.append(child.to_html())
            else:
                children.append(child)

        return ParentNode(tag, children)

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