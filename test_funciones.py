
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
def f4():
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
def f5():
  global tabla_simbolos
  if (tabla_simbolos["nombre"] == guionId(constante)).any():
    pass
  else:
    row = [guionId(constante), constante, "-"]
    tabla_simbolos.loc[len(tabla_simbolos)] = row

#funcion nula
def f6():
  None


#para generar identificadores de ejemplo
f1("v")    
f1("a")
f1("r")
f1("i")
f1("a")
f1("b")
f1("l")
f1("e")

#para generar constantes de ejemplo
f2("6")
f2("5")
f2("5")
f2("3")
f2("6")
f2("0")

#ejecucion de funciones
f4()
f5()
f6()

#imprimo por pantalla la TS
print(tabla_simbolos)


