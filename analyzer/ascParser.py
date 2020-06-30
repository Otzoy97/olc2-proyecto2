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
from interpreter.expression.unary import Unary
from interpreter.expression.cast import Cast
from interpreter.expression.multiplicative import Multiplicative
from interpreter.expression.additive import Additive
from interpreter.expression.shift import Shift
from interpreter.expression.relational import Relational
from interpreter.expression.equality import Equality
from interpreter.expression.andbw import AndBitWise
from interpreter.expression.orbw import OrBitWise
from interpreter.expression.xorbw import XorBitWise
from interpreter.expression.andlog import AndLogical
from interpreter.expression.orlog import OrLogical
from interpreter.expression.conditional import Conditional
from interpreter.expression.assignment import Assignment
from interpreter.expression.jump import Jump
from interpreter.expression.struct import Struct
from interpreter.declaration import Declaration

def p_init_minorCList0(t):
    '''inst_minorCList  :   inst_minorC'''
    t[0] = [t[1]]

def p_init_minorCList1(t):
    '''inst_minorCList  :   inst_minorCList inst_minorC'''
    t[1].append(t[2])
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
    t[0] = t[1].append(t[3])
    print(t[3])

def p_struct_dec(t):
    '''struct_dec       :    dec_spec struct_decr_list SCOLON'''
    for i in t[2]:
        i.insert(0,t[1])
    t[0] =  t[2]

def p_struct_decr_list0(t):
    '''struct_decr_list :   declarator'''
    t[0] = [t[1]]

def p_struct_decr_list1(t):
    '''struct_decr_list :   struct_decr_list COMMA declarator'''
    t[1].append(t[3])
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
    '''dec_cor_list     :   dec_cor_list CORL constantExpression CORR'''
    t[1].append(t[3])
    t[0] = t[1]

def p_dec_cor_list1(t):
    '''dec_cor_list     :   CORL constantExpression CORR'''
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

def p_statement(t):
    '''statement        :   exp_statement
                        |   compound_statement
                        |   sel_statement
                        |   lop_statement
                        |   jmp_statement
                        |   declaration
                        |   switch_statement
    '''
    pass

def p_switch_statement(t):
    '''switch_statement :   CASE constantExpression COLON statement
                        |   DEFAULT COLON statement
    '''
    pass

def p_exp_statement0(t):
    '''exp_statement    :   expression SCOLON'''
    pass

def p_exp_statement1(t):
    '''exp_statement    :   SCOLON'''
    pass

def p_compound_statement(t):
    '''compound_statement :  LLVL statement_list LLVR
                        |   LLVL LLVR
    '''
    pass

def p_statement_list(t):
    '''statement_list   :   statement
                        |   statement_list statement
    '''
    pass

def p_sel_statement(t):
    '''sel_statement    :   IF PARL expression PARR statement else_statement
                        |   SWITCH PARL expression PARR statement
    '''
    pass

def p_else_statement(t):
    '''else_statement   :   ELSE statement
                        |   empty
    '''
    pass

def p_lop_statement(t):
    '''lop_statement    :   WHILE PARL expression PARR statement
                        |   DO statement WHILE PARL expression PARR SCOLON
                        |   FOR PARL for_dec_exp SCOLON expression SCOLON expression PARR statement
    '''
    pass

def p_for_dec_exp(t):
    '''for_dec_exp      :   expression
                        |   dec_spec expression
    '''
    pass


def p_jmp_statement(t):
    '''jmp_statement    :   CONTINUE SCOLON
                        |   BREAK SCOLON
                        |   RETURN expression SCOLON
                        |   RETURN SCOLON
    '''
    pass

def p_expression0(t):
    '''expression       :   assignmentExpression'''
    t[0] = [t[1]]

def p_expression1(t):
    '''expression       :   expression COMMA assignmentExpression'''
    t[1].append(t[3])
    t[0] = t[1]

def p_assignmentExpression0(t):
    '''assignmentExpression :   conditionalExpression'''
    t[0] = Assignment(None, None, t[1], t.lexer.lexdata[0: t.lexer.lexpos].count("\n") + 1)

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

#FIXME: ver si el orden de estas cosas es el correcto
def p_constantExpression(t):
    '''constantExpression :  conditionalExpression '''
    t[0] = t[1]

def p_conditionalExpression0(t):
    '''conditionalExpression : orExpression'''
    t[0] = Conditional(t[1], None, None, t.lexer.lexdata[0: t.lexer.lexpos].count("\n") + 1)

def p_conditionalExpression1(t):
    '''conditionalExpression : orExpression QUESR expression COLON conditionalExpression'''
    t[0] = Conditional(t[1], t[3], t[5], t.lexer.lexdata[0: t.lexer.lexpos].count("\n") + 1)

def p_orExpression0(t):
    '''orExpression     :   andExpression'''
    t[0] = OrLogical(t[1], [], t.lexer.lexdata[0: t.lexer.lexpos].count("\n") + 1)

def p_orExpression1(t):
    '''orExpression     :   orExpression OR andExpression'''
    t[1].acc.append((Operator.OR, t[3]))
    t[0] = t[1]

def p_andExpression0(t):
    '''andExpression    :   orBwExpression'''
    t[0] = AndLogical(t[1], [], t.lexer.lexdata[0: t.lexer.lexpos].count("\n") + 1)

def p_andExpression1(t):
    '''andExpression    :   andExpression AND orBwExpression'''
    t[1].acc.append((Operator.AND, t[3]))
    t[0] = t[1]

def p_orBwExpression0(t):
    '''orBwExpression   :   xorBwExpression'''
    t[0] = OrBitWise(t[1], [], t.lexer.lexdata[0: t.lexer.lexpos].count("\n") + 1)

def p_orBwExpression1(t):
    '''orBwExpression   :   orBwExpression ORBW xorBwExpression'''
    t[1].acc.append((Operator.ORBW, t[3]))
    t[0] = t[1]

def p_xorBwExpression0(t):
    '''xorBwExpression  :   andBwExpression'''
    t[0] = XorBitWise(t[1], [], t.lexer.lexdata[0: t.lexer.lexpos].count("\n") + 1)

def p_xorBwExpression1(t):
    '''xorBwExpression  :   xorBwExpression XORBW andBwExpression'''
    t[1].acc.append((Operator.XORBW, t[3]))
    t[0] = t[1]

def p_andBwExpression0(t):
    '''andBwExpression  :   equalExpression'''
    t[0] = AndBitWise(t[1], [], t.lexer.lexdata[0: t.lexer.lexpos].count("\n") + 1)

def p_andBwExpression1(t):
    '''andBwExpression  :   andBwExpression ANDBW equalExpression'''
    t[1].acc.append((Operator.ANDBW, t[3]))
    t[0] = t[1]

def p_equalExpression0(t):
    '''equalExpression  :   relaExpression'''
    t[0] = Equality(t[1], [], t.lexer.lexdata[0: t.lexer.lexpos].count("\n") + 1)

def p_equalExpression1(t):
    '''equalExpression  :   equalExpression EQ relaExpression'''
    t[1].acc.append((Operator.EQ, t[3]))
    t[0] = t[1]
    
def p_equalExpression2(t):
    '''equalExpression  :   equalExpression NEQ relaExpression'''
    t[1].acc.append((Operator.NEQ, t[3]))
    t[0] = t[1]

def p_relaExpression0(t):
    '''relaExpression   :   shiftExpression'''
    t[0] = Relational(t[1], [], t.lexer.lexdata[0: t.lexer.lexpos].count("\n") + 1)

def p_relaExpression1(t):
    '''relaExpression   :   relaExpression LS shiftExpression'''
    t[1].acc.append((Operator.LS, t[3]))
    t[0] = t[1]

def p_relaExpression2(t):
    '''relaExpression   :   relaExpression GR shiftExpression'''
    t[1].acc.append((Operator.GR, t[3]))
    t[0] = t[1]

def p_relaExpression3(t):
    '''relaExpression   :   relaExpression LSE shiftExpression'''
    t[1].acc.append((Operator.LSE, t[3]))
    t[0] = t[1]

def p_relaExpression4(t):
    '''relaExpression   :   relaExpression GRE shiftExpression'''
    t[1].acc.append((Operator.GRE, t[3]))
    t[0] = t[1]

def p_shiftExpression0(t):
    '''shiftExpression  :   addExpression'''
    t[0] = Shift(t[1], [], t.lexer.lexdata[0: t.lexer.lexpos].count("\n") + 1)

def p_shiftExpression1(t):
    '''shiftExpression  :   shiftExpression SHL addExpression'''
    t[1].acc.append((Operator.SHL, t[3]))
    t[0] = t[1]

def p_shiftExpression2(t):
    '''shiftExpression  :   shiftExpression SHR addExpression'''
    t[1].acc.append((Operator.SHR, t[3]))
    t[0] = t[1]

def p_addExpression0(t):
    '''addExpression    :   multiExpression'''
    t[0] = Additive(t[1], [], t.lexer.lexdata[0: t.lexer.lexpos].count("\n") + 1)

def p_addExpression1(t):
    '''addExpression    :   addExpression PLUS multiExpression'''
    t[1].acc.append((Operator.PLUS, t[3]))
    t[0] = t[1]

def p_addExpression2(t):
    '''addExpression    :   addExpression MINUS multiExpression'''
    t[1].acc.append((Operator.MINUS, t[3]))
    t[0] = t[1]

def p_multiExpression0(t):
    '''multiExpression  :   castExpression'''
    t[0] = Multiplicative(t[1], [], t.lexer.lexdata[0: t.lexer.lexpos].count("\n") + 1)

def p_multiExpression1(t):
    '''multiExpression  :   multiExpression TIMES castExpression'''
    t[1].acc.append((Operator.TIMES, t[3]))
    t[0] = t[1]

def p_multiExpression2(t):
    '''multiExpression  :   multiExpression QUOT castExpression'''
    t[1].acc.append((Operator.QUOTIENT, t[3]))
    t[0] = t[1]

def p_multiExpression3(t):
    '''multiExpression  :   multiExpression REM castExpression'''
    t[1].acc.append((Operator.REMAINDER, t[3]))
    t[0] = t[1]

def p_castExpression0(t):
    '''castExpression   :   unaryExpression'''
    t[0] = Cast(t[1], [], t.lexer.lexdata[0: t.lexer.lexpos].count("\n") + 1)

def p_castExpression1(t):
    '''castExpression   :   PARL dec_spec PARR castExpression'''
    t[4].acc.append((t[2], None))
    t[0] = t[4]
    
def p_unaryExpression0(t):
    '''unaryExpression  :   postfixExpression'''
    t[0] = Unary(t[1], [], t.lexer.lexdata[0: t.lexer.lexpos].count("\n") + 1)
    
def p_unaryExpression1(t):
    '''unaryExpression  :   INC unaryExpression'''
    t[2].acc.append((Operator.INCREMENT, None))
    t[0] = t[2]

def p_unaryExpression2(t):
    '''unaryExpression  :   DEC unaryExpression'''
    t[2].acc.append((Operator.DECREMENT, None))
    t[0] = t[2]

def p_unaryExpression3(t):
    '''unaryExpression  :   unaryOperator castExpression'''
    t[2].acc.append((t[1], None))
    t[0] = t[2]
    
def p_unaryExpression4(t):
    '''unaryExpression  :   SIZEOF unaryExpression'''
    t[2].acc.append((Operator.SIZEOF, None))
    t[0] = t[2]

def p_unaryExpression5(t):
    '''unaryExpression  :   SIZEOF PARL dec_spec PARR'''
    t[2].acc.append((Operator.SIZEOF, None))
    t[0] = t[2]

def p_postExpression0(t):
    '''postfixExpression :  primaryExpression'''
    t[0] = Postfix(t[1], [], t.lexer.lexdata[0: t.lexer.lexpos].count("\n") + 1)

def p_postExpression1(t):
    '''postfixExpression :  postfixExpression CORL expression CORR'''
    t[1].acc.append((Operator.ARRAYACCESS, t[3]))
    t[0] = t[1]
    
def p_postExpression2(t):
    '''postfixExpression :  postfixExpression PARL PARR'''
    t[1].acc.append((Operator.CALL, None))
    t[0] = t[1]

def p_postExpression3(t):
    '''postfixExpression :  postfixExpression PARL assignmentExpressionList PARR'''
    t[1].acc.append((Operator.CALL, t[3]))
    t[0] = t[1]

def p_postExpression4(t):
    '''postfixExpression :  postfixExpression DOT ID'''
    t[1].acc.append((Operator.STRUCTACCESS, t[3]))
    t[0] = t[1]

def p_postExpression5(t):
    '''postfixExpression :  postfixExpression INC'''
    t[1].acc.append((Operator.INCREMENT))
    t[0] = t[1]

def p_postExpression6(t):
    '''postfixExpression :  postfixExpression DEC'''
    t[1].acc.append((Operator.DECREMENT))
    t[0] = t[1]

def p_fExpression0(t):
    '''primaryExpression :  constant'''
    #rise value
    t[0] = t[1]

def p_fExpression1(t):
    '''primaryExpression :  PARL expression PARR'''
    #rise value
    t[0] = t[2]

def p_fExpression2(t):
    '''primaryExpression :   ID'''
    t[0] = Primary(t[1], PrimaryType.IDENTIFIER, t.lexer.lexdata[0: t.lexer.lexpos].count("\n") + 1)

def p_fExpression3(t):
    '''primaryExpression :   STRVAL'''
    t[0] = Primary(t[1], PrimaryType.CONSTANT, t.lexer.lexdata[0: t.lexer.lexpos].count("\n") + 1)


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

def p_unaryOperator(t):
    '''unaryOperator    :   ANDBW
                        |   PLUS
                        |   MINUS
                        |   NOTBW
                        |   NOT'''
    if (t[1] == '&'):
        t[0] == Operator.AMPERSAND
    elif (t[1] == '+'):
        t[0] == Operator.UPLUS
    elif (t[1] == '-'):
        t[0] == Operator.UMINUS
    elif (t[1] == '~'):
        t[0] == Operator.NOTBW
    elif (t[1] == '!'):
        t[0] == Operator.NOT

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
