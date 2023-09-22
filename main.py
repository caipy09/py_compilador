from analyzer import Analyzer
import pandas as pd
############################################
#Codigo para probar el funcionamiento
############################################

lista_tokens = pd.DataFrame()
lista_tokens["id"] = [256, 257, 258, 259, 260, 261, 262, 263, 264, 268, 269, 266, 267, 265, 272, 273, 274, 275, 276, 277, 278, 279, 270, 271]
lista_tokens["nombre"] = ["ID", "CTE", "IF", "ELSE", "WHILE", "PRINT", "INT", "ASIG", "IGUALA", "MAYOR", "MAYORIGUAL", "MENOR", "MENORIGUAL", "DIST", "SUMA", "RESTA", "MULT", "DIV", "PARA", "PARC", "LLAVEA", "LLAVEC", "AND", "OR"]
lista_tokens["valor"] = ["NA", "NA", "if", "else", "while", "print", "int", "=", "==", ">", ">=", "<", "<=", "<>", "+", "-", "*", "/", "(", ")", "{", "}", "&", "|"]

#analyzer = Analyzer(filename='./test1.txt')
analyzer = Analyzer(filename='C:/Users/ferna/Onedrive/Documents/GitHub/py_compilador/test.txt')

a = 0
while a != -1:
    a = analyzer.lex()
    print(lista_tokens[lista_tokens["id"] == a])
print("===================")    
print("Tabla de simbolos:")
print("===================")
print(analyzer.symbol_table)
