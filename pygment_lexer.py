from pygments.lexer import RegexLexer
from pygments.token import *

class LambdaLexer(RegexLexer):
    name = 'Lambda'
    aliases = ['lambda']
    filenames = ['*.lambda']

    tokens = {
        'root': [
            (r'lambda', Keyword),
            (r'(\w| )* => ', Text),
            (r'\.|\(|\)', Punctuation),
            (r'(?!lambda)([a-zA-Z])+', Literal),
            (r' ', Whitespace),
        ]
    }
