from interpreter.expression.expression import Expression

class OrBitWise(Expression):
    def __init__(self, xorbw, orbw, row):
        self.xorbw = xorbw
        self.orbw = orbw
        self.row = row