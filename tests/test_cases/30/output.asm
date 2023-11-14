include macros.asm
include number.asm

.MODEL LARGE; tipo de modelo de memoria utilizado
.386
.STACK 200h; bytes en el stack


.DATA; bloque de definicion de variables

	_a	DD	0
	_b	DD	0
	_c	DD	0
	_d	DD	0
	$_20	dd	20
	$_4	dd	4
	$_10	dd	10
	$_400	dd	400
	aux1	DD	0
	aux2	DD	0
	aux3	DD	0

.CODE; bloque de definiciones de codigo

START:

	mov AX, @DATA; carga de variables
	mov DS, AX
	mov es, ax

		mov eax, [$_20]
		mov [_a], eax
		mov eax, [$_4]
		mov [_b], eax
		mov eax, [$_10]
		mov [_c], eax
		mov eax, [$_400]
		mov [_d], eax
		mov eax, [_a]
		imul eax, [_b]
		mov [aux1], eax
		mov eax, aux1
		add eax, [_c]
		mov [aux2], eax
		mov eax, [_d]
		sub eax, aux2
		mov [aux3], eax
		mov eax, aux3
		mov [_d], eax
		displayInteger _d
		jmp END_PROGRAM

	END_PROGRAM:
		mov ax, 4c00h
		int 21h; interrupcion del programa
		END START; fin del programa
