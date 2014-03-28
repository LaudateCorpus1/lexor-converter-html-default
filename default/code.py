"""LEXOR to HTML CODE NodeConverter

"""

from lexor.core import NodeConverter, replace


class CodeBlockNC(NodeConverter):
    """Change to pre. There will be more options, for now
    we just need a quick way of writing code blocks. """

    def end(self, node):
        node.name = 'pre'
        node[0].data = replace(
            node[0].data,
            ('<', '&lt;'),
            ('&', '&amp;'),
            ('>', '&gt;')
        )
        return node
