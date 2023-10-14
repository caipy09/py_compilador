# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 23:24:27 2023

@author: ferna
"""
import symbolTable as st

a = st.SymbolTable("a")
b = st.SymbolTable("b")

a.addSymbol("x", "x", 1, True)
b.addSymbol("y", "y", 2, True)

a.__str__()
b.__str__()