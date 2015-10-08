"""LEXOR to HTML INCLUDE NodeConverter

"""

import os
import os.path as pth
from lexor.core.parser import Parser
from lexor.core.converter import Converter
from lexor.core.converter import NodeConverter


class IncludeNC(NodeConverter):
    """Remove the include nodes. """

    directive = 'include'

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

    def update_log(self, plog, clog):
        """Helper function for the start method. """
        if plog:
            self.converter.update_log(plog)
        if clog:
            self.converter.update_log(clog)

    @staticmethod
    def get_text(info, node):
        """Obtain the text. """
        try:
            text = open(info['src'], 'r').read()
            return text
        except IOError:
            if 'search' not in node:
                return None
        try:
            lexorinputs = os.environ['LEXORINPUTS']
        except KeyError:
            return None
        for directory in lexorinputs.split(':'):
            path = '%s/%s' % (directory, node['src'])
            try:
                return open(path, 'r').read()
            except IOError:
                pass
        return None

    def start(self, node):
        if 'src' not in node:
            return Converter.remove_node(node)
        info = self.get_info(node)
        text = self.get_text(info, node)
        if text is None:
            self.msg('E001', node, [info['src']])
            return Converter.remove_node(node)
        parser = Parser(info['parser_lang'],
                        info['parser_style'],
                        info['parser_defaults'])
        try:
            parser.parse(text, info['src'])
        except ImportError:
            self.msg(
                'E002', node, [
                    info['parser_lang'],
                    info['parser_style'],
                ]
            )
            return Converter.remove_node(node)
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
            try:
                converter.convert(parser.doc)
            except ImportError:
                self.msg(
                    'E003', node, [
                        info['convert_from'],
                        info['convert_to'],
                        info['convert_style'],
                    ]
                )
                return Converter.remove_node(node)
            cdoc = converter.doc.pop()
            clog = converter.log.pop()
        else:
            cdoc = parser.doc
            clog = None
        self.update_log(parser.log, clog)
        if info['adopt']:
            cdoc.temporary = True
            node.parent.extend_before(node.index, cdoc)
        else:
            cdoc.temporary = False
            node.parent.insert_before(node.index, cdoc)
        return Converter.remove_node(node)


MSG = {
    'E001': 'file `{0}` not found',
    'E002': 'parsing style not found {0}:{1}',
    'E003': 'converting style not found [{0} ==> {1}:{2}]',
}
MSG_EXPLANATION = [
    """
    - Python was not able to open the file specified.

    Reports error E001.

""", """
    - Python was not able to find the specified converting style.

    Reports error E002.

""",
]
