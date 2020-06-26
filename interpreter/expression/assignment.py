from interpreter.expression import Expression
from enum import Enum

class AssignmentType(Enum):
    ASSIGN = 0
    TIMESA = 1
    QUOTA = 2
    REMA = 3
    PLUSA = 4
    MINUSA = 5
    SHRA = 6
    SHLA = 7
    ANDBWA = 8
    XORBWA = 9
    ORBWA = 10

class Assignment(Expression):
    def __init__(self, identifier, assignment_type ,expression, row):
        self.identifier = identifier
        self.assignment_type = assignment_type
        self.expression = expression
        self.row = row
    
    def genCode(self):
        pass