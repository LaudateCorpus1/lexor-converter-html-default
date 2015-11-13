"""LEXOR to HTML LIST NodeConverter

Creates a list with the information provided.

"""

from lexor.core.converter import NodeConverter
from lexor.core.elements import Element


class ListNC(NodeConverter):
    """Build a list. """

    directive = 'list'
    remove = 'post_link'

    @staticmethod
    def start_list(ltype):
        """Create a new list element. """
        node = Element(ltype)
        node.append_child(Element('li'))
        return node

    @staticmethod
    def make_list(main):
        """Return a list. """
        item = main[0]
        if item.name == '#text':
            if main.prev is not None and main.prev.name == '#text':
                main.prev.data += item.data
                del main[0]
                item = main[0]
            else:
                item = item.next
                main.parent.insert_before(main.index, item.prev)
        level = 1
        list_node = ListNC.start_list(item['type'])
        crt = list_node
        while item['level'] > level:
            crt[-1].append_child(ListNC.start_list(item['type']))
            crt = crt[-1][-1]
            level += 1
        crt[-1].extend_children(item)
        for key in item.attributes:
            if key.startswith('__'):
                crt[key[2:]] = item[key]
            elif key.startswith('_'):
                crt[-1][key[1:]] = item[key]
        item = item.next
        while item is not None:
            if 'flag' in item and item['flag'] == 'close':
                while level >= item['level']:
                    crt = crt.parent.parent
                    level -= 1
            else:
                if item['level'] == level:
                    crt.append_child(Element('li'))
                elif item['level'] > level:
                    if len(crt) == 0:
                        crt.append_child(Element('li'))
                    while item['level'] > level:
                        crt[-1].append_child(ListNC.start_list(item['type']))
                        crt = crt[-1][-1]
                        level += 1
                else:
                    while item['level'] < level:
                        crt = crt.parent.parent
                        level -= 1
                    crt.append_child(Element('li'))
            crt[-1].extend_children(item)
            for key in item.attributes:
                if key.startswith('__'):
                    crt[key[2:]] = item[key]
                elif key.startswith('_'):
                    crt[-1][key[1:]] = item[key]
            item = item.next
        del main[:]
        return list_node

    def post_link(self, node, dir_info, trans_ele, required):
        """Modifies the nodes caught by this node converter. """
        list_node = ListNC.make_list(node)
        node.parent.insert_before(node.index, list_node)
