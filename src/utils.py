from textnode import TextNode, TextType
from block import block_to_blocktype, BlockType
from parentnode import ParentNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    
    for node in old_nodes:
        text = node.text
        while delimiter in text:
            # Find the start of the delimited text
            before, _, remainder = text.partition(delimiter)
            if before:
                result.append(TextNode(before, node.text_type))
            
            # Find the end of the delimited text
            inside, delim, after = remainder.partition(delimiter)
            if not delim:
                raise ValueError(f"Unmatched delimiter in text: {text}")

            result.append(TextNode(inside, text_type))
            
            # Update the text to process the remaining part
            text = after
        
        # Add any remaining text after the last delimiter
        if text:
            result.append(TextNode(text, node.text_type))
    
    return result

def extract_markdown_images(text):
    matches = re.findall(r'!\[(.*?)\]\((.*?)\)', text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r'\[(.*?)\]\((.*?)\)', text)
    return matches

def split_nodes_image(old_nodes):
    result = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        text = node.text
        images = extract_markdown_images(text)

        if not images:
            result.append(node)
            continue

        # Split the text into parts based on images
        parts = re.split(r'!\[(.*?)\]\((.*?)\)', text)
        for i, part in enumerate(parts):
            part = part
            if not part:
                continue
            if i % 3 == 0:
                # It's a regular text part
                result.append(TextNode(part, node.text_type))
            elif i % 3 == 1:
                # It's an image part
                url = parts[i + 1]
                result.append(TextNode(part, TextType.IMAGE, url=url))
    
    return result


def split_nodes_links(old_nodes):
    result = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        text = node.text
        images = extract_markdown_links(text)

        if not images:
            result.append(node)
            continue

        # Split the text into parts based on images
        parts = re.split(r'\[(.*?)\]\((.*?)\)', text)
        for i, part in enumerate(parts):
            part = part
            if not part:
                continue
            if i % 3 == 0:
                # It's a regular text part
                result.append(TextNode(part, node.text_type))
            elif i % 3 == 1:
                # It's an image part
                url = parts[i + 1]
                result.append(TextNode(part, TextType.LINK, url=url))
    
    return result

def text_to_textnodes(text):
    nodes = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_links(nodes)
    return nodes

def markdown_to_blocks(markdown):
    lines = markdown.split("\n\n")
    blocks = []
    for line in lines:
        blocks.append(re.sub(r'\n\s+', '\n', (line.strip())))

    return blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        if html_node:
            children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_blocktype(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node.to_html_node()
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    if not paragraph:
        return None
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = raw_text_node.to_html_node()
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def extract_title(markdown):
    lines = markdown.split("\n")
    title = ""
    for line in lines:
        if line.strip().startswith("# "):
            title = line[2:]
            break
    return title