"""LEXOR to HTML REFERENCE NodeConverter

Fixes the references.

"""

from lexor.core.converter import NodeConverter, get_converter_namespace
import lexor.core.elements as core

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

    def __init__(self, converter):
        NodeConverter.__init__(self, converter)
        namespace = get_converter_namespace()
        if 'block_ref' not in namespace:
            namespace['block_ref'] = dict()

    def start(self, node):
        block_ref = get_converter_namespace()['block_ref']
        refname = node['_reference_name']
        if refname in block_ref:
            pos1 = node['_pos']
            pos2 = block_ref[refname]['_pos']
            self.msg(
                'E001', node, (
                    refname, pos1[0], pos1[1], pos2[0], pos2[1]
                )
            )
        block_ref[refname] = node
        parent = node.parent
        index = node.index
        del node.parent[node.index]
        try:
            if index - 1 > -1:
                return parent[index-1]
            else:
                raise IndexError
        except IndexError:
            parent.append_child('')
        return parent[0]

    def __getitem__(self, refname):
        """Return a node containing the reference. """
        return get_converter_namespace()['block_ref'][refname]


class ReferenceInlineNC(NodeConverter):
    """Handle references. """

    def start(self, node):
        self.converter.document.namespace['inline_ref'].append(node)
        return node

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
        template = template % "\\%s{%s}"
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
                self.msg(
                    'E100', node, (
                        key, node['_pos'][0], node['_pos'][1]
                    )
                )
        else:
            node['_address'] = ref['_address']
            for item in ref:
                if item[0] != '_':
                    node[item] = ref[item]
        return True

    @staticmethod
    def rename(node, tex_ref):
        """Final stage in the conversion. """
        del node['_pos']
        if tex_ref is not None:
            node.parent.insert_before(node.index, tex_ref)
            del node.parent[node.index]
        elif isinstance(node, core.Void):
            node.name = 'img'
            node.rename('_address', 'src')
        else:
            node.name = 'a'
            node.rename('_address', 'href')

    def convert(self):
        """Modifies the nodes caught by this node converter. """
        ref_block_nc = self.converter['ReferenceBlockNC']
        inline_ref = self.converter.document.namespace['inline_ref']
        doc_level = len(self.converter.doc)
        for node in inline_ref:
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
                        self.msg(
                            'E101', node, (
                                node['_pos'][0], node['_pos'][1]
                            )
                        )
            if doc_level > 1 and update is False:
                if 'uri' not in node:
                    node['uri'] = node.owner.uri
                namespace = self.converter.doc[-2].namespace
                namespace['inline_ref'].append(node)
                continue
            self.rename(node, tex_ref)


MSG = {
    'E001': '`{0}` at {1}:{2:2} already defined at {3}:{4:2}',
    'E100': 'undefined reference `{0}` at {1}:{2:2}',
    'E101': 'implicit link at {0}:{1:2} contains elements',
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
