from django.test import TestCase
from django.template import Template,Context
from django.template.loader import get_template, get_template_from_string

base1 = """{% ifblock extras %}<p>base1a</p>{{ blockoutput }}<p>base1b</p>{% endifblock %}"""
base2 = """{% extends baseX %}{% ifblock extras %}<p>base2a</p>{{ blockoutput }}<p>base2b</p>{% endifblock %}"""
base3 = """{% extends baseY %}{% ifblock extras %}<p>base3a</p>{{ blockoutput }}<p>base3b</p>{% endifblock %}"""

exp1 = """{% extends baseA %}{% block extras %}<p>expected1</p>{% endblock %}"""
exp2 = """{% extends baseB %}{% block extras %}<p>expected2</p>{% endblock %}"""

alt1 = """{% extends baseC %}{% block extras %}{{ block.super }}<p>alternate1</p>{% endblock %}"""
alt2 = """{% extends baseD %}{% block extras %}{{ block.super }}<p>alternate2</p>{% endblock %}"""

class AppTestCase(TestCase):
    """
    Populate this class with unit tests for your application
    """
    
    urls = 'conditionalblock.testsuites.urls'
    
    def test_ifblock_does_nothing_if_no_child_block_exists(self):
        expected = ""
        
        t1 = get_template_from_string(base1)
        
        result = t1.render(Context({}))
        
        self.assertEqual(result, expected, result)
    
    def test_ifblock_renders_child_with_wrapper_when_child_block_exists(self):
        expected = """<p>base1a</p><p>expected1</p><p>base1b</p>"""
        
        t1 = get_template_from_string(base1)
        t2 = get_template_from_string(exp1)
        
        result = t2.render(Context({'baseA': t1}))
        
        self.assertEqual(result, expected, result)
    
    def test_ifblock_renders_child_with_wrapper_when_child_block_exists_and_ignores_super(self):
        expected = """<p>base1a</p><p>alternate1</p><p>base1b</p>"""
        
        t1 = get_template_from_string(base1)
        t2 = get_template_from_string(alt1)
        
        result = t2.render(Context({'baseC': t1}))
        
        self.assertEqual(result, expected, result)
    
    def test_ifblock_renders_last_child_with_wrapper(self):
        expected = """<p>base1a</p><p>expected2</p><p>base1b</p>"""
        
        t1 = get_template_from_string(base1)
        t2 = get_template_from_string(exp1)
        t3 = get_template_from_string(exp2)
        
        result = t3.render(Context({'baseB': t2, 'baseA': t1}))
        
        self.assertEqual(result, expected, result)
    
    def test_ifblock_renders_both_children_with_wrapper_when_super_used(self):
        expected = """<p>base1a</p><p>expected1</p><p>alternate1</p><p>base1b</p>"""
        
        t1 = get_template_from_string(base1)
        t2 = get_template_from_string(exp1)
        t3 = get_template_from_string(alt1)
        
        result = t3.render(Context({'baseC': t2, 'baseA': t1}))
        
        self.assertEqual(result, expected, result)
    
    def test_ifblock_renders_child_with_double_wrapper(self):
        expected = """<p>base1a</p><p>base2a</p><p>expected1</p><p>base2b</p><p>base1b</p>"""
        
        t1 = get_template_from_string(base1)
        t2 = get_template_from_string(base2)
        t3 = get_template_from_string(exp1)
        
        result = t3.render(Context({'baseA': t2, 'baseX': t1}))
        
        self.assertEqual(result, expected, result)
    











