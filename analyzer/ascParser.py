"""
This grammar intends to emulate the grammar of the C programming language
So it was adapted from Appendix A, subsection 13 of the
The C programming language [PDF] (pp. 181-188) 2nd edition
by Kernighan, B. W., & Ritchie, D. M., Prentice-Hall (1988)
Retrieved from https://hikage.freeshell.org/books/theCprogrammingLanguage.pdf
"""

import ply.yacc as yacc
from analyzer.lexer import tokens, lexer

# precedence = (
#     #('left','COMMA'),
#     ('right','ASSIGN','TIMESA','QUOTA','REMA','PLUSA'
#     ,'MINUSA','SHRA','SHLA','ANDBWA','XORBWA','ORBWA'),
#     ('right','QUESR','COLON'),
#     ('left','OR'),
#     ('left','AND'),
#     ('left','ORBW'),
#     ('left','XORBW'),
#     ('left','ANDBW'),
#     ('left','EQ','NEQ'),
#     ('left','LS','LSE','GR','GRE'),
#     ('left','SHL','SHR'),
#     ('left','PLUS','MINUS'),
#     ('left','TIMES','QUOT','REM'),
#     ('right','UMINUS','UPLUS','NOT', 'NOTBW', 'AMP', 'DEC', 'INC'),
#     #('right','UMINUS','UPLUS','NOT', 'NOTBW', 'AMP', 'DEC', 'INC', 'FLOAT','CHAR','INT','DOUBLE', 'SIZEOF'),
#     ('left','DOT','CORL','CORR','PARR','PARL')
#     #('left','DOT','CORL','CORR','PARR','PARL')
#     )




def p_function_def(t):
    '''function_def     :   dec_spec declarator dec_list c_statments
                        |   dec_spec declarator c_statments
    '''
    pass

def p_declaration(t):
    '''declaration      :   
    '''
    pass

def p_dec_spec(t):
    '''dec_spec         :   VOID 
                        |   INT
                        |   CHAR
                        |   STRING
                        |   DOUBLE
                        |   FLOAT
                        |   struct_spec
    '''
    pass

def p_declarationLst(t):
    '''declarator       :   declaratorD'''
    pass

def p_declarator(t):
    '''declaratorD      :   ID
                        |   PARL declaratorD PARR
                        |   declaratorD CORL CORR
                        |   declaratorD CORL constantExpression CORR
                        |   declaratorD PARL PARR
                        |   declaratorD PARL PARR
    '''
    pass

def p_par_list(t):
    '''par_list         :   par_list COMMA par_dec
                        |   par_dec
    '''
    pass

def p_par_dec(t):
    '''par_dec          :   dec_spec declarator
    '''
    pass

def p_constantExpression(t):
    '''constantExpression:  conditionalExpression  
    '''
    pass


def p_conditionalExpression(t):
    '''conditionalExpression: orExpression
                        |   orExpression QUESR expression COLON conditionalExpression
    '''
    pass

def p_orExpression(t):
    '''orExpression     :   andExpression
                        |   orExpresssion OR andExpression 
    '''
    pass


def p_andExpression(t):
    '''andExpression    :   orBwExpression
                        |   andExpression AND orBwExpression
    '''
    pass

def p_orBwExpression(t):
    '''orBwExpression   :   xorBwExpression
                        |   orBwExpression ORBW xorBwExpression
    '''
    pass

def p_xorBwExpression(t):
    '''xorBwExpression  :   andBwExpression
                        |   xorBwExpression XORBW andBwExpression
    '''
    pass

def p_andBwExpression(t):
    '''andBwExpression  :   equalExpression
                        |   andBwExpression ANDBW  equalExpression
    '''
    pass


def p_equalExpression(t):
    '''equalExpression  :   relaExpression
                        |   equalExpression EQ relaExpression
                        |   equalExpression NEQ relaExpression
    '''
    pass

def p_relaExpression(t):
    '''relaExpression   :   shiftExpression
                        |   relaExpression LS shiftExpression
                        |   relaExpression GR shiftExpression
                        |   relaExpression LSE shiftExpression
                        |   relaExpression GRE shiftExpression
    '''
    pass

def p_shiftExpression(t):
    '''shiftExpression  :   addExpression
                        |   shiftExpression SHL addExpression
                        |   shiftExpression SHR addExpression'''

def p_addExpression(t):
    '''addExpression    :   multiExpression
                        |   addExpression PLUS multiExpression
                        |   addExpression MINUS multiExpression'''
    pass

def p_multiExpression(t):
    '''multiExpression  :   castExpression
                        |   multiExpression TIMES castExpression
                        |   multiExpression QUOT castExpression
                        |   multiExpression REM castExpression'''
    pass

def p_castExpression(t):
    '''castExpression   :   unaryExpression
                        |   PARL typeName PARR castExpression'''
    pass    
    
def p_unaryExpression(t):
    '''unaryExpression  :   postfixExpression
                        |   INC unaryExpression
                        |   DEC unaryExpression
                        |   unaryOperator castExpression
                        |   SIZEOF unaryExpression
                        |   SIZEOF PARL typeName PARR'''
    pass

def p_postExpression(t):
    '''postfixExpression:   primaryExpression
                        |   postExp CORL expression CORR
                        |   postExp PARL PARR
                        |   postExp PARL assignmentExpressionList PARR
                        |   postExp DOT ID
                        |   postExp INC
                        |   postExp DEC'''
    pass

def p_fExpression(t):
    '''primaryExpression:   ID
                        |   constant
                        |   STRVAL
                        |   PARL expression PARR'''
    pass

def p_primExp(t):
    '''constant         :   INTVAL
                        |   FLOATVAL
                        |   CHARVAL'''
    pass

def p_expression(t):
    '''expression       :   assignmentExpression
                        |   expression COMMA assignmentExpression'''
    pass 

def p_assignmentExpressionList(t):
    '''assignmentExpressionList: assignmentExpression 
                        |   assignmentExpressionList COMMA assignmentExpression
    '''
    pass

def p_assignmentExpression(t):
    '''assignmentExpression:   conditionalExpression
                        |   unaryExpression assignmentOperator assignmentExpression'''
    pass

def p_assignmentOperator(t):
    '''assignmentOperator:   ASSIGN
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
    '''unaryOperator    :   ANDBW
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

