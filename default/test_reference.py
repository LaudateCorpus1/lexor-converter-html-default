"""LEXOR to HTML Converter DEFAULT REFERENCE test

Testing suite for converter lexor to html reference in the default style.

"""

from lexor.command.test import nose_msg_explanations


def test_reference():
    """lexor.converter.html.default.reference: MSG_EXPLANATION """
    nose_msg_explanations(
        'lexor', 'converter', 'default', 'reference', 'html',
        converter_opt={
            'to_lang': 'html',
            'from_lang': 'lexor',
            'style': 'default',
            'defaults': None,
            'parser_info': None
        }
    )
