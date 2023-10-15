import pandas as pd

class SymbolTable(object):
    
    desc = ""

    def __init__(self, desc = None):
        
        self.table = pd.DataFrame()
        #tabla de simbolos con columnas principales
        self.table["id"] = None
        self.table["name"] = None
        self.table["value"] = None
        self.table["length"] = None
        self.table["declared"] = None
        self.desc = desc

    #metodo para impresion de la TS
    def __str__(self):
        print("======================================")    
        print("Tabla de simbolos [", self.desc, "]:")
        print("======================================")
        print(self.table)
        
    #obtener la tabla de simbolos
    def getSymbolTable(self):
        return self.table
    
    #agrega un guionbajo al string que recibe
    def addUnderscore(self, _id):
        aux = ("_" + str(_id))
        return aux
    
    #agregar registro a la tabla de simbolos
    def addSymbol(self, _id = None, name = None, value = None, leng = None, decl = None):
        if self.checkIfExist(_id):
            pass
        else:
            row = [self.addUnderscore(_id), name, value, leng, decl]
            self.table.loc[len(self.table)] = row
    
    #verificar si un registro existe en ts, mediante el nombre
    def checkIfExist(self, _id = None):
        return (self.getSymbolTable()["id"] == self.addUnderscore(_id)).any()
    
    #obtener una fila de la TS, segun el nombre
    def getSymbolByID(self, _id = None):
        return self.getSymbolTable()[self.getSymbolTable()["id"] == self.addUnderscore(_id)]
    
    #modificar valor de un registro, dado su nombre
    def setSymbolValue(self, _id=None, value=None):
        self.table.loc[self.table["id"] == self.addUnderscore(_id), "value"] = value
        
    #modificar valor de longitud de un simbolo
    def setSymbolLength(self, _id = None, leng = None):
        self.table.loc[self.table["id"] == self.addUnderscore(_id), "length"] = leng
        
    def setDeclaration(self, _id = None):
        self.table.loc[self.table["id"] == self.addUnderscore(_id), "declared"] = True

    def getDeclaration(self, _id = None):
        return (self.table.loc[self.table["id"] == self.addUnderscore(_id), "declared"]).iloc[0]
    
    
    
    
    