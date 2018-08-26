# -*- coding: utf-8 -*-
#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

import re
import copy

from pygments.lexer import RegexLexer, ExtendedRegexLexer, bygroups, using, \
     include, this
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
     Number, Other, Punctuation, Literal
from pygments.util import get_bool_opt, get_list_opt, looks_like_xml, \
                          html_doctype_matches


class KLLexer(RegexLexer):
    """
    For KL source code.
    """

    name = 'KL'
    aliases = ['kl']
    filenames = ['*.kl', ]
    mimetypes = ['application/x-kl', 'text/x-kl', ]

    flags = re.DOTALL
    tokens = {
        'commentsandwhitespace': [
            (r'\s+', Text),
            (r'//.*?\n', Comment.Single),
            (r'/\*.*?\*/', Comment.Multiline)
        ],
        'root': [
            include('commentsandwhitespace'),
            (r'<<<|>>>|\+\+|--|~|&&|\?|:|\|\||\\(?=\n)|'
             r'(<<?|>>?|==?|!=?|[-+*%&\|\^/])=?', Operator),
            (r'[{(\[;,]', Punctuation),
            (r'[})\].]', Punctuation),
            (r'(for|in|io|while|do|break|return|continue|switch|case|'
             r'default|if|else|throw|this|public|protected|private|permits)\b', Keyword),
            (r'(function|operator|inline)\b', Keyword.Declaration),
            (r'(Boolean|SInt8|UInt16|SInt16|UInt32|SInt32|UInt64|'
             r'SInt64|Float32|Float64|UInt8|Byte|Integer|Index|Count|String|struct|object|'
             r'interface|const|require|FUNC|FILE|LINE)\b', Keyword.Reserved),
            (r'(true|false|null|NaN|Inf)\b', Keyword.Constant),
            (r'(report|isInf|isNaN|isReg)\b', Name.Builtin),
            (r'[$a-zA-Z_][a-zA-Z0-9_]*', Name.Other),
            (r'[0-9][0-9]*\.[0-9]+([eE][0-9]+)?(f(32|64)?)?', Number.Float),
            (r'0x[0-9a-fA-F]+([su](8|16|32|64)?)?', Number.Hex),
            (r'[0-9]+([su](8|16|32|64)?)?', Number.Integer),
            (r'"(\\\\|\\"|[^"])*"', String.Double),
            (r"'(\\\\|\\'|[^'])*'", String.Single),
        ]
    }
