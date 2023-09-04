
import pandas as pd

#tabla de simbolos con columnas principales
tabla_simbolos = pd.DataFrame()
tabla_simbolos["nombre"] = None
tabla_simbolos["valor"] = None
tabla_simbolos["longitud"] = None

#variables
identificador = ""
long_max_identificador = 6
long_actual_identificador = 0
constante = ""
long_max_constante = pow(2, 16) - 1


#Preguntas
# como manejar los errores lexicos? ej. si el numero excede los 16 bits o si el identificador excede el largo definido


#funcion de respaldo que devuelve un 0 cuando el string esta vacio
# y la conversion a numerico del string en caso contrario
def a_numerico(string):
  if string == "":
    return 0
  else:
    return int(string)

#funcion para reiniciar el identificador
def limpiarIdentificador():
  global identificador
  global long_actual_identificador
  identificador = ""
  long_actual_identificador = 0

#funcion para reiniciar la constante
def limpiarConstante():
  global constante
  constante = ""

#agrega el guion bajo al identificador
def guionId(identif):
  return "_" + identif


#IDENTIFICADOR
#inicializa un string con el contenido de los caracteres recibidos 
#nota: cumple lo que hace f1 y f3
def f1(c):
  global long_actual_identificador
  global long_max_identificador
  if long_actual_identificador < long_max_identificador:
    global identificador
    identificador = identificador + c
    long_actual_identificador = long_actual_identificador + 1

#CONSTANTE
#inicializa un string con el contenido de los digitos recibidos
def f2(c):
  global long_max_constante
  global constante
  aux = constante + c
  if a_numerico(aux) < long_max_constante:
    constante = aux

#IDENTIFICADOR
#si el presente identificador no está en TS, lo agrega
# de lo contrario se lo omite
def f4(c):
  global tabla_simbolos
  if (tabla_simbolos["nombre"] == guionId(identificador)).any():
    pass
  else:
    row = [guionId(identificador), identificador, long_actual_identificador]
    tabla_simbolos.loc[len(tabla_simbolos)] = row

#CONSTANTE
#si el presente identificador no está en TS, lo agrega
# de lo contrario se lo omite
#NOTA: cumple lo que hace f5 y f6
def f5(c):
  global tabla_simbolos
  if (tabla_simbolos["nombre"] == guionId(constante)).any():
    pass
  else:
    row = [guionId(constante), constante, "-"]
    tabla_simbolos.loc[len(tabla_simbolos)] = row

#funcion nula
def f6(c):
  None


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
tabla_unreads = [[0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0], #inicial
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
                 [268, 268, 268, 268,  -1, 268, 268, 268, 268, 268, 268, 268, 268, 268, 268, 268, 268, 268, 268, 268], #MAYOR
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
tabla_funciones = [[f1, f2, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6], #inicial
                   [f1, f1, f4, f4, f4, f4, f4, f4, f4, f4, f4, f4, f4, f4, f4, f4, f4, f4, f4, f4], #ID
                   [f5, f2, f5, f5, f5, f5, f5, f5, f5, f5, f5, f5, f5, f5, f5, f5, f5, f5, f5, f5], #CTE
                   [f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6], #comentario
                   [f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6], #ASIG
                   [f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6], #IGUALA
                   [f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6], #MAYOR
                   [f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6], #MAYORIGUAL
                   [f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6], #MENOR
                   [f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6], #MENORIGUAL
                   [f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6], #DIST
                   [f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6], #SUMA
                   [f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6], #RESTA
                   [f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6], #MULT
                   [f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6], #DIV
                   [f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6], #PARA
                   [f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6], #PARC
                   [f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6], #LLAVEA
                   [f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6], #LLAVEC
                   [f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6], #AND
                   [f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6, f6]] #OR
#                  L   D   #   =   >   <  +   -   *   /   (    )  {    }  &   |   \t  \n  "" EOF 


#posicion de la lectura
pos = 0
file = "test.txt"

#apertura del archivo en modo lectura
f = open(file,'r')

#se lee el contenido del archivo y se lo guarda en su completitud en la variable contents
with open(file) as f:
  contents = f.read()

#defino la longitud de contents
contents_size = len(contents)

#funcion que permite leer secuencialmente el contenido de 'contents'
# si llega al final devuelve un EOF
def getChar(buffer):
  global pos
  if(pos >= len(buffer)):
    return 'EOF'
  else:
    res = buffer[pos]
    pos = pos + 1
    return res
  
def unreadChar():
  global pos
  pos = pos - 1

#funcion de eventos: segun que sea el caracter leido retornara un id numerico
def getEven(char):
  if(char.isalpha()):
    return 1
  if(char.isnumeric()):
    return 2
  if(char == '#'):
    return 3
  if(char == '='):
    return 4
  if(char == '>'):
    return 5
  if(char == '<'):
    return 6
  if(char == '+'):
    return 7
  if(char == '-'):
    return 8
  if(char == '*'):
    return 9
  if(char == '/'):
    return 10
  if(char == '('):
    return 11
  if(char == ')'):
    return 12
  if(char == '{'):
    return 13
  if(char == '}'):
    return 14
  if(char == '&'):
    return 15
  if(char == '|'):
    return 16
  if(char.startswith('\t')):
    return 17
  if(char.startswith('\n')):
    return 18
  if(char == ' '):
    return 19
  if(char == 'EOF'):
    return 20








estado_actual = 0


#while que permite operar con todos los caracteres del archivo txt
while pos < contents_size:
  if(estado_actual == -1):
    estado_actual = 0
  
  #ver por que pos sigue en 1 al ejecutar todo junto
  c = getChar(contents)
  #debug
  #print("El valor es: ", c, " Y su id es: ", getEven(c))
  #agrego el caracter leido segun sea al string temporal que corresponda
  tabla_funciones[estado_actual][getEven(c)-1](c)
  print(tabla_simbolos)
  
  #al finalizar hago la transicion al siguiente estado
  estado_actual = tabla_estados[estado_actual][getEven(c)-1]

#cierro la conexion con el archivo leido
f.close()    
