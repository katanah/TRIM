from AST import Node, Tree
from Lexer import Lexer


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens

    def advance(self):
        pass

    def peek(self):
        pass

    def match_token(self):
        pass

    def match(self):
        pass

    def parse_function(self):
        pass

    def parse_class(self):
        pass

    def parse_conditional(self):
        pass
    
    # return, break, continue
    def parse_flow_control(self):
        pass

    def parse_(self):
        pass

    def parse_program(self):
        pass

    def parse_declaration(self):
        pass
