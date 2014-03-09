"""LEXOR to HTML INLINE NodeConverter

Convert the `strong_em` and `em_strong` tags to proper html nodes.

"""

from lexor.core.converter import NodeConverter
from lexor.core.elements import Element


class StrongEmNC(NodeConverter):
    """Modify the `strong_em` and `em_strong` to proper html nodes."""

    def end(self, node):
        if node.name == 'strong_em':
            node.name = 'strong'
            tmp = Element('em')
            tmp.extend_children(node)
            node.append_child(tmp)
        else:
            node.name = 'em'
            tmp = Element('strong')
            tmp.extend_children(node)
            node.append_child(tmp)
        return node
