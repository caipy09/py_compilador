
class LexToken(object):
    
    type = ""
    value = ""
    
    def __init__(self, att_type, att_value):
        self.type = att_type
        self.value = att_value
        
    def __str__(self):
        return f'TOKEN <Type: {self.type}, Value: {self.value}>'
    
    def isValidToken(self):
        return self.value != -1