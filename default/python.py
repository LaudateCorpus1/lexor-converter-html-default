"""LEXOR to HTML PYTHON NodeConverter

Collect and execute python embeddings.

"""

from lexor.core.converter import NodeConverter
from lexor.core.parser import Parser


class PythonNC(NodeConverter):
    """Append a node with python instructions to a list. """

    def __init__(self, converter):
        NodeConverter.__init__(self, converter)
        converter.python = list()

    def process(self, node):
        self.converter.python.append(node)

    @staticmethod
    def convert(converter):
        """Execute the python embeddings. """
        parser = Parser('html', 'default')
        err = True
        if converter.defaults['error'] in ['off', 'false']:
            err = False
        if converter.defaults['exec'] in ['on', 'true']:
            for num, node in enumerate(converter.python):
                converter.exec_python(node, num, parser, err)
