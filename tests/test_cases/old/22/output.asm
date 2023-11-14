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
	_e	DD	0
	$_10	DD	0
	$_20	DD	0
	$_30	DD	0
	$_40	DD	0
	$_50	DD	0
	$_2	DD	0
	$_3	DD	0
	aux1	DD	0
	aux2	DD	0
	aux3	DD	0
	aux4	DD	0
	aux5	DD	0
	aux6	DD	0
	aux7	DD	0
	aux8	DD	0
	aux9	DD	0
	aux10	DD	0
	aux11	DD	0
	aux12	DD	0
	aux13	DD	0
	aux14	DD	0
	aux15	DD	0
	aux16	DD	0
	aux17	DD	0
	aux18	DD	0
	aux19	DD	0
	aux20	DD	0
	aux21	DD	0
	aux22	DD	0
	aux23	DD	0
	aux24	DD	0
	aux25	DD	0
	aux26	DD	0

.CODE; bloque de definiciones de codigo

START:

	mov eax, @DATA; carga de variables

		mov ebx, $_10
		mov _a, ebx
		mov ebx, $_20
		mov _b, ebx
		mov ebx, $_30
		mov _c, ebx
		mov ebx, $_40
		mov _d, ebx
		mov ebx, $_50
		mov _e, ebx
		mov ebx, _a
		cmp ebx, _b
		mov aux1, ebx
		mov ebx, _a
		mul ebx, $_2
		mov aux2, ebx
		mov ebx, aux2
		mov _a, ebx
		mov ebx, _a
		cmp ebx, _c
		mov aux3, ebx
		mov ebx, _b
		mul ebx, $_2
		mov aux4, ebx
		mov ebx, aux4
		mov _a, ebx
		mov ebx, _a
		cmp ebx, _d
		mov aux5, ebx
		mov ebx, _c
		mul ebx, $_2
		mov aux6, ebx
		mov ebx, aux6
		mov _a, ebx
		mov ebx, _b
		div ebx, $_2
		mov aux7, ebx
		mov ebx, aux7
		mov _a, ebx
		mov ebx, _a
		cmp ebx, _c
		mov aux8, ebx
		mov ebx, _d
		mul ebx, $_2
		mov aux9, ebx
		mov ebx, aux9
		mov _a, ebx
	LABEL68:
		mov ebx, _a
		add ebx, $_2
		mov aux10, ebx
		mov ebx, aux10
		mov _a, ebx
		mov ebx, _a
		cmp ebx, _b
		mov aux11, ebx
		mov ebx, _b
		add ebx, $_2
		mov aux12, ebx
		mov ebx, aux12
		mov _a, ebx
		mov ebx, _a
		cmp ebx, _e
		mov aux13, ebx
		mov ebx, _d
		div ebx, $_2
		mov aux14, ebx
		mov ebx, aux14
		mov _a, ebx
		mov ebx, _b
		sub ebx, $_2
		mov aux15, ebx
		mov ebx, aux15
		mov _a, ebx
		mov ebx, _a
		cmp ebx, _d
		mov aux16, ebx
		mov ebx, _d
		div ebx, $_3
		mov aux17, ebx
		mov ebx, aux17
		mov _a, ebx
		mov ebx, _a
		cmp ebx, _c
		mov aux18, ebx
		mov ebx, _a
		mul ebx, $_2
		mov aux19, ebx
		mov ebx, aux19
		mov _a, ebx
		mov ebx, _a
		cmp ebx, _c
		mov aux20, ebx
		mov ebx, _b
		mul ebx, $_2
		mov aux21, ebx
		mov ebx, aux21
		mov _a, ebx
		mov ebx, _a
		cmp ebx, _d
		mov aux22, ebx
		mov ebx, _c
		mul ebx, $_2
		mov aux23, ebx
		mov ebx, aux23
		mov _a, ebx
		mov ebx, _b
		div ebx, $_2
		mov aux24, ebx
		mov ebx, aux24
		mov _a, ebx
		mov ebx, _a
		cmp ebx, _c
		mov aux25, ebx
		mov ebx, _d
		mul ebx, $_2
		mov aux26, ebx
		mov ebx, aux26
		mov _a, ebx

mov ax, 4c00h
int 21h; interrupcion del programa
END START; fin del programa
