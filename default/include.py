"""LEXOR to HTML INCLUDE NodeConverter

"""

import os
import os.path as pth
from lexor.core.parser import Parser
from lexor.core.converter import Converter, remove_node
from lexor.core.converter import NodeConverter


class IncludeNC(NodeConverter):
    """Remove the include nodes. """

    @staticmethod
    def get_info(node):
        """Format the node information. """
        info = {
            'parser_style': '_',
            'parser_lang': None,
            'parser_defaults': None,
            'convert_style': '_',
            'convert_from': None,
            'convert_to': 'html',
            'convert_defaults': None,
            'adopt': True,
            'convert': 'true'
        }
        for att in node:
            info[att] = node[att]
        if info['src'][0] != '/':
            base = os.path.dirname(node.owner.uri_)
            if base != '':
                base += '/'
            info['src'] = '%s%s' % (base, info['src'])
        if info['parser_lang'] is None:
            path = pth.realpath(info['src'])
            name = pth.basename(path)
            name = pth.splitext(name)
            info['parser_lang'] = name[1][1:]
        return info

    def start(self, node):
        if 'src' not in node:
            return
        info = self.get_info(node)
        text = open(info['src'], 'r').read()
        parser = Parser(info['parser_lang'],
                        info['parser_style'],
                        info['parser_defaults'])
        parser.parse(text, info['src'])
        if info['convert'] == 'true' and info['convert_to'] is not None:
            if info['convert_from'] is None:
                info['convert_from'] = info['parser_lang']
            if self.converter.match_info(info['convert_from'],
                                         info['convert_to'],
                                         info['convert_style'],
                                         info['convert_defaults']):
                converter = self.converter
            else:
                converter = Converter(info['convert_from'],
                                      info['convert_to'],
                                      info['convert_style'],
                                      info['convert_defaults'])
            converter.convert(parser.doc)
            cdoc = converter.doc.pop()
            clog = converter.log.pop()
        else:
            cdoc = parser.doc
            clog = None
        if parser.log:
            self.converter.update_log(parser.log)
        if clog:
            self.converter.update_log(clog)

        if info['adopt']:
            node.parent.extend_before(node.index, cdoc)
        else:
            node.parent.insert_before(node.index, cdoc)

        return remove_node(node)
