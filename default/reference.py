"""LEXOR to HTML REFERENCE NodeConverter

Fixes the references.

"""
from lexor.util import Position
import lexor.core.elements as core
from lexor.core.converter import (
    NodeConverter
)

REF = [
    'chap', 'c',
    'sec',
    'subsec',
    'fig', 'f',
    'tab',
    'eq', 'e',
    'lst',
    'itm',
    'app',
]


class ReferenceBlockNC(NodeConverter):
    """Handle references. """

    directive = 'lx:address-reference'
    remove = 'compile'

    def __init__(self, converter):
        NodeConverter.__init__(self, converter)
        namespace = converter.root_document.namespace
        if 'lx:address-reference' not in namespace:
            namespace['lx:address-reference'] = dict()
        self.namespace = namespace

    def compile(self, node, dir_info, t_node, required):
        namespace = self.namespace
        ref = namespace['lx:address-reference']
        ref_name = node['_reference-name']
        if ref_name in ref:
            self.msg(
                'E001', node, (
                    ref_name,
                    Position(ref[ref_name].node_position)
                )
            )
        ref[ref_name] = node

    def __getitem__(self, ref_name):
        """Return a node containing the reference. """
        ref = self.namespace['lx:address-reference']
        return ref[ref_name]


class ReferenceInlineNC(NodeConverter):
    """Handle references. """

    directive = 'lx:reference'

    def pre_link(self, node, dir_info, trans_ele, required):
        ref_block_nc = self.converter['ReferenceBlockNC']
        doc_level = len(self.converter.doc)
        tex_ref = None
        node['_address'] = ''
        if '_reference_id' in node:
            update = self.update_node(
                node, ref_block_nc, '_reference_id'
            )
            if update or doc_level == 1:
                del node['_reference_id']
        else:
            if isinstance(node, core.Void):
                update = self.update_node(
                    node, ref_block_nc, 'alt'
                )
            else:
                if len(node) == 1 and node[0].name == '#text':
                    update = self.update_node(
                        node, ref_block_nc, node[0].data
                    )
                    if isinstance(update, str):
                        tex_ref = core.RawText('script', update)
                        tex_ref['type'] = "math/tex"
                elif doc_level > 1:
                    update = False
                else:
                    self.msg('E101', node)
        if doc_level > 1 and update is False:
            if 'uri' not in node:
                node['uri'] = node.owner.uri
            # namespace = self.converter.doc[-2].namespace
            # namespace['inline_ref'].append(node)
            return
        self.rename(node, tex_ref)

    @staticmethod
    def format_latex_ref(key):
        """Helper function for update_node. Handles the latex
        references. """
        ref_type = 'cite'
        template = '%s'
        if key[0] == '!':
            ref_type = 'pageref'
            key = key[1:]
        if ':' in key:
            ltype, _ = key.split(':')
            ltype = ltype.lower()
            if ltype in REF:
                ref_type = 'ref'
                if ltype in ['eq', 'e']:
                    template = '(%s)'
                elif ltype in ['fig', 'f']:
                    template = 'Fig.%s'
                else:
                    template = '%s'
        template %= "\\%s{%s}"
        return template % (ref_type, key)

    def update_node(self, node, ref_block_nc, key):
        """Updates a given node with the information of an
        address_reference node given by the key."""
        if key in node:
            key = node[key]
        try:
            ref = ref_block_nc[key]
        except KeyError:
            try:
                if key in get_converter_namespace()['latex_labels']:
                    return self.format_latex_ref(key)
                else:
                    raise KeyError
            except KeyError:
                if len(self.converter.doc) > 1:
                    return False
                self.msg('E100', node, [key])
        else:
            node['_address'] = ref['_address']
            for item in ref.attributes:
                if item[0] != '_':
                    node[item] = ref[item]
        return True

    @staticmethod
    def rename(node, tex_ref):
        """Final stage in the conversion. """
        if tex_ref is not None:
            node.parent.insert_before(node.index, tex_ref)
            del node.parent[node.index]
        elif isinstance(node, core.Void):
            node.name = 'img'
            node.rename('_address', 'src')
        else:
            node.name = 'a'
            node.rename('_address', 'href')


MSG = {
    'E001': '`{0}` already defined at {1}',
    'E100': 'undefined reference `{0}`',
    'E101': 'implicit link contains elements',
}
MSG_EXPLANATION = [
    """
    - Address references can only be defined once. 'E001' tells you
      the location of where it was first defined.

    Okay:
        [1]: http://google.com
        [2]: http://daringfireball.net/projects/markdown/

    E001:
        [1]: http://google.com
        [1]: http://daringfireball.net/projects/markdown/

""", """
    - The reference provided does have a reference defined in a
      block. For instance, if you provide `[google][1]` Then you must
      have a block with `[1]: link/to/google`.

    Okay:
        Here is a link to [google][1].

        [1]: http://google.com

    E100:
        Here is a link to [google][1].
""", """
    - When using implicit links you can only define address references
      that contain no elements. An id should be defined instead.

    Okay:
        This is the [link to google].

        [link to google]: http://google.com

    E101:
        This is the [**link** to _google_].

        [**link** to _google_]: http://google.com

""",
]
