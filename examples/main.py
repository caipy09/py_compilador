
############################################
#Codigo para probar el funcionamiento
############################################

#importo codigo de la ts y el lexer
import lexer as lex
#creo el objeto tabla de simbolos
ts = lex.SymbolTable()
#creo el objeto lexer
lexer = lex.Lexer(filename='C:/Users/ferna/Onedrive/Documents/GitHub/py_compilador/test.txt', ts=ts)
#lexer = lex.Lexer(filename='C:/Users/fheredia/Documents/GitHub/py_compilador/test.txt', ts=ts)

#comienzo la impresion de tokens de ejemplo
# tok = lexer.token()
# print(tok.__str__())
# while tok != None:
#       tok = lexer.token()
#       print(tok.__str__())

#imprimo la tabla de simbolos
#ts.__str__() 


# def roundAndConvertToStr(value):
#     return str(int(value))


###############################################################
#prueba del parser

#importar el sintactico de ply
import ply.yacc as yacc

#orden de precedencia de operadores
precedence = (
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULT', 'DIV'),
    #('right', 'URESTA'),
)

#lista de palabras reservadas
reserved = {
   #'if' : 'IF',
   #'else' : 'ELSE',
   #'while' : 'WHILE',
   #'print' : 'PRINT',
   #'int' : 'INT'
}

#lista completa de tokens
tokens = [
    "ID", 
    "CTE", 
    "SUMA", 
    "RESTA", 
    "MULT", 
    "DIV", 
    "PARA", 
    "PARC", 
    "ASIG"
] + list(reserved.values())

polaca_inversa = []
terceto = []
lista_tercetos = {}
t = 1

#contempla que el programa se componga de multiples declaraciones en varias lineas de codigo
def p_statement_prog(p):
    'program : program statement'
    pass

#contempla que el programa se componga de una declaracion (expresion en una linea)
def p_statement_prog_s(p):
    'program : statement'
    pass

#cada declaracion se puede componer de una expresion
def p_statement_expr(p):
    'statement : expression'
    #pass
    #print("[DEBUG]: p[0]: ", p[0], " p[1]: ", p[1])
    

#para la asignacion de valores a variables (x = 2)
def p_expression_asig(p):
    'statement : ID ASIG expression'
    ts.setSymbolValue(p[1], int(p[3]))
    ts.setSymbolLength(p[1], len(str(int(p[3]))))
    ts.addSymbol(str(int(p[3])), str(int(p[3])), len(str(int(p[3]))))
    
    #generacion de polaca inversa
    polaca_inversa.append(p[1])
    polaca_inversa.append(p[2])
    
    #generacion de tercetos
    global t
    terceto.append(p[1])
    nuevo_terceto = ("T" + str(t))
    lista_tercetos[nuevo_terceto] = [p[2], terceto.pop(len(terceto)-1), terceto.pop(len(terceto)-2)]
    t = t + 1
    
    #print("[DEBUG]: p[0]: ", p[0], " p[1]: ", p[1], " = ", " p[3]: ", p[3])

#para la suma de variables/constantes (2 + 3)
def p_expression_suma(p):
    'expression : expression SUMA term'
    p[0] = p[1] + p[3]
    
    #generacion de polaca inversa
    polaca_inversa.append("+")
    
    #generacion de tercetos
    global t
    nuevo_terceto = ("T" + str(t))
    lista_tercetos[nuevo_terceto] = [p[2], terceto.pop(len(terceto)-2), terceto.pop(len(terceto)-1)]
    terceto.append(nuevo_terceto)
    t = t + 1
    
    #print("[DEBUG]: p[0]: ", p[0], " p[1]: ", p[1], " + ", " p[3]: ", p[3])

#para la resta de variables/constantes (2 - 3)
def p_expression_resta(p):
    'expression : expression RESTA term'
    p[0] = p[1] - p[3]
    
    #generacion de polaca inversa
    polaca_inversa.append("-")
    
    #generacion de tercetos
    global t
    nuevo_terceto = ("T" + str(t))
    lista_tercetos[nuevo_terceto] = [p[2], terceto.pop(len(terceto)-2), terceto.pop(len(terceto)-1)]
    terceto.append(nuevo_terceto)
    t = t + 1

#las expresiones pueden ser terminos
def p_expression_term(p):
    'expression : term'
    p[0] = p[1]
    #pass

#para la multiplicacion de variables/constantes (2 * 3)
def p_term_mult(p):
    'term : term MULT factor'
    p[0] = p[1] * p[3]
    
    #generacion de polaca inversa
    polaca_inversa.append("*")
    
    #generacion de tercetos
    global t
    nuevo_terceto = ("T" + str(t))
    lista_tercetos[nuevo_terceto] = [p[2], terceto.pop(len(terceto)-2), terceto.pop(len(terceto)-1)]
    terceto.append(nuevo_terceto)
    t = t + 1

#para la division de variables/constantes (2 / 3)
def p_term_div(p):
    'term : term DIV factor'
    p[0] = p[1] / p[3]
    
    #generacion de polaca inversa
    polaca_inversa.append("/")
    
    #generacion de tercetos
    global t
    nuevo_terceto = ("T" + str(t))
    lista_tercetos[nuevo_terceto] = [p[2], terceto.pop(len(terceto)-2), terceto.pop(len(terceto)-1)]
    terceto.append(nuevo_terceto)
    t = t + 1

#un termino puede ser un factor
def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

#un factor puede ser una constante
def p_factor_cte(p):
    'factor : CTE'
    p[0] = p[1]
    
    #generacion de polaca inversa
    polaca_inversa.append(p[1])
    
    #generacion de tercetos
    terceto.append(p[1])
    
# def p_factor_cte_n(p):
#     "factor : RESTA CTE %prec URESTA"
#     p[0] = -p[2]


#un factor puede ser una variable
def p_factor_id(p):
    'factor : ID'
    valorSimbolo = (ts.getSymbolByName(str(p[1]))["valor"]).iloc[0]
    if (ts.getSymbolByName(str(p[1]))).empty == False and valorSimbolo.isdigit(): 
        p[0] = int(valorSimbolo) #asigno su valor
        
        #generacion de polaca inversa
        polaca_inversa.append(p[1])
        
        #generacion de tercetos
        terceto.append(p[1])
    else:
        print("[ERR] Variable '%s' no definida" % p[1]) #descripcion del error
        p[0] = 0 #para evitar error a nivel lenguaje
        raise SyntaxError #hago generar un error de parsing intencional en el parser.
    #print("[DEBUG]: p[0]: ", p[0], " p[1]: ", p[1], " valorSimbolo: ", valorSimbolo)

#un factor puede ser una expresion encerrada entre parentesis ('(2*3)')
def p_factor_expr(p):
    'factor : PARA expression PARC'
    p[0] = p[2]

#permite expresiones como por ej: -(-5 * 8)
# def p_factor_expr_n(p):
#     'factor : RESTA PARA expression PARC %prec URESTA'
#     p[0] = -p[3]
    
# Error rule for syntax errors
def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

# Build the parser
yacc.yacc(write_tables=False)
yacc.parse(lexer=lexer, debug=False)

ts.__str__() 
print("polaca_inversa: ", polaca_inversa)
print("lista tercetos: ", lista_tercetos)

