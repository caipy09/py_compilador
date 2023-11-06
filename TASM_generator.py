
import parser as p

ntest = "30"
path_input = "C:/Users/ferna/Onedrive/Documents/GitHub/py_compilador/lote_pruebas/" + ntest + "/"
path_output = "C:/Users/ferna/Onedrive/Documents/GitHub/py_compilador/lote_pruebas/" + ntest + "/"

assembler_elements = p.parser(ntest, path_input, path_output)

polaca_inversa = assembler_elements[0]
#polaca_inversa = ['a', 'b', '+', 'c', 'd', '-', '*', 'e', 'f', '-', 'g', 'h', '-', '*', '/']

symbol_table = assembler_elements[1]
_vars = symbol_table.getSymbolTable().query('declared == True')["id"].values
_consts = symbol_table.getSymbolTable().query('declared != True')["id"].values

################################################################################
#GENERACION DE CODIGO ASSEMBLER

assembler = [] #en esta lista se guarda el codigo generado
pila = [] #pila utilizada para el algoritmo de generacion de codigo
pila_saltos = []


#funcion que retorna la cantidad de variables aux que va a utilizar el programa
def defineAuxVarsQ():
    global polaca_inversa
    symbols = ['+', '-', '*', '/', '>', '<', '>=', '<=', '==', '<>', '&', '|']
    aux_list = []
    cant = 0
    for x in polaca_inversa:
        if x in symbols:
            cant += 1
            aux_list.append(('aux' + str(cant)))
    return aux_list

#obtengo la cantidad de var auxiliares
aux_vars = defineAuxVarsQ()
#copio las variables auxiliares a una pila que sera utilizada en la generacion del codigo de START:
pila_aux = aux_vars.copy()

#verifica si el valor es un identificador de variable
def checkID(val):
    aux = str(val)
    if aux.isalpha() and aux != 'BF' and aux != 'BI':
        return True
    return False

#verificia si el valor es una constante numerica
def checkCTE(val, pos):
    aux = str(val)
    if aux.isnumeric() and checkJump(pos) == False:
        return True
    return False

#verifica si el valor es una asignacion
def checkAssing(val):
    aux = str(val)
    assi = '='
    if aux == assi:
        return True
    return False

#verifica si el valor es un operador
def checkOperator(val):
    aux = str(val)
    oper = ['+', '-', '*', '/']
    if aux in oper:
        return True
    return False

#verifica si el valor es un comparador
def checkComparator(val):
    aux = str(val)
    comp = ['>', '<', '>=', '<=', '==', '<>', '&', '|']
    if aux in comp:
        return True
    return False

#verifica si el valor corresponde a una posicion de salto
def checkJump(pos):
    global polaca_inversa
    biff = ['BF', 'BI']
    if pos+1 < len(polaca_inversa):
        if polaca_inversa[pos+1] in biff:
            return True
    return False

#dado un operador retorna su correspondiente comando assembler
def getAssemblerOP(op):
    l = {'+':'add', '*': 'mul', '/':'div', '-':'sub'}
    if op in l:
        return l[op]

reg1 = "ebx"

#algoritmo generador de codigo
def polaca_assembler(pol):
    global assembler
    global pila
    global pila_saltos
    cont = 1 #para crear variables auxiliares numeradas
    pos = 0 #para controlar que posicion en la lista polaca se esta leyendo en cada iteracion
    for x in pol:
        ####################################
        #revisar esta parte porque funciona solo con el ejemplo de la teoria
        if len(pila_saltos) != 0:
            salto = pila_saltos[0]
            if pos == salto:
                aux0 = 'LABEL' + str(salto) + ':'
                assembler.append(aux0)
                pila_saltos.pop(0)
        ###################################
        if checkID(x): #si es una variable o constante
            pila.append('_' + x) #apilo
        if checkCTE(x, pos): #si es una variable o constante
            pila.append('$_' + x) #apilo
        if checkAssing(x): #si es una asignacion
            #genero codigo
            aux0 = '\tmov ' + pila.pop() + ', ' + reg1 
            aux1 = '\tmov ' + reg1 + ', ' + pila.pop()
            assembler.append(aux1)
            assembler.append(aux0)
        if checkOperator(x): #si es un operador
            op = getAssemblerOP(x) #obtengo el comando assembler del operador
            #genero codigo
            assembler_aux = pila_aux.pop(0)
            aux0 = '\t' + op + ' ' + reg1 + ', ' + pila.pop()
            aux1 = '\tmov ' + reg1 + ', ' + pila.pop()
            aux2 = '\tmov ' + assembler_aux + ', ' + reg1
            assembler.append(aux1)
            assembler.append(aux0)
            assembler.append(aux2)
            pila.append(assembler_aux)
            cont += 1
        if checkComparator(x): #si es un comparador
            #genero codigo
            assembler_aux = pila_aux.pop(0)
            #label = 'LABEL' + str(polaca_inversa[pos+1])
            aux0 = '\tcmp ' + reg1 + ', ' + pila.pop()
            aux1 = '\tmov ' + reg1 + ', ' + pila.pop()
            aux2 = '\tmov ' + assembler_aux + ', ' + reg1
            #aux3 = '\tjl ' + label
            assembler.append(aux1)
            assembler.append(aux0)
            #assembler.append(aux3)
            assembler.append(aux2)
            pila.append(assembler_aux)
            cont += 1
        if checkJump(pos): #si es una posicion de salto
            pila_saltos.append(x)
            #genero etiqueta
            aux = 'LABEL' + str(x)
            pila.append(aux)
        if str(x) == 'BF': #si es una bifurcacion por falso
            #genero codigo 
            aux0 = '\tjl ' + pila.pop()
            #aux0 = '\tBF ' + pila.pop()
            aux1 = '\tmov ' + reg1 + ', ' + pila.pop()
            assembler.append(aux1)
            assembler.append(aux0)
        if str(x) == 'BI': #si es una bifurcacion incondicional
            #genero codigo
            val = pila.pop()
            if int(val[5:]) >= len(polaca_inversa):
                assembler.append("\tjmp END_PROGRAM")
            else:
                aux0 = '\tjmp ' + val
                assembler.append(aux0)
            #assembler.append("\tjmp END_PROGRAM")
        pos += 1
    assembler.append("\tjmp END_PROGRAM")
                     
            
        

polaca_assembler(polaca_inversa)

#print("Pila assembler: ", pila)
#print("Pila saltos: ", pila_saltos)
#print("assembler: ", assembler)


#Grabado de resultados a archivo txt
file = open(path_output + 'output.asm', "w")

file.write("include macros.asm" + '\n')
file.write("include number.asm" + '\n')
file.write('\n')
file.write(".MODEL LARGE; tipo de modelo de memoria utilizado" + '\n')
file.write(".386" + '\n')
file.write(".STACK 200h; bytes en el stack" + '\n')
#file.write("MAXTEXTSIZE equ 120" + '\n')
file.write('\n')
file.write('\n')
file.write('.DATA; bloque de definicion de variables' + '\n')
file.write('\n')


for x in _vars:
    file.write('\t' +  x + '\t' + 'DD' + '\t0' + '\n')
for y in _consts:
    file.write('\t$' +  y + '\t' + 'DD' + '\t0' + '\n')
for z in aux_vars:
    file.write('\t' +  z + '\t' + 'DD' + '\t0' + '\n')
    

file.write('\n')
file.write('.CODE; bloque de definiciones de codigo' + '\n')
file.write('\n')
file.write('START:' + '\n')
file.write('\n')

file.write('\tmov eax, @DATA; carga de variables' + '\n')

file.write('\n')
file.write('\t')
file.write('\n\t' .join(assembler))
file.write('\n')
file.write('\n')
file.write('\tEND_PROGRAM:\n')
file.write('\t\tmov ax, 4c00h' + '\n')
file.write('\t\tint 21h; interrupcion del programa' + '\n')
file.write('\t\tEND START; fin del programa' + '\n')


file.close()

