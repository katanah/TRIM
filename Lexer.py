import Tokens
    
class Lexer:
    def __init__(self, source):
        self.tokens = []
        self.code = source
        self.line = 0
        self.position = 0
        self.current_char = self.code[0][0]
        
    def advance(self):
        pass
    def skip_whitespace(self):
        while 
    def skip_comments(self):
        pass
    def peek(self):
        pass
    def find_num():
        pass
    def find_name_or_keyword():
        pass
    def find_string():
        pass
    def find_operator_or_symbol():
        pass