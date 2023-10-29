
import parser as p

ntest = "27"
path_input = "C:/Users/ferna/Onedrive/Documents/GitHub/py_compilador/lote_pruebas/" + ntest + "/"
path_output = "C:/Users/ferna/Onedrive/Documents/GitHub/py_compilador/lote_pruebas/" + ntest + "/"

polaca_inversa = p.parser(ntest, path_input, path_output)
#polaca_inversa = ['a', 'b', '+', 'c', 'd', '-', '*', 'e', 'f', '-', 'g', 'h', '-', '*', '/']

################################################################################
#GENERACION DE CODIGO ASSEMBLER

assembler = [] #en esta lista se guarda el codigo generado
pila = [] #pila utilizada para el algoritmo de generacion de codigo
pila_saltos = []

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
    l = {'+':'ADD', '*': 'MUL', '/':'DIV', '-':'SUB'}
    if op in l:
        return l[op]

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
        if checkID(x) or checkCTE(x, pos): #si es una variable o constante
            pila.append(x) #apilo
        if checkAssing(x): #si es una asignacion
            #genero codigo
            aux0 = 'MOV ' + pila.pop() + ', R1' 
            aux1 = 'MOV R1, ' + pila.pop()
            assembler.append(aux1)
            assembler.append(aux0)
        if checkOperator(x): #si es un operador
            op = getAssemblerOP(x) #obtengo el comando assembler del operador
            #genero codigo
            assembler_aux = 'AUX' + str(cont)
            aux0 = op + ' R1, ' + pila.pop()
            aux1 = 'MOV R1, ' + pila.pop()
            aux2 = 'MOV ' + assembler_aux + ', R1'
            assembler.append(aux1)
            assembler.append(aux0)
            assembler.append(aux2)
            pila.append(assembler_aux)
            cont += 1
        if checkComparator(x): #si es un comparador
            #genero codigo
            assembler_aux = 'AUX' + str(cont)
            aux0 = 'CMP R1, ' + pila.pop()
            aux1 = 'MOV R1, ' + pila.pop()
            aux2 = 'MOV ' + assembler_aux + ', R1'
            assembler.append(aux1)
            assembler.append(aux0)
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
            aux0 = 'BF ' + pila.pop()
            aux1 = 'MOV R1, ' + pila.pop()
            assembler.append(aux1)
            assembler.append(aux0)
        if str(x) == 'BI': #si es una bifurcacion incondicional
            #genero codigo
            aux0 = 'BI ' + pila.pop()
            assembler.append(aux0)     
        pos += 1
                     
            
        

polaca_assembler(polaca_inversa)

#print("Pila assembler: ", pila)
print("Pila saltos: ", pila_saltos)
print("assembler: ", assembler)

#Grabado de resultados a archivo txt
file = open(path_output + 'output.asm', "w")
#file.write(str(assembler) + '\n')
file.write('\n'.join(assembler))
file.close()

