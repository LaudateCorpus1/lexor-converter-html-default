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
        self.use_package(node.data, node)

    def use_package(self, name, node):
        """Load the package. """
        try:
            mod = self.get_module(name)
        except ImportError:
            return self.msg('E100', node, [name])
        try:
            repo = mod.REPOSITORY
        except AttributeError:
            repo = self.converter.find_node_converters(mod)
        for nc_class in repo:
            self.converter.register(nc_class)

    def get_module(self, src):
        """Load the module specified by name. """
        name = os.path.basename(src)
        name = os.path.splitext(name)[0]
        if src[0] != '/':
            base = os.path.dirname(self.converter.doc[0].uri_)
            if base != '':
                base += '/'
            path = '%s%s' % (base, src)
            if not path.endswith('.py'):
                path += '.py'
            try:
                return load_source('lexor-package_%s' % name, path)
            except IOError:
                try:
                    lexorinputs = os.environ['LEXORINPUTS']
                except KeyError:
                    raise ImportError
                for directory in lexorinputs.split(':'):
                    path = '%s/%s.py' % (directory, name)
                    if os.path.exists(path):
                        modname = 'lexor-package_%s' % name
                        return load_source(modname, path)
                raise ImportError


MSG = {
    'E001': 'more than one documentclass node found',
    'E100': 'package `{0}` not found',
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
    """
    - A "lexor" package is a python script which declares the
      one or several node converters and optionally a post_process
      function.

    - If the package is not found in the same directory as the
      document or some relative location to the document then it it
      searches in each of the paths declared by the environment
      variable `LEXORINPUTS`.

    Reports error E100.

""",
]
