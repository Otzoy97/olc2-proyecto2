from interpreter.instruction import Instruction
from interpreter.st import SymbolTable, Symbol, SymbolType
from interpreter.dspecifier import DSpecifier
from interpreter.environment.Function import Function
from PyQt5 import QtWidgets
from interpreter.quadruple import Quadruple, OperatorQuadruple
from copy import deepcopy, copy

class Program(Instruction):
    def __init__(self):
        self.sym = SymbolTable()
        self.ist = []

    def firstRun(self):
        '''Recorre los arreglos de function y declaration'''
        #Busca una función con etiqueta main
        mainF = [(i,main) for i,main in enumerate(self.ist) if isinstance(main, Function) and main.dec[0] == "main" ]
        #Se asegura que solo haya un main:
        if len(mainF) > 1:
            QtWidgets.QMessageBox.warning(None, 
            "Conflicto de función main", 
            "Hay más de un main declarado",
            QtWidgets.QMessageBox.Ok)
            return
        elif len(mainF) == 0:
            QtWidgets.QMessageBox.warning(None, 
            "Conflicto de función main", 
            "¡No hay main declarado!",
            QtWidgets.QMessageBox.Ok)
            return
        #extrae el main
        mainF = self.ist.pop(mainF[0][0])
        #introduce la etiqueta main
        Quadruple.QDict.append(Quadruple(OperatorQuadruple.LABEL, None, None, "main"))           
        #introduce el stack y el stackpointer
        Quadruple.QDict.append(Quadruple(OperatorQuadruple.ASSIGNMENT, -1, None, "$sp"))
        Quadruple.QDict.append(Quadruple(OperatorQuadruple.ASSIGNMENT, "array()", None, "$s0"))           
        while len(self.ist) > 0:
            inst = self.ist.pop(0)
            if isinstance(inst, Function):
                #volverá a insertar el elemento al inicio de la lista
                self.ist.insert(0, inst)
                break
            inst.firstRun(self)
        #realiza una copia profunda de qdict
        self.tmpQDict = deepcopy(Quadruple.QDict)
        Quadruple.QDict.clear()
        #sigue con la ejecución del programa
        for i in self.ist:
            i.firstRun(self)
        #este es el indice para empezar a remover
        idxQdict = len(Quadruple.QDict)
        #ejecuta el main
        self.executeMain(mainF)
        #reordena los cuadruplos
        Quadruple.QDict = self.tmpQDict + Quadruple.QDict[idxQdict:] + Quadruple.QDict[:idxQdict]
        #añade las etiquetas almacnadas en qreturn
        Quadruple.appendReturnLabels()

    def findSymbol(self, identifier):
        '''Busca un simbolo'''
        return self.sym.find(identifier)

    def retrieveEnvironment(self):
        return "global/main"

    def searchForLoop(self):
        return None
    
    def executeMain(self, mainF):
        #ejecuta los statements
        for sta in mainF.csta:
            sta.firstRun(self)
        #añada la etiqueta de salida
        Quadruple.QDict.append(Quadruple(OperatorQuadruple.EXIT_, None, None, None))
