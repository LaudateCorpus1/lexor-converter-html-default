"""LEXOR to HTML DEFAULT Converter Style

Converts a lexor file to a valid html file. Note that when using
python embeddings, everything outputed by the print statement will be
parsed in html.

"""

from lexor import init, load_aux

INFO = init(
    version=(0, 0, 1, 'rc', 3),
    lang='lexor',
    to_lang='html',
    type='converter',
    description='Convert lexor files to html.',
    url='http://jmlopez-rod.github.io/'
        'lexor-lang/lexor-converter-html-default',
    author='Manuel Lopez',
    author_email='jmlopez.rod@gmail.com',
    license='BSD License',
    path=__file__
)
DEFAULTS = {
    'error': 'on',
    'exec': 'on',
}
MOD = load_aux(INFO)
REPOSITORY = [
    MOD['define'].DefineNC,
    MOD['define'].MacroNC,
    MOD['define'].UndefineNC,
    MOD['figure'].FigureNC,
    MOD['include'].IncludeNC,
    MOD['inline'].StrongEmNC,
    MOD['latex'].LatexNC,
    MOD['latex'].LatexEnvironNC,
    MOD['list'].ListNC,
    MOD['paragraph'].ParagraphNC,
    MOD['python'].PythonNC,
    MOD['reference'].ReferenceBlockNC,
    MOD['reference'].ReferenceInlineNC,
]
MAPPING = {
    '?python': 'PythonNC',
    'strong_em': 'StrongEmNC',
    'em_strong': 'StrongEmNC',
    'p': 'ParagraphNC',
    'list': 'ListNC',
    'address_reference': 'ReferenceBlockNC',
    'reference': 'ReferenceInlineNC',
    'latex': 'LatexNC',
    'equation': 'LatexEnvironNC',
    #'align': 'LatexEnvironNC', # todo: figure out subequations
    'figure': 'FigureNC',
    'define': 'DefineNC',
    'undef': 'UndefineNC',
    'macro': 'MacroNC',
    'include': 'IncludeNC',
}


def init_conversion(_, doc):
    """Initialiazing the conversion of a document. """
    doc.namespace['inline_ref'] = list()


def convert(converter, _):
    """Evaluate the python embeddings. """
    converter['ReferenceInlineNC'].convert()
