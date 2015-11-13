"""LEXOR to HTML DEFAULT Converter Style

Converts a lexor file to a valid html file. Note that when using
python embeddings, everything outputted by the print statement will be
parsed in html.

"""
from lexor import init, load_aux
from lexor.core.converter import NodeConverter

INFO = init(
    version=(0, 0, 3, 'rc', 0),
    lang='lexor',
    to_lang='html',
    type='converter',
    description='Convert lexor files to html.',
    git={
        'host': 'github',
        'user': 'jmlopez-rod',
        'repo': 'lexor-converter-html-default'
    },
    author={
        'name': 'Manuel Lopez',
        'email': 'jmlopez.rod@gmail.com'
    },
    docs='http://jmlopez-rod.github.io/'
         'lexor-lang/lexor-converter-html-default',
    license='BSD License',
    path=__file__
)
DEFAULTS = {
    'error': 'on',
    'exec': 'on',
}


class BaseConverter(NodeConverter):

    directive = 'lx:base-converter'
    template_parser = {
        'lang': 'lexor',
        'style': '_',
        'defaults': {
            'inline': 'on'
        }
    }


class LXRemoveWrapNC(BaseConverter):

    directive = 'lx:remove-wrap'
    restrict = 'A'
    template = '<target/>'
    auto_transclude = 'target'
    replace = True


def pre_process(converter, doc):
    pass


def post_process(converter, doc):
    pass


MOD = load_aux(INFO)
