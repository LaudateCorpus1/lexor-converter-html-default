"""LEXOR to HTML CODE NodeConverter

"""
from lexor import style_reference
from lexor.core import replace
MOD = style_reference(lang='lexor', to_lang='html')


class CodeBlockNC(MOD.BaseConverter):
    """Change to pre. There will be more options, for now
    we just need a quick way of writing code blocks. """

    directive = 'codeblock'

    def end(self, node):
        node.name = 'pre'
        node[0].data = replace(
            node[0].data,
            ('<', '&lt;'),
            ('&', '&amp;'),
            ('>', '&gt;')
        )
        return node


class InlineCodeNC(MOD.BaseConverter):

    directive = 'code'

    def post_link(self, node, dir_info, trans_ele, required):
        node[0].data = replace(
            node[0].data,
            ('<', '&lt;'),
            ('&', '&amp;'),
            ('>', '&gt;')
        )
        return node
