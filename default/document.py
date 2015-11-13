"""LEXOR to HTML DOCUMENT NodeConverter

"""

import os
from imp import load_source
from lexor.core import NodeConverter, DocumentType, Element


def find_element(name, node, index=0, **keywords):
    """Looks for an element in the node children. If it is not found,
    a new element is created and placed before the specified index.
    """
    result = None
    for ele in node.child:
        if ele.name.lower() == name:
            result = ele
            break
    if result is None and keywords.get('insert', True):
        args = keywords.get('args', None)
        etype = keywords.get('etype', Element)
        if args is None:
            result = etype(name)
        else:
            result = etype(*args)
        node.insert_before(index, result)
    return result


class DocumentClassNC(NodeConverter):
    """Appends a DocumentType node. """

    directive = 'documentclass'
    remove = 'post_link'

    def compile(self, node, dir_info, t_node, required):
        scope = self.converter.root_document.namespace
        if 'documentclass_count' not in scope:
            scope['documentclass_count'] = 0
        scope['documentclass_count'] += 1
        if scope['documentclass_count'] > 1:
            self.msg('E001', node)
        doc = node.owner
        find_element(
            '#doctype', doc, 0, etype=DocumentType, args=['html']
        )

    def post_link(self, node, dir_info, trans_ele, required):
        """Append an html node and the header node. """
        document = node.owner
        find_element(
            '#doctype', document, 0, etype=DocumentType, args=['html']
        )
        html = find_element('html', document, 1)
        head = find_element('head', document, insert=False)
        if head is None:
            head = find_element('head', html, 0)
        else:
            html.insert_before(0, head)
        body = find_element('body', document, insert=False)
        if body is None:
            body = find_element('body', html, 1)
        else:
            head.extend_children(document[html.index+1:body.index])
            html.insert_before(1, body)
        body.extend_children(document[body.parent.index+1:])


class UsePackageNC(NodeConverter):
    """Loads an external python script. """

    directive = 'usepackage'
    remove = True

    def compile(self, node, dir_info, t_node, required):
        self.converter.load_package(node.data, node)


MSG = {
    'E001': 'more than one documentclass node found',
}
MSG_EXPLANATION = [
    """
    - There can only be one documentclass node in a document. Make
      sure that documents included within a document do not contain
      such nodes.

    - Make sure the body node is declared when using the
      documentclass node.

    Reports error E001.

""",
]
