"""LEXOR to HTML INLINE NodeConverter

Convert the `strong_em` and `em_strong` tags to proper html nodes.

"""
from lexor.core.converter import NodeConverter


class StrongEmNC(NodeConverter):
    """Replace 'strong_em' by the tags 'strong' and 'em'. """

    directive = 'strong_em'
    template = '%%{strong}%%{em}%%{target/}%%%%'
    replace = True
    auto_transclude = 'target'


class EmStrongNC(NodeConverter):
    """Replace 'strong_em' by the tags 'em' and 'strong'. """

    directive = 'em_strong'
    template = '%%{em}%%{strong}%%{target/}%%%%'
    replace = True
    auto_transclude = 'target'
