"""LEXOR to HTML ENTITY NodeConverter

Replace quotes symbols.

"""

from lexor.core.converter import NodeConverter


class EntityNC(NodeConverter):
    """Replace special symbols. """
    val = {
        "'": '&rsquo;',
    }

    def start(self, node):
        if node.data in self.val:
            node.data = self.val[node.data]
        return node
