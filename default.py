"""LEXOR to HTML DEFAULT Converter Style

Converts a lexor file to a valid html file. Note that when using
python embeddings, everything outputed by the print statement will be
parsed in html.

"""

from lexor import init, load_aux
from lexor.core.converter import NodeConverter


class BaseConverter(NodeConverter):

    template_parser = {
        'lang': 'lexor',
        'style': '_',
        'defaults': {
            'inline': 'on'
        }
    }


class LXRemoveWrapNC(BaseConverter):

    directive = 'lx-remove-wrap'
    restrict = 'A'
    template = '<target/>'
    auto_transclude = 'target'
    replace = True


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
MOD = load_aux(INFO)
REPOSITORY = [
    LXRemoveWrapNC,
    MOD['code'].InlineCodeNC,
    MOD['code'].CodeBlockNC,
    MOD['define'].DefineNC,
    MOD['define'].MacroNC,
    MOD['define'].UndefineNC,
    MOD['document'].DocumentClassNC,
    MOD['document'].UsePackageNC,
    MOD['entity'].EntityNC,
    MOD['figure'].FigureNC,
    MOD['include'].IncludeNC,
    MOD['inline'].StrongEmNC,
    MOD['inline'].EmStrongNC,
    MOD['latex'].LatexPINC,
    MOD['latex'].LatexNC,
    MOD['latex'].LatexEquationEnvironNC,
    MOD['latex'].LatexAlignEnvironNC,
    MOD['list'].ListNC,
    MOD['meta'].MetaNC,
    MOD['meta'].MetaEntryNC,
    MOD['meta'].MetaItemNC,
    MOD['quote'].QuoteNC,
    MOD['reference'].ReferenceBlockNC,
    MOD['reference'].ReferenceInlineNC,
]


def pre_process(converter, doc):
    pass


def post_process(converter, doc):
    pass


def init_conversion(converter, doc):
    """Initialiazing the conversion of a document. """
    doc.namespace['inline_ref'] = list()
    if 'usepackage' not in converter.doc[0].namespace:
        converter.doc[0].namespace['usepackage'] = list()


def convert(converter, _):
    """Evaluate the python embeddings. """
    converter['ReferenceInlineNC'].convert()
    converter['DocumentClassNC'].convert()
    converter['UsePackageNC'].convert()
