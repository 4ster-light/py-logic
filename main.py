import sys
from lexer import Lexer, Token
from parser import Parser, Expression
from evaluator import TruthTableGenerator


def debug(formula: str, tokens: list[Token], expression: Expression) -> None:
    print(f"- Formula:\n  - {formula}", end="\n\n")
    print("- Tokens:", *[f"  - {token}" for token in tokens], sep="\n", end="\n\n")
    print(f"- Expression:\n  - {expression}")


if __name__ == "__main__":
    print("Enter a logical formula (e.g., P & Q -> R, !A | B):")

    try:
        formula = input("\n")
        print()

        tokens = Lexer(formula).lex()
        expression = Parser(tokens).parse()

        if len(sys.argv) > 1 and sys.argv[1] == "--debug":
            debug(formula, tokens, expression)
        else:
            TruthTableGenerator(expression, formula).generate_and_print()
    except Exception as ex:
        print(f"Error: {ex}", file=sys.stderr)
