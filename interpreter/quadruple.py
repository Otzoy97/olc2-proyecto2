from enum import Enum

class OperatorQuadruple(Enum):
    PLUS        = "+"  # +
    MINUS       = "-"  # -
    TIMES       = "*"  # *
    QUOTIENT    = "/"  # /
    REMAINDER   = "%"  # %
    #NEGATIVE    = 6  # -
    ABS         = 7  # abs
    NOT         = "!"  # !
    AND         = "&&"  # &&
    XOR         = "xor" # xor
    OR          = "||" # ||
    NOTBW       = "~" # ~ 
    ANDBW       = "&" # &
    ORBW        = "|" # |
    XORBW       = "^" # ^
    SHL         = "<<" # <<
    SHR         = ">>" # >>
    EQ          = "==" # =
    NEQ         = "!=" # !=
    GR          = ">" # >
    GRE         = ">=" # >=
    LS          = "<" # <
    LSE         = "<=" # <=
    AMP         = "&" # &
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
    IdxReturn = 0
    QReturn = []

    @staticmethod
    def addReturnLabel():
        Quadruple.IdxReturn += 1
        Quadruple.QReturn.append(Quadruple(OperatorQuadruple.IF, f"$s0[$sp] == {Quadruple.IdxReturn}", None, f"ret{Quadruple.IdxReturn}"))
        return Quadruple.IdxReturn

    BinaryOp = [
        OperatorQuadruple.PLUS,
        OperatorQuadruple.MINUS,
        OperatorQuadruple.TIMES,
        OperatorQuadruple.QUOTIENT,
        OperatorQuadruple.REMAINDER,
        OperatorQuadruple.AND,
        OperatorQuadruple.XOR,
        OperatorQuadruple.OR,
        OperatorQuadruple.ANDBW,
        OperatorQuadruple.ORBW,
        OperatorQuadruple.XORBW,
        OperatorQuadruple.SHL,
        OperatorQuadruple.SHR,
        OperatorQuadruple.EQ,
        OperatorQuadruple.NEQ,
        OperatorQuadruple.GR,
        OperatorQuadruple.GRE,
        OperatorQuadruple.LS,
        OperatorQuadruple.LSE
    ]
    UnaryOp = [
        OperatorQuadruple.NOTBW,
        OperatorQuadruple.NOT,
        OperatorQuadruple.AMP
    ]

    @staticmethod
    def createLabel(lbl = None):
        if lbl == None:
            lbl =  f"L{Quadruple.IdxLabel}"
            Quadruple.IdxLabel += 1
        q = Quadruple(OperatorQuadruple.LABEL, None, None, lbl)
        #Quadruple.QDict.append(q)
        return q   

    @staticmethod
    def create3DCode():
        '''this function creates a file with all the instructions
            stored id QDict'''
        with open("augus3DCode.txt", "w") as f:
            for quad in Quadruple.QDict:
                if quad.op == OperatorQuadruple.ASSIGNMENT:
                    f.write(f"{quad.r} = {quad.arg1};\n")
                elif quad.op == OperatorQuadruple.LABEL:
                    f.write(f"{quad.r}:\n")
                elif quad.op == OperatorQuadruple.IF:
                    f.write(f"if ({quad.arg1}) goto {quad.r};\n")
                elif quad.op == OperatorQuadruple.GOTO:
                    f.write(f"goto {quad.r};\n")
                elif quad.op in Quadruple.BinaryOp:
                    f.write(f"{quad.r} = {quad.arg1} {quad.op.value} {quad.arg2};\n")
                elif quad.op in Quadruple.UnaryOp:
                    f.write(f"{quad.r} = {quad.op.value}{quad.arg1};\n")
        return "augus3DCode.txt"