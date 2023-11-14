#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#clase LexToken: la clase creará un objeto de este tipo y le asignará su type and value ya definidos para despues retornarlo
class LexToken(object):
    
    #variables
    type = ""
    value = ""
    
    #constructor
    def __init__(self, att_type, att_value):
        self.type = att_type
        self.value = att_value
    
    #metodo para impresion de tokens
    def __str__(self):
        return f'TOKEN <Type: {self.type}, Value: {self.value}>'