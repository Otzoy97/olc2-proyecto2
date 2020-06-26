from interpreter.expression.expression import Expression

class Conditional(Expression):
    def __init__(self, orlog, exp, cond, row):
        self.orlog = orlog
        self.exp = exp
        self.cond = cond
        self.row = row