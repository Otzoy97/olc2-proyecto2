"""
This grammar intends to emulate the grammar of the C programming language
So it was adapted from Appendix A, subsection 13 of the
The C programming language [PDF] (pp. 181-188) 2nd edition
by Kernighan, B. W., & Ritchie, D. M., Prentice-Hall (1988)
Retrieved from https://hikage.freeshell.org/books/theCprogrammingLanguage.pdf
"""

import ply.yacc as yacc
from analyzer.lexer import tokens, lexer
from analyzer.err import ErrType, addErr
from interpreter.dspecifier import DSpecifier
from interpreter.operator import Operator
from interpreter.expression.primary import Primary, PrimaryType
from interpreter.expression.postfix import Postfix
from interpreter.expression.binary import Binary
from interpreter.expression.unary import Unary
from interpreter.expression.conditional import Conditional
from interpreter.expression.assignment import Assignment
from interpreter.expression.jump import Jump
from interpreter.expression.struct import Struct
from interpreter.declaration import Declaration
from interpreter.environment.Program import Program
from interpreter.environment.For import For
from interpreter.environment.Do import Do
from interpreter.environment.While import While
from interpreter.environment.Function import Function
from interpreter.environment.If import If
from interpreter.environment.Switch import Switch, Label, Case
from interpreter.environment.While import While
from interpreter.expression.printf import Printf

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'ORBW'),
    ('left', 'XORBW'),
    ('left', 'ANDBW'),
    ('left', 'EQ', 'NEQ'),
    ('left', 'LS', 'LSE', 'GR', 'GRE'),
    ('left', 'SHL', 'SHR'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'QUOT', 'REM'),
    ('right', 'INC', 'DEC', 'NOT', 'NOTBW', 'UMINUS', 'UPLUS', 'POINT'),
    ('left', 'DOT')
)

def p_init_minorCList0(t):
    '''inst_minorCList  :   inst_minorC'''
    t[0] = Program()
    t[0].ist.append(t[1])

def p_init_minorCList1(t):
    '''inst_minorCList  :   inst_minorCList inst_minorC'''
    t[1].ist.append(t[2])
    t[0] = t[1]

def p_empty(t):
    '''empty            :   '''
    pass

def p_init_minorC0(t):
    '''inst_minorC      :   function_def'''
    pass

def p_init_minorC1(t):
    '''inst_minorC      :   declaration'''
    t[0] = Declaration(t[1], t.lexer.lexdata[0: t.lexer.lexpos].count("\n") + 1)

def p_function_def(t):
    '''function_def     :   dec_spec declarator compound_statement
                        |   declarator compound_statement
    '''
    pass

def p_declaration0(t):
    '''declaration      :   dec_spec init_dec_list SCOLON'''
    t[2].insert(0, t[1])
    t[0] = t[2]
    print(t[0])

def p_declaration1(t):
    '''declaration      :   dec_spec SCOLON'''
    t[0] = [t[1]]

def p_dec_spec(t):
    '''dec_spec         :   VOID 
                        |   INT
                        |   CHAR
                        |   DOUBLE
                        |   FLOAT
                        |   struct_spec'''
    if str(t[1]) == "void":
        t[0] = DSpecifier.VOID
    elif str(t[1]) == "int":
        t[0] = DSpecifier.INTEGER
    elif str(t[1]) == "char":
        t[0] = DSpecifier.CHARACTER
    elif str(t[1]) == "double":
        t[0] = DSpecifier.FLOATING
    elif str(t[1]) == "float":
        t[0] = DSpecifier.FLOATING
    else:
        print(f"{t[1].id}->{t[1].dec}")
        t[0] = t[1]

def p_struct_spec0(t):
    '''struct_spec      :   STRUCT ID LLVL struct_dec_list LLVR'''
    t[0] = Struct(t[2], t[4])

def p_struct_spec1(t):
    '''struct_spec      :   STRUCT ID'''
    t[0] = Struct(t[2], None)

def p_struct_dec_list0(t):
    '''struct_dec_list  :   struct_dec'''
    t[0] = t[1]

def p_struct_dec_list1(t):
    '''struct_dec_list  :   struct_dec_list struct_dec'''
    for i in t[2]:
        t[1].append(i)
    t[0] = t[1]

def p_init_dec_list0(t):
    '''init_dec_list    :   init_declarator'''
    t[0] = [t[1]]
    
def p_init_dec_list1(t):
    '''init_dec_list    :   init_dec_list COMMA init_declarator'''
    t[1].append(t[3])
    t[0] = t[1]

def p_init_declarator0(t):
    '''init_declarator  :   declarator'''
    t[0] = t[1]

def p_init_declarator1(t):
    '''init_declarator  :   declarator ASSIGN init'''
    t[1].append(t[3])
    t[0] = t[1]

def p_struct_dec(t):
    '''struct_dec       :    dec_spec struct_decr_list SCOLON'''
    t[0] = []
    for i in t[2]:
        t[0].append(i)
    print(t[0])

def p_struct_decr_list0(t):
    '''struct_decr_list :   declarator'''
    t[0] = [t[1][0]]

def p_struct_decr_list1(t):
    '''struct_decr_list :   struct_decr_list COMMA declarator'''
    t[1].append(t[3][0])
    t[0] = t[1]

def p_declarationLst(t):
    '''declarator       :   ID declaratorD'''
    t[0] = [t[1], t[2]]

def p_declarator0(t):
    '''declaratorD      :   PARL PARR'''
    t[0] = []

def p_declarator1(t):
    '''declaratorD      :   PARL par_list PARR'''
    t[0] = t[2]

def p_declarator2(t):
    '''declaratorD      :   dec_cor_list'''
    t[0] = t[1]

def p_declarator3(t):
    '''declaratorD      :   empty '''
    t[0] = None

def p_dec_cor_list0(t):
    '''dec_cor_list     :   dec_cor_list CORL constant CORR'''
    t[1].append(t[3])
    t[0] = t[1]

def p_dec_cor_list1(t):
    '''dec_cor_list     :   CORL constant CORR'''
    t[0] = [t[2]]

def p_par_list0(t):
    '''par_list         :   par_list COMMA par_dec'''
    t[1].append(t[3])
    t[0] = t[1]

def p_par_list1(t):
    '''par_list         :   par_dec'''
    t[0] = [t[1]]

def p_par_dec(t):
    '''par_dec          :   dec_spec declarator'''
    t[0] = (t[0], t[1])

def p_init0(t):
    '''init             :   assignmentExpression'''
    t[0] = t[1]

def p_init1(t):
    '''init             :   LLVL init_list LLVR'''
    t[0] = t[2]

def p_init_list0(t):
    '''init_list        :   init'''
    t[0] = [t[1]]

def p_init_list1(t):
    '''init_list        :   init_list COMMA init'''
    if isinstance(t[3], list):
        for i in t[3]:
            t[1].append(i)
    else:
        t[1].append(t[3])
    t[0] = t[1]

def p_statement0(t):
    '''statement        :   exp_statement
                        |   compound_statement
                        |   sel_statement
                        |   lop_statement
                        |   jmp_statement
                        |   declaration
                        |   switch_statement'''
    t[0] = t[1]

def p_statement1(t):
    '''statement        :   PRINTF PARL expression PARR'''
    t[0] = Printf(t[3])

def p_switch_statement(t):
    '''switch_statement :   CASE constantExpression COLON statement
                        |   DEFAULT COLON statement
                        |   ID COLON statement
    '''
    if t[1] == "case":
        t[0] = Case(t[2], t[4])
    elif t[1] == "default":
        t[0] = Case(None, t[4])
    else:
        t[0] = Label(t[1], t[3])

def p_exp_statement0(t):
    '''exp_statement    :   assignmentExpression SCOLON'''
    t[0] = t[1]

def p_exp_statement1(t):
    '''exp_statement    :   SCOLON'''
    t[0] = []

def p_compound_statement0(t):
    '''compound_statement :  LLVL statement_list LLVR
    '''
    t[0] = t[2]

def p_compound_statement1(t):
    '''compound_statement :  LLVL LLVR
    '''
    t[0] = []

def p_statement_list0(t):
    '''statement_list   :   statement'''
    if isinstance(t[1], list):
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_statement_list1(t):
    '''statement_list   :   statement_list statement'''
    if isinstance(t[2], list):
        for i in t[2]:
            t[1].append(i)
    else:
        t[1].append(t[2])
    t[0] = t[1]

def p_sel_statement(t):
    '''sel_statement    :   IF PARL assignmentExpression PARR statement else_statement
                        |   SWITCH PARL assignmentExpression PARR statement
    '''
    if t[1] == 'if':
        t[0] = If(t[3],t[5],t[6])
    elif t[1] == 'switch':
        t[0] = Switch(t[3],t[5])

def p_else_statement0(t):
    '''else_statement   :   ELSE statement'''
    t[0] = t[2]

def p_else_statement1(t):
    '''else_statement   :   empty
    '''
    t[0] = None

def p_lop_statement(t):
    '''lop_statement    :   WHILE PARL assignmentExpression PARR statement
                        |   DO statement WHILE PARL assignmentExpression PARR SCOLON
                        |   FOR PARL for_dec_exp SCOLON assignmentExpression SCOLON assignmentExpression PARR statement
    '''
    if t[1] == "while":
        t[0] = While(t[3], t[5])
    elif t[1] == "do":
        t[0] = Do(t[5],t[2])
    elif t[1] == "for":
        t[0] = For(t[3], t[5], t[7], t[8])

def p_for_dec_exp0(t):
    '''for_dec_exp      :   assignmentExpression'''
    t[0] = t[1]

def p_for_dec_exp1(t):
    '''for_dec_exp      :   dec_spec init_dec_list'''
    t[2].insert(0, t[1])
    t[0] = Declaration(t[2], t.lexer.lexdata[0: t.lexer.lexpos].count("\n") + 1)

def p_jmp_statement(t):
    '''jmp_statement    :   CONTINUE SCOLON
                        |   BREAK SCOLON
                        |   RETURN assignmentExpression SCOLON
                        |   RETURN SCOLON
                        |   GOTO ID SCOLON
    '''
    if t[1] == "continue":
        t[0] = Jump(Operator.CONTINUE_, None)
    elif t[1] == "break":
        t[0] = Jump(Operator.BREAK_, None)
    elif t[1] == "return":
        t[0] = Jump(Operator.RETURN_, None if t[2] == ";" else t[2])
    elif t[1] == "goto":
        t[0] = Jump(Operator.GOTO, t[2])

def p_expression0(t):
    '''expression       :   assignmentExpression'''
    t[0] = [t[1]]

def p_expression1(t):
    '''expression       :   expression COMMA assignmentExpression'''
    t[1].append(t[3])
    t[0] = t[1]

def p_assignmentExpression0(t):
    '''assignmentExpression :   conditionalExpression'''
    t[0] = t[1]

def p_assignmentExpression1(t):
    '''assignmentExpression : unaryExpression assignmentOperator conditionalExpression'''
    t[0] = Assignment(t[1], t[2], t[3], t.lexer.lexdata[0: t.lexer.lexpos].count("\n") + 1)

def p_assignmentOperator(t):
    '''assignmentOperator :   ASSIGN
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
    if t[1] == '=':
        t[0] = Operator.ASSIGN
    elif t[1] == '*=':
        t[0] = Operator.TIMESA
    elif t[1] == '/=':
        t[0] = Operator.QUOTA
    elif t[1] == '%=':
        t[0] = Operator.REMA
    elif t[1] == '+=':
        t[0] = Operator.PLUSA
    elif t[1] == '-=':
        t[0] = Operator.MINUSA
    elif t[1] == '>>=':
        t[0] = Operator.SHRA
    elif t[1] == '<<=':
        t[0] = Operator.SHLA
    elif t[1] == '&=':
        t[0] = Operator.ANDBWA
    elif t[1] == '^=':
        t[0] = Operator.XORBWA
    elif t[1] == '|=':
        t[0] = Operator.ORBWA

def p_constantExpression(t):
    '''constantExpression :  conditionalExpression '''
    t[0] = t[1]

def p_conditionalExpression0(t):
    '''conditionalExpression : binaryExpressions'''
    t[0] = t[1]

def p_conditionalExpression1(t):
    '''conditionalExpression : binaryExpressions QUESR conditionalExpression COLON conditionalExpression'''
    t[0] = Conditional(t[1], t[3], t[5], t.lexer.lexdata[0: t.lexer.lexpos].count("\n") + 1)

def p_binaryExpression0(t):
    '''binaryExpressions    :   binaryExpressions OR binaryExpressions
                            |   binaryExpressions AND binaryExpressions
                            |   binaryExpressions ORBW binaryExpressions
                            |   binaryExpressions XORBW binaryExpressions
                            |   binaryExpressions ANDBW binaryExpressions
                            |   binaryExpressions EQ binaryExpressions
                            |   binaryExpressions NEQ binaryExpressions
                            |   binaryExpressions LS binaryExpressions
                            |   binaryExpressions GR binaryExpressions
                            |   binaryExpressions LSE binaryExpressions
                            |   binaryExpressions GRE binaryExpressions
                            |   binaryExpressions SHL binaryExpressions
                            |   binaryExpressions SHR binaryExpressions
                            |   binaryExpressions PLUS binaryExpressions
                            |   binaryExpressions MINUS binaryExpressions
                            |   binaryExpressions TIMES binaryExpressions 
                            |   binaryExpressions QUOT binaryExpressions
                            |   binaryExpressions REM binaryExpressions'''
    if t[2] == "||":
        t[0] = Binary(t[1], Operator.OR, t[3])
    elif t[2] == "&&":
        t[0] = Binary(t[1], Operator.AND, t[3])
    elif t[2] == "|":
        t[0] = Binary(t[1], Operator.ORBW, t[3])
    elif t[2] == "^":
        t[0] = Binary(t[1], Operator.XORBW, t[3])
    elif t[2] == "&":
        t[0] = Binary(t[1], Operator.ANDBW, t[3])
    elif t[2] == "==":
        t[0] = Binary(t[1], Operator.EQ, t[3])
    elif t[2] == "!=":
        t[0] = Binary(t[1], Operator.NEQ, t[3])
    elif t[2] == "<":
        t[0] = Binary(t[1], Operator.LS, t[3])
    elif t[2] == ">":
        t[0] = Binary(t[1], Operator.GR, t[3])
    elif t[2] == "<=":
        t[0] = Binary(t[1], Operator.LSE, t[3])
    elif t[2] == ">=":
        t[0] = Binary(t[1], Operator.GRE, t[3])
    elif t[2] == "<<":
        t[0] = Binary(t[1], Operator.SHL, t[3])
    elif t[2] == ">>":
        t[0] = Binary(t[1], Operator.SHR, t[3])
    elif t[2] == "+":
        t[0] = Binary(t[1], Operator.PLUS, t[3])
    elif t[2] == "-":
        t[0] = Binary(t[1], Operator.MINUS, t[3])
    elif t[2] == "*":
        t[0] = Binary(t[1], Operator.TIMES, t[3])
    elif t[2] == "/":
        t[0] = Binary(t[1], Operator.QUOTIENT, t[3])
    elif t[2] == "%":
        t[0] = Binary(t[1], Operator.REMAINDER, t[3])

def p_binaryExpression18(t):
    '''binaryExpressions   :   unaryExpression'''
    t[0] = t[1]

def p_unaryExpression0(t):
    '''unaryExpression    :   PARL dec_spec PARR postfixExpression'''
    if t[2] == DSpecifier.INTEGER:
        t[0] = Unary(t[4], Operator.CASTINT)
    elif t[2] == DSpecifier.FLOATING:
        t[0] = Unary(t[4], Operator.CASTFLOAT)
    elif t[2] == DSpecifier.CHARACTER:
        t[0] = Unary(t[4], Operator.CASTCHAR)

def p_unaryExpression1(t):
    '''unaryExpression  :   INC postfixExpression
                        |   DEC postfixExpression
                        |   ANDBW postfixExpression %prec POINT
                        |   PLUS postfixExpression %prec UPLUS
                        |   MINUS postfixExpression %prec UMINUS
                        |   NOTBW postfixExpression
                        |   NOT postfixExpression'''
    if t[1] == '++':
        t[0] = Unary(t[2], Operator.INCREMENT)
    elif t[1] == '--':
        t[0] = Unary(t[2], Operator.DECREMENT)
    elif t[1] == '&':
        t[0] = Unary(t[2], Operator.AMPERSAND)
    elif t[1] == '+':
        t[0] = Unary(t[2], Operator.PLUS)
    elif t[1] == '-':
        t[0] = Unary(t[2], Operator.MINUS)
    elif t[1] == '~':
        t[0] = Unary(t[2], Operator.NOTBW)
    elif t[1] == '!':
        t[0] = Unary(t[2], Operator.NOT)

def p_unaryExpression2(t):
    '''unaryExpression    :   postfixExpression'''
    t[0] =  t[1]

def p_postExpression0(t):
    '''postfixExpression :  primaryExpression'''
    t[0] = t[1]

def p_postExpression1(t):
    '''postfixExpression :  postfixExpression CORL assignmentExpression CORR'''
    t[0] = Postfix(t[1], Operator.ARRAYACCESS, t[3])
    
def p_postExpression2(t):
    '''postfixExpression :  postfixExpression PARL PARR'''
    t[0] = Postfix(t[1], Operator.CALL, None)

def p_postExpression3(t):
    '''postfixExpression :  postfixExpression PARL assignmentExpressionList PARR'''
    t[0] = Postfix(t[1], Operator.CALL, t[3])

def p_postExpression4(t):
    '''postfixExpression :  postfixExpression DOT ID'''
    t[0] = Postfix(t[1], Operator.STRUCTACCESS, t[3])

def p_postExpression5(t):
    '''postfixExpression :  postfixExpression INC'''
    t[0] = Postfix(t[1], Operator.INCREMENT, None)

def p_postExpression6(t):
    '''postfixExpression :  postfixExpression DEC'''
    t[0] = Postfix(t[1], Operator.DECREMENT, None)

def p_fExpression0(t):
    '''primaryExpression :  constant'''
    #rise value
    t[0] = t[1]

def p_fExpression1(t):
    '''primaryExpression :  PARL conditionalExpression PARR'''
    #rise value
    t[0] = t[2]

def p_fExpression2(t):
    '''primaryExpression :   ID'''
    t[0] = Primary(t[1], PrimaryType.IDENTIFIER, t.lexer.lexdata[0: t.lexer.lexpos].count("\n") + 1)

def p_fExpression3(t):
    '''primaryExpression :   STRVAL'''
    t[0] = Primary(t[1], PrimaryType.CONSTANT, t.lexer.lexdata[0: t.lexer.lexpos].count("\n") + 1)

def p_fExpression4(t):
    '''primaryExpression :  SCANF PARL PARR'''
    #rise value
    t[0] = Primary(f"read()", PrimaryType.CONSTANT, t.lexer.lexdata[0: t.lexer.lexpos].count("\n") + 1)

def p_assignmentExpressionList0(t):
    '''assignmentExpressionList : assignmentExpression'''
    t[0] = [t[1]]

def p_assignmentExpressionList1(t):
    '''assignmentExpressionList :  assignmentExpressionList COMMA assignmentExpression'''
    t[1].append(t[3])
    t[0] = t[1]

def p_primExp0(t):
    '''constant         :   INTVAL
                        |   FLOATVAL
                        |   CHARVAL'''
    t[0] = Primary(t[1], PrimaryType.CONSTANT, t.lexer.lexdata[0: t.lexer.lexpos].count("\n") + 1)

def p_primExp1(t):
    '''constant         :   TRUE
                        |   FALSE'''
    t[0] = Primary(0 if t[1] == 'false' else 1, PrimaryType.CONSTANT, t.lexer.lexdata[0: t.lexer.lexpos].count("\n") + 1)

def p_error(t):
    if t:
        tmp = str(t.value)
        if t.value == '>':
            tmp = "greater-than symbol"
        elif t.value == '<':
            tmp = "less-than symbol"
        addErr(ErrType.SINTACTIC, "Can't reduce '" + tmp + "'", t.lexer.lexdata[0: t.lexer.lexpos].count("\n") + 1)
        parser.errok()
    else:
        addErr(ErrType.SINTACTIC, "Unexpected EOF", "")

parser = yacc.yacc()

def parse(input):
    lexer.lineno = 1
    return parser.parse(input)
