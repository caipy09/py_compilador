
ntest = "07"
path_input = "C:/Users/ferna/Onedrive/Documents/GitHub/py_compilador/lote_pruebas/" + ntest + "/"
path_output = "C:/Users/ferna/Onedrive/Documents/GitHub/py_compilador/lote_pruebas/" + ntest + "/"


############################################
#Codigo para probar el funcionamiento del lexico y sintactico
############################################

#importo codigo de la ts y el lexer
import lexer as lex
#creo el objeto lexer 
lexer = lex.Lexer(filename= path_input + 'input.txt')

###############################################################
#prueba del sintactico

#importar el sintactico de ply
import ply.yacc as yacc

#orden de precedencia de operadores
precedence = (
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULT', 'DIV'),
    #('right', 'URESTA'), #contempla resta unaria, si las reglas de resta unaria estan comentadas comentar esto tambien
)

#lista de palabras reservadas
reserved = {
   'if' : 'IF',
   'else' : 'ELSE',
   'while' : 'WHILE',
   'print' : 'PRINT',
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
    "OR",
    "AND",
    "IGUALA",
    "DIST",
    "MENOR",
    "MENORIGUAL",
    "MAYOR",
    "MAYORIGUAL"
] + list(reserved.values())


err = []
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

#una declaracion puede ser una declaracion de print
def p_statement_print(p):
    'statement : print_statement'
    pass

#una declaracion puede ser una declaracion de comparacion
def p_comp_statement(p):
    'statement : comp_statement'
    pass

#una declaracion puede ser una declaracion logica
def p_logic_statement(p):
    'statement : logic_statement'
    pass

#una declaracion puede una declaracion de un while
def p_while_statement(p):
    'statement : while_statement'
    pass

#una declaracion puede una declaracion de un if
def p_if_statement(p):
    'statement : if_statement'
    pass

def p_expr_statement(p):
    'statement : expression'
    pass

#bloque de declaraciones
def p_statement_decl(p):
    'statement : LLAVEA INT block_decl'
    pass

#el bloque de declaraciones puede tener solo una variable
def p_block_decl(p):
    'block_decl : ID LLAVEC'
    if(lexer.ts.getDeclaration(p[1])):
        e = "[WAR] Var: " + p[1] + " is already declared."
        err.append(e)
        print(e)
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
        #generacion de polaca inversa
        polaca_inversa.append(p[1])
        polaca_inversa.append(p[2])        
    else:
        e = "[ERR] Var: " + p[1] + "not declared."
        err.append(e)
        print(e)
        raise(SyntaxError)

#una expresion puede ser un termino
def p_expression(p):
    'expression : term'
    p[0] = p[1]

#una expresion se puede sumar a un termino    
def p_expression_suma(p):
    'expression : expression SUMA term'
    p[0] = int(p[1]) + int(p[3])
    #generacion de polaca inversa
    polaca_inversa.append("+")

#una termino puede restarse de una expresion
def p_expression_resta(p):
    'expression : expression RESTA term'
    p[0] = int(p[1]) - int(p[3])
    #generacion de polaca inversa
    polaca_inversa.append("-")

#un termino es un factor
def p_term(p):
    'term : factor'
    p[0] = p[1]

#un termino puede ser multiplicado por un factor
def p_expression_mult(p):
    'term : term MULT factor'
    p[0] = int(p[1]) * int(p[3])
    #generacion de polaca inversa
    polaca_inversa.append("*")

#un factor puede dividir a un termino, si la division arroja un float, castea el float a int y tira un warning avisando    
def p_expression_div(p):
    'term : term DIV factor'
    aux = int(p[1]) / int(p[3])
    if isinstance(p[0], int):
        p[0] = aux
    else:
        p[0] = int(aux)
        e = "[WAR] DIV result was casted to int: " + str(aux) + " >> " + str(p[0])
        print(e)
        err.append(e)
    #generacion de polaca inversa
    polaca_inversa.append("/")

#un factor puede ser una expresion encerrada entre parentesis
def p_factor_par(p):
    'factor : PARA expression PARC'
    p[0] = p[2]

#un factor puede ser una constante
def p_factor_1(p):
    'factor : CTE'
    p[0] = int(p[1])
    #generacion de polaca inversa
    polaca_inversa.append(p[1])

#un factor puede ser un identificador, en este caso busca el valor numerico del identificador antes de asignar a p
def p_factor_2(p):
    'factor : ID'
    valorSimbolo = (lexer.ts.getSymbolByID(p[1])["value"]).iloc[0]
    p[0] = valorSimbolo
    #generacion de polaca inversa
    polaca_inversa.append(p[1])

#estas reglas generan 1 shift-reduce, sin embargo permiten operaciones unarias con constantes y expresiones
#permite restas unarias, ej: x = -5
# def p_factor_cte_n(p):
#     "factor : RESTA CTE %prec URESTA"
#     p[0] = -int(p[2])

# #permite expresiones como por ej: -(-5 * 8)
# def p_factor_expr_n(p):
#     'factor : RESTA PARA expression PARC %prec URESTA'
#     p[0] = -int(p[3])

#imprimir valor
def p_print(p):
    'print_statement : PRINT PARA expression PARC'
    print("[PRINT]: ", p[3])

def p_f_cond(p):
    'f_cond : comp_statement'
    pass

def p_f_cond_2(p):
    'f_cond : logic_statement'
    pass

#comparador ==
def p_comparator_iguala(p):
    'comp_statement : expression IGUALA factor'
    p[0] = p[1] == p[3]
    #generacion de polaca inversa
    polaca_inversa.append("==")

#comparador <>
def p_comparator_dist(p):
    'comp_statement : expression DIST factor'
    p[0] = p[1] != p[3]
    #print(p[0], " : ", p[1], " DIST ", p[3])
    #generacion de polaca inversa
    polaca_inversa.append("<>")
    
#comparador <
def p_comparator_menor(p):
    'comp_statement : expression MENOR factor'
    p[0] = p[1] < p[3]
    #print(p[0], " : ", p[1], " MENOR ", p[3])
    #generacion de polaca inversa
    polaca_inversa.append("<")
    
#comparador <=
def p_comparator_menorigual(p):
    'comp_statement : expression MENORIGUAL factor'
    p[0] = p[1] <= p[3]
    #generacion de polaca inversa
    polaca_inversa.append("<=")
    
#comparador >
def p_comparator_mayor(p):
    'comp_statement : expression MAYOR factor'
    p[0] = p[1] > p[3]
    #generacion de polaca inversa
    polaca_inversa.append(">")
    
#comparador >=
def p_comparator_mayorigual(p):
    'comp_statement : expression MAYORIGUAL factor'
    p[0] = p[1] >= p[3]
    #generacion de polaca inversa
    polaca_inversa.append(">=")

#el operador logico OR puede ser usado en dos expresiones de comparacion
def p_logic_expr_or(p):
    'logic_statement : comp_statement OR comp_expression'
    p[0] = p[1] or p[3]
    #print(p[0], " : ", p[1], " OR ", p[3])
    #generacion de polaca inversa
    polaca_inversa.append("|")

#el operador logico AND puede ser usado en dos expresiones de comparacion
def p_logic_expr_and(p):
    'logic_statement : comp_statement AND comp_expression'
    p[0] = p[1] and p[3]
    #print(p[0], " : ", p[1], " AND ", p[3])
    #generacion de polaca inversa
    polaca_inversa.append("&")

#una expresion de comparacion es una declaracion de comparacion
def p_comp_expression(p):
    'comp_expression : comp_statement'
    p[0] = p[1]

#preguntar si los while/if deben ejecutarse en etapa de parsing
#preguntar de no ejecutarse en esta etapa, que hacer para mantener actualizada las TS
#https://stackoverflow.com/questions/62603001/while-cycle-implementation-never-ends-in-ply-issue
#https://copyprogramming.com/howto/python-ply-issue-with-if-else-and-while-statements#python-ply-issue-with-if-else-and-while-statements

#regla complementaria del while para poder hacer los saltos
def p_while(p): 
    'while : WHILE'
    pass

#regla del while
def p_iter_while(p):
    'while_statement : while PARA f_cond PARC LLAVEA sub_program'
    #print("p_while")

#regla del bloque de codigo dentro de una sentencia de control
def p_subprogram(p):
    'sub_program : program LLAVEC'

#reglas que permite saltos para los if
def p_if_fcpo_1(p):
    'fcpo1 : sub_program'
    print("if")

#reglas que permite saltos para los else if
def p_if_fcpo_2(p):
    'fcpo2 : sub_program'
    print("else")


#regla del if
def p_condition_if(p):
    'if_statement : IF PARA f_cond PARC LLAVEA fcpo1 else_statement'
    pass
    

#regla del else
def p_condition_else(p):
    '''else_statement : ELSE LLAVEA fcpo2
                      | empty'''
    pass

#regla lambda
def p_empty(p):
    'empty :'
    pass

    
# Error rule for syntax errors
def p_error(p):
    if p:
        e = "[ERR] Syntax error at '"+ p.value + "'"
    else:
        e = "[ERR] Syntax error at EOF"
    err.append(e)
    print(e)




# Build the parser
yacc.yacc(write_tables=False)
yacc.parse(lexer=lexer, debug=False)

#impresion de resulados por consola
lexer.ts.__str__() 
print("polaca_inversa: ", polaca_inversa)

#Grabado de resultados a archivo txt
file = open(path_output + 'output.txt', "w")
file.write("Errores/Warnings: " + '\n')
file.write(str(err) + '\n')
file.write('\n' + "Tabla de simbolos: " + '\n')
file.write(str(lexer.ts.table) + '\n')
file.write('\n'+ "polaca_inversa: " + '\n')
file.write(str(polaca_inversa) + '\n')
file.close()
