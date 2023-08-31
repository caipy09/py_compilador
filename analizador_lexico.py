
#posicion de la lectura
pos = 0
file = "ejemplo_programa.txt"

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
    if(char == '!'):
        return 7
    if(char == '+'):
        return 8
    if(char == '-'):
        return 9
    if(char == '*'):
        return 10
    if(char == '/'):
        return 11
    if(char == '('):
        return 12
    if(char == ')'):
        return 13
    if(char == ':'):
        return 14
    if(char == '\t'):
        return 15
    if(char == '\n'):
        return 16
    if(char == ' '):
        return 17
    if(char == 'EOF'):
        return 18

#while que permite operar con todos los caracteres del archivo txt
while pos < contents_size:
    c = getChar(contents)
    print("El valor es: ", c, " Y su id es: ", getEven(c))
    


#cierro la conexion con el archivo leido
f.close()    





