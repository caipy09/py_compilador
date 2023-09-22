from analyzer import Analyzer
############################################
#Codigo para probar el funcionamiento
############################################


#analyzer = Analyzer(filename='./test1.txt')
analyzer = Analyzer(filename='C:/Users/ferna/Onedrive/Documents/GitHub/py_compilador/test.txt')

    
tok = analyzer.token()
print(tok.__str__())
while tok.isValidToken():
    tok = analyzer.token()
    print(tok.__str__())


print("===================")    
print("Tabla de simbolos:")
print("===================")
print(analyzer.symbol_table)

