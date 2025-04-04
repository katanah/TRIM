class Token:
    def __init__(self, token_type, value, line=None, position=None):
        self.token_type = token_type
        self.value = value
        self.line = None
        self.position = position

class TokenType:
    NUMBER = "NUMBER"
    STRING = "STRING"
    NAME = "NAME"
    KEYWORD = "KEYWORD"
    SYMBOL =  "SYMBOL"
    OPERATOR = "OPERATOR"
    EOF = "EOF"