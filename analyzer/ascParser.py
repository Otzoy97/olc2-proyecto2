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

def p_init_minorCList(t):
    '''inst_minorCList  :   inst_minorC
                        |   inst_minorCList inst_minorC
    '''
    pass

def p_empty(t):
    '''empty            :   
    '''
    pass

def p_init_minorC(t):
    '''inst_minorC      :   function_def
                        |   declaration
    '''
    pass

def p_function_def(t):
    '''function_def     :   dec_spec declarator compound_statement
                        |   declarator compound_statement
    '''
    pass

def p_declaration(t):
    '''declaration      :   dec_spec init_dec_list SCOLON
                        |   dec_spec SCOLON
    '''
    pass

def p_dec_spec(t):
    '''dec_spec         :   VOID 
                        |   INT
                        |   CHAR
                        |   DOUBLE
                        |   FLOAT
                        |   struct_spec
    '''
    pass

def p_struct_spec(t):
    '''struct_spec      :   STRUCT ID LLVL struct_dec_list LLVR
                        |   STRUCT ID
    '''
    pass

def p_struct_dec_list(t):
    '''struct_dec_list  :   struct_dec
                        |   struct_dec_list struct_dec
    '''
    pass

def p_init_dec_list(t):
    '''init_dec_list    :   init_declarator
                        |   init_dec_list COMMA init_declarator
    '''
    pass

def p_init_declarator(t):
    '''init_declarator  :   declarator
                        |   declarator ASSIGN init
    '''
    pass

def p_struct_dec(t):
    '''struct_dec       :    dec_spec struct_decr_list SCOLON
    '''
    pass

def p_struct_decr_list(t):
    '''struct_decr_list :   declarator
                        |   struct_decr_list COMMA declarator
    '''
    pass

def p_declarationLst(t):
    '''declarator       :   ID declaratorD'''
    pass

def p_declarator(t):
    '''declaratorD      :   PARL PARR
                        |   PARL par_list PARR
                        |   dec_cor_list
                        |   empty 
    '''
    pass

def p_dec_cor_list(t):
    '''dec_cor_list     :   dec_cor_list CORL dec_cor_list_in CORR
                        |   CORL dec_cor_list_in CORR
    '''
    pass

def p_dec_cor_list_in(t):
    '''dec_cor_list_in  :   constantExpression
                        |   empty
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

def p_init(t):
    '''init             :   assignmentExpression
                        |   LLVL init_list LLVR
    '''
    pass

def p_init_list(t):
    '''init_list        :   init
                        |   init_list COMMA init
    '''
    pass

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

def p_exp_statement(t):
    '''exp_statement    :   expression SCOLON
                        |   SCOLON
    '''
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

def p_expression(t):
    '''expression       :   assignmentExpression'''
    t[0] = [t[1]]

def p_expression(t):
    '''expression       :   expression COMMA assignmentExpression'''
    t[1].append(t[3])
    t[0] = t[1]

def p_assignmentExpression(t):
    '''assignmentExpression :   conditionalExpression'''
    t[0] = Assignment(t[1], None, None, t.lexer.lexdata[0: t.lexpos].count("\n") + 1)

def p_assignmentExpression(t):
    '''assignmentExpression : unaryExpression assignmentOperator conditionalExpression'''
    t[0] = Assignment(t[1], t[2], t[3], t.lexer.lexdata[0: t.lexpos].count("\n") + 1)

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

def p_conditionalExpression(t):
    '''conditionalExpression : orExpression'''
    t[0] = Conditional(t[1], None, None, t.lexer.lexdata[0: t.lexpos].count("\n") + 1)

def p_conditionalExpression(t):
    '''conditionalExpression : orExpression QUESR expression COLON conditionalExpression'''
    t[0] = Conditional(t[1], t[3], t[5], t.lexer.lexdata[0: t.lexpos].count("\n") + 1)

def p_orExpression(t):
    '''orExpression     :   andExpression'''
    t[0] = OrLogical(t[1], [], t.lexer.lexdata[0: t.lexpos].count("\n") + 1)

def p_orExpression(t):
    '''orExpression     :   orExpression OR andExpression'''
    t[1].acc.append(tuple(Operator.OR, t[3]))
    t[0] = t[1]

def p_andExpression(t):
    '''andExpression    :   orBwExpression'''
    t[0] = AndLogical(t[1], [], t.lexer.lexdata[0: t.lexpos].count("\n") + 1)

def p_andExpression(t):
    '''andExpression    :   andExpression AND orBwExpression'''
    t[1].acc.append(tuple(Operator.AND, t[3]))
    t[0] = t[1]

def p_orBwExpression(t):
    '''orBwExpression   :   xorBwExpression'''
    t[0] = OrBitWise(t[1], [], t.lexer.lexdata[0: t.lexpos].count("\n") + 1)

def p_orBwExpression(t):
    '''orBwExpression   :   orBwExpression ORBW xorBwExpression'''
    t[1].acc.append(tuple(Operator.ORBW, t[3]))
    t[0] = t[1]

def p_xorBwExpression(t):
    '''xorBwExpression  :   andBwExpression'''
    t[0] = XorBitWise(t[1], [], t.lexer.lexdata[0: t.lexpos].count("\n") + 1)

def p_xorBwExpression(t):
    '''xorBwExpression  :   xorBwExpression XORBW andBwExpression'''
    t[1].acc.append(tuple(Operator.XORBW, t[3]))
    t[0] = t[1]

def p_andBwExpression(t):
    '''andBwExpression  :   equalExpression'''
    t[0] = AndBitWise(t[1], [], t.lexer.lexdata[0: t.lexpos].count("\n") + 1)

def p_andBwExpression(t):
    '''andBwExpression  :   andBwExpression ANDBW equalExpression'''
    t[1].acc.append(tuple(Operator.ANDBW, t[3]))
    t[0] = t[1]

def p_equalExpression(t):
    '''equalExpression  :   relaExpression'''
    t[0] = Equality(t[1], [], t.lexer.lexdata[0: t.lexpos].count("\n") + 1)

def p_equalExpression(t):
    '''equalExpression  :   equalExpression EQ relaExpression'''
    t[1].acc.append(tuple(Operator.EQ, t[3]))
    t[0] = t[1]
    
def p_equalExpression(t):
    '''equalExpression  :   equalExpression NEQ relaExpression'''
    t[1].acc.append(tuple(Operator.NEQ, t[3]))
    t[0] = t[1]

def p_relaExpression(t):
    '''relaExpression   :   shiftExpression'''
    t[0] = Relational(t[1], [], t.lexer.lexdata[0: t.lexpos].count("\n") + 1)

def p_relaExpression(t):
    '''relaExpression   :   relaExpression LS shiftExpression'''
    t[1].acc.append(tuple(Operator.LS, t[3]))
    t[0] = t[1]

def p_relaExpression(t):
    '''relaExpression   :   relaExpression GR shiftExpression'''
    t[1].acc.append(tuple(Operator.GR, t[3]))
    t[0] = t[1]

def p_relaExpression(t):
    '''relaExpression   :   relaExpression LSE shiftExpression'''
    t[1].acc.append(tuple(Operator.LSE, t[3]))
    t[0] = t[1]

def p_relaExpression(t):
    '''relaExpression   :   relaExpression GRE shiftExpression'''
    t[1].acc.append(tuple(Operator.GRE, t[3]))
    t[0] = t[1]

def p_shiftExpression(t):
    '''shiftExpression  :   addExpression'''
    t[0] = Shift(t[1], [], t.lexer.lexdata[0: t.lexpos].count("\n") + 1)

def p_shiftExpression(t):
    '''shiftExpression  :   shiftExpression SHL addExpression'''
    t[1].acc.append(tuple(Operator.SHL, t[3]))
    t[0] = t[1]

def p_shiftExpression(t):
    '''shiftExpression  :   shiftExpression SHR addExpression'''
    t[1].acc.append(tuple(Operator.SHR, t[3]))
    t[0] = t[1]

def p_addExpression(t):
    '''addExpression    :   multiExpression'''
    t[0] = Additive(t[1], [], t.lexer.lexdata[0: t.lexpos].count("\n") + 1)

def p_addExpression(t):
    '''addExpression    :   addExpression PLUS multiExpression'''
    t[1].acc.append(tuple(Operator.PLUS, t[3]))
    t[0] = t[1]

def p_addExpression(t):
    '''addExpression    :   addExpression MINUS multiExpression'''
    t[1].acc.append(tuple(Operator.MINUS, t[3]))
    t[0] = t[1]

def p_multiExpression(t):
    '''multiExpression  :   castExpression'''
    t[0] = Multiplicative(t[1], [], t.lexer.lexdata[0: t.lexpos].count("\n") + 1)

def p_multiExpression(t):
    '''multiExpression  :   multiExpression TIMES castExpression'''
    t[1].acc.append(tuple(Operator.TIMES, t[3]))
    t[0] = t[1]

def p_multiExpression(t):
    '''multiExpression  :   multiExpression QUOT castExpression'''
    t[1].acc.append(tuple(Operator.QUOTIENT, t[3]))
    t[0] = t[1]

def p_multiExpression(t):
    '''multiExpression  :   multiExpression REM castExpression'''
    t[1].acc.append(tuple(Operator.REMAINDER, t[3]))
    t[0] = t[1]

def p_castExpression0(t):
    '''castExpression   :   unaryExpression'''
    t[0] = Cast(t[1], [], t.lexer.lexdata[0: t.lexpos].count("\n") + 1)

def p_castExpression1(t):
    '''castExpression   :   PARL dec_spec PARR castExpression'''
    t[4].acc.append(tuple(t[2], None))
    t[0] = t[4]
    
def p_unaryExpression0(t):
    '''unaryExpression  :   postfixExpression'''
    t[0] = Unary(t[1], [], t.lexer.lexdata[0: t.lexpos].count("\n") + 1)
    
def p_unaryExpression1(t):
    '''unaryExpression  :   INC unaryExpression'''
    t[2].acc.append(tuple(Operator.INCREMENT, None))
    t[0] = t2

def p_unaryExpression2(t):
    '''unaryExpression  :   DEC unaryExpression'''
    t[2].acc.append(tuple(Operator.DECREMENT, None))
    t[0] = t[2]

def p_unaryExpression3(t):
    '''unaryExpression  :   unaryOperator castExpression'''
    t[2].acc.append(tuple(t[1], None))
    t[0] = t[2]
    
def p_unaryExpression4(t):
    '''unaryExpression  :   SIZEOF unaryExpression'''
    t[2].acc.append(tuple(Operator.SIZEOF, None))
    t[0] = t[2]

def p_unaryExpression5(t):
    '''unaryExpression  :   SIZEOF PARL dec_spec PARR'''
    t[2].acc.append(tuple(Operator.SIZEOF, None))
    t[0] = t[2]

def p_postExpression0(t):
    '''postfixExpression :  primaryExpression'''
    t[0] = Postfix(t[1], [], t.lexer.lexdata[0: t.lexpos].count("\n") + 1)

def p_postExpression1(t):
    '''postfixExpression :  postfixExpression CORL expression CORR'''
    t[1].acc.append(tuple(Operator.ARRAYACCESS, t[3]))
    t[0] = t[1]
    
def p_postExpression2(t):
    '''postfixExpression :  postfixExpression PARL PARR'''
    t[1].acc.append(tuple(Operator.CALL, None))
    t[0] = t[1]

def p_postExpression3(t):
    '''postfixExpression :  postfixExpression PARL assignmentExpressionList PARR'''
    t[1].acc.append(tuple(Operator.CALL, t[3]))
    t[0] = t[1]

def p_postExpression4(t):
    '''postfixExpression :  postfixExpression DOT ID'''
    t[1].acc.append(tuple(Operator.STRUCTACCESSS, t[3]))
    t[0] = t[1]

def p_postExpression5(t):
    '''postfixExpression :  postfixExpression INC'''
    t[1].acc.append(tuple(Operator.INCREMENT))
    t[0] = t[1]

def p_postExpression6(t):
    '''postfixExpression :  postfixExpression DEC'''
    t[1].acc.append(tuple(Operator.DECREMENT)
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
    t[0] = Primary(t[1], PrimaryType.IDENTIFIER, t.lexer.lexdata[0: t.lexpos].count("\n") + 1)

def p_fExpression3(t):
    '''primaryExpression :   STRVAL'''
    t[0] = Primary(t[1], PrimaryType.CONSTANT, t.lexer.lexdata[0: t.lexpos].count("\n") + 1)


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
    t[0] = Primary(t[1], PrimaryType.CONSTANT, t.lexer.lexdata[0: t.lexpos].count("\n") + 1)

def p_unaryOperator(t):
    '''unaryOperator    :   ANDBW
                        |   PLUS
                        |   MINUS
                        |   NOTBW
                        |   NOT'''
    if (t[1]] == '&'):
        t[0] == Operator.AMPERSAND
    elif (t[1]] == '+'):
        t[0] == Operator.UPLUS
    elif (t[1]] == '-'):
        t[0] == Operator.UMINUS
    elif (t[1]] == '~'):
        t[0] == Operator.NOTBW
    elif (t[1]] == '!'):
        t[0] == Operator.NOT

def p_error(t):
    if t:
        tmp = str(t.value)
        if t.value == '>':
            tmp = "greater-than symbol"
        elif t.value == '<':
            tmp = "less-than symbol"
        addErr(ErrType.SINTACTIC, "Can't reduce '" + tmp + "'", t.lexer.lexdata[0: t.lexpos].count("\n") + 1)
        parser.errok()
    else:
        addErr(ErrType.SINTACTIC, "Unexpected EOF", "")

parser = yacc.yacc()

def parse(input):
    lexer.lineno = 1
    return parser.parse(input)
