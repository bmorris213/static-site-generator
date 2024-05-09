# static site generator
# 5/6/2024
# Brian Morris

# document converter
# takes an input document, and converts it to a different format
# uses file i/o to read and write documents
# SUPPORTED CONVERSIONS:
#   markdown to html

import re
from parentnode import ParentNode
from leafnode import LeafNode

class DocumentConverter:
    # supported types of documents
    class SupportedTypes(Enum):
        TXT = auto()
        MARKDOWN = auto()
        HTML = auto()

    # this document converter stores a parentnode Root
    # which is None until a document is read
    def __init__(self):
        self.root_node = None
    
    # read document
    # converts a given document into an internal textnode tree
    # takes input text value, the type of document
    # builds and stores a tree of textnodes
    def read_document(document, document_type):
        if document_type == DocumentConverter.SupportedTypes.TXT:
            # conversion of .txt files is WIP
            pass
        elif document_type == DocumentConverter.SupportedTypes.HTML:
            # conversion of .html files is WIP
            pass
        elif document_type == DocumentConverter.SupportedTypes.MARKDOWN:
            self.root_node = DocumentConverter.read_markdown(document)
    
    # read markdown
    # converts a document of markdown into internal textnode tree
    # takes a string containing a document's contents
    # returns a root textnode
    @staticmethod
    def read_markdown(document):
        blocks = DocumentConverter.split_markdown(document)
        node_list = []
        # process each block structure
        
        # split_line_delimiter needs delimiter:text_type dictionary
        # these are the markdown inline delimiters
        delimiters = {
            "**" : LeafNode.TextType.BOLD,
            "*" : LeafNode.TextType.ITALIC,
            "`" : LeafNode.TextType.CODE
        }

        # process each block, adding a parent containing its contents to node_list
        for block in blocks: # blocks are made of (type, list of lines)
            leaf_nodes = []
            leaf_values = []
            for line in block[1]:
                leaf_values.extend(DocumentConverter.split_line_delimiter(line, delimiters, LeafNode.TextType.NORMAL))

            for pair in leaf_values: # where pair[0] is text_type and pair[1] is value
                # we still need to test for image and links
                extracted_values = DocumentConverter.extract_markdown_references(pair[1], pair[0])
                
                # returns a list of 
                for triple in extracted_values: # extracted values are (text_type, text, url) triples
                    # we need to build a leaf node with these three : text_type, text, props
                    if triple[0] == LeafNode.TextType.LINK:
                        leaf_nodes.append(LeafNode(triple[0], triple[1], {"href":triple[2]}))
                    elif triple[0] == LeafNode.TextType.IMAGE:
                        leaf_nodes.append(LeafNode(triple[0], "", {"alt":triple[1],"href":triple[2]}))
                    else:
                        leaf_nodes.append(LeafNode(triple[0], triple[1]))
            # we now have a list of leaf nodes
            node_list.append(ParentNode(block[0],leaf_nodes))
        
        return ParentNode(ParentNode.TextType.ROOT, node_list)
    
    # split markdown
    # takes the raw text from a markdown document
    # returns blocks : list of (parent_node text_type, list[text lines])
    @staticmethod
    def split_markdown(document):
        text_lines = document.split('\n')

        # blocks are a type and a list of lines
        blocks = []
        new_block = []
        counter = 0
        star_type = False
        dash_type = False
        new_block_type = ParentNode.TextType.NORMAL

        # split document into blocks
        for line in text_lines:
            # test if we need to reset counter for ordered lists
            if counter != 0 and line[:len(str(counter)) + 1] != f"{counter}.":
                counter = 0
            
            # test for which block type new line is
            if line == ""
                continue
            elif line[0] == ">":
                if new_block_type != ParentNode.TextType.QUOTE:
                    # we are coming across a new block
                    new_block_type = ParentNode.TextType.QUOTE
                    star_type = False
                    dash_type = False
                    if len(new_block) != 0:
                        blocks.append((new_block_type, new_block))
                        new_block = []
                # check for skippable items with nothing on them
                if len(line) < 3:
                    continue
                new_block.append(line[:2]) # skip '> '
            elif new_block_type == ParentNode.TextType.CODE:
                if len(line) >= 3 and line[:3] == "```":
                    # we are looking at a closing delimiter
                    if len(new_block) != 0:
                        blocks.append((new_block_type, new_block))
                        new_block = []
                    # we can skip adding 0 len code blocks
                    new_block_type = ParentNode.TextType.NORMAL
                    star_type = False
                    dash_type = False
                    continue
                # else add code_block line
                new_block.append(line)
            elif len(line) >= 3 and line[:3] == "```":
                # we are looking at an opening delimiter
                new_block_type = ParentNode.TextType.CODE
                star_type = False
                dash_type = False
                if len(new_block) != 0:
                    blocks.append((new_block_type, new_block))
                    new_block = []
                continue
            elif line[0] == "*":star_type_text
                if new_block_type != ParentNode.TextType.UNORDERED_LIST or dash_type:
                    # we have come across a new block
                    if len(new_block) != 0:
                        blocks.append((new_block_type, new_block))
                        new_block = []
                    new_block_type = ParentNode.TextType.UNORDERED_LIST
                    star_type = True
                    dash_type = False
                new_block.append(line)
            elif line[0] == "-":
                if new_block_type != ParentNode.TextType.UNORDERED_LIST or star_type:
                    # we have come across a new block
                    if len(new_block) != 0:
                        blocks.append((new_block_type, new_block))
                        new_block = []
                    new_block_type = ParentNode.TextType.UNORDERED_LIST
                    dash_type = True
                    star_type = False
                new_block.append(line)
            elif line[0] == "#":
                star_type = False
                dash_type = False
                # heading block, can only be size 1, so we don't need
                # to test if we're introing into a new block: we are
                if len(new_block) != 0:
                    blocks.append((new_block_type, new_block))
                    new_block = []

                # determine the level of heading
                heading_level = 0
                while heading_level < 6:
                    heading_level += 1
                    if line[:heading_level] != len(line[:heading_level]) * "#":
                        break
                if heading_level == 1:
                    new_block_type = ParentNode.TextType.HEADING1
                elif heading_level == 2:
                    new_block_type = ParentNode.TextType.HEADING2
                elif heading_level == 3:
                    new_block_type = ParentNode.TextType.HEADING3
                elif heading_level == 4:
                    new_block_type = ParentNode.TextType.HEADING4
                elif heading_level == 5:
                    new_block_type = ParentNode.TextType.HEADING5
                elif heading_level == 6:
                    new_block_type = ParentNode.TextType.HEADING6
                else:
                    raise Exception("heading level fell outside of range")

                blocks.append((new_block_type, line[heading_level:]))
            elif counter != 0 or line[0:2] == "1.":
                if new_block_type != ParentNode.TextType.ORDERED_LIST:
                    # we have come across a new block
                    if len(new_block) != 0:
                        blocks.append((new_block_type, new_block))
                        new_block = []
                    new_block_type = ParentNode.TextType.ORDERED_LIST
                    star_type = False
                    dash_type = False
                counter += 1
                # ordered lists must count up from 1
                if line[:len(str(counter)) + 1] == f"{counter}.":
                    new_block.append(line[len(str(counter)):])
            else:
                if block_type != ParentNode.TextType.NORMAL:
                    if len(new_block) != 0:
                        blocks.append((new_block_type, new_block))
                        new_block = []
                    block_type = ParentNode.TextType.NORMAL
                    star_type = False
                    dash_type = False
                new_block.append(line)
            
        # look for edge cases escaping for loop
        if len(blocks) == 0:
            if len(new_block) == 0:
                raise Exception("block creation escaped with no result...")
            else:
                blocks.append((ParentNode.TextType.NORMAL, text_lines))
        if len(new_block) != 0:
            blocks.append((new_block_type, new_block))
        
        return blocks
    
    # split line delimiter
    # based on a dictionary of delimiter : text_type
    # returns a list of (text_type, substring) tuples if and only if
    #   the substring was found surrounded by that delimiter
    @staticmethod
    def split_line_delimiter(line, delimiters, normal_type):
        # delimiters[key] == value
        # values in delimiters{} store text_types
        if len(line) == 0:
            return None
        if len(line) == 1:
            return [(normal_type, line)]
        
        # initialize list to store (text_type, substring) tuples
        result = []
        current_index = 0
        current_text = ""

        for delimiter in delimiters:
            # look for instance of this delimiter
            start_index = line.find(delimiter, current_index)

            # if we found nothing, continue testing other delimiters
            if start_index == -1:
                continue
            
            # look for instance of a closing delimiter
            end_index = line.find(delimiter, current_index + len(delimiter))

            # if we found nothing, this delimiter does not count as special text
            if end_index == -1:
                # we need to add the delimiter itself to current_text
                # and continue testing delimiters
                current_text += delimiter
                current_index += len(delimiter)
                continue

            # otherwise we found a delimiter pair with something between them
            enclosed_text = line[start_index + len(delimiter):end_index + len(delimiter) - 1]
            
            # we should append any prior text
            current_text = current_text + line[current_index:start_index]
            result.append((normal_type, current_text))
            current_text = ""

            # if there is actually no text enclosed, we should continue searching
            if enclosed_text == "":
                current_index = end_index + len(delimiter)
                continue

            # now we should recursively search contents for different delimiters present
            inner_text_group = split_line_delimiter(enclosed_text, delimiters, delimiters[delimiter])
            result.extend(inner_text_group)
            current_index = end_index + len(delimiter)

            # test if we've reached the end and can stop testing delimiters
            if current_index >= len(line):
                break
            
        # once we are done testing delimiters there should still be some text left
        if current_index < len(line):
            current_text = current_text + line[current_index:]
            result.append((normal_type, current_text))
        
        # if result is still empty somehow, we can just return the line
        if len(result) == 0:
            result.append((normal_type, line))
        
        return result

    # extract markdown references
    # used to find any image or link substrings
    # returns a list of (text_type, substring1, substring2) tuples
    @staticmethod
    def extract_markdown_references(input_string, normal_type):
        if len(text) == 0:
            return None
        if len(text) <= 2:
            return ((normal_type, text, None))
        result = []
        
        text = input_string
        image_group = re.findall(r"!\[(.*?)\]\((.*?)\)", self.text)
        if len(image_group) != 0:
            for item in image_group:
                substrings = text.split(f"![{item[0]}]({item[1]})", 1)
                result.append((normal_type, substrings[0], None))
                if len(substrings) != 1:
                    result.append((LeafNode.TextType.IMAGE, item[0], item[1]))
                text = substrings[1]
        
        text = input_string
        link_group = re.findall(r"\[(.*?)\]\((.*?)\)", self.text)
        if len(link_group) != 0:
            for item in link_group:
                substrings = text.split(f"[{item[0]}]({item[1]})", 1)
                result.append((normal_type, substrings[0], None))
                result.append((LeafNode.TextType.LINK, item[0], item[1]))
                text = substrings[1]
        
        if len(result) == 0:
            return ((normal_type, text, None))
        
        return result