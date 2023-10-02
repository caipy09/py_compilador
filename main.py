
############################################
#Codigo para probar el funcionamiento
############################################

import lex as lex

#analyzer = Analyzer(filename='./test1.txt')
lexer = lex.Lexer(filename='C:/Users/fheredia/Documents/GitHub/py_compilador/test.txt')

tok = lexer.token()
print(tok.__str__())
while tok != None:
    tok = lexer.token()
    print(tok.__str__())


print("===================")    
print("Tabla de simbolos:")
print("===================")
print(lexer.symbol_table)    



























