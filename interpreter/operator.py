from enum import Enum

class Operator(Enum):
    INCREMENT = 0
    DECREMENT = 1    
    CALL = 2
    STRUCTACCESS = 3
    ARRAYACCESS = 4
    AMPERSAND = 5
    UPLUS = 6
    UMINUS = 7
    NOTBW = 8
    NOT = 9
    CAST = 10
    SIZEOF = 11
    TIMES = 12
    QUOTIENT = 13
    REMAINDER = 14
    PLUS = 15
    MINUS = 16
    SHL = 17
    SHR = 18