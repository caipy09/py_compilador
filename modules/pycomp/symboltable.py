#!/usr/bin/env python3
# -*- coding: utf-8 -*-


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
    
    def addCheckPoint(self, _id = None, name = None):
        self.addSymbol(_id, name, None, 9999, None)
    
    #verifica si existe al menos un checkpoint en la tabla de simbolos
    #def existsCHKP(self):
    #    return "_CHKP" in self.table["id"].values
    
    # #retorna la posicion del ultimo checkpoint encontrado
    # def getPosOfLastCHKP(self, actualPos):
    #     if actualPos <= 0 or self.existsCHKP() == False:
    #         return -1
    #     count = actualPos
    #     isChkp = False
    #     endOfTable = False
    #     while isChkp == False and endOfTable == False:
    #         if self.table.iloc[[count-1]]["id"].iloc[0] == "_CHKP":
    #             isChkp = True
    #         if count == 0:
    #             endOfTable = True
    #         count = count - 1
    #     return count
        
    # #recorre la TS desde el ultimo checkpoint hasta el anterior y verifica si el id ingresado esta presente
    # def checkIfIDExistsUntilLastCHKP(self, _id):
    #     if self.existsCHKP() == False:
    #         return {}
    #     table_length = len(self.table)-1
    #     pos_lastCHKP = self.getPosOfLastCHKP(table_length)
    #     pos_prev_lastCHKP = self.getPosOfLastCHKP(pos_lastCHKP)
    #     pos = pos_lastCHKP
    #     listID = {}
    #     while pos > pos_prev_lastCHKP and pos >= 1:
    #         aux = self.table.iloc[[pos-1]]
    #         if aux["declared"].iloc[0] == True:
    #             listID[aux["id"].iloc[0]] = aux["value"].iloc[0]
    #         pos = pos -1
            
    #     return {k: listID[k] for k in listID.keys() & {_id}}     


    
    # def scanIDUntilCHKP(self):
    #     if self.existsCHKP() == False:
    #         return []
    #     count = len(self.table)-1
    #     if count == self.getPosOfLastCHKP(len(self.table)):
    #         return []
    #     isChkp = False
    #     stack = []
    #     while isChkp == False or count < 1:
    #         if self.table.iloc[[count-1]]["id"].iloc[0] == "_CHKP":
    #             isChkp = True
    #         aux = self.checkIfIDExistsUntilLastCHKP(self.table.iloc[[count]]["id"].iloc[0])
    #         if len(aux) == 1:
    #             stack.append(aux[self.table.iloc[[count]]["id"].iloc[0]])
    #             stack.append(self.table.iloc[[count]]["name"].iloc[0])
    #             stack.append('=')
    #         count = count - 1
    #     return stack
    
    def removeUntilCHKP(self):
        count = len(self.table)-1
        isChkp = False
        while isChkp == False or count < 1:
            if self.table.iloc[[count]]["length"].iloc[0] == 9999:
                isChkp = True
            self.table.drop(count, inplace=True)
            count = count - 1
        
  









 
    
    