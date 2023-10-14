
#importo biblioteca pandas
import pandas as pd
import symbolTable as st
import lexToken as lt

class Lexer(object):
    
    cache = ""
    
#                     L   D   =  \n  "" EOF 
    state_matrix = [[ 1,  2,  3,  0,  0, -1], #inicial
                    [ 1,  1, -1, -1, -1, -1], #ID
                    [-1,  2, -1, -1, -1, -1], #CTE
                    [-1, -1, -1, -1, -1, -1], #ASIG
                    ]
    #                  L   D   #   =   >   <  +   -   *   /   (    )  {    }  &   |   \t  \n  "" EOF 

    #                 L   D  =  \n  "" EOF 
    unread_matrix =[[0,  0,  0,  0,  0,  0], #inicial
                    [0,  0,  1,  0,  0,  0], #ID
                    [1,  0,  1,  0,  0,  0], #CTE
                    [1,  1,  0,  0,  0,  0], #ASIG
                    ]
    #                 L   D   #   =   >   <  +   -   *   /   (    )  {    }  &   |   \t  \n  "" EOF 

    #                   L   D       =       \n   ""   EOF 
    token_matrix = [[ None,  None,  None,  None,  None,  None], #inicial
                    [ None,  None, "ID", "ID", "ID"], #ID
                    ["CTE",  None, "CTE", "CTE", "CTE", "CTE"], #CTE
                    ["ASIG", "ASIG",  None, "ASIG", "ASIG", "ASIG"], #ASIG
                    ]
    #                   L   D    #    =    >    <    +    -    *    /    (    )    {    }    &    |   \t   \n   ""   EOF 

    def _function_matrix_generator(self):
        return [
            [self.f1, self.f1, self.fn, self.fn, self.fn, self.fn], #inicial
            [self.f3, self.f3, self.f4, self.f4, self.f4, self.f4], #ID
            [self.f4, self.f6, self.f4, self.f4, self.f4, self.f4],
            [self.fn, self.fn, self.fn, self.fn, self.fn, self.fn]]
    
    def __init__(self, filename = None):
        self.token_list = pd.DataFrame()
        self.token_list["name"] = ["ID", "CTE", "ASIG"]
        self.token_list["value"] = [None, None, "="]
        self.function_matrix = self._function_matrix_generator()
        self.ts = st.SymbolTable("DummyLexer EV S2")
        self.position = 0
        with open(filename, 'r') as f:
            self.content = f.read()
    
    #funcion de eventos: segun que sea el caracter leido retornara un id numerico
    def _getEven(self, char: str) -> int:
        if(char.isalpha() and char != "EOF"):
            return 0
        elif(char.isnumeric()):
            return 1
        elif(char == '='):
            return 2
        elif(char.startswith('\n')):
            return 3
        elif(char == ' '):
            return 4
        elif(char == 'EOF'):
            return 5
        else:
            return -1

  #funcion que retorna un caracter leido
    def _getChar(self, buffer = None):
        if(self.position >= len(buffer)):
            return 'EOF'
        else:
            res = buffer[self.position]
            self.position += 1
        return res

  #funcion para hacer unreads
    def _unreadChar(self):
        self.position -= 1


    def f1(self, c):
        self.cache = c

    #verifica si la longitud del ID no sobrepasa la permitida, si no es el caso agrega la nueva letra al string
    # y aumenta en 1 el contador de longitud actual del ID.
    def f3(self, c):
        self.cache = self.cache + c

    #verifica si el ID conformado no esta presente en TS.
    # Si no está, lo agrega.
    def f4(self, c):
        # if self.ts.checkIfExist(self.cache):
        #     pass
        # else:
        self.ts.addSymbol(self.cache, self.cache, 1, False)

    #agrega el digito recibido a la constante
    def f6(self, c):
        self.cache += c

    #funcion nula
    def fn(self, c):
        None


    def token(self):
        
        #print("a")
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
        
        #print("b")
        
        #consulto matriz de tokens para asignar el id
        tokenId = self.token_matrix[last_state][column]
            
        #inicializo la variable que contendrá el tipo del token:
        tokenType = ""
        #inicializo la variable que contendrá el lexema del token:
        tokenValue = ""
        
        #print("c")
        
        #se asigna -1 cuando se alcanza el EOF
        if(tokenId != None):
            #defino el tipo del token obtenido consultando en la lista de tokens
            tokenType = (self.token_list[self.token_list["name"] == tokenId]["name"]).iloc[0]
            #print("ca")
            if(tokenId != "ASIG"):
                #print("ca1")
                tokenValue = self.ts.getSymbolByID(self.cache)["name"].iloc[0]
                print("CTE/ID: ", tokenType, " val: ", tokenValue)
            else:
                #print("ca3")
                tokenValue = (self.token_list.loc[self.token_list["name"] == tokenId]["value"]).iloc[0]
                
                print("ASIG val: ", tokenValue)
            #teniendo todos los atributos del token definidos se procede a crear el objeto token y devolverlo
            #print("d1")
            tok = lt.LexToken(tokenType, tokenValue)
            print(tok.__str__())
            return tok
        else:
            #print("d2")
            #si se alcanzo EOF retorno None
            return None
        
        

