from interpreter.instruction import Instruction

class For(Instruction):
    def __init__(self, expressionInit, condition, increment, statement, row):
        self.expressionInit = expressionInit
        self.condition = condition
        self.increment = increment
        self.statement = statement
        self.row = row