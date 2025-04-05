from enum import Enum

class Token:
    def __init__(self, token_type, value, line=None, position=None):
        self.token_type = token_type
        self.value = value
        self.line = line
        self.position = position

    def __repr__(self):
        return f"[Token]:: Type: [{self.token_type}], Val: [{self.value}], Line: [{self.line}], Pos: [{self.position}]"

    def __str__(self):
        return self.__repr__()


class TokenType(Enum):
    NUMBER = "NUMBER"
    STRING = "STRING"
    NAME = "NAME"
    KEYWORD = "KEYWORD"
    SYMBOL = "SYMBOL"
    OPERATOR = "OPERATOR"
    EOF = "EOF"
    ERROR = "ERR"
    UNKNOWN = "UNKW"
