

import symbolTable as st
import lexToken as lt

class Lexer(object):
    
    def __init__(self, filename = None):
        self.ts = st.SymbolTable("DummyLexer")
        self.contador = 0
        self.listaToken = [
            lt.LexToken("ID", "x"),
            lt.LexToken("ASIG", "="),
            lt.LexToken("CTE", "1"),
            lt.LexToken("ID", "x"),
            lt.LexToken("ASIG", "="),
            lt.LexToken("CTE", "2"),
            lt.LexToken("ID", "x"),
            lt.LexToken("ASIG", "="),
            lt.LexToken("CTE", "3"),
            lt.LexToken("ID", "x"),
            lt.LexToken("ASIG", "="),
            lt.LexToken("CTE", "4"),
            ]
    
    def token(self):
        if self.contador >= len(self.listaToken):
            return None
        else:
            res = self.listaToken[self.contador]
            if res.type == "ID":
                self.ts.addSymbol(res.value, res.value, 1, False)
            if res.type == "CTE":
                self.ts.addSymbol(res.value, res.value, 1, None)
            self.contador += 1
            return res
        

