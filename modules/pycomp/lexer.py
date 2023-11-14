#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from .symboltable import SymbolTable
from .lextoken import LexToken


class Lexer(object):
    
    cache = ""
    
#                  L   D   #   =   >   <  +   -   *   /   (    )  {    }  &   |   \t  \n  "" EOF 
    state_matrix = [[ 1,  2,  3,  4,  6,  8, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,  0,  0,  0, -1], #inicial
                    [ 1,  1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], #ID
                    [-1,  2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], #CTE
                    [ 3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  0,  3,  0], #comentario
                    [-1, -1, -1,  5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], #ASIG
                    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], #IGUALA
                    [-1, -1, -1,  7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], #MAYOR
                    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], #MAYORIGUAL
                    [-1, -1, -1,  9, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], #MENOR
                    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], #MENORIGUAL
                    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], #DIST
                    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], #SUMA
                    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], #RESTA
                    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], #MULT
                    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], #DIV
                    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], #PARA
                    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], #PARC
                    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], #LLAVEA
                    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], #LLAVEC
                    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], #AND
                    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]] #OR
    #                  L   D   #   =   >   <  +   -   *   /   (    )  {    }  &   |   \t  \n  "" EOF 

    #                 L   D   #   =   >   <  +   -   *   /   (    )  {    }  &   |   \t  \n  "" EOF 
    unread_matrix =[[0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0], #inicial
                    [0,  0,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  0,  0,  0,  0], #ID
                    [1,  0,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  0,  0,  0,  0], #CTE
                    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0], #comentario
                    [1,  1,  1,  0,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  0,  0,  0,  0], #ASIG
                    [1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  0,  0,  0,  0], #IGUALA
                    [1,  1,  1,  0,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  0,  0,  0,  0], #MAYOR
                    [1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  0,  0,  0,  0], #MAYORIGUAL
                    [1,  1,  1,  0,  0,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  0,  0,  0,  0], #MENOR
                    [1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  0,  0,  0,  0], #MENORIGUAL
                    [1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  0,  0,  0,  0], #DIST
                    [1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  0,  0,  0,  0], #SUMA
                    [1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  0,  0,  0,  0], #RESTA
                    [1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  0,  0,  0,  0], #MULT
                    [1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  0,  0,  0,  0], #DIV
                    [1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  0,  0,  0,  0], #PARA
                    [1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  0,  0,  0,  0], #PARC
                    [1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  0,  0,  0,  0], #LLAVEA
                    [1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  0,  0,  0,  0], #LLAVEC
                    [1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  0,  0,  0,  0], #AND
                    [1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  0,  0,  0,  0]] #OR
    #                 L   D   #   =   >   <  +   -   *   /   (    )  {    }  &   |   \t  \n  "" EOF 

    #                   L   D    #    =    >    <    +    -    *    /    (    )    {    }    &    |   \t   \n   ""   EOF 
    token_matrix = [[ None,  None,  None,  None,  None,  None,  None,  None,  None,  None,  None,  None,  None,  None,  None,  None,  None,  None,  None,  None], #inicial
                    [ None,  None, "ID", "ID", "ID", "ID", "ID", "ID", "ID", "ID", "ID", "ID", "ID", "ID", "ID", "ID", "ID", "ID", "ID", "ID"], #ID
                    ["CTE",  None, "CTE", "CTE", "CTE", "CTE", "CTE", "CTE", "CTE", "CTE", "CTE", "CTE", "CTE", "CTE", "CTE", "CTE", "CTE", "CTE", "CTE", "CTE"], #CTE
                    [ None,  None,  None,  None,  None,  None,  None,  None,  None,  None,  None,  None,  None,  None,  None,  None,  None,  None,  None,  None], #comentario
                    ["ASIG", "ASIG", "ASIG",  None, "ASIG", "ASIG", "ASIG", "ASIG", "ASIG", "ASIG", "ASIG", "ASIG", "ASIG", "ASIG", "ASIG", "ASIG", "ASIG", "ASIG", "ASIG", "ASIG"], #ASIG
                    ["IGUALA", "IGUALA", "IGUALA", "IGUALA", "IGUALA", "IGUALA", "IGUALA", "IGUALA", "IGUALA", "IGUALA", "IGUALA", "IGUALA", "IGUALA", "IGUALA", "IGUALA", "IGUALA", "IGUALA", "IGUALA", "IGUALA", "IGUALA"], #IGUALA
                    ["MAYOR", "MAYOR", "MAYOR",  None,  None, "MAYOR", "MAYOR", "MAYOR", "MAYOR", "MAYOR", "MAYOR", "MAYOR", "MAYOR", "MAYOR", "MAYOR", "MAYOR", "MAYOR", "MAYOR", "MAYOR", "MAYOR"], #MAYOR
                    ["MAYORIGUAL", "MAYORIGUAL", "MAYORIGUAL", "MAYORIGUAL", "MAYORIGUAL", "MAYORIGUAL", "MAYORIGUAL", "MAYORIGUAL", "MAYORIGUAL", "MAYORIGUAL", "MAYORIGUAL", "MAYORIGUAL", "MAYORIGUAL", "MAYORIGUAL", "MAYORIGUAL", "MAYORIGUAL", "MAYORIGUAL", "MAYORIGUAL", "MAYORIGUAL", "MAYORIGUAL"], #MAYORIGUAL
                    ["MENOR", "MENOR", "MENOR",  None,  None, "MENOR", "MENOR", "MENOR", "MENOR", "MENOR", "MENOR", "MENOR", "MENOR", "MENOR", "MENOR", "MENOR", "MENOR", "MENOR", "MENOR", "MENOR"], #MENOR
                    ["MENORIGUAL", "MENORIGUAL", "MENORIGUAL", "MENORIGUAL", "MENORIGUAL", "MENORIGUAL", "MENORIGUAL", "MENORIGUAL", "MENORIGUAL", "MENORIGUAL", "MENORIGUAL", "MENORIGUAL", "MENORIGUAL", "MENORIGUAL", "MENORIGUAL", "MENORIGUAL", "MENORIGUAL", "MENORIGUAL", "MENORIGUAL", "MENORIGUAL"], #MENORIGUAL
                    ["DIST", "DIST", "DIST", "DIST", "DIST", "DIST", "DIST", "DIST", "DIST", "DIST", "DIST", "DIST", "DIST", "DIST", "DIST", "DIST", "DIST", "DIST", "DIST", "DIST"], #DIST
                    ["SUMA", "SUMA", "SUMA", "SUMA", "SUMA", "SUMA", "SUMA", "SUMA", "SUMA", "SUMA", "SUMA", "SUMA", "SUMA", "SUMA", "SUMA", "SUMA", "SUMA", "SUMA", "SUMA", "SUMA"], #SUMA
                    ["RESTA", "RESTA", "RESTA", "RESTA", "RESTA", "RESTA", "RESTA", "RESTA", "RESTA", "RESTA", "RESTA", "RESTA", "RESTA", "RESTA", "RESTA", "RESTA", "RESTA", "RESTA", "RESTA", "RESTA"], #RESTA
                    ["MULT", "MULT", "MULT", "MULT", "MULT", "MULT", "MULT", "MULT", "MULT", "MULT", "MULT", "MULT", "MULT", "MULT", "MULT", "MULT", "MULT", "MULT", "MULT", "MULT"], #MULT
                    ["DIV", "DIV", "DIV", "DIV", "DIV", "DIV", "DIV", "DIV", "DIV", "DIV", "DIV", "DIV", "DIV", "DIV", "DIV", "DIV", "DIV", "DIV", "DIV", "DIV"], #DIV
                    ["PARA", "PARA", "PARA", "PARA", "PARA", "PARA", "PARA", "PARA", "PARA", "PARA", "PARA", "PARA", "PARA", "PARA", "PARA", "PARA", "PARA", "PARA", "PARA", "PARA"], #PARA
                    ["PARC", "PARC", "PARC", "PARC", "PARC", "PARC", "PARC", "PARC", "PARC", "PARC", "PARC", "PARC", "PARC", "PARC", "PARC", "PARC", "PARC", "PARC", "PARC", "PARC"], #PARC
                    ["LLAVEA", "LLAVEA", "LLAVEA", "LLAVEA", "LLAVEA", "LLAVEA", "LLAVEA", "LLAVEA", "LLAVEA", "LLAVEA", "LLAVEA", "LLAVEA", "LLAVEA", "LLAVEA", "LLAVEA", "LLAVEA", "LLAVEA", "LLAVEA", "LLAVEA", "LLAVEA"], #LLAVEA
                    ["LLAVEC", "LLAVEC", "LLAVEC", "LLAVEC", "LLAVEC", "LLAVEC", "LLAVEC", "LLAVEC", "LLAVEC", "LLAVEC", "LLAVEC", "LLAVEC", "LLAVEC", "LLAVEC", "LLAVEC", "LLAVEC", "LLAVEC", "LLAVEC", "LLAVEC", "LLAVEC"], #LLAVEC
                    ["AND", "AND", "AND", "AND", "AND", "AND", "AND", "AND", "AND", "AND", "AND", "AND", "AND", "AND", "AND", "AND", "AND", "AND", "AND", "AND"], #AND
                    ["OR", "OR", "OR", "OR", "OR", "OR", "OR", "OR", "OR", "OR", "OR", "OR", "OR", "OR", "OR", "OR", "OR", "OR", "OR", "OR"]] #OR
    #                   L   D    #    =    >    <    +    -    *    /    (    )    {    }    &    |   \t   \n   ""   EOF 

    def _function_matrix_generator(self):
        return [
            [self.f1, self.f2, self.fn, self.fn, self.fn, self.fn, self.fn, self.fn, self.fn, self.fn, self.fn, self.fn, self.fn, self.fn, self.fn, self.fn, self.fn, self.fn, self.fn, self.fn], #inicial
            [self.f3, self.f3, self.f4, self.f4, self.f4, self.f4, self.f4, self.f4, self.f4, self.f4, self.f4, self.f4, self.f4, self.f4, self.f4, self.f4, self.f4, self.f4, self.f4, self.f4], #ID
            [self.f5, self.f6, self.f5, self.f5, self.f5, self.f5, self.f5, self.f5, self.f5, self.f5, self.f5, self.f5, self.f5, self.f5, self.f5, self.f5, self.f5, self.f5, self.f5, self.f5]
        ]+[[self.fn] * 20] * 18
    
    def __init__(self, filename = None):
        self.token_list = pd.DataFrame()
        self.token_list["id"] = ["ID", "CTE", "IF", "ELSE", "WHILE", "PRINT", "INT", "ASIG", "IGUALA", "MAYOR", "MAYORIGUAL", "MENOR", "MENORIGUAL", "DIST", "SUMA", "RESTA", "MULT", "DIV", "PARA", "PARC", "LLAVEA", "LLAVEC", "AND", "OR"]
        self.token_list["value"] = [None, None, "if", "else", "while", "print", "int", "=", "==", ">", ">=", "<", "<=", "<>", "+", "-", "*", "/", "(", ")", "{", "}", "&", "|"]

        self.ts = SymbolTable("Lexer")

        #palabras reservadas
        self.keywords = pd.DataFrame()
        self.keywords["id"] = ["IF", "ELSE", "WHILE", "PRINT", "INT"]
        self.keywords["value"] = ["if", "else", "while", "print", "int"]

        self.position = 0
        self.function_matrix = self._function_matrix_generator()
        with open(filename, 'r') as f:
            self.content = f.read()
    
    #funcion de eventos: segun que sea el caracter leido retornara un id numerico
    def _getEven(self, char: str) -> int:
        if(char.isalpha() and char != "EOF"):
            return 0
        elif(char.isnumeric()):
            return 1
        elif(char == '#'):
            return 2
        elif(char == '='):
            return 3
        elif(char == '>'):
            return 4
        elif(char == '<'):
            return 5
        elif(char == '+'):
            return 6
        elif(char == '-'):
            return 7
        elif(char == '*'):
            return 8
        elif(char == '/'):
            return 9
        elif(char == '('):
            return 10
        elif(char == ')'):
            return 11
        elif(char == '{'):
            return 12
        elif(char == '}'):
            return 13
        elif(char == '&'):
            return 14
        elif(char == '|'):
            return 15
        elif(char.startswith('\t')):
            return 16
        elif(char.startswith('\n')):
            return 17
        elif(char == ' '):
            return 18
        elif(char == 'EOF'):
            return 19
        else:
            return -1

  #funcion que retorna un caracter leido
    def _getChar(self, buffer: str) -> str:
        if(self.position >= len(buffer)):
            return 'EOF'
        else:
            res = buffer[self.position]
            self.position += 1
        return res

  #funcion para hacer unreads
    def _unreadChar(self):
        self.position -= 1

  #funcion que retorna T o F segun sea o no palabra reservada
    def _is_keyword(self, t):
        return (self.keywords["value"] == t).any()

    def f1(self, c):
        self.cache = c

    #inicia el string de CTE con un digito
    def f2(self, c):
        self.cache = c

    #verifica si la longitud del ID no sobrepasa la permitida, si no es el caso agrega la nueva letra al string
    # y aumenta en 1 el contador de longitud actual del ID.
    def f3(self, c):
        self.cache = self.cache + c

    #verifica si el ID conformado no esta presente en TS.
    # Si no está, lo agrega.
    def f4(self, c):
        pass
        if self._is_keyword(self.cache):
            pass
        else:
            #print("deb:" ,self.ts.checkIfExist(self.cache))
            if self.ts.checkIfExist(self.cache):
                pass
            else:
                self.ts.addSymbol(self.cache, self.cache, self.cache, 0, False)


    #verifica si la CTE conformada no esta presente en TS.
    # Si no está, la agrega.
    def f5(self, c):
        if self.ts.checkIfExist(self.cache):
            pass
        else:
            self.ts.addSymbol(self.cache, self.cache, self.cache, len(self.cache), None)

    #agrega el digito recibido a la constante
    def f6(self, c):
        self.cache += c

    #funcion nula
    def fn(self, c):
        None
    
    
    
    def token(self):
        # defino estados 
        state = 0
        final_state = -1
        last_state = 0
        # mientras no sea el estado final
        while state != final_state:
            c = self._getChar(self.content)
            column = self._getEven(c)
            self.function_matrix[state][column](c)
            last_state = state
            state = self.state_matrix[state][column]
        #consulto la matriz de unreads para realizar la acción si es necesaria
        if self.unread_matrix[last_state][column] == 1:
            self._unreadChar()
        #consulto matriz de tokens para asignar el id
        tokenId = self.token_matrix[last_state][column]
        #si ocurre que el tokenId es 256 (un identificador) y ese identificador existe dentro
        # de la tabla de palabras reservadas, entonces es una palabra reservada y le reasigno el tokenId correspondiente
        if(tokenId == "ID" and self._is_keyword(self.cache)): 
            tokenId = (self.keywords[self.keywords["value"] == self.cache]["id"]).iloc[0]
        #inicializo la variable que contendrá el tipo del token:
        tokenType = ""
        #inicializo la variable que contendrá el lexema del token:
        tokenValue = ""
        #se asigna -1 cuando se alcanza el EOF
        if(tokenId != None):
            #defino el tipo del token obtenido consultando en la lista de tokens
            tokenType = (self.token_list[self.token_list["id"] == tokenId]["id"]).iloc[0]
            if(tokenId == "CTE" or tokenId == "ID"):
                tokenValue = self.ts.getSymbolByID(self.cache)["name"].iloc[0]
            else:
                tokenValue = (self.token_list.loc[self.token_list["id"] == tokenId]["value"]).iloc[0]
            #teniendo todos los atributos del token definidos se procede a crear el objeto token y devolverlo
            return LexToken(tokenType, tokenValue)
        else:
            #si se alcanzo EOF retorno None
            return None
        
        

