include macros.asm
include number.asm

.MODEL LARGE; tipo de modelo de memoria utilizado
.386
.STACK 200h; bytes en el stack


.DATA; bloque de definicion de variables

	_a	DD	0
	$_20	dd	20
	$_10	dd	10
	$_40	dd	40

.CODE; bloque de definiciones de codigo

START:

	mov AX, @DATA; carga de variables
	mov DS, AX
	mov es, ax

		mov eax, [$_20]
		mov [_a], eax
		
		cmp [$_20], [$_10]
		jl _condition
		
		displayInteger _a
		jmp END_PROGRAM

	END_PROGRAM:
		mov ax, 4c00h
		int 21h; interrupcion del programa
		END START; fin del programa

	_condition:
		mov eax, [$_40]
		mov [_a], eax