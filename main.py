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
    for token in tokens:
        print(token)


if __name__ == "__main__":
    main()