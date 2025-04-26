import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.NORMAL)
        self.assertNotEqual(node, node2)
    
    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        expected_repr = "TextNode(This is a text node, bold, https://www.boot.dev)"
        self.assertEqual(repr(node), expected_repr)

    def test_repr_no_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        expected_repr = "TextNode(This is a text node, bold, None)"
        self.assertEqual(repr(node), expected_repr)


if __name__ == "__main__":
    unittest.main()