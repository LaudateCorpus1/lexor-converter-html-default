"""LEXOR to HTML Converter DEFAULT INLINE test

Testing suite for converter lexor to html inline in the default style.

"""
import lexor
from lexor.command.test import nose_msg_explanations, equal_nodes

LEXOR_INLINE_SETTINGS = {
    'parser_defaults': {'inline': 'on'},
}
HTML_SETTINGS = {
    'parser_lang': 'html',
    'convert': 'false'
}


def test_inline():
    """lexor.converter.html.default.inline: MSG_EXPLANATION """
    nose_msg_explanations(
        'lexor', 'converter', 'default', 'inline', 'html'
    )


def test_strong_em():
    """lexor.converter.html.default.inline: strong_em """
    txt_test = """***strong_em***"""
    txt_exp = """<strong><em>strong_em</em></strong>"""
    doc_test, _ = lexor.lexor(txt_test, **LEXOR_INLINE_SETTINGS)
    doc_exp, _ = lexor.lexor(txt_exp, **HTML_SETTINGS)
    assert equal_nodes(doc_test, doc_exp)


def test_em_strong():
    """lexor.converter.html.default.inline: em_strong """
    txt_test = """___em_strong___"""
    txt_exp = """<em><strong>em_strong</strong></em>"""
    doc_test, _ = lexor.lexor(txt_test, **LEXOR_INLINE_SETTINGS)
    doc_exp, _ = lexor.lexor(txt_exp, **HTML_SETTINGS)
    assert equal_nodes(doc_test, doc_exp)
