import lex as lex

tokens = (
    "ID", "CTE", "SUMA", "RESTA", "MULT", "DIV", "PARA", "PARC", "ASIG"
)

precedence = (
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULT', 'DIV'),
    ('right', 'UMINUS'),
)


#x = lex.Lexer(filename='C:/Users/ferna/Onedrive/Documents/GitHub/py_compilador/test.txt')
x = lex.Lexer(filename='C:/Users/fheredia/Documents/GitHub/py_compilador/test.txt')

# lista de variables. La ejecucion de las reglas podra guardar variables en esta lista
names = {}

import ply.yacc as yacc

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
    pass

#para la asignacion de valores a variables (x = 2)
def p_expression_asig(p):
    'statement : ID ASIG expression'
    names[p[1]] = p[3]

#para la suma de variables/constantes (2 + 3)
def p_expression_suma(p):
    'expression : expression SUMA term'
    p[0] = p[1] + p[3]

#para la resta de variables/constantes (2 - 3)
def p_expression_resta(p):
    'expression : expression RESTA term'
    p[0] = p[1] - p[3]

#las expresiones pueden ser terminos
def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

#regla que permite el uso de constantes negativas (-1) al inicio de una expresion
def p_expression_uminus(p):
    "expression : RESTA expression %prec UMINUS"
    p[0] = -p[2]

#regla que permite el uso de constantes con un más adelante (+1) al inicio de una expresion    
def p_expression_uplus(p):
    "expression : SUMA expression"
    p[0] = p[2]

# def p_expression_id(p):
#     "expression : ID"
#     try:
#         p[0] = names[p[1]]
#     except LookupError:
#         print("Undefined id '%s'" % p[1])
#         p[0] = 0

#para la multiplicacion de variables/constantes (2 * 3)
def p_term_mult(p):
    'term : term MULT factor'
    p[0] = p[1] * p[3]

#para la division de variables/constantes (2 / 3)
def p_term_div(p):
    'term : term DIV factor'
    p[0] = p[1] / p[3]

#un termino puede ser un factor
def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

#un factor puede ser una constante
def p_factor_cte(p):
    'factor : CTE'
    p[0] = p[1]
    
#un factor puede ser una constante
def p_factor_alt(p):
    'factor : ID'
    try:
        p[0] = names[p[1]] #busca en la lista de variables si hay alguna que se llame como el ID reconocido
    except LookupError: #si no lo encuentra en la lista entonces tira error
        print("Undefined id '%s'" % p[1])
        p[0] = 0

#un factor puede ser una expresion encerrada entre parentesis ('(2*3)')
def p_factor_expr(p):
    'factor : PARA expression PARC'
    p[0] = p[2]


# Error rule for syntax errors
def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

# Build the parser
parser = yacc.yacc()
parser = yacc.parse(lexer=x, debug=True)




