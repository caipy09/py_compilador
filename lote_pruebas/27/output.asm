;ejemplo assembler

section .data
	;definir identificadores de la tabla de simbolos
	a dw 0
	b dw 0
	c dw 0
	

section .text
	;programa principal
	global _start
	_start:
	
	MOV ax, 0
	MOV [a], ax
	MOV ax, 3
	MOV [b], ax
	MOV ax, 2
	IMUL ax, [b] ;en reemplazo de MUL ax, b
	AUX1 dw 0
	MOV [AUX1], ax
	
	int 0x80 ;fin de programa