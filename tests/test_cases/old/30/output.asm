include macros.asm
include number.asm

.MODEL LARGE; tipo de modelo de memoria utilizado
.386
.STACK 200h; bytes en el stack


.DATA; bloque de definicion de variables

	_a	DD	0
	_b	DD	0
	_c	DD	0
	$_2	DD	0
	$_3	DD	0
	$_4	DD	0
	$_0	DD	0
	$_20	DD	0
	aux1	DD	0

.CODE; bloque de definiciones de codigo

START:

	mov eax, @DATA; carga de variables

		mov ebx, $_2
		mov _a, ebx
		mov ebx, $_3
		mov _b, ebx
		mov ebx, _a
		cmp ebx, _b
		mov aux1, ebx
		mov ebx, aux1
		jl LABEL16
		mov ebx, $_4
		mov _c, ebx
		jmp LABEL19
	LABEL16:
		mov ebx, $_0
		mov _c, ebx
	LABEL19:
		mov ebx, $_20
		mov _a, ebx
		jmp END_PROGRAM

	END_PROGRAM:
		mov ax, 4c00h
		int 21h; interrupcion del programa
		END START; fin del programa
