from interpreter.instruction import Instruction

class Assignment(Instruction):
    def __init__(self, exp1, assignment_type, exp2, row):
        self.exp1 = exp1
        self.assignment_type = assignment_type
        self.exp2 = exp2
        self.row = row
    
    def firstRun(self):
        pass