from enum import Enum
from copy import copy, deepcopy
from interpreter.quadruple import Quadruple, OperatorQuadruple

class SymbolType(Enum):
    FUNCTION = 0
    VARIABLE = 1
    STRUCT = 2
    ARRAY = 3

class Symbol():
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
        self.parlist = []
        self.returnLabel = None
        self.param = False
        self.idxParam = 0

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
            r =  self.table[name]
            if r.param:
                Quadruple.QDict.append(Quadruple(OperatorQuadruple.MINUS,"$sp", r.idxParam,"$ra"))
            return r
        return None

    @staticmethod
    def genRep():
        '''create a report of the stored symbols in St '''
        with open("st.html", "w", encoding='utf8') as f:
            f.write("<html>\n<head>\n<title>Tabla de simbolos</title>\n</head>\n")
            f.write("<body>\n")
            f.write('<table border=1 align=center style="width:100%">\n')
            f.write("<tr>\n")
            f.write("<td>Id.</td>\n")
            f.write("<td>Ref</td>\n")
            f.write("<td>Dimensión</td>\n")
            f.write("<td>Valor</td>\n")
            f.write("<td>Tipo</td>\n")
            f.write("<td>Fila</td>\n")
            f.write("<td>Entorno</td>\n")
            f.write("</tr>\n")
            for k,v in SymbolTable.St.items():
                f.write("<tr>\n")
                f.write(f"<td>{k}</td>\n")
                f.write(f"<td>{v.temp}</td>\n")
                f.write(f"<td>{v.dimension if len(v.dimension) > 0 else None}</td>\n")
                f.write(f"<td>{v.value}</td>\n")
                f.write(f"<td>{v.type.name}</td>\n")
                f.write(f"<td>{v.row}</td>\n")
                f.write(f"<td>{v.environment}</td>\n")
                f.write("</tr>\n")
            f.write("</table>\n")
            f.write("</body>\n")
            f.write("</html>\n")