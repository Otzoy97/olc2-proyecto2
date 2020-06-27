import ply.lex as lex
from analyzer.err import ErrType, addErr

reserved = {
    'int': 'INT',
    'char': 'CHAR',
    'double': 'DOUBLE',
    'float': 'FLOAT',
    'struct': 'STRUCT',
    'void': 'VOID',
    'for': 'FOR',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'do': 'DO',
    'switch': 'SWITCH',
    'case': 'CASE',
    'continue': 'CONTINUE',
    'break': 'BREAK',
    'default': 'DEFAULT',
    'return': 'RETURN',
    #'true': 'TRUE',
    #'false': 'FALSE',
    'sizeof': 'SIZEOF'
}

tokens = [
    'INTVAL',
    'FLOATVAL',
    'STRVAL',
    'CHARVAL',
    'ID',
    'CORL',
    'CORR',
    'PARR',
    'PARL',
    'LLVR',
    'LLVL',
    'DOT',
    'MINUS',
    'PLUS',
    'TIMES',
    'QUOT',
    'REM',
    'NOT',
    'AND',
    'OR',
    'NOTBW',
    'ANDBW',
    'ORBW',
    'XORBW',
    'SHL',
    'SHR',
    'EQ',
    'ASSIGN',
    'NEQ',
    'GR',
    'GRE',
    'LS',
    'LSE',
    'INC',
    'DEC',
    'TIMESA',
    'QUOTA',
    'REMA',
    'PLUSA',
    'MINUSA',
    'SHRA',
    'SHLA',
    'ANDBWA',
    'XORBWA',
    'ORBWA',
    'QUESR',
    'SCOLON',
    'COLON',
    'COMMA'
] + list(reserved.values())

t_DOT           = r'\.'
t_CORL          = r'\['
t_CORR          = r'\]'
t_PARL          = r'\('
t_PARR          = r'\)'
t_LLVL          = r'\{'
t_LLVR          = r'\}'
t_MINUS         = r'-'
t_PLUS          = r'\+'
t_TIMES         = r'\*'
t_QUOT          = r'/'
t_REM           = r'%'
t_NOT           = r'!'
t_AND           = r'&&'
t_OR            = r'\|\|'
t_NOTBW         = r'~'
t_ANDBW         = r'&'
t_ORBW          = r'\|'
t_XORBW         = r'\^'
t_SHL           = r'<<'
t_SHR           = r'>>'
t_EQ            = r'=='
t_ASSIGN        = r'='
t_NEQ           = r'!='
t_GR            = r'>'
t_GRE           = r'>='
t_LS            = r'<'
t_LSE           = r'<='
t_DEC           = r'--'
t_INC           = r'\+\+'
t_TIMESA        = r'\*='
t_QUOTA         = r'/='
t_REMA          = r'%='
t_PLUSA         = r'\+='
t_MINUSA        = r'-='
t_SHRA          = r'>>='
t_SHLA          = r'<<='
t_ANDBWA        = r'&='
t_XORBWA        = r'\^='
t_ORBWA         = r'\|='
t_QUESR         = r'\?'
t_SCOLON        = r'\;'
t_COLON         = r'\:'
t_COMMA         = r'\,'

def t_FLOATVAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except:
        #TODO: this is an error: this is not a number
        t.value = 0.0
    return t

def t_INTVAL(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError: 
        #TODO: this is an error: overflow int data
        # implicit cast
        try:
            t.value = float(t.value)
            t.type = 'FLOATVAL'
        except:
            #TODO: this is an error: this is not a number
            t.value = 0
    return t

def t_STRVAL(t):
    r'\"[^\"\\]*(\\.[^\"\\]*)*\"'
    #replace \\ with \
    str_ = t.value[1:-1]
    #str_ = str_.replace("\\n","\n")
    #str_ = str_.replace("\\r","\r")
    #str_ = str_.replace("\\t","\t")
    t.value = str_
    return t

def t_CHARVAL(t):
    r"'((\\.)|([^'\\]))'"
    t.value = t.value[1:-1]
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    #print("id->", t)
    t.type = reserved.get(t.value, 'ID')
    return t

def t_COMMENT(t):
    r'\/\/.*\n*?'
    t.lexer.lineno += t.value.count('\n')

def t_MCOMMENT(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    addErr(ErrType.LEXIC, 'Illegal character: ' + str(t.value[0]), t.lexer.lineno)
    t.lexer.skip(1)

lexer = lex.lex()