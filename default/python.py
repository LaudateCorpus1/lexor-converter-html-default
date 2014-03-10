"""LEXOR to HTML PYTHON NodeConverter

Execute python embeddings.

"""

from lexor.core.converter import NodeConverter
from lexor.core.parser import Parser


class PythonNC(NodeConverter):
    """Execute python embeddings. """

    def __init__(self, converter):
        NodeConverter.__init__(self, converter)
        self.parser = Parser('html', 'default')
        self.err = True
        if converter.defaults['error'] in ['off', 'false']:
            self.err = False
        self.num = 0

    def start(self, node):
        self.num += 1
        ctr = self.converter
        if ctr.defaults['exec'] not in ['on', 'true']:
            return node
        return ctr.exec_python(node, self.num, self.parser, self.err)
