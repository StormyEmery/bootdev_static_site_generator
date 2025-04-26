from textnode import TextNode

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