
#importo biblioteca pandas
import pandas as pd

#tabla de simbolos con columnas principales
tabla_simbolos = pd.DataFrame()
tabla_simbolos["nombre"] = None
tabla_simbolos["valor"] = None
tabla_simbolos["longitud"] = None

#palabras reservadas
lista_palabras_reservadas = pd.DataFrame()
lista_palabras_reservadas["id"] = [258, 259, 260, 261, 262]
lista_palabras_reservadas["valor"] = ["if", "else", "while", "print", "int"]

#variables
identificador = ""
constante = ""
LONG_MAX_ID = 6
long_id = 0

#posicion de la lectura
pos = 0
#path del archivo
file = "C:/Users/ferna/Onedrive/Documents/GitHub/py_compilador/test.txt"

#apertura del archivo en modo lectura
f = open(file,'r')

#se lee el contenido del archivo y se lo guarda en su completitud en la variable contents
with open(file) as f:
  contenido = f.read()

#defino la longitud de contents
long_contenido = len(contenido)

#cierro la conexion con el archivo leido
f.close()

############################################
#funciones auxiliares
############################################

#retorna el identificador/constante con un guion bajo al inicio
def agregarGuionBajo(v):
    return "_" + v

#comprueba la limitacion impuesta de 16 bits
def comprobarConstante16bits(cons):
    return int(constante) < 65536

#funcion de eventos: segun que sea el caracter leido retornara un id numerico
def getEven(char):
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
def getChar(buffer):
  global pos
  if(pos >= len(buffer)):
    return 'EOF'
  else:
    res = buffer[pos]
    pos = pos + 1
    return res

#funcion para hacer unreads
def unreadChar():
  global pos
  pos = pos - 1

#funcion que retorna T o F segun sea o no palabra reservada
def esPalabraReservada(t):
    return (lista_palabras_reservadas["valor"] == t).any()
    
############################################
#funciones de la lista de funciones
############################################

#inicia el string de ID con una letra y añade 1 al contador
def f1(c):
    global identificador
    global long_id
    identificador = ""
    identificador = identificador + c
    long_id = 1

#inicia el string de CTE con un digito
def f2(c):
    global constante
    constante = ""
    constante = constante + c

#verifica si la longitud del ID no sobrepasa la permitida, si no es el caso agrega la nueva letra al string
# y aumenta en 1 el contador de longitud actual del ID.
def f3(c):
    global long_id
    global identificador
    if long_id < LONG_MAX_ID:
        long_id = long_id + 1
        identificador = identificador + c

#verifica si el ID conformado no esta presente en TS.
# Si no está, lo agrega.
def f4(c):
    global tabla_simbolos
    if esPalabraReservada(identificador):
        pass
    else:
        if (tabla_simbolos["nombre"] == agregarGuionBajo(identificador)).any():
            pass
        else:
            row = [agregarGuionBajo(identificador), identificador, long_id]
            tabla_simbolos.loc[len(tabla_simbolos)] = row


#verifica si la CTE conformada no esta presente en TS.
# Si no está, la agrega.
def f5(c):
    global tabla_simbolos
    if comprobarConstante16bits(constante):
        if(tabla_simbolos["nombre"] == agregarGuionBajo(constante)).any():
            pass
        else:
            row = [agregarGuionBajo(constante), constante, "-"]
            tabla_simbolos.loc[len(tabla_simbolos)] = row

#agrega el digito recibido a la constante
def f6(c):
    global constante
    constante = constante + c

#funcion nula
def fn(c):
    None
        
############################################
#Matrices
############################################

#                  L   D   #   =   >   <  +   -   *   /   (    )  {    }  &   |   \t  \n  "" EOF 
tabla_estados = [[ 1,  2,  3,  4,  6,  8, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,  0,  0,  0, -1], #inicial
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
tabla_unreads = [[0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0], #inicial
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
tabla_tokens =  [[ -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1], #inicial
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


#                    L   D   #   =   >   <  +   -   *   /   (    )  {    }  &   |   \t  \n  "" EOF 
tabla_funciones = [[f1, f2, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn], #inicial
                   [f3, f3, f4, f4, f4, f4, f4, f4, f4, f4, f4, f4, f4, f4, f4, f4, f4, f4, f4, f4], #ID
                   [f5, f6, f5, f5, f5, f5, f5, f5, f5, f5, f5, f5, f5, f5, f5, f5, f5, f5, f5, f5], #CTE
                   [fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn], #comentario
                   [fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn], #ASIG
                   [fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn], #IGUALA
                   [fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn], #MAYOR
                   [fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn], #MAYORIGUAL
                   [fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn], #MENOR
                   [fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn], #MENORIGUAL
                   [fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn], #DIST
                   [fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn], #SUMA
                   [fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn], #RESTA
                   [fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn], #MULT
                   [fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn], #DIV
                   [fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn], #PARA
                   [fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn], #PARC
                   [fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn], #LLAVEA
                   [fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn], #LLAVEC
                   [fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn], #AND
                   [fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn, fn]] #OR
#                    L   D   #   =   >   <  +   -   *   /   (    )  {    }  &   |   \t  \n  "" EOF 


############################################
# Funcion principal
############################################


def yylex():
    #defino estados 
    estado = 0
    estado_final = -1
    estado_anterior = 0
    #mientras no sea el estado final
    while estado != estado_final:
        c = getChar(contenido)
        columna = getEven(c)
        tabla_funciones[estado][columna](c)
        estado_anterior = estado
        estado = tabla_estados[estado][columna]
    if tabla_unreads[estado_anterior][columna] == 1:
        unreadChar()
    token = tabla_tokens[estado_anterior][columna]
    if(token == 256 and esPalabraReservada(identificador)):
        token = int(lista_palabras_reservadas[lista_palabras_reservadas["valor"] == identificador]["id"])
    return token
    
############################################
#Codigo para probar el funcionamiento
############################################

lista_tokens = pd.DataFrame()
lista_tokens["id"] = [256, 257, 258, 259, 260, 261, 262, 263, 264, 268, 269, 266, 267, 265, 272, 273, 274, 275, 276, 277, 278, 279, 270, 271]
lista_tokens["nombre"] = ["ID", "CTE", "IF", "ELSE", "WHILE", "PRINT", "INT", "ASIG", "IGUALA", "MAYOR", "MAYORIGUAL", "MENOR", "MENORIGUAL", "DIST", "SUMA", "RESTA", "MULT", "DIV", "PARA", "PARC", "LLAVEA", "LLAVEC", "AND", "OR"]
lista_tokens["valor"] = ["NA", "NA", "if", "else", "while", "print", "int", "=", "==", ">", ">=", "<", "<=", "<>", "+", "-", "*", "/", "(", ")", "{", "}", "&", "|"]

a = 0
while a != -1:
    a = yylex()
    print(lista_tokens[lista_tokens["id"] == a])
print("===================")    
print("Tabla de simbolos:")
print("===================")
print(tabla_simbolos)
    
























    