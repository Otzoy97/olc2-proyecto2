from interpreter.expression.expression import Expression

class OrLogical(Expression):
    def __init__(self, andlog,  orlog, row):
        self.andlog = andlog
        self.orlog = orlog
        self.row = row