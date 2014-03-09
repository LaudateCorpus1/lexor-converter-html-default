"""LEXOR to HTML LATEX NodeConverter

"""

from lexor.core.converter import NodeConverter, get_converter_namespace
from lexor.core.elements import RawText


class LatexNC(NodeConverter):
    """Adjust the node for mathjax. """

    def start(self, node):
        node.data = self.converter['MacroNC'].eval_text(node.data)
        if node['type'] == 'display':
            node.name = 'script'
            node['type'] = "math/tex; mode=display"
            del node['char']
        else:
            node.name = 'script'
            node['type'] = "math/tex"
            del node['char']
        return node


class LatexEnvironNC(NodeConverter):
    """Adjust the enviroments. """

    def __init__(self, converter):
        NodeConverter.__init__(self, converter)
        namespace = get_converter_namespace()
        if 'latex_labels' not in namespace:
            namespace['latex_labels'] = list()
        self.handle = {
            'equation': self.handle_equation
        }

    def end(self, node):
        return self.handle[node.name](node)

    def handle_equation(self, node):
        """Transform an equation. """
        latex_labels = get_converter_namespace()['latex_labels']
        name = node.name
        cdata = self.converter['MacroNC'].eval_text(node[0].data)
        if 'id' in node:
            if node['id'] in latex_labels:
                self.msg('E001', node, [node['id']])
            else:
                latex_labels.append(node['id'])
            data = '\\begin{%s}\\label{%s}%s\\end{%s}'
            data = data % (name, node['id'], cdata, name)
        else:
            data = '\\begin{%s*}%s\\end{%s*}'
            data = data % (name, cdata, name)
        newnode = RawText('script', data)
        newnode['type'] = "math/tex; mode=display"
        node.parent.insert_before(node.index, newnode)
        del node.parent[node.index]
        return newnode


MSG = {
    'E001': 'LaTeX label `{0}` already defined',
}
MSG_EXPLANATION = [
    """
    - Address references can only be defined once. 'E001' tells you
      the location of where it was first defined and the location
      where you are trying to redefine it.

    Okay:
        [1]: http://google.com
        [2]: http://daringfireball.net/projects/markdown/

    E001:
        [1]: http://google.com
        [1]: http://daringfireball.net/projects/markdown/

""",
]
