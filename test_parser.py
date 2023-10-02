tokens = (
    'CTE', "SUMA", "RESTA", "MULT", "DIV", "PARA", "PARC",
)


import lex as lex

#analyzer = Analyzer(filename='./test1.txt')
#x = lex.Lexer(filename='C:/Users/ferna/Onedrive/Documents/GitHub/py_compilador/test.txt')
x = lex.Lexer(filename='C:/Users/fheredia/Documents/GitHub/py_compilador/test.txt')

#lexer.token()._str_()


import ply.yacc as yacc

def p_expression_suma(p):
    'expression : expression SUMA term'
    p[0] = p[1] + p[3]

def p_expression_resta(p):
    'expression : expression RESTA term'
    p[0] = p[1] - p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_mult(p):
    'term : term MULT factor'
    p[0] = p[1] * p[3]

def p_term_div(p):
    'term : term DIV factor'
    p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_cte(p):
    'factor : CTE'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : PARA expression PARC'
    p[0] = p[2]

# Error rule for syntax errors
def p_error(p):
    print("Error de sintaxis!!!")

# Build the parser
parser = yacc.yacc()
parser = yacc.parse(lexer=x, debug=True)




