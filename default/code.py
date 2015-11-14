"""LEXOR to HTML CODE NodeConverter

"""
from lexor.core.converter import NodeConverter
from lexor.core import replace


class CodeBlockNC(NodeConverter):
    """Change to pre. There will be more options, for now
    we just need a quick way of writing code blocks. """

    directive = 'codeblock'

    def post_link(self, node, dir_info, trans_ele, required):
        node.name = 'pre'
        node[0].data = replace(
            node[0].data,
            ('<', '&lt;'),
            ('&', '&amp;'),
            ('>', '&gt;')
        )
        return node


class InlineCodeNC(NodeConverter):

    directive = 'code'

    def post_link(self, node, dir_info, trans_ele, required):
        node[0].data = replace(
            node[0].data,
            ('<', '&lt;'),
            ('&', '&amp;'),
            ('>', '&gt;')
        )
        return node
