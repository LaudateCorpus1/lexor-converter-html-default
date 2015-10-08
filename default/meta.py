"""LEXOR to HTML META NodeConverter

Attach the meta info to the main document.

"""

import re
from lexor.core.converter import NodeConverter
from lexor.core.writer import replace
RE = re.compile(r'\$\((.*?)\)')


class MetaNC(NodeConverter):
    """Attach the entries to the document meta attribute. """

    directive = 'lexor-meta'

    @staticmethod
    def handle_data(data, node):
        """Look for sequences of the form `$(variable)` and
        do a replacement with the current variable. """
        variables = RE.findall(data)
        replace_list = list()
        meta = node.owner.meta
        for var in variables:
            if var in meta:
                replace_list.append(('$(%s)' % var, meta[var]))
            else:
                replace_list.append(('$(%s)' % var, ""))
        if replace_list:
            return replace(data, *replace_list)
        return data

    def end(self, node):
        for entry in node.child:
            node.owner.meta[entry['name']] = self.handle_data(
                entry[0].data, node  # TODO: add all the data
            )
        return self.converter.remove_node(node)
