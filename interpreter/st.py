from enum import Enum
from copy import copy, deepcopy

class SymbolType(Enum):
    FUNCTION = 0
    VARIABLE = 1

class Symbol():
    def __init__(self, temp, value, type, environment, row):
        #temp is a $t + idx
        #value is the value stored
        #type is the type of the symbol (function or variable)
        #environment can be if, switch, for, etc.
        #row is the row in which is declared
        self.temp = temp
        self.value = value
        self.type = type
        self.environment = environment
        self.row = row

class SymbolTable():
    #Keep track of the index for temporal variables
    IdxTempVar = 0
    #Keep track of all variables and functions
    St = {}

    def __init__(self):
        '''Init a dict'''
        self.table = {}
        
    def add(self, name, sym):
        '''add a variable'''
        if not name in self.table:
            #set temp variable name
            sym.tempName = str(f"$t{SymbolTable.IdxTempVar}")
            #add variable to symbol table
            self.table[name] = sym
            #make a deep copy of the symbol
            symC = deepcopy(sym)
            #add the symbol to global symbol table
            SymbolTable.St[name] = symC
            #increase idx
            SymbolTable.IdxTempVar += 1
    
    def find(self, name):
        '''find a symbol'''
        if name in self.table:
            return self.table[name]
        return None

    @staticmethod
    def genRep():
        '''create a report of the stored symbols in St '''
        pass