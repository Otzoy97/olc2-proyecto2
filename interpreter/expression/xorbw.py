from interpreter.expression.expression import Expression

class XorBitWise(Expression):
    def __init__(self, andbw, xorbw, row):
        self.andbw = andbw
        self.xorbw = xorbw
        self.row = row