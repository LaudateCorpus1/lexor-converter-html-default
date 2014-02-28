"""LEXOR to HTML DEFAULT Converter Style

Converts a lexor file to a valid html file. Note that when using
python embeddings, everything outputed by the print statement will be
parsed in html.

"""

from lexor import init, load_aux

INFO = init(
    version=(0, 0, 1, 'rc', 0),
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
MAPPING = {
    '?python': MOD['python'].PythonNC,
    'strong_em': MOD['inline'].StrongEmNC,
    'em_strong': 'strong_em',
}


def convert(converter, _):
    """Evaluate the python embeddings. """
    converter['strong_em'].convert(converter)
    converter['?python'].convert(converter)
