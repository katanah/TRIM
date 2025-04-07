from AST import Node, Tree
from token import Token, TokenType
from Errors import ParserError


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None if self.tokens is None else self.tokens[0]
        self.current_idx = 0
        self.num_tokens = len(self.tokens)
        self.AST = Tree(Node("ProgramNode"))  # root of AST

    def advance(self) -> None:
        self.current_idx += 1
        if self.current_idx < self.num_tokens:
            self.current_token = self.tokens[self.current_idx]
        else:
            self.current_token = None

    def peek(self) -> Token:
        next_idx = self.current_idx + 1
        if next_idx < self.num_tokens:
            return self.tokens[next_idx]
        else:
            return None

    def parse_function(self):
        

    def parse_class(self):
        pass

    def parse_conditional(self):
        pass

    # return, break, continue
    def parse_flow_control(self):
        pass

    def parse_loops(self):
        pass

    def parse_program(self):
        pass

    def parse_declaration(self):
        pass

    def parse_modules(self):
        pass
    
    def parse_variables(self):
        pass

    def parse_statement(self):
        match self.current_token.token_type:
            case TokenType.KEYWORD:
                if self.current_token.value == "fn":
                    self.parse_function()
                elif self.current_token.value == "class":
                    self.parse_class()
                elif self.current_token.value == "if":
                    self.parse_conditional()
                elif self.current_token.value == "hide":
                    if self.peek().value == "fn":
                        self.parse_function()
                    elif self.peek().value == "class":
                        self.parse_class()
                    else:
                        # TODO: Assert when stable. this shouldn't happen if parser is built right
                        raise ParserError(f"Unexpected keyword after hide '{self.peek().value}' ", self.current_token)
                elif self.current_token.value in {"return", "break", "continue"}:
                    self.parse_flow_control()
                elif self.current_token.value in {"for", "while"}:
                    self.parse_loops()
                elif self.current_token.value in {"import", "export"}:
                    self.parse_modules()
                else:
                    # TODO: Assert when stable. this shouldn't happen if parser is built right
                    raise ParserError(f"Unexpected keyword '{self.current_token.value}'", self.current_token)
            case TokenType.NAME:
                self.parse_variables()
            case TokenType.ERROR:
                pass
            case TokenType.EOF:
                pass
