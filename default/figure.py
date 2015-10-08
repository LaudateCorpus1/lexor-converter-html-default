"""LEXOR to HTML FIGURE NodeConverter

Node writer description.

"""

from lexor.core.converter import NodeConverter, get_converter_namespace
import lexor.core.elements as core


class FigureNC(NodeConverter):
    """Adjust a figure. """

    directive = 'figure'

    num = 0

    def end(self, node):
        if 'id' in node:
            latex_labels = get_converter_namespace()['latex_labels']
            if node['id'] in latex_labels:
                self.converter['LatexNC'].msg('E001', node, [node['id']])
            else:
                latex_labels.append(node['id'])
        caption = core.Element('figcaption')
        self.num += 1
        caption.append_child('Figure %d: ' % self.num)
        caption.extend_children(node)
        if 'src' in node:
            image = core.Void('img')
            image['src'] = node['src']
            del node['src']
            node.append_child(image)
        node.append_child(caption)
        return node
