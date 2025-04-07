from Lexer import Lexer


def main():
    # Example Trim source code
    with open("example.trm", "r") as file:
        code = file.read()

    # Create a lexer
    # code = code.strip()
    lexer = Lexer(code)

    # Tokenize the source code
    tokens = lexer.tokenize()

    # Print all tokens
    # print(tokens)
    print("\t\b\bTYPE" + "\t\t\b\b" + "value")
    print("----------------------------------")
    for token in tokens:
        beginning = len("TokenType.Operator     ")
        string =  str(token.token_type)
        spaces = beginning - len(string)
        string = string + " "*spaces + str(token.value)
        print(string)


if __name__ == "__main__":
    main()