import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_parent_node_to_html(self):
        child1 = LeafNode("p", "Hello, world!")
        child2 = LeafNode("a", "Click here", {"href": "https://www.example.com"})
        parent = ParentNode("div", [child1, child2], {"class": "container"})
        
        expected_html = (
            '<div class="container">'
            '<p>Hello, world!</p>'
            '<a href="https://www.example.com">Click here</a>'
            '</div>'
        )
        self.assertEqual(parent.to_html(), expected_html)
    
    def test_parent_node_no_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, []).to_html()
    
    def test_parent_node_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )