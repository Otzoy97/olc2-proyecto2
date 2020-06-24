"""
This grammar intends to emulate the grammar of the C programming language
So it was adapted from Appendix A, subsection 13 of the
The C programming language [PDF] (pp. 181-188) 2nd edition
by Kernighan, B. W., & Ritchie, D. M., Prentice-Hall (1988)
Retrieved from https://hikage.freeshell.org/books/theCprogrammingLanguage.pdf
"""

import ply.yacc as yacc
from analyzer.lexer import tokens, lexer

precedence = (
    #('left','COMMA'),
    ('right','ASSIGN','TIMESA','QUOTA','REMA','PLUSA'
    ,'MINUSA','SHRA','SHLA','ANDBWA','XORBWA','ORBWA'),
    ('right','QUESR','COLON'),
    ('left','OR'),
    ('left','AND'),
    ('left','ORBW'),
    ('left','XORBW'),
    ('left','ANDBW'),
    ('left','EQ','NEQ'),
    ('left','LS','LSE','GR','GRE'),
    ('left','SHL','SHR'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','QUOT','REM'),
    ('right','UMINUS','UPLUS','NOT', 'NOTBW', 'AMP', 'DEC', 'INC'),
    #('right','UMINUS','UPLUS','NOT', 'NOTBW', 'AMP', 'DEC', 'INC', 'FLOAT','CHAR','INT','DOUBLE', 'SIZEOF'),
    ('left','DOT','CORL','CORR','PARR','PARL')
    #('left','DOT','CORL','CORR','PARR','PARL')
    )
    

def p_postExpression(t):
    '''postExp  :   prim
                |   postExp CORL exp CORR
                |   postExp PARL PARR
                |   postExp PARL asexp PARR
                |   postExp DOT ID
                |   postExp INC
                |   postExp DEC'''
    pass

def p_fExpression(t):
    '''fexp     :   ID
                |   prim
                |   STRING
                |   PARR exp PARL'''
    pass

def p_primExp(t):
    '''prim     :   INT
                |   FLOAT
                |   CHAR'''
    pass

def p_expression(t):
    '''exp      :   asexp
                |   exp COMMA asexp'''
    pass 

def p_assignmentExpression(t):
    '''asexp    :   coexp
                |   unexp aop asexp'''
    pass

def p_assignmentOperator(t):
    '''aop      :   ASSIGN
                |   TIMESA
                |   QUOTA
                |   REMA
                |   PLUSA
                |   MINUSA
                |   SHRA
                |   SHLA
                |   ANDBWA
                |   XORBWA
                |   ORBWA'''
    t[0] = t[1]

def p_unaryOperator(t):
    '''uop      :   ANDBW
                |   TIMES
                |   PLUS
                |   MINUS
                |   NOTBW
                |   NOT'''
    t[0] = t[1]

def p_error(t):
    if t:
        print("error->",str(t))
        parser.errok()

parser = yacc.yacc()

def parse(input):
    lexer.lineno = 1
    return parser.parse(input)

