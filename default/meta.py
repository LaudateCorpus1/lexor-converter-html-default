"""LEXOR to HTML META NodeConverter

Attach the meta info to the main document. There are several
modifications that are done to the values before they get added
to the document meta property.

- $(KEY): uses an already declared meta property to replace the string
- $(KEY)[index]: specifies the value of meta property
- ${KEY}: Uses an environment variable.

For instance

    -------
    name: ${USER}
    description: The user $(name) is awesome!
        You are awesome!
    who-is-awesome: $(description)[1]
    --------

"""
import re
import os
from lexor.core.converter import NodeConverter
from lexor.core.writer import replace
from lexor.core.elements import RawText
RE = re.compile(r'\$\((.*?)\)(?!\[)')
RE_NUM = re.compile(r'\$\((.*?)\)\[(.*?)\]')
RE_ENV = re.compile(r'\$\{(.*?)\}')


def handle_data(data, meta):
    variables = RE.findall(data)
    variables_line = RE_NUM.findall(data)
    env_variables = RE_ENV.findall(data)
    replace_list = list()
    for var, num in variables_line:
        num = int(num)
        try:
            value = meta.get(var, [''])[num]
        except IndexError:
            value = ''
        replace_list.append(
            ('$(%s)[%d]' % (var, num), value)
        )
    for var in variables:
        replace_list.append(
            ('$(%s)' % var, meta.get(var, [''])[0])
        )
    for var in env_variables:
        replace_list.append(
            ('${%s}' % var, os.environ.get(var, ''))
        )
    if replace_list:
        return replace(data, *replace_list)
    return data


class MetaNC(NodeConverter):
    """Attach the entries to the document meta attribute. """

    directive = 'lx:meta'
    remove = 'pre_link'


class MetaEntryNC(NodeConverter):

    directive = 'lx:meta-entry'
    require = '^(1)lx:meta'

    def compile(self, node, info, t_node, required):
        key = node['name']
        if key not in node.owner.meta:
            node.owner.meta[key] = []


class MetaItemNC(NodeConverter):

    directive = 'lx:meta-item'
    require = '^(1)lx:meta-entry'

    def compile(self, node, info, t_node, required):
        _, entry = required[0]
        if not isinstance(node, RawText):
            return self.msg('E100', node)
        item = handle_data(node.data, node.owner.meta)
        entry_name = entry['name']
        node.owner.meta[entry_name].append(item)
        if entry_name == 'usepackage':
            trans = self.converter
            names = [i.strip() for i in item.split(',')]
            for pkg in names:
                if pkg:
                    trans.load_package(pkg, node)


MSG = {
    'E100': '`lx:meta-item` found in non `RawText` element',
}
MSG_EXPLANATION = [
    """
    - Lexor meta items are build by the lexor parser so that we may
      process them only during the compilation phase when converting.

    - You may be seeing this error if another parser language was
      used which is different from the language the converter is
      converting from.

    - For instance, the html parser may parse `lx:meta-item` tags
      correctly, but they will be treated as plain Elements, not
      RawText elements.

    Reports E100

""",
]
