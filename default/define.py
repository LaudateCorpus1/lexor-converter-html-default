"""LEXOR to HTML DEFINE NodeConverter

"""

from lexor.core.converter import NodeConverter
from lexor.core.writer import replace


class DefineNC(NodeConverter):
    """Remove the define nodes. """

    directive = 'define'

    def end(self, node):
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


class UndefineNC(NodeConverter):
    """Remove the undef nodes. """

    directive = 'undef'

    def start(self, node):
        macro = get_converter_namespace()['macro']
        if 'class' in node and 'clear' in node['class']:
            keys = macro.keys()
            for key in keys:
                if macro[key]['flag'] == 'set':
                    del macro[key]
        data = [item.strip() for item in node.data.split(',')]
        for item in data:
            if item in macro:
                del macro[item]
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

    @staticmethod
    def convert(converter):
        """Modifies the nodes caught by this node converter. """
        for node in converter.undefine_nodes:
            del node.parent[node.index]


def next_char(text, index):
    """Return index if it is a nonblank space. Otherwise search for
    the first nonblank space. """
    if index >= len(text):
        return index
    while text[index] in ' \t\r\n\f\v':
        index += 1
        if index >= len(text):
            return index
    return index


def get_input(text, index):
    """Return the input and the index where the next character
    begins."""
    level = 0
    buff = ''
    while index < len(text):
        char = text[index]
        if char == '}' and level == 0:
            return buff, next_char(text, index+1)
        else:
            buff += char
            if char == '{' and text[index-1] != '\\':
                level += 1
            if char in '}' and text[index-1] != '\\':
                level -= 1
        index += 1
    print 'ERROR in FILE, working in lexor-converter-html:define.py'
    exit(1)


class MacroNC(NodeConverter):
    """Adjust the node for mathjax. """

    directive = 'macro'

    def __init__(self, converter):
        NodeConverter.__init__(self, converter)
        # namespace = get_converter_namespace()
        # if 'macro' not in namespace:
        #     namespace['macro'] = dict()

    @classmethod
    def handle_braces(cls, char, text, index):
        """Helper function for handle_token. """
        if char in '([' and text[index-5:index] != '\\left':
            return '\\left' + char
        elif char in ')]' and text[index-6:index] != '\\right':
            return '\\right' + char
        return char

    # pylint: disable=W0142
    def handle_set_delayed(self, text, index, node):
        """"Helper function for handle_token and eval_text. """
        args = []
        next_index = next_char(text, index)
        while text[next_index] == '{':
            arg, next_index = get_input(text, next_index+1)
            args.append(self.eval_text(arg))
            if next_index == len(text):
                break
        index = next_index
        evaled_val = self.eval_text(node['value'])
        if 'arg' in node:
            od_ = node['arg'].copy()
            keys = od_.keys()
            for i in xrange(len(args)):
                od_[keys[i]] = args[i]
            mapping = []
            for key, val in od_.iteritems():
                mapping.append([':'+key+':', val])
            return replace(evaled_val, *mapping), index
        return evaled_val, index

    def handle_token(self, text, token, new_text, index):
        """Helper function for eval_text. """
        macro = get_converter_namespace()['macro']
        char = text[index]
        if token in macro:
            node = macro[token]
            if node['flag'] == 'set':
                new_text += node['value']
                new_text += self.handle_braces(char, text, index)
                index += 1
            else:
                tmp, index = self.handle_set_delayed(text, index, node)
                new_text += tmp
        else:
            new_text += token
            new_text += self.handle_braces(char, text, index)
            index += 1
        return new_text, index

    def eval_text(self, text):
        """Perform replacement on text. """
        macro = get_converter_namespace()['macro']
        new_text = ''
        token = ''
        command = False
        index = 0
        while index < len(text):
            if text[index:index+2] in ['\\(', '\\)']:
                new_text += text[index+1]
                index += 2
                continue
            if text[index] == '\\' and command is False:
                command = True
                token += text[index]
                index += 1
                continue
            elif text[index].isalpha():
                token += text[index]
                index += 1
            else:
                new_text, index = self.handle_token(
                    text, token, new_text, index
                )
                token = ''
                command = False
        if token in macro:
            node = macro[token]
            if node['flag'] == 'set':
                new_text += node['value']
            else:
                tmp, index = self.handle_set_delayed(text, index, node)
                new_text += tmp
        else:
            new_text += token
        return new_text

    def start(self, node):
        if node['flag'] == 'set':
            node['value'] = self.eval_text(node['value'])
        get_converter_namespace()['macro'][node['name']] = node
        return node
