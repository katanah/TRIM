from Tokens import Token, TokenType


class Lexer:
    def __init__(self, source) -> None:
        self.names = {}
        self.code: str = source
        self.size = len(self.code)
        self.line: int = 1
        self.position: int = 0
        self.column = 0
        self.current_char: chr = None if not self.code else self.code[0]
        self.SYMBOLS = set("()+-*/%&|!<>\{\}[],.:#=")
        self.ALPHABET = set("qwertyuioplkjhgfdsazxcvbnm")
        self.NUMBERS = set("1234567890")
        self.SKIPABLE = set([" ", "\n", "\t", "\r"])
        self.KEYWORDS = {
            "fn",
            "class",
            "hide",
            "export",
            "if",
            "elif",
            "else",
            "for",
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
            "from",
            "where",
            "by",
        }

    def advance(self) -> None:
        self.position += 1
        self.column += 1
        if self.position < self.size:
            self.current_char = self.code[self.position]
        else:
            self.current_char = None

    def skip_whitespace(self) -> None:
        while self.current_char and self.current_char in [" ", "\n", "\t", "\r"]:
            if self.current_char == "\n":
                self.line += 1
                self.column = 0
            self.advance()

    def skip_comments(self) -> None:
        start = self.line, self.column
        self.advance()
        self.advance()

        while not (self.current_char == "}" and self.peek() == "#"):
            self.advance()
            if self.current_char is None:
                return Token(TokenType.ERROR, "Unclosed Comment", start[0], start[1])

        self.advance()
        self.advance()

    def peek(self) -> str:
        if self.position + 1 < len(self.code):
            return self.code[self.position + 1]
        return None

    def make_number(self) -> float | int:
        start = self.line, self.column
        decimal_count = 0
        number = ""
        while self.current_char and (
            self.current_char == "." or self.current_char.isdigit()
        ):
            if self.current_char == ".":
                decimal_count += 1
                # Case where either a loop is detected or too many decimals
                if self.peek() == ".":
                    token = Token(TokenType.NUMBER, int(number), start[0], start[1])
                    return token

                if decimal_count > 1:
                    # Too many nonsuccessive decimals
                    return Token(
                        TokenType.ERROR, "Too many decimals", self.line, self.column
                    )

            number += self.current_char
            self.advance()

        number = float(number) if decimal_count == 1 else int(number)
        return Token(TokenType.NUMBER, number, start[0], start[1])

    def make_range(self) -> Token | list[Token]:
        start = self.line, self.column
        decimal_count = 0

        while self.current_char == ".":
            decimal_count += 1
            self.advance()

        if decimal_count == 3:
            range_operator = Token(TokenType.OPERATOR, "...", start[0], start[1])
            end_of_range = ""
            end_of_range_column = None
            self.skip_whitespace()

            if not self.current_char.isdigit():
                end_of_range = 0
                end_of_range_column = start[1] + 3
            else:
                end_of_range_column = self.column
                while self.current_char and self.current_char.isdigit():
                    end_of_range += self.current_char
                    self.advance()
            
            end_of_range = Token(
                TokenType.NUMBER, int(end_of_range), start[0], end_of_range_column
            )
            return [range_operator, end_of_range]
        else:
            # Handles error wrong amount of decimals for iteration
            invalid_operator = "." * decimal_count
            return Token(
                TokenType.ERROR,
                f"Invalid operator: expected '...', found '{invalid_operator}'",
                start[0],
                start[1],
            )

    def make_name_or_keyword(self):
        word = ""
        start = self.line, self.column

        while self.current_char and (
            self.current_char.isalnum() or self.current_char == "_"
        ):
            word += self.current_char
            self.advance()

        if word in self.KEYWORDS:
            return Token(TokenType.KEYWORD, word, start[0], start[1])
        return Token(TokenType.NAME, word, start[0], start[1])

    def make_string(self) -> str:
        start = self.line, self.column
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
                        return Token(
                            TokenType.ERROR,
                            "Invalid Esacape Sequence",
                            self.line,
                            self.column,
                        )

            else:
                string += self.current_char

            self.advance()

        if self.current_char == "'":
            self.advance()
            return Token(TokenType.STRING, string, start[0], start[1])
        else:
            return Token(TokenType.ERROR, "String not closed", start[0], start[1])

    # Note finishes on character after symbol
    def make_operator(self) -> Token:
        start = self.line, self.column
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
                # if true ==, else =
                if self.peek() == "=":
                    symbol += "="
                    self.advance()
                token = Token(TokenType.OPERATOR, symbol, start[0], start[1])
            case "!":
                # if true !=, else !
                if self.peek() == "=":
                    symbol += "="
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
                # &= if true else &
                if self.peek() == "=":
                    symbol += "="
                    self.advance()
                    self.advance()
                    # Bitwise operations not support as of April 6, 2025
                    return Token(
                        TokenType.ERROR,
                        "Bitwise operations not supported",
                        start[0],
                        start[1],
                    )
                token = Token(TokenType.OPERATOR, symbol, start[0], start[1])
            case ".":
                # ... or error if true, else ".". if error it's handled in make_range() function
                if self.peek() == ".":
                    return self.make_range()
                token = Token(TokenType.OPERATOR, symbol, start[0], start[1])
            # catch all for symbols in this list ["(", ")", "[","]", "{", "}", ",", ".", ":"]
            case _:
                if self.current_char in {"(", ")", "[", "]", "{", "}", ",", ".", ":"}:
                    token = Token(TokenType.OPERATOR, symbol, start[0], start[1])
                else:
                    return Token(
                        TokenType.ERROR, "Operator Not Recognized", start[0], start[1]
                    )
        self.advance()
        return token

    def tokenize(self) -> list[Token]:
        tokens = []
        while self.current_char is not None:
            token = None

            if self.current_char in self.SKIPABLE:
                self.skip_whitespace()
            elif self.current_char == "#" and self.peek() == "{":
                token = self.skip_comments()
            if self.current_char in self.ALPHABET:
                token = self.make_name_or_keyword()
            elif self.current_char in self.NUMBERS:
                token = self.make_number()
            elif self.current_char == "'":
                token = self.make_string()
            elif self.current_char in self.SYMBOLS:
                token = self.make_operator()
            elif self.current_char is None:
                eof = Token(TokenType.EOF, "", self.line, self.column + 1)
                tokens.append(eof)
                return tokens
            else:
                # Unknown character
                token = Token(
                    TokenType.ERROR, "Unknown Character", self.line, self.column
                )

            if type(token) is list:
                tokens.extend(token)
            elif type(token) is Token:
                tokens.append(token)
            else:
                continue

        eof = Token(TokenType.EOF, "", self.line, self.column + 1)
        tokens.append(eof)
        return tokens
