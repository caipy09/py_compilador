
############################################
#Codigo para probar el funcionamiento del lexico y sintactico
############################################
#importo biblioteca pandas
#import pandas as pd
#importo codigo de la ts y el lexer
import lexer as lex

#import symbolTable as st
#creo el objeto lexer
lexer = lex.Lexer(filename='C:/Users/ferna/Onedrive/Documents/GitHub/py_compilador/test.txt')

###############################################################
#prueba del sintactico

#importar el sintactico de ply
import ply.yacc as yacc

tokens = (
    'ID', 'CTE', 'ASIG',
)

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
)


def p_program_1(p):
    'program : program statement'
    #print(p[1])

def p_program_2(p):
    'program : statement'
    #print(p[1])

def p_statement_assign(p):
    'statement : ID ASIG expression'
    #print("[DEBUG]: p[1]: ", p[1], " = ", " p[3]: ", p[3])
    lexer.ts.setSymbolValue(p[1], p[3])
    lexer.ts.addSymbol(str(int(p[3])), str(int(p[3])), str(int(p[3])), len(str(int(p[3]))), None) #agrega constante calculada
    

def p_statement_expr(p):
    'statement : expression'
    #print(p[1])


def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]


def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[2]


def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]


def p_expression_number(p):
    "expression : CTE"
    p[0] = p[1]


def p_expression_name(p):
    "expression : ID"
    try:
        p[0] = p[1]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

# Build the parser
yacc.yacc(write_tables=False)
yacc.parse(lexer=lexer, debug=False)


lexer.ts.__str__()
#print("polaca_inversa: ", polaca_inversa)
