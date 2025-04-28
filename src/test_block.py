import unittest
from block import block_to_blocktype, BlockType

class TestBlock(unittest.TestCase):
    def test_block_to_blocktype(self):
        self.assertEqual(block_to_blocktype("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_blocktype("> Quote"), BlockType.QUOTE)
        self.assertEqual(block_to_blocktype("``` Code ```"), BlockType.CODE)
        self.assertEqual(block_to_blocktype("1. Ordered List"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_blocktype("- Unordered List"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_blocktype("Paragraph"), BlockType.PARAGRAPH)

    def test_block_to_blocktype_invalid(self):
        # Test with an invalid block type
        self.assertEqual(block_to_blocktype("Invalid Block"), BlockType.PARAGRAPH)
    
    def test_block_to_blocktype_empty(self):
        # Test with an empty string
        self.assertEqual(block_to_blocktype(""), BlockType.PARAGRAPH)
    
    def test_block_to_blocktype_heading(self):
        # Test with a heading
        self.assertEqual(block_to_blocktype("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_blocktype("## Subheading"), BlockType.HEADING)
        self.assertEqual(block_to_blocktype("### Sub-subheading"), BlockType.HEADING)
        self.assertEqual(block_to_blocktype("#### Sub-sub-subheading"), BlockType.HEADING)
        self.assertEqual(block_to_blocktype("##### Sub-sub-sub-subheading"), BlockType.HEADING)
        self.assertEqual(block_to_blocktype("###### Sub-sub-sub-sub-subheading"), BlockType.HEADING)
    
    def test_block_to_blocktype_quote(self):
        # Test with a quote
        self.assertEqual(block_to_blocktype("> Quote"), BlockType.QUOTE)
        self.assertEqual(block_to_blocktype("> Another Quote"), BlockType.QUOTE)
        self.assertEqual(block_to_blocktype("> Yet Another Quote"), BlockType.QUOTE)
        self.assertEqual(block_to_blocktype("> Quote with multiple lines\n> Another line"), BlockType.QUOTE)
        self.assertEqual(block_to_blocktype("> Quote with multiple lines\n> Another line\n> Yet another line"), BlockType.QUOTE)
    
    def test_block_to_blocktype_ordered_list(self):
        # Test with an ordered list
        self.assertEqual(block_to_blocktype("1. Ordered List"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_blocktype("1. First Item\n2. Second Item\n3. Third Item"), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_blocktype("2. Another Ordered List"), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_blocktype("1. First Item\n3. Second Item\n2. Third Item"), BlockType.ORDERED_LIST)
    
    def test_block_to_blocktype_unordered_list(self):
        # Test with an unordered list
        self.assertEqual(block_to_blocktype("- Unordered List"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_blocktype("- First Item\n- Second Item\n- Third Item"), BlockType.UNORDERED_LIST)
        self.assertNotEqual(block_to_blocktype("Another Unordered List"), BlockType.UNORDERED_LIST)
        self.assertNotEqual(block_to_blocktype("- First Item\n- Third Item\nSecond Item"), BlockType.UNORDERED_LIST)
