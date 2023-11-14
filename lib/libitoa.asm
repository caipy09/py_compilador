
section .text
global itoa  ; Hace la función visible para el linker.

; Función itoa: entero a ascii
; RDI - El número entero a convertir.
; RSI - El buffer donde se guardará la cadena ASCII terminada en NULL.
itoa:
    mov rax, rdi        ; Mueve el entero a RAX para la división.
    mov rcx, 10         ; carga el 10
    add rsi, 30         ; maximo tamaño del buffer ;antes 15
    mov rdi, rsi        
    mov byte [rdi], 0   ; NULL-termina la cadena.

reverse_loop:
    dec rdi             ; Mueve el puntero hacia atrás para el siguiente carácter.
    xor rdx, rdx        ; Limpia RDX para 'div'.
    div rcx             ; Divide RAX por 10, resultado en RAX, resto en RDX.
    add dl, '0'         ; Convierte el resto a su representación ASCII.
    mov [rdi], dl       ; Guarda el carácter en el buffer.

    test rax, rax       ; Comprueba si el cociente es 0.

    jnz reverse_loop    ; Si no es 0, sigue procesando.
    ret
