"""LEXOR to HTML ENTITY NodeConverter

Replace quotes symbols.

"""

from lexor.core.converter import NodeConverter
from lexor.core.elements import Entity


class QuoteNC(NodeConverter):
    """Wrap child nodes with the proper entity nodes. """

    def end(self, node):
        if node['char'] == "'":
            lnode = Entity('&lsquo;')
            newnode = Entity('&rsquo;')
        else:
            lnode = Entity('&ldquo;')
            newnode = Entity('&rdquo;')
        node.parent.insert_before(node.index, lnode)
        node.parent.insert_before(node.index, newnode)
        newnode.parent.extend_before(newnode.index, node)
        del node.parent[node.index]
        return newnode
