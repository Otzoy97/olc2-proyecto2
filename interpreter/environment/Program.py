from interpreter.instruction import Instruction
from interpreter.st import SymbolTable, Symbol, SymbolType
from interpreter.dspecifier import DSpecifier

class Program(Instruction):
    def __init__(self):
        self.sym = SymbolTable()
        self.ist = []

    def firstRun(self):
        '''Recorre los arreglos de function y declaration'''
        for i in self.ist:
            i.firstRun(self)
    
    def findSymbol(self, identifier):
        '''Busca un simbolo'''
        return self.sym.find(identifier)

    def retrieveEnvironment(self):
        return "main/global"

    def searchForLoop(self):
        return None