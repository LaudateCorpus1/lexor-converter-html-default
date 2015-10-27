"""LEXOR to HTML Converter DEFAULT META test

Testing suite for converter lexor to html meta in the default style.

"""
import lexor
import os
from lexor.command.test import nose_msg_explanations
from nose.tools import eq_


def test_meta():
    """lexor.converter.html.default.meta: MSG_EXPLANATION """
    nose_msg_explanations(
        'lexor', 'converter', 'default', 'meta', 'html'
    )


def test_meta_example():
    """lexor.converter.html.default.meta: example """
    text = """---
name: ${USER}
description: The user $(name) is awesome!
    You are awesome!
who-is-awesome: $(description)[1]
---
"""
    doc, _ = lexor.lexor(text)
    meta = doc.meta
    eq_(meta['who-is-awesome'], ['You are awesome!'])
    eq_(meta['name'], [os.environ['USER']])
    eq_(meta['description'], [
        'The user %s is awesome!' % meta['name'][0],
        'You are awesome!'
    ])
