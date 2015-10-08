"""LEXOR to HTML INLINE NodeConverter

Convert the `strong_em` and `em_strong` tags to proper html nodes.

"""
from lexor import style_reference
MOD = style_reference(lang='lexor', to_lang='html')


class StrongEmNC(MOD.BaseConverter):
    """Replace 'strong_em' by the tags 'strong' and 'em'. """

    directive = 'strong_em'
    template = '%%{strong}%%{em}%%{target/}%%%%'
    replace = True
    auto_transclude = 'target'


class EmStrongNC(MOD.BaseConverter):
    """Replace 'strong_em' by the tags 'em' and 'strong'. """

    directive = 'em_strong'
    template = '%%{em}%%{strong}%%{target/}%%%%'
    replace = True
    auto_transclude = 'target'
