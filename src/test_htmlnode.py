import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode("div", "This is a div", [], {"class": "container"})
        self.assertRaises(NotImplementedError, node.to_html)
    
    def test_props_to_html(self):
        node = HTMLNode("div", "This is a div", [], {"href": "https://www.google.com", "target": "_blank"})
        expected_props = 'href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_props)
    
    def test_repr(self):
        node = HTMLNode("div", "This is a div", [], {"class": "container"})
        expected_repr = "HTMLNode(tag=div, value=This is a div, children=[], props={'class': 'container'})"
        self.assertEqual(repr(node), expected_repr)

    def test_repr_no_props(self):
        node = HTMLNode("div", "This is a div")
        expected_repr = "HTMLNode(tag=div, value=This is a div, children=[], props={})"
        self.assertEqual(repr(node), expected_repr)
    
    def test_repr_no_children(self):
        node = HTMLNode("div", "This is a div", props={"class": "container"})
        expected_repr = "HTMLNode(tag=div, value=This is a div, children=[], props={'class': 'container'})"
        self.assertEqual(repr(node), expected_repr)
    
if __name__ == "__main__":
    unittest.main()