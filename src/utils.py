from textnode import TextNode, TextType
import re
import itertools

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