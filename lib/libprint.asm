
section .text
    enter_char db 0x0D,0x0A ; correr y saltar
global print

; Función print:
; RDI - La dirección de la cadena de caracteres para imprimir.
print:
    mov rax, 4
    mov rbx, 1
    mov rdx, 30 ;17
    mov rcx, rdi
    int 0x80
    mov rax, 4
    mov rbx, 1    
    mov rdx, 2
    mov rcx, enter_char
    int 0x80
    ret