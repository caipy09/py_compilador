
import lexer as dlv

lexer = dlv.Lexer(filename='C:/Users/ferna/Onedrive/Documents/GitHub/py_compilador/ejemplo4.txt')

#comienzo la impresion de tokens de ejemplo
tok = lexer.token()
print(tok.__str__())
while tok != None:
      tok = lexer.token()
      print(tok.__str__())


#imprimo la tabla de simbolos
lexer.ts.__str__() 


# import dummy_lexer as dl

# lexer = dl.Lexer(filename='C:/Users/ferna/Onedrive/Documents/GitHub/py_compilador/test.txt')

# #comienzo la impresion de tokens de ejemplo
# tok = lexer.token()
# print(tok.__str__())
# while tok != None:
#       tok = lexer.token()
#       print(tok.__str__())


# #imprimo la tabla de simbolos
# lexer.ts.__str__() 