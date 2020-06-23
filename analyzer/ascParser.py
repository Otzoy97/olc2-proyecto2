import ply.yacc as yacc
from analyzer.lexer import tokens, lexer

def p_opr(p):
    '''opr  : opr '+' opr
            | opr '-' opr
            | opr '*' opr
            | opr '/' opr
            | opr '%' opr
            | opr '&&' opr
            | opr '^' opr
            | opr '||' opr
            | opr '&' opr
            | opr '|' opr
            | opr '<<' opr
            | opr '>>' opr
            | opr '==' opr
            | opr '!=' opr
            | opr '<' opr
            | opr '>' opr
            | opr '<=' opr
            | opr '>=' opr
            | '-' opr
            | '+' opr
            | '!' opr
            | '~' opr
            | '&' opr
            | opr '++'
            | opr '--'
            | '++' opr
            | '--' opr
            | opr '?' opr ':' opr'''

def p_opr_u1(t):
    '''opr  : '-' opr
            | '+' opr
            | '!' opr
            | '~' opr
            | '&' opr
            | opr '++'
            | opr '--'
            | '++' opr
            | '--' opr'''

def p_opr_u2(t):
    '''opr  : opr '++'
            | opr '--'
            | '++' opr
            | '--' opr'''

def p_opr_u3(t):
    '''opr  : '++' opr
            | '--' opr'''

def parse(input):
    lexer.lineno = 1
    return parser.parse(input)

