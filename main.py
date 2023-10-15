
############################################
#Codigo para probar el funcionamiento del lexico y sintactico
############################################

#importo codigo de la ts y el lexer
import lexer as lex
#creo el objeto lexer
lexer = lex.Lexer(filename='C:/Users/ferna/Onedrive/Documents/GitHub/py_compilador/test.txt')

###############################################################
#prueba del sintactico

#importar el sintactico de ply
import ply.yacc as yacc

#orden de precedencia de operadores
precedence = (
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULT', 'DIV'),
    #('right', 'URESTA'), #contempla resta unaria
)

#lista de palabras reservadas
reserved = {
   #'if' : 'IF',
   #'else' : 'ELSE',
   #'while' : 'WHILE',
   #'print' : 'PRINT',
   'int' : 'INT'
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
    "LLAVEA",
    "LLAVEC",
    "ASIG",
    "OR"
] + list(reserved.values())


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


polaca_inversa = []

#########################################################################################
#Reglas de la gramatica

#contempla que el programa se componga de multiples declaraciones en varias lineas de codigo
def p_statement_prog(p):
    'program : program statement'
    pass

#contempla que el programa se componga de una declaracion (expresion en una linea)
def p_statement_prog_s(p):
    'program : statement'
    pass

#bloque de declaraciones
def p_statement_decl(p):
    'statement : LLAVEA INT block_decl'
    pass

#el bloque de declaraciones puede tener solo una variable
def p_block_decl(p):
    'block_decl : ID LLAVEC'
    lexer.ts.setDeclaration(p[1])

#el bloque de declaraciones puede tener multiples variables separadas por un OR
def p_block_decl2(p):
    'block_decl : ID OR other_decl'
    lexer.ts.setDeclaration(p[1])
    
#regla que hace recursiva las declaraciones, permitiendo declarar la cantidad que sea
def p_block_decl3(p):
    'other_decl : block_decl'
    pass

#regla de asignacion, valida si la variable esta declarada previamente y asigna, de lo contrario tira error
def p_statement_asig(p):
    'statement : ID ASIG expression'
    if lexer.ts.getDeclaration(p[1]): 
        lexer.ts.setSymbolValue(p[1], p[3])
        lexer.ts.setSymbolLength(p[1], len(str(p[3])))     
    else:
        print("[ERR] Variable no declarada: ", p[1])
        raise(SyntaxError)

#una expresion puede ser un termino
def p_expression(p):
    'expression : term'
    p[0] = p[1]

#una expresion se puede sumar a un termino    
def p_expression_suma(p):
    'expression : expression SUMA term'
    p[0] = int(p[1]) + int(p[3])

#una termino puede restarse de una expresion
def p_expression_resta(p):
    'expression : expression RESTA term'
    p[0] = int(p[1]) - int(p[3])

#un termino es un factor
def p_term(p):
    'term : factor'
    p[0] = p[1]

#un termino puede ser multiplicado por un factor
def p_expression_mult(p):
    'term : term MULT factor'
    p[0] = int(p[1]) * int(p[3])

#un factor puede dividir a un termino, si la division arroja un float, castea el float a int y tira un warning avisando    
def p_expression_div(p):
    'term : term DIV factor'
    aux = int(p[1]) / int(p[3])
    if isinstance(p[0], int):
        p[0] = aux
    else:
        p[0] = int(aux)
        print("[WAR] DIV result was casted to int: ", aux , " >> ", p[0])

#un factor puede ser una expresion encerrada entre parentesis
def p_factor_par(p):
    'factor : PARA expression PARC'
    p[0] = p[2]

#un factor puede ser una constante
def p_factor_1(p):
    'factor : CTE'
    p[0] = p[1]

#un factor puede ser un identificador, en este caso busca el valor numerico del identificador antes de asignar a p
def p_factor_2(p):
    'factor : ID'
    valorSimbolo = (lexer.ts.getSymbolByID(p[1])["value"]).iloc[0]
    p[0] = valorSimbolo




# #cada declaracion se puede componer de una expresion
# def p_statement_expr(p):
#     'statement : expression'
#     pass

# #para la asignacion de valores a variables (x = 2)
# def p_expression_asig(p):
#     'statement : ID ASIG expression'
#     lexer.ts.setSymbolValue(p[1], p[3])
#     lexer.ts.addSymbol(str(int(p[3])), str(int(p[3])), str(int(p[3])), len(str(int(p[3]))), None) #agrega constante calculada
#     lexer.ts.setSymbolLength(p[1], len(str(p[3])))
#     #generacion de polaca inversa
#     polaca_inversa.append(p[1])
#     polaca_inversa.append(p[2])

# #para la suma de variables/constantes (2 + 3)
# def p_expression_suma(p):
#     'expression : expression SUMA term'
#     p[0] = int(p[1]) + int(p[3])
#     #generacion de polaca inversa
#     polaca_inversa.append("+")

# #para la resta de variables/constantes (2 - 3)
# def p_expression_resta(p):
#     'expression : expression RESTA term'
#     p[0] = int(p[1]) - int(p[3])
#     #generacion de polaca inversa
#     polaca_inversa.append("-")


# #las expresiones pueden ser terminos
# def p_expression_term(p):
#     'expression : term'
#     p[0] = p[1]

# #para la multiplicacion de variables/constantes (2 * 3)
# def p_term_mult(p):
#     'term : term MULT factor'
#     p[0] = int(p[1]) * int(p[3])
#     #generacion de polaca inversa
#     polaca_inversa.append("*")
    
# #para la division de variables/constantes (2 / 3)
# def p_term_div(p):
#     'term : term DIV factor'
#     p[0] = int(p[1]) / int(p[3])
#     #generacion de polaca inversa
#     polaca_inversa.append("/")


# #un termino puede ser un factor
# def p_term_factor(p):
#     'term : factor'
#     p[0] = p[1]

# #un factor puede ser una constante
# def p_factor_cte(p):
#     'factor : CTE'
#     p[0] = p[1]
#     #generacion de polaca inversa
#     polaca_inversa.append(p[1])
    

# def p_factor_cte_n(p):
#     "factor : RESTA CTE %prec URESTA"
#     p[0] = -p[2]

# #permite expresiones como por ej: -(-5 * 8)
# def p_factor_expr_n(p):
#     'factor : RESTA PARA expression PARC %prec URESTA'
#     p[0] = -p[3]    

# #un factor puede ser una variable
# def p_factor_id(p):
#     'factor : ID'
#     valorSimbolo = (lexer.ts.getSymbolByID(p[1])["value"]).iloc[0]
#     #print(valorSimbolo)
#     if (lexer.ts.getSymbolByID(p[1])).empty == False: 
#         p[0] = valorSimbolo #asigno su valor
#         #generacion de polaca inversa
#         polaca_inversa.append(p[1])
#     else:
#         print("[ERR] Variable '%s' no inicializada" % p[1]) #descripcion del error
#         p[0] = 0 #para evitar error a nivel lenguaje
#         raise SyntaxError #hago generar un error de parsing intencional en el parser.
#     #print("[DEBUG_]: p[0]: ", p[0], " p[1]: ", p[1], " valorSimbolo: ", valorSimbolo)

# #un factor puede ser una expresion encerrada entre parentesis ('(2*3)')
# def p_factor_expr(p):
#     'factor : PARA expression PARC'
#     p[0] = p[2]


    
# Error rule for syntax errors
def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")



# Build the parser
yacc.yacc(write_tables=False)
yacc.parse(lexer=lexer, debug=False)

lexer.ts.__str__() 
print("polaca_inversa: ", polaca_inversa)
