import ply.yacc as yacc
from analyzer.lexer import tokens, lexer

precedence = (
    ('left','COMMA'),
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
    ('right','UMINUS','UPLUS','NOT', 'NOTBW', 'AMP', 'DEC', 'INC', 'FLOAT','CHAR','INT','DOUBLE', 'SIZEOF'),
    ('left','DOT','CORL','CORR','PARR','PARL')
    )

    # opr1    :   opr1 PLUS opr2
    #            |   opr1 MINUS opr2
    #            |   PLUS 
    #    opr2    :   PLUS 
    #            |   MINUS
    #            |   Fopr TIMES    
    #'
def p_assign1

def p_opr1(p):
    '''opr  : opr PLUS opr
            | opr MINUS opr
            | opr TIMES opr
            | opr QUOT opr
            | opr REM opr
            | opr AND opr
            | opr XORBW opr
            | opr OR opr
            | opr ANDBW opr
            | opr ORBW opr
            | opr SHL opr
            | opr SHR opr
            | opr EQ opr
            | opr NEQ opr
            | opr LS opr
            | opr GR opr
            | opr LSE opr
            | opr GRE opr'''
    pass

def p_opr2(t):
    '''opr  : MINUS opr %prec UMINUS
            | PLUS opr %prec UPLUS
            | NOT opr
            | NOTBW opr
            | ANDBW opr %prec AMP'''
    pass

def p_opr3(t):
    '''opr  : opr INC
            | opr DEC '''
    pass

def p_opr4(t):
    '''opr  : INC opr
            | DEC opr'''
    pass

def p_opr5(t):
    '''opr  : INTVAL 
            | CHARVAL
            | STRVAL
            | FLOATVAL
            | TRUE
            | FALSE
            | ID
            | PARL opr PARR'''
    pass

def p_error(t):
    if t:
        print("error->",str(t))
        parser.errok()

parser = yacc.yacc()

def parse(input):
    lexer.lineno = 1
    return parser.parse(input)

