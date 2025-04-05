from Tokens import Token, TokenType


class Lexer:
    def __init__(self, source) -> None:
        self.names = {}
        self.code: str = source
        self.size = len(self.code)
        self.line: int = 1
        self.position: int = 0
        self.current_char: chr = self.code[0]
        self.SYMBOLS = set("()+-*/%&|!<>\{\}[],.:#=")
        self.KEYWORDS = {
            "fn",
            "class",
            "hide",
            "export",
            "if",
            "elif",
            "elsefor",
            "return",
            "raise",
            "break",
            "continue",
            "handles",
            "not",
            "in",
            "is",
            "import",
            "use",
            "as",
            "null",
            "true",
            "false",
            "and",
            "or",
        }

    def advance(self) -> None:
        self.position += 1
        if self.position < self.size:
            self.current_char = self.code[self.position]
        else:
            self.current_char = None

    def skip_whitespace(self) -> None:
        while self.current_char in [" ", "\n", "\t", "\r"]:
            if self.current_char == "\n":
                self.line += 1
            self.advance()

    def skip_comments(self) -> None:
        start = self.line, self.position
        self.advance()
        self.advance()

        while not (self.current_char == "}" and self.peek() == "#"):
            self.advance()

            if self.current_char is None:
                # TODO: rewrite with errors later
                print(
                    f"ERR: Unclosed Comment starting at line: {start[0]}, pos: {start[1]}"
                )
                break

        self.advance()
        self.advance()

    def peek(self) -> str:
        if self.position + 1 < len(self.code):
            return self.code[self.position + 1]
        return None

    def make_number(self) -> float | int:
        start = self.line, self.position
        decimal_count = 0
        number = ""

        while self.current_char.isdigit() or self.current_char == ".":
            if self.current_char == ".":
                decimal_count += 1

                if decimal_count > 1:
                    # TODO: rewrite this with handling when you make errors
                    print(
                        f"ERR: Too many decimals at line: {self.line}, pos: {self.position}"
                    )
                    return None
            number += self.current_char
            self.advance()

        number = float(number) if decimal_count == 1 else int(number)
        return Token(TokenType.NUMBER, number, start[0], start[1])

    def make_name_or_keyword(self):
        word = ""
        start = self.line, self.position

        while self.current_char and (
            self.current_char.isalnum() or self.current_char == "_"
        ):
            word += self.current_char
            self.advance()

        if word in self.KEYWORDS:
            return Token(TokenType.KEYWORD, word, start[0], start[1])
        return Token(TokenType.NAME, word, start[0], start[1])

    def make_string(self) -> str:
        start = self.line, self.position
        string = ""
        self.advance()

        while self.current_char and self.current_char != "'":
            if self.current_char == "\\":
                self.advance()

                match self.current_char:
                    case "n":
                        string += "\n"
                    case "t":
                        string += "\t"
                    case "'":
                        string += "'"
                    case "\\":
                        string += "\\"

                    # include documentation as to why this have to be escaped
                    # the reason is that strings in trim are treated as f strings in python
                    # this means that {} cannot just be used
                    case "{":
                        string += "{"
                    case "}":
                        string += "}"
                    case _:
                        # TODO: Raise error
                        print(
                            f"ERR: Escape sequence isn't recognized line: {self.line}, pos{self.position - 1}"
                        )
            else:
                string += self.current_char

            self.advance()

        if self.current_char == "'":
            self.advance()
            return Token(TokenType.STRING, string, start[0], start[1])
        else:
            # TODO: Raise erro
            print(f"ERR: String not closed properly line: {start[0]}, pos: {start[1]}")
        return None

    # Note finishes on character after symbol
    def make_operator_or_symbol(self) -> Token:
        start = self.line, self.position
        symbol = self.current_char
        token = None
        match self.current_char:
            case "+":
                # +=
                if self.peek() == "=":
                    symbol += "="
                    self.advance()
                # ++
                elif self.peek() == "+":
                    symbol += "+"
                    self.advance()
                # if all previous fail operator is: "+"
                token = Token(TokenType.OPERATOR, symbol, start[0], start[1])
            case "-":
                # --
                if self.peek() == "-":
                    symbol += "-"
                    self.advance()
                # -=
                elif self.peek() == "=":
                    symbol += "="
                    self.advance()
                # if all previous fail operator is: "-"
                token = Token(TokenType.OPERATOR, symbol, start[0], start[1])
            case "*":
                # if false, *
                if self.peek() == "*":
                    symbol += "*"
                    self.advance()
                    # **= if true, else **
                    if self.peek() == "=":
                        symbol += "="
                        self.advance()
                # */
                elif self.peek() == "/":
                    symbol += "/"
                    self.advance()
                # *=
                elif self.peek() == "=":
                    symbol += "="
                    self.advance()
                token = Token(TokenType.OPERATOR, symbol, start[0], start[1])
            case "/":
                # if false, /
                if self.peek() == "/":
                    symbol += "/"
                    self.advance()
                    # //= if true else //
                    if self.peek() == "=":
                        symbol += "="
                        self.advance()
                # /%
                elif self.peek() == "%":
                    symbol += "%"
                    self.advance()
                # /=
                elif self.peek() == "=":
                    symbol += "="
                    self.advance()
                token = Token(TokenType.OPERATOR, symbol, start[0], start[1])
            case "%":
                # %= if true else %
                if self.peek() == "=":
                    symbol += "="
                    self.advance()
                token = Token(TokenType.OPERATOR, symbol, start[0], start[1])
            case "=":
                # if false, =
                if self.peek() == "=":
                    symbol += "="
                    self.advance()
                    # ==| if true else ==
                    if self.peek() == "|":
                        symbol += "|"
                        self.advance()
                token = Token(TokenType.OPERATOR, symbol, start[0], start[1])
            case "!":
                # if false, !
                if self.peek() == "=":
                    symbol += "="
                    self.advance()
                    # !=& if true else !=
                    if self.peek() == "&":
                        symbol += "&"
                        self.advance()
                token = Token(TokenType.OPERATOR, symbol, start[0], start[1])
            case "<":
                # <= if true else <
                if self.peek() == "=":
                    symbol += "="
                    self.advance()
                token = Token(TokenType.OPERATOR, symbol, start[0], start[1])
            case ">":
                # >= if true else >
                if self.peek() == "=":
                    symbol += "="
                    self.advance()
                token = Token(TokenType.OPERATOR, symbol, start[0], start[1])
            case "&":
                # &== if true else &
                if self.peek() == "=":
                    symbol += "="
                    self.advance()
                    if self.peek() == "=":
                        symbol += "="
                        self.advance()
                    else:
                        # TODO: either support this or raise error
                        print(
                            f"ERR: Operator is not currently support. line: {start[0]}, pos: {start[1]}"
                        )
                        self.advance()
                        return None
                token = Token(TokenType.OPERATOR, symbol, start[0], start[1])
            # catch all for symbols in this list ["(", ")", "[","]", "{", "}", ",", ".", ":"]
            case _:
                if self.current_char in {"(", ")", "[", "]", "{", "}", ",", ".", ":"}:
                    token = Token(TokenType.OPERATOR, symbol, start[0], start[1])
                else:
                    # TODO: raise ERR
                    print(f"ERR: Invalid symbol on line: {start[0]}, pos: {start[1]}")
                    self.advance()
                    return None
        self.advance()
        return token

    def tokenize(self) -> list[Token]:
        pass
        