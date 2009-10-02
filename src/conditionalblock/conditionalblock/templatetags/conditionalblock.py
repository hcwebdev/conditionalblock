"""
@author: Jacob Radford (jradford)
"""

from django.template import Library, Context, NodeList
from django.template.loader_tags import BlockNode
from django.conf import settings
from django.utils.safestring import mark_safe

register = Library()



class IfBlockNode(BlockNode):
    def __init__(self, name, nodelist, parent=None, check_node=None):
        self.name, self.nodelist, self.parent = name, nodelist, parent
        self.original_nodelist = NodeList()
        self.final_nodelist = NodeList()
        self.original_nodelist.extend( self.nodelist )
        self.final_nodelist.extend( self.nodelist )
        self.check_node = check_node
        
        self.index = None
        for i, node in enumerate( nodelist ):
            if isinstance(node, self.check_node.__class__):
                if node.filter_expression.token == self.check_node.filter_expression.token:
                    self.index = i
                    break
        
    
    def __repr__(self):
        return "<MyBlock Node: %s. Contents: %r>" % (self.name, self.nodelist)
    
    def render(self, context):
        result = ''
        
        if self.parent:
            p = self
            pre = []
            post = []
            while p.parent:
                p = p.parent
                if p.nodelist == self.original_nodelist:
                    p.nodelist = NodeList()
                else:
                    index = None
                    found = False
                    for i, node in enumerate( p.nodelist ):
                        if isinstance(node, self.check_node.__class__):
                            if node.filter_expression.token == self.check_node.filter_expression.token:
                                index = i
                                found = True
                    if found:
                        pre[0:0] = p.nodelist[:index]
                        post.extend(p.nodelist[index+1:])

                        p.nodelist = NodeList()
            if pre:
                self.final_nodelist[self.index:self.index] = pre
                self.index += len(pre)
            if post:
                self.final_nodelist[self.index+1:self.index+1] = post
            
            context.push()
            # Save context in case of block.super().
            self.context = context
            context['block'] = self
            pre_result = self.nodelist.render(context)
            
            context['blockoutput'] = pre_result
            result = self.final_nodelist.render(context)
            context.pop()
        
        return result
    
    def super(self):
        if self.parent:
            return mark_safe(self.parent.render(self.context))
        return ''
    
    def add_parent(self, nodelist):
        if self.parent:
            self.parent.add_parent(nodelist)
        else:
            self.parent = BlockNode(self.name, nodelist)
    

@register.tag(name="ifblock")
def do_ifblock(parser, token):
    bits = token.contents.split()
    if len(bits) != 2:
        raise TemplateSyntaxError, "'%s' tag takes only one argument" % bits[0]
    block_name = bits[1]
    # Keep track of the names of BlockNodes found in this template, so we can
    # check for duplication.
    try:
        if block_name in parser.__loaded_blocks:
            raise TemplateSyntaxError, "'%s' tag with name '%s' appears more than once" % (bits[0], block_name)
        parser.__loaded_blocks.append(block_name)
    except AttributeError: # parser.__loaded_blocks isn't a list yet
        parser.__loaded_blocks = [block_name]
    
    nodelist = parser.parse(('endifblock', 'endifblock %s' % block_name))
    parser.delete_first_token()
    
    check_node = parser.create_variable_node(parser.compile_filter('blockoutput'))
    return IfBlockNode(block_name, nodelist, check_node=check_node)



