#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse 
import sys
import os

from modules.pycomp.lexer import Lexer
from modules.pycomp.parser import Parser
from modules.pycomp.transpiler import Transpiler

TEMP_DIR = '/tmp'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reads a file from a given path.")
    parser.add_argument('file_path', type=str, help='Path of the file to read.')
    
    args = parser.parse_args()
    

    lexer = Lexer(filename=args.file_path)
    parser = Parser(lexer=lexer)
    ipolish = parser.parse(get_info=True)
    transpiler = Transpiler(
        token_list=ipolish
    )

    src_filename = os.path.basename(args.file_path)
    asm_filename = f"{src_filename.split('.')[0]}.asm"
    try:
        with open(os.path.join(TEMP_DIR, asm_filename), 'w') as f:
            f.write(
                transpiler.transpile()
            )
            f.flush()
        sys.exit(0)
    except Exception as err:
        print(err)
        sys.exit(1)
    