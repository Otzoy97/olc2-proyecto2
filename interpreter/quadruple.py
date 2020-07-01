from enum import Enum

class OperatorQuadruple(Enum):
    PLUS        = 1  # +
    MINUS       = 2  # -
    TIMES       = 3  # *
    QUOTIENT    = 4  # /
    REMAINDER   = 5  # %
    NEGATIVE    = 6  # -
    ABS         = 7  # abs
    NOT         = 8  # !
    AND         = 9  # &&
    XOR         = 10 # xor
    OR          = 11 # ||
    NOTBW       = 12 # ~ 
    ANDBW       = 13 # &
    ORBW        = 14 # |
    XORBW       = 15 # ^
    SHL         = 16 # <<
    SHR         = 17 # >>
    EQ          = 18 # =
    NEQ         = 19 # !=
    GR          = 20 # >
    GRE         = 21 # >=
    LS          = 22 # <
    LSE         = 23 # <=
    AMP         = 24 # &
    CINT        = 25 # int
    CFLOAT      = 26 # float
    CCHAR       = 27 # string
    READ        = 28 # read()
    ARRAY       = 29 # array()
    ASSIGNMENT  = 30 # assignment
    LABEL       = 31
    IF          = 32
    GOTO        = 33
    
class Quadruple():
    def __init__(self, op, arg1, arg2, r):
        self.op = op
        self.arg1 = arg1    
        self.arg2 = arg2
        self.r = r

    QDict = []
    IdxLabel = 0

    @staticmethod
    def createLabel(lbl = None):
        if lbl == None:
            lbl =  f"L{Quadruple.IdxLabel}"
            Quadruple.IdxLabel += 1
        q = Quadruple(OperatorQuadruple.LABEL, None, None, lbl)
        #Quadruple.QDict.append(q)
        return q   
