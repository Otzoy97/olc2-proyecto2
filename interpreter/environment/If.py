class If(Instruction):
    def __init__(self, expression, statement, else_statement, row):
        self.expression = expression
        self.statement = statement
        self.else_statement = statement
        self.row = row