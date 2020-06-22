# Recuperado el 21/06/2020 de https://wiki.python.org/moin/PyQt/Python%20syntax%20highlighting
# Autor : https://wiki.python.org/moin/DavidBoddie 
# Modificaciones : S. Otzoy

import sys

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter


def format(color, style=''):
    """Return a QTextCharFormat with the given attributes.
    """
    _color = QColor()
    _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QFont.Bold)
    return _format

# Syntax styles that can be shared by all languages
STYLES = {
    'keyword': format('blue', 'bold'),
    'operator': format('red'),
    'string': format('blue'),
    'comment': format('darkCyan'),
    'numbers': format('darkMagenta'),
}


class MinorCSyntaxHighligther (QSyntaxHighlighter):
    """Syntax highlighter for the Python language.
    """
    # Python keywords
    keywords = [
        'int',
        'char',
        'double',
        'float',
        'char',
        'struct',
        'for',
        'if',
        'else',
        'while',
        'do',
        'switch',
        'case',
        'continue',
        'break',
        'default',
        'return',
        'sizeof',
        'auto',
        'const',
        'extern',
        'cast'
    ]

    # Python operators
    operators = [
        r'\(', r'\)', r'\[', r'\]', r'\{', r'\}',
        r'\.',
        r'\+', r'\-', '!', r'\~',
        r'\*', r'\&',
        r'/', r'\%',
        '==', '!=', '>=', '<=', '>', '<',
        '=',
        r'\^',
        r'\&', r'\|',
        r'\?', r'\:',
        ',', ';'
    ]

    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)
        rules = []

        # Keyword, operator, and brace rules
        rules += [(r'\b%s\b' % w, 0, STYLES['keyword'])
            for w in MinorCSyntaxHighligther.keywords]
        rules += [(r'%s' % o, 0, STYLES['operator'])
            for o in MinorCSyntaxHighligther.operators]

        # All other rules
        rules += [
            # Double-quoted string, possibly containing escape sequences
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),

            # From '//' until a newline
            (r'//[^\n]*', 0, STYLES['comment']),

            # Numeric literals
            (r'\d+', 0, STYLES['numbers']),
            (r'\d+\.\d+', 0, STYLES['numbers']),
        ]

        # Build a QRegExp for each pattern
        self.rules = [(QRegExp(pat), index, fmt)
            for (pat, index, fmt) in rules]

    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.
        """
        # Do other syntax formatting
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)

            while index >= 0:
                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)


        initComment = QRegExp(r"/\*")
        finalComment = QRegExp(r"\*/")

        startIndex = 0
        add = 0
        if(self.previousBlockState() != 1):
            startIndex = initComment.indexIn(text)
            add = initComment.matchedLength()

        while (startIndex >= 0):
            endIndex = finalComment.indexIn(text, startIndex + add)
            length = 0
            if endIndex >= add:
                length = endIndex - startIndex + add + finalComment.matchedLength() - 2
                self.setCurrentBlockState(0)
            else:
                self.setCurrentBlockState(1)
                length = len(text) - startIndex + add
            self.setFormat(startIndex, length, STYLES['comment'])
            startIndex = initComment.indexIn(text, startIndex + length)
