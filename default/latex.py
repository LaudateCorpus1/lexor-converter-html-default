"""LEXOR to HTML LATEX NodeConverter

"""

from lexor.core.converter import NodeConverter
from lexor.core.elements import RawText


class LatexPINC(NodeConverter):
    """Remove latex processing instructions. """

    directive = '?latex'
    copy = False
    remove = True


class LatexNC(NodeConverter):
    """Adjust the node for mathjax. """

    directive = 'latex'

    def start(self, node):
        try:
            node.data = self.converter['MacroNC'].eval_text(node.data)
        except AttributeError:
            pass
        if node['type'] == 'display':
            node.name = 'script'
            node['type'] = "math/tex; mode=display"
            del node['char']
        else:
            node.name = 'script'
            node['type'] = "math/tex"
            del node['char']
        return node

    def end(self, node):
        node[0].data = self.converter['MacroNC'].eval_text(node[0].data)

class LatexEnvironNC(NodeConverter):
    """Adjust the enviroments. """

    def __init__(self, converter):
        NodeConverter.__init__(self, converter)
        # namespace = get_converter_namespace()
        # if 'latex_labels' not in namespace:
        #     namespace['latex_labels'] = list()
        self.handle = {
            'equation': self.handle_equation,
            'align': self.handle_align,
        }

    def end(self, node):
        return self.handle[node.name](node)

    def handle_label(self, node):
        """Collect labels. """
        latex_labels = get_converter_namespace()['latex_labels']
        if node['id'] in latex_labels:
            self.msg('E001', node, [node['id']])
        else:
            latex_labels.append(node['id'])

    def handle_equation(self, node):
        """Transform an equation. """
        name = node.name
        cdata = self.converter['MacroNC'].eval_text(node[0].data)
        if 'id' in node:
            self.handle_label(node)
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

    @staticmethod
    def label(node):
        """Check if we need to label. """
        if '\\label' in node[0].data:
            return True
        if 'class' in node and 'nolabel' in node['class']:
            return False
        if 'id' in node and node['id'] != '':
            return True
        return False

    @staticmethod
    def wrap(node):
        """Check if we need to surround the align enviroment. """
        if 'class' in node:
            if 'subeq' in node['class']:
                return 'subequations'
        return False

    def handle_align(self, node):
        """Translate align enviroment. """
        cdata = self.converter['MacroNC'].eval_text(node[0].data)
        label = self.label(node)
        if 'at' in node:
            if label:
                data = '\\begin{alignat}{%s}' % node['at']
            else:
                data = '\\begin{alignat*}{%s}' % node['at']
            if 'id' in node and '\\label' not in cdata:
                data += '\\label{%s}' % node['id']
                self.handle_label(node)
            data += cdata
            if label:
                data += '\\end{alignat}'
            else:
                data += '\\end{alignat*}'
        else:
            if label:
                data = '\\begin{align}'
            else:
                data = '\\begin{align*}'
            if 'id' in node and '\\label' not in cdata:
                data += '\\label{%s}' % node['id']
                self.handle_label(node)
            data += cdata
            if label:
                data += '\\end{align}'
            else:
                data += '\\end{align*}'
        newnode = RawText('script', data)
        newnode['type'] = "math/tex; mode=display"
        node.parent.insert_before(node.index, newnode)
        del node.parent[node.index]
        return newnode


class LatexEquationEnvironNC(LatexEnvironNC):

    directive = 'equation'


class LatexAlignEnvironNC(LatexEnvironNC):

    directive = 'align'


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
