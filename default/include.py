"""LEXOR to HTML INCLUDE NodeConverter

"""

import os
import lexor
from lexor.core.converter import NodeConverter


class IncludeNC(NodeConverter):
    """Remove the include nodes. """

    def start(self, node):
        if 'src' not in node:
            return
        src = node['src']
        if src[0] != '/':
            base = os.path.dirname(node.owner.uri_)
            if base != '':
                base += '/'
            src = '%s%s' % (base, src)
        pdoc, plog = lexor.read(src)
        self.converter.convert(pdoc)
        cdoc = self.converter.doc.pop()
        clog = self.converter.log.pop()
        node.parent.extend_before(node.index, cdoc)
        parent = node.parent
        index = node.index
        del node.parent[node.index]
        try:
            if index - 1 > -1:
                return parent[index-1]
            else:
                raise IndexError
        except IndexError:
            parent.append_child('')
        return parent[0]
