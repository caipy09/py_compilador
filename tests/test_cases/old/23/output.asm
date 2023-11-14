include macros.asm
include number.asm

.MODEL LARGE; tipo de modelo de memoria utilizado
.386
.STACK 200h; bytes en el stack


.DATA; bloque de definicion de variables

	_a	DD	0
	_b	DD	0
	_c	DD	0
	$_0	DD	0
	$_3	DD	0
	$_2	DD	0
	$_5	DD	0
	$_1	DD	0
	$_6	DD	0
	$_4	DD	0
	aux1	DD	0
	aux2	DD	0
	aux3	DD	0
	aux4	DD	0
	aux5	DD	0
	aux6	DD	0
	aux7	DD	0

.CODE; bloque de definiciones de codigo

START:

	mov eax, @DATA; carga de variables

		mov ebx, $_0
		mov _a, ebx
		mov ebx, $_3
		mov _b, ebx
		mov ebx, $_2
		mul ebx, _b
		mov aux1, ebx
		mov ebx, aux1
		mov _a, ebx
		mov ebx, _a
		cmp ebx, $_5
		mov aux2, ebx
		mov ebx, _a
		add ebx, $_1
		mov aux3, ebx
		mov ebx, aux3
		mov _a, ebx
		mov ebx, _b
		add ebx, $_1
		mov aux4, ebx
		mov ebx, aux4
		mov _b, ebx
	LABEL28:
		mov ebx, $_6
		mov _a, ebx
		mov ebx, $_4
		mov _b, ebx
	LABEL34:
		mov ebx, _a
		cmp ebx, $_0
		mov aux5, ebx
		mov ebx, _a
		sub ebx, $_1
		mov aux6, ebx
		mov ebx, aux6
		mov _a, ebx
		mov ebx, _b
		add ebx, $_1
		mov aux7, ebx
		mov ebx, aux7
		mov _b, ebx
	LABEL51:
		mov ebx, $_0
		mov _c, ebx

mov ax, 4c00h
int 21h; interrupcion del programa
END START; fin del programa
