from enum import Enum
from copy import copy, deepcopy
from interpreter.quadruple import Quadruple

class SymbolType(Enum):
    FUNCTION = 0
    VARIABLE = 1
    STRUCT = 2
    ARRAY = 3

class Symbol():
    # TODO: añadir una forma de determinar de determinar la dimensión de los array
    def __init__(self, temp = None, value = None, type = None, environment = None, row = None):
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
        self.dimension = []
        self.struct = []
        self.parlist = []
        self.returnLabel = None

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
            #sym.temp = str(f"$t{SymbolTable.IdxTempVar}")
            #add variable to symbol table
            self.table[name] = sym
            #make a deep copy of the symbol
            symC = deepcopy(sym)
            #add the symbol to global symbol table
            SymbolTable.St[name] = symC
            #increase idx
            #SymbolTable.IdxTempVar += 1
            #return sym.temp
    
    def addFunction(self, name, sym):
        '''add a function'''
        if not name in self.table:
            #add function name to symbol table
            self.table[name] = sym
            #make a deep copy of the symbol
            symC = deepcopy(sym)
            #add the symbol to global symbol table
            SymbolTable.St[name] = symC
            #increase idx
            SymbolTable.IdxTempVar += 1
            #set return label
            q = Quadruple.createLabel(name)
            sym.returnLabel = q.r

    def find(self, name):
        '''find a symbol'''
        if name in self.table:
            return self.table[name]
        return None

    @staticmethod
    def genRep():
        '''create a report of the stored symbols in St '''
        pass