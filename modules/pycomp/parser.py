#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .lexer import Lexer

from ply import yacc
class Parser(object):

    outputdir = "/tmp"
    precedence = (
        ('left', 'SUMA', 'RESTA'),
        ('left', 'MULT', 'DIV'),
    )

    reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'print': 'PRINT',
    'int': 'INT'
    }

    tokens = [
        "ID", "CTE", "SUMA","RESTA", "MULT", "DIV", "PARA", "PARC", 
        "LLAVEA", "LLAVEC", "ASIG", "OR", "AND", "IGUALA", "DIST",
        "MENOR", "MENORIGUAL", "MAYOR", "MAYORIGUAL"
    ] + list(reserved.values())


    err = []
    ipolish = []
    stack_while = []
    stack_if = []
    stack_nestings = []
    stack_comparators = []

    local = {}

    def __init__(self, lexer: Lexer):
        self.lexer = lexer

    def check_limit_nested_statements(self, stack):
        if len(stack) > 3:
            e = "[ERR] More than 3-level nested statements are not allowed"
            self.err.append(e)
            self.ipolish = []
            raise(SyntaxError)

    def p_statement_prog(self, p):
        'program : program statement'
        pass

    def p_statement_prog_s(self, p):
        'program : statement'
        pass

    def p_statement_print(self, p):
        'statement : print_statement'
        pass

    def p_comp_statement(self, p):
        'statement : comp_statement'
        pass

    def p_logic_statement(self, p):
        'statement : logic_statement'
        pass

    def p_while_statement(self, p):
        'statement : while_statement'
        pass

    def p_if_statement(self, p):
        'statement : if_statement'
        pass

    def p_expr_statement(self, p):
        'statement : expression'
        pass

    def p_statement_decl(self, p):
        'statement : LLAVEA INT block_decl'
        pass

    def p_block_decl(self, p):
        'block_decl : ID LLAVEC'
        if(len(self.stack_nestings) > 0):
            self.lexer.ts.addSymbol(p[1] + '%' + str(len(self.stack_nestings)), p[1], p[1], 0, True)
            self.local['level' + str(len(self.stack_nestings))].append(p[1])
        else:
            self.lexer.ts.setDeclaration(p[1])


    def p_block_decl2(self, p):
        'block_decl : ID OR other_decl'
        if(len(self.stack_nestings) > 0):
            self.lexer.ts.addSymbol(p[1] + '%' + str(len(self.stack_nestings)), p[1], p[1], 0, True)
            self.local['level' + str(len(self.stack_nestings))].append(p[1])
        else:
            self.lexer.ts.setDeclaration(p[1])

        
    def p_block_decl3(self, p):
        'other_decl : block_decl'
        pass

    def p_statement_asig(self, p):
        'statement : ID ASIG expression'
        self.ipolish.append(p[1])
        self.ipolish.append(p[2])


    def p_expression(self, p):
        'expression : term'

    def p_expression_suma(self, p):
        'expression : expression SUMA term'
        self.ipolish.append("+")

    def p_expression_resta(self, p):
        'expression : expression RESTA term'
        self.ipolish.append("-")

    def p_term(self, p):
        'term : factor'

    def p_expression_mult(self, p):
        'term : term MULT factor'
        self.ipolish.append("*")

    def p_expression_div(self, p):
        'term : term DIV factor'
        self.ipolish.append("/")

    def p_factor_par(self, p):
        'factor : PARA expression PARC'

    def p_factor_1(self, p):
        'factor : ID'
        self.ipolish.append(p[1])

    def p_factor_2(self, p):
        'factor : CTE'
        self.ipolish.append(p[1])

    def p_print(self, p):
        'print_statement : PRINT PARA expression PARC'
        self.ipolish.append("PRNT")

    def p_comparator_iguala(self, p):
        'comp_statement : expression IGUALA factor'
        self.ipolish.append("==")

    def p_comparator_dist(self, p):
        'comp_statement : expression DIST factor'
        self.ipolish.append("<>")
        
    def p_comparator_menor(self, p):
        'comp_statement : expression MENOR factor'
        self.ipolish.append("<")
        
    def p_comparator_menorigual(self, p):
        'comp_statement : expression MENORIGUAL factor'
        self.ipolish.append("<=")
        
    def p_comparator_mayor(self, p):
        'comp_statement : expression MAYOR factor'
        self.ipolish.append(">")
        
    def p_comparator_mayorigual(self, p):
        'comp_statement : expression MAYORIGUAL factor'
        self.ipolish.append(">=")

    def p_logic_expr_or(self, p):
        'logic_statement : comp_statement OR comp_expression'
        self.ipolish.append("|")

    def p_logic_expr_and(self, p):
        'logic_statement : comp_statement AND comp_expression'
        self.ipolish.append("&")

    def p_comp_expression(self, p):
        'comp_expression : comp_statement'
        pass

    def p_subprogram(self, p):
        'sub_program : program LLAVEC'
        pass
        
    def p_condicion_while(self, p):
        '''cond_while : comp_statement
                    | logic_statement'''
        self.ipolish.append("wfree") #reservo un espacio en la lista
        self.ipolish.append("BF") #el siguiente espacio pongo BF
        self.stack_while.append(len(self.ipolish)-2) #en la pila while apilo el numero de pos del lugar vacio antes del BF para completar despues

    def p_while(self, p): 
        'while : WHILE'
        self.stack_while.append(len(self.ipolish)) #apilo el nro de paso actual cuando encuentro el while
        self.stack_nestings.append("WHILE") #registro que entro en un while: apilo
        self.check_limit_nested_statements(self.stack_nestings) #verifico que no sean mas de tres anidamientos

    def p_iter_while(self, p):
        'while_statement : while PARA cond_while PARC LLAVEA sub_program'
        self.ipolish.append("wfree") #reservo otro espacio vacio
        self.ipolish.append("BI") #el siguiente espacio pongo BI
        self.ipolish[self.stack_while.pop()] = len(self.ipolish) #desapilo la posicion guardada y en ese posicion agrego la posicion siguiente a la actual
        self.ipolish[len(self.ipolish)-2] = self.stack_while.pop() #desapilo la otra posicion guardada y la asigno como valor en la casilla anterior a la posicion actual
        self.stack_nestings.pop() #si se cumple esta regla entonces el while fue parseado, desapilo

    def p_condicion_if(self, p):
        '''cond_if : comp_statement
                | logic_statement'''

        self.ipolish.append("ifree") #reservo un espacio vacio
        self.stack_if.append(len(self.ipolish)-1) #apilo en self.stack_if la posicion actual
        self.ipolish.append("BF") #el siguiente espacio pongo BF
        

    def p_if_fcpo_1(self, p):
        'fcpo1 : sub_program'
        self.ipolish.append("ifree") #reservo otro espacio vacio
        self.stack_if.append(len(self.ipolish)-1) #apilo en self.stack_if la posicion actual
        self.ipolish.append("BI") #el siguiente espacio pongo BI
        self.stack_if.append(len(self.ipolish)) #apilo en self.stack_if la posicion siguiente a la actual

    def p_if_fcpo_2(self, p):
        'fcpo2 : sub_program'
        pass

    def p_if(self, p):
        'if : IF'
        self.lexer.ts.addCheckPoint("CHKP" + str(len(self.stack_nestings)), "IF")
        self.stack_nestings.append("IF")
        self.check_limit_nested_statements(self.stack_nestings)
        self.local['level' + str(len(self.stack_nestings))] = []
        

    def p_selection_if(self, p):
        'if_statement : if PARA cond_if PARC LLAVEA fcpo1 else_statement'
        self.lexer.ts.__str__()
        self.lexer.ts.removeUntilCHKP()
        despues_BI  = self.stack_if.pop()
        self.ipolish[self.stack_if.pop()] = len(self.ipolish)
        self.ipolish[self.stack_if.pop()] = despues_BI 
        self.stack_nestings.pop() 

    def p_condition_else(self, p):
        '''else_statement : ELSE LLAVEA fcpo2
                        | empty'''
        pass

    def p_empty(self, p):
        'empty :'
        pass

    def p_error(self, p):
        if p:
            e = "[ERR] Syntax error at '"+ p.value + "'"
        else:
            e = "[ERR] Syntax error at EOF"
        self.err.append(e)

    def get_info(self):
        return "\n".join(
            [
                "",
                "Errors:",
                "\n".join(self.err),
                "",
                str(self.lexer.ts.table),
                "",
                f"stack_if: {str(self.stack_if)}" 
            ]
        )

    def parse(self, get_info=False):
        self.yacc = yacc.yacc(
            module=self, # creo un objeto yacc y le pasamos a traves del metodo yacc() el objeto donde se encuentran los metodos p_ poniendo module
            outputdir=self.outputdir
        )
        self.parsed = self.yacc.parse(lexer=self.lexer, debug=False)
        if get_info:
            print(self.get_info())
        return self.ipolish



















