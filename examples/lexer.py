
#importo biblioteca pandas
import pandas as pd

#clase LexToken: la clase creará un objeto de este tipo y le asignará su type and value ya definidos para despues retornarlo
class LexToken(object):
    
    #variables
    type = ""
    tokenId = ""
    value = ""
    
    #constructor
    def __init__(self, att_type, att_tokenId, att_value):
        self.type = att_type
        self.tokenId = att_tokenId
        self.value = att_value
    
    #metodo para impresion de tokens
    def __str__(self):
        return f'TOKEN <Type: {self.type}, id: {self.tokenId}, Value: {self.value}>'
    
    #Validacion de tokens: un token es valido si su 'value' esta entre 256 y 279
    def isValidToken(self):
        flag = self.value >= 256 and self.value <= 279
        return flag

class SymbolTable(object):
    
    table = pd.DataFrame()

    def __init__(self):

        #tabla de simbolos con columnas principales
        self.table["nombre"] = None
        self.table["valor"] = None
        self.table["longitud"] = None
        self.table["declarado"] = None

    #metodo para impresion de la TS
    def __str__(self):
        print("===================")    
        print("Tabla de simbolos:")
        print("===================")
        print(self.table)
        
    #obtener la tabla de simbolos
    def getSymbolTable(self):
        return self.table
    
    #agrega un guionbajo al string que recibe
    def addUnderscore(self, name):
        aux = ("_" + str(name))
        return aux
    
    #agregar registro a la tabla de simbolos
    def addSymbol(self, name, value, leng, decl):
        if self.checkIfExist(value):
            pass
        else:
            row = [self.addUnderscore(name), value, leng, decl]
            self.table.loc[len(self.table)] = row
    
    #verificar si un registro existe en ts, mediante el nombre
    def checkIfExist(self, name):
        return (self.getSymbolTable()["nombre"] == self.addUnderscore(name)).any()
    
    #obtener una fila de la TS, segun el nombre
    def getSymbolByName(self, name):
        return self.getSymbolTable()[self.getSymbolTable()["nombre"] == self.addUnderscore(name)]
    
    #modificar valor de un registro, dado su nombre
    def setSymbolValue(self, name=None, value=None):
        self.table.loc[self.table["nombre"] == self.addUnderscore(name), "valor"] = value
        
    #modificar valor de longitud de un simbolo
    def setSymbolLength(self, name, leng):
        self.table.loc[self.table["nombre"] == self.addUnderscore(name), "longitud"] = leng
        
    def setDeclaration(self, name):
        self.table.loc[self.table["nombre"] == self.addUnderscore(name), "declarado"] = True

    def getDeclaration(self, name):
        return self.table.loc[self.table["nombre"] == self.addUnderscore(name), "declarado"]


#clase principal Lexer: el analizador léxico propiamente definido.
class Lexer(object):

    #variables
    identificator = ""
    constant_number = ""
    LONG_MAX_ID = 6
    long_id = 0
    

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
    token_matrix = [[ -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1], #inicial
                    [ -1,  -1, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256], #ID
                    [257,  -1, 257, 257, 257, 257, 257, 257, 257, 257, 257, 257, 257, 257, 257, 257, 257, 257, 257, 257], #CTE
                    [ -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1], #comentario
                    [263, 263, 263,  -1, 263, 263, 263, 263, 263, 263, 263, 263, 263, 263, 263, 263, 263, 263, 263, 263], #ASIG
                    [264, 264, 264, 264, 264, 264, 264, 264, 264, 264, 264, 264, 264, 264, 264, 264, 264, 264, 264, 264], #IGUALA
                    [268, 268, 268,  -1,  -1, 268, 268, 268, 268, 268, 268, 268, 268, 268, 268, 268, 268, 268, 268, 268], #MAYOR
                    [269, 269, 269, 269, 269, 269, 269, 269, 269, 269, 269, 269, 269, 269, 269, 269, 269, 269, 269, 269], #MAYORIGUAL
                    [266, 266, 266,  -1,  -1, 266, 266, 266, 266, 266, 266, 266, 266, 266, 266, 266, 266, 266, 266, 266], #MENOR
                    [267, 267, 267, 267, 267, 267, 267, 267, 267, 267, 267, 267, 267, 267, 267, 267, 267, 267, 267, 267], #MENORIGUAL
                    [265, 265, 265, 265, 265, 265, 265, 265, 265, 265, 265, 265, 265, 265, 265, 265, 265, 265, 265, 265], #DIST
                    [272, 272, 272, 272, 272, 272, 272, 272, 272, 272, 272, 272, 272, 272, 272, 272, 272, 272, 272, 272], #SUMA
                    [273, 273, 273, 273, 273, 273, 273, 273, 273, 273, 273, 273, 273, 273, 273, 273, 273, 273, 273, 273], #RESTA
                    [274, 274, 274, 274, 274, 274, 274, 274, 274, 274, 274, 274, 274, 274, 274, 274, 274, 274, 274, 274], #MULT
                    [275, 275, 275, 275, 275, 275, 275, 275, 275, 275, 275, 275, 275, 275, 275, 275, 275, 275, 275, 275], #DIV
                    [276, 276, 276, 276, 276, 276, 276, 276, 276, 276, 276, 276, 276, 276, 276, 276, 276, 276, 276, 276], #PARA
                    [277, 277, 277, 277, 277, 277, 277, 277, 277, 277, 277, 277, 277, 277, 277, 277, 277, 277, 277, 277], #PARC
                    [278, 278, 278, 278, 278, 278, 278, 278, 278, 278, 278, 278, 278, 278, 278, 278, 278, 278, 278, 278], #LLAVEA
                    [279, 279, 279, 279, 279, 279, 279, 279, 279, 279, 279, 279, 279, 279, 279, 279, 279, 279, 278, 279], #LLAVEC
                    [270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270, 270], #AND
                    [271, 271, 271, 271, 271, 271, 271, 271, 271, 271, 271, 271, 271, 271, 271, 271, 271, 271, 271, 271]] #OR
    #                   L   D    #    =    >    <    +    -    *    /    (    )    {    }    &    |   \t   \n   ""   EOF 

    def _function_matrix_generator(self):
        return [
            [self.f1, self.f2, self.fn, self.fn, self.fn, self.fn, self.fn, self.fn, self.fn, self.fn, self.fn, self.fn, self.fn, self.fn, self.fn, self.fn, self.fn, self.fn, self.fn, self.fn], #inicial
            [self.f3, self.f3, self.f4, self.f4, self.f4, self.f4, self.f4, self.f4, self.f4, self.f4, self.f4, self.f4, self.f4, self.f4, self.f4, self.f4, self.f4, self.f4, self.f4, self.f4], #ID
            [self.f5, self.f6, self.f5, self.f5, self.f5, self.f5, self.f5, self.f5, self.f5, self.f5, self.f5, self.f5, self.f5, self.f5, self.f5, self.f5, self.f5, self.f5, self.f5, self.f5]
        ]+[[self.fn] * 20] * 18
               

    def __init__(self, filename, ts):

        self.token_list = pd.DataFrame()
        self.token_list["id"] = [256, 257, 258, 259, 260, 261, 262, 263, 264, 268, 269, 266, 267, 265, 272, 273, 274, 275, 276, 277, 278, 279, 270, 271]
        self.token_list["nombre"] = ["ID", "CTE", "IF", "ELSE", "WHILE", "PRINT", "INT", "ASIG", "IGUALA", "MAYOR", "MAYORIGUAL", "MENOR", "MENORIGUAL", "DIST", "SUMA", "RESTA", "MULT", "DIV", "PARA", "PARC", "LLAVEA", "LLAVEC", "AND", "OR"]
        self.token_list["valor"] = ["NA", "NA", "if", "else", "while", "print", "int", "=", "==", ">", ">=", "<", "<=", "<>", "+", "-", "*", "/", "(", ")", "{", "}", "&", "|"]

        self.ts = ts

        #palabras reservadas
        self.keywords = pd.DataFrame()
        self.keywords["id"] = [258, 259, 260, 261, 262]
        self.keywords["valor"] = ["if", "else", "while", "print", "int"]

        self.position = 0
        self.function_matrix = self._function_matrix_generator()
        with open(filename, 'r') as f:
            self.content = f.read()


    #comprueba la limitacion impuesta de 16 bits
    def _is16bit(self, cons):
        return int(cons) < 65536

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
        return (self.keywords["valor"] == t).any()

    def f1(self, c):
        self.identificator = c
        self.long_id = 1

    #inicia el string de CTE con un digito
    def f2(self, c):
        self.constant_number = c

    #verifica si la longitud del ID no sobrepasa la permitida, si no es el caso agrega la nueva letra al string
    # y aumenta en 1 el contador de longitud actual del ID.
    def f3(self, c):
        if self.long_id < self.LONG_MAX_ID:
            self.long_id = self.long_id + 1
            self.identificator = self.identificator + c

    #verifica si el ID conformado no esta presente en TS.
    # Si no está, lo agrega.
    def f4(self, c):
        if self._is_keyword(self.identificator):
            pass
        else:
            if self.ts.checkIfExist(self.identificator):
                pass
            else:
                self.ts.addSymbol(self.identificator, self.identificator, self.long_id, False)


    #verifica si la CTE conformada no esta presente en TS.
    # Si no está, la agrega.
    def f5(self, c):
        if self._is16bit(self.constant_number):
                if self.ts.checkIfExist(self.constant_number):
                    pass
                else:
                    self.ts.addSymbol(self.constant_number, self.constant_number, len(self.constant_number), None)

    #agrega el digito recibido a la constante
    def f6(self, c):
        self.constant_number += c

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
        if(tokenId == 256 and self._is_keyword(self.identificator)):
            tokenId = int(self.keywords[self.keywords["valor"] == self.identificator]["id"])
        #inicializo la variable que contendrá el tipo del token:
        tokenType = ""
        #inicializo la variable que contendrá el lexema del token:
        tokenValue = ""
        #se asigna -1 cuando se alcanza el EOF
        if(tokenId != -1):
            #defino el tipo del token obtenido consultando en la lista de tokens
            tokenType = (self.token_list[self.token_list["id"] == tokenId]["nombre"]).iloc[0]
            if(tokenId == 257):
                tokenValue = int(self.ts.getSymbolByName(self.constant_number)["valor"].iloc[0])
            elif(tokenId == 256):
                tokenValue = self.ts.getSymbolByName(self.identificator)["valor"].iloc[0]
            else:
                tokenValue = (self.token_list.loc[self.token_list["id"] == tokenId]["valor"]).iloc[0]
            #teniendo todos los atributos del token definidos se procede a crear el objeto token y devolverlo
            return LexToken(tokenType, tokenId, tokenValue)
        else:
            #si se alcanzo EOF retorno None
            return None
        


