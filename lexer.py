from typing import Optional
from dataclasses import dataclass


class TokenType:
    LParen = "LParen"
    RParen = "RParen"
    NotOp = "NotOp"
    AndOp = "AndOp"
    OrOp = "OrOp"
    ImpliesOp = "ImpliesOp"
    BiconditionalOp = "BiconditionalOp"
    Variable = "Variable"
    Eof = "Eof"


@dataclass(frozen=True)
class Token:
    type: str
    lexeme: Optional[str] = None


class Lexer:
    def __init__(self, input: str) -> None:
        self._input = input
        self._position = 0

    def _peek(self, offset: int = 0) -> Optional[str]:
        if self._position + offset < len(self._input):
            return self._input[self._position + offset]
        return None

    def _advance(self, count: int = 1) -> None:
        self._position += count

    def lex(self) -> list[Token]:
        tokens: list[Token] = []
        while self._position < len(self._input):
            current_char = self._input[self._position]
            match current_char:
                case char if char.isspace():
                    self._advance()
                case "(":
                    tokens.append(Token(TokenType.LParen, "("))
                    self._advance()
                case ")":
                    tokens.append(Token(TokenType.RParen, ")"))
                    self._advance()
                case "!":
                    tokens.append(Token(TokenType.NotOp, "!"))
                    self._advance()
                case "&":
                    tokens.append(Token(TokenType.AndOp, "&"))
                    self._advance()
                case "|":
                    tokens.append(Token(TokenType.OrOp, "|"))
                    self._advance()
                case "-":
                    if self._peek(1) == ">":
                        tokens.append(Token(TokenType.ImpliesOp, "->"))
                        self._advance(2)
                    else:
                        raise Exception(
                            f"Lexer error: Unexpected character '{current_char}' at position {self._position}. Expected '->'."
                        )
                case "<":
                    if self._peek(1) == "-" and self._peek(2) == ">":
                        tokens.append(Token(TokenType.BiconditionalOp, "<->"))
                        self._advance(3)
                    else:
                        raise Exception(
                            f"Lexer error: Unexpected character '{current_char}' at position {self._position}. Expected '<->'."
                        )
                case char if "A" <= char <= "Z":
                    tokens.append(Token(TokenType.Variable, char))
                    self._advance()
                case _:
                    raise Exception(
                        f"Lexer error: Unexpected character '{current_char}' at position {self._position}"
                    )

        tokens.append(Token(TokenType.Eof))

        return tokens
