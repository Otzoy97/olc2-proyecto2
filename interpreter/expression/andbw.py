from interpreter.expression.expression import Expression

class AndBitWise(Expression):
    def __init__(self, equal, andbw, row):
        self.equal = equal
        self.andbw = andbw
        self.row = row