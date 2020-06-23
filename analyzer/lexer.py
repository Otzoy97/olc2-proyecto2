import ply.lex as lex

reserved = {
    'int': 'INT',
    'char': 'CHAR',
    'double': 'DOUBLE',
    'float': 'FLOAT',
    'struct': 'STRUCT',
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
    'sizeof': 'SIZEOF',
    #'auto': 'AUTO',
    #'const': 'CONST',
    'cast': 'CAST'
}

tokens = [
    'INTVAL',
    'FLOATVAL',
    'STRVAL',
    'CHARVAL',
    'ID'
] + list(reserved.values())

def t_FLOATVAL(self,t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except:
        t.value = 0.0
    return t

def t_INTVAL(self,t):
    r'\d+'
    try:
        t.value = int(t.value)
    except:
        t.value = 0
    return t

def t_STRVAL(self,t):
    r'\"[^\"\\]*(\\.[^\"\\]*)*\"'
    #replace \\ with \
    str_ = t.value[1:-1]
    #str_ = str_.replace("\\n","\n")
    #str_ = str_.replace("\\r","\r")
    #str_ = str_.replace("\\t","\t")
    t.value = str_

def t_CHARVAL(self,t):
    r"'((\\.)|([^'\\]))'"
    t.value = t.value[1:-1]

def t_ID(self,t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')

def t_COMMENT(self,t):
    r'\#.*\n*?'
    t.lexer.lineno += 1

def t_MCOMMENT(self,t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

t_ignore = " \t"

def t_newline(self,t):
    r'\n+'
    t.lexer.lineno += len("\n")

def t_error(self,t):
    t.lexer.skip(1)

lexer = lex.lex()