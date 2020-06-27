class While(Instruction):
    def __init__(self, expression, statement, row):
        self.expression = expression
        self.statement = statement
        self.row = row