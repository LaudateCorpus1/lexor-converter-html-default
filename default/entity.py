"""LEXOR to HTML ENTITY NodeConverter

Replace quotes symbols.

"""

from lexor.core.converter import NodeConverter


class EntityNC(NodeConverter):
    """Replace special symbols. """

    directive = '#entity'

    val = {
        "'": '&rsquo;',
        "<": '&lt;'
    }

    def start(self, node):
        if node.data[0] == '\\':
            node.data = node.data[1:]
        if node.data in self.val:
            node.data = self.val[node.data]
        return node
