"""LEXOR to HTML INLINE NodeConverter

Convert the `strong_em` and `em_strong` tags to proper html nodes.

"""

from lexor.core.converter import NodeConverter
from lexor.core.elements import Element


class StrongEmNC(NodeConverter):
    """Append a strong_em or em_strong to a list. """

    def __init__(self, converter):
        NodeConverter.__init__(self, converter)
        converter.strong_em = list()

    def process(self, node):
        self.converter.strong_em.append(node)

    @staticmethod
    def convert(converter):
        """Modifies the nodes caught by this node converter. """
        for node in converter.strong_em:
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
