from interpreter.expression.expression import Expression

class AndLogical(Expression):
    def __init__(self, orbw, andlog, row):
        self.orbw = orbw
        self.andlog = andlog
        self.row = row