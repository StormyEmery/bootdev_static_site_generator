from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    QUOTE = "quote"
    CODE = "code"
    ORDERED_LIST = "ordered_list"
    UNORDERED_LIST = "unordered_list"

def block_to_blocktype(text):
    # Check for empty string
    if not text:
        return BlockType.PARAGRAPH
    
    if re.match(r"^#{1,6} ", text):
        return BlockType.HEADING
    
    if all(line.strip().startswith(">") for line in text.splitlines()):
        return BlockType.QUOTE
    
    if text.startswith("```") and text.endswith("```"):
        return BlockType.CODE
    
    lines = text.splitlines()
    if all(re.match(r"^\d+\. ", line.strip()) for line in lines):
        numbers = [int(line.strip().split(".")[0]) for line in lines]
        if numbers == list(range(1, len(numbers) + 1)):
            return BlockType.ORDERED_LIST
    
    if all(line.strip().startswith("- ") for line in text.splitlines()):
        return BlockType.UNORDERED_LIST

    return BlockType.PARAGRAPH