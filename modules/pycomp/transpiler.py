#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from re import compile

INT_SIZE = 64

class Transpiler:

    var_name_regex = compile(r'^[_a-zA-Z][_a-zA-Z0-9]*$')
    numeric_regex = compile(r'^[0-9]+$')
    math_operator_regex = compile(r'^[+\-*/]+$')
    math_comparators = ['==', '!=', '<', '>', '=>', '<=']
    cmp_jumps = ['JNE', 'JE', 'JGE', 'JLE', 'JL', 'JG']
    polish_jmps = ['BF', "BI"]
    label_basename = 'label'

    def __init__(self, token_list):
        self.tokens = token_list.copy()
        self.variables_to_mem = dict()
        self.memory_counter = 1
        self.value_stack = list()
        self.assembler_code = list()
        self.label_counter = 0
        self.label_positions = dict()
        self.precompiled_tokens = None
        self.all_variables = list()

    def _get_memory_address(self, token):
        """
            Genera o recupera una dirección de memoria para una variable o token.
            Si el token ya es una dirección de memoria, número o temporal, se devuelve directamente.
            Si no, se asigna una nueva dirección de memoria y se actualiza el contador de memoria.
        Args:
            token (str): El token para el cual se busca una dirección de memoria.

        Returns:
            str: La dirección de memoria asociada con el token.

        Example:
            address = self._get_memory_address('variable1')
        """
        if token.startswith("mem_") or token.startswith("num_") or \
            token.startswith("temp_"):
            # El token ya es una dirección de memoria o un número/temporal asignado
            return token
        if token not in self.variables_to_mem:
            name = f"mem_{self.memory_counter}"
            self.variables_to_mem[token] = name
            self.memory_counter += 1
            self.all_variables.append(name)
        return self.variables_to_mem[token]

    def _generate_unique_label(self, position: int):
        """
        Genera una etiqueta única para ser usada en las instrucciones de salto.
        Incrementa el contador de etiquetas y almacena la posición de la etiqueta.
        Args:
            position (int): La posición de la instrucción en la lista de tokens.

        Returns:
            str: Una etiqueta única generada.

        Example:
            label = self._generate_unique_label(5)        
        """
        unique_label = f"{self.label_basename}_{self.label_counter}"
        self.label_counter += 1
        adjusted_position = position if position not in self.label_positions else position + 1
        self.label_positions[adjusted_position] = unique_label
        return unique_label

    def _insert_labels(self):
        """
        Inserta las etiquetas en las posiciones correspondientes dentro del array precompilado.
        Modifica el array precompilado para incluir las etiquetas en las posiciones correctas.
        Returns:
            None

        Example:
            self._insert_labels()
        """
        modified_array = self.precompiled_tokens.copy()
        label_count = 0
        for position, label in self.label_positions.items():
            print(label_count)

            modified_array.insert(
                position + label_count,
                [f"{label}:"]
            )
            label_count += 1
        self.precompiled_tokens = modified_array.copy()

    def _assign_value_to_variable(self, variable_name, token_index):
        """
        Asigna el valor del tope de la pila de valores a una variable.
        Genera instrucciones de ensamblador para mover el valor desde el tope de la pila
        a la dirección de memoria de la variable.
        Args:
            variable_name (str): El nombre de la variable a la que se le asignará el valor.
            token_index (int): El índice del token en la lista de tokens.

        Returns:
            None

        Example:
            self._assign_value_to_variable('x', 2)
        """
        value = self.value_stack.pop()
        self.precompiled_tokens[token_index] = [
            f"MOV RAX, [{self._get_memory_address(value)}]",
            f"MOV [{self._get_memory_address(variable_name)}], RAX"
        ]

    def _get_temp_variable(self):
        """
        Genera una nueva variable temporal.
        Incrementa el contador de memoria y devuelve el nombre de la variable temporal.

        Returns:
            str: El nombre de una nueva variable temporal.

        Example:
            temp_var = self._get_temp_variable()
        """
        temp_var = f"temp_{self.memory_counter}"
        self.all_variables.append(temp_var)
        self.memory_counter += 1
        return temp_var

    def _perform_arithmetic_operation(self, operator, token_index):
        """
        Realiza una operación aritmética entre dos operandos.
        Los operandos se extraen de la pila de valores y se generan instrucciones de ensamblador
        para realizar la operación. El resultado se almacena en una variable temporal.
        Args:
            operator (str): El operador aritmético ('+', '-', '*', '/').
            token_index (int): El índice del token en la lista de tokens.

        Returns:
            None

        Example:
            self._perform_arithmetic_operation('+', 3)
        """
        operand_b = self.value_stack.pop()
        operand_a = self.value_stack.pop()
        
        math_operations = {
            "+": f"ADD RAX, [{self._get_memory_address(operand_b)}]",
            "-": f"SUB RAX, [{self._get_memory_address(operand_b)}]",
            "*": f"IMUL RAX, [{self._get_memory_address(operand_b)}]",
            "/": "CQO\nIDIV QWORD [{self.get_memory_address(operand_b)}]"
        }
        temp_var = self._get_temp_variable()
        self.precompiled_tokens[token_index] = [
            f"MOV RAX, [{self._get_memory_address(operand_a)}]",
            math_operations[operator],
            f"MOV [{self._get_memory_address(temp_var)}], RAX"
        ]
        

        self.value_stack.append(temp_var)

    def _print_top_value(self, token_index):
        """
        Imprime el valor en el tope de la pila.
        Genera instrucciones de ensamblador para imprimir el valor usando las funciones 'itoa' y 'print'.
        Args:
            token_index (int): El índice del token en la lista de tokens.

        Returns:
            None

        Example:
            self._print_top_value(4)
        """
        value = self.value_stack.pop()
        value_address = self._get_memory_address(value)
        temp_var = self._get_temp_variable()
        self.precompiled_tokens[token_index] = [
            f"MOV rdi, [{value_address}]",
            f"MOV rsi, {temp_var}",
            "CALL itoa",
            f"MOV rdi, {temp_var}",
            "CALL print"
        ]

    def _make_bss_section(self):
        """
        Crea la sección .bss del código de ensamblador.
        Genera declaraciones para reservar espacio para todas las variables utilizadas.

        Returns:
            str: La sección .bss del código de ensamblador.

        Example:
            bss_section = self._make_bss_section()
        """
        variables = [f"{name} resb {INT_SIZE}" for name in self.all_variables]
        return '\n'.join(
            ['section .bss'] + list(set(variables))
        )
    
    def transpile(self):
        """
        Transpila la lista de tokens a código de ensamblador.
        Preprocesa los tokens, inserta etiquetas y genera el código de ensamblador final.
        Returns:
            str: El código de ensamblador transpilado.

        Example:
            asm_code = self.transpile()
        """
        self._pretranspile()
        self._insert_labels()
        transpiled = [

            self._make_bss_section(),
            "\n",
            "section .text",
            "global _start",
            "extern itoa",
            "extern print",
            "\n",
            "_start:"

        ]
        
        for i, item in enumerate(self.precompiled_tokens):
            if not item:
                continue
            for j, jtem in enumerate(item):
                transpiled.append(jtem)
        return '\n'.join(

            transpiled + [
                "mov rax, 60",
                "xor rdi, rdi",
                "syscall",                
            ] 
        )

    def _pretranspile(self):
        """
        Preprocesa los tokens antes de la transpilación.
        Analiza los tokens y genera un conjunto de instrucciones de ensamblador
        preliminares basadas en la polaca inversa proporcionada.
        Returns:
            None

        Example:
            self._pretranspile()
        """
        self.precompiled_tokens = [None] * (len(self.tokens) + 1)

        for token_index, token in enumerate(self.tokens):

            if token == "PRNT":
                self._print_top_value(token_index)

            elif token in self.math_comparators:
                b = self.value_stack.pop()  # Supongamos que 'b' es el valor superior
                a = self.value_stack.pop()  # 'a' es el siguiente valor superior
                self.precompiled_tokens[token_index] = [
                    f"MOV RAX, [{self._get_memory_address(a)}]",
                    f"CMP RAX, [{self._get_memory_address(b)}]"
                ]

            elif token == "BF":
                cmp_type = self.tokens[self.tokens.index(token) - 2]
                jmp_type = self.cmp_jumps[self.math_comparators.index(cmp_type)]
                unique_label = self._generate_unique_label(
                    self.tokens[token_index - 1]
                )
  
                self.precompiled_tokens[token_index] = [f"{jmp_type} {unique_label}"]

            elif token == "BI":
                unique_label = self._generate_unique_label(
                    self.tokens[token_index - 1]
                )
                self.assembler_code.insert(
                    self.tokens[self.tokens.index(token) - 1],
                    f'{unique_label}:'
                )
                self.precompiled_tokens[token_index] = [f"JMP {unique_label}"]

            elif self.numeric_regex.match(str(token)):

                # acá compruebo si el literal que estoy por procesar
                # no pertenece a posición de salto BI/BF
                if token_index != len(self.tokens) - 1 and \
                    self.tokens[token_index + 1] in self.polish_jmps:
                    continue
                self.precompiled_tokens[token_index] = [f"MOV RAX, {token}"]
                temp_var = self._get_temp_variable()
                self.precompiled_tokens[token_index] += [
                    f"MOV [{self._get_memory_address(temp_var)}], RAX"
                ]
                self.value_stack.append(temp_var)

            elif self.var_name_regex.match(str(token)):
                var_address = self._get_memory_address(token)
                self.value_stack.append(var_address)

            elif self.math_operator_regex.match(str(token)):
                self._perform_arithmetic_operation(token, token_index)
                
            elif token == "=":
                self._assign_value_to_variable(
                    self.value_stack.pop(),
                    token_index
                )
