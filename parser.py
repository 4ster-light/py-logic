from dataclasses import dataclass
from lexer import Token, TokenType


class Expression:
    pass


@dataclass(frozen=True)
class Var(Expression):
    name: str


@dataclass(frozen=True)
class Not(Expression):
    expression: Expression


@dataclass(frozen=True)
class And(Expression):
    left: Expression
    right: Expression


@dataclass(frozen=True)
class Or(Expression):
    left: Expression
    right: Expression


@dataclass(frozen=True)
class Implies(Expression):
    left: Expression
    right: Expression


@dataclass(frozen=True)
class Biconditional(Expression):
    left: Expression
    right: Expression


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self._tokens = tokens
        self._position = 0

    def _consume(self, expected_type: TokenType) -> None:
        if self._peek().type == expected_type:
            self._position += 1
        else:
            raise Exception(
                f"Parser error: Expected {expected_type} but found {self._peek().type}"
            )

    def _peek(self) -> Token:
        if self._position < len(self._tokens):
            return self._tokens[self._position]
        return Token(TokenType.Eof)

    def _parse_primary(self) -> Expression:
        token = self._peek()
        if token.type == TokenType.Variable:
            self._consume(TokenType.Variable)
            if token.lexeme is None:
                raise Exception("Parser error: Variable name is missing.")
            return Var(token.lexeme)
        elif token.type == TokenType.LParen:
            self._consume(TokenType.LParen)
            expr = self._parse_biconditional()
            self._consume(TokenType.RParen)
            return expr
        else:
            raise Exception(
                f"Parser error: Expected variable or '(' but found {token.type}"
            )

    def _parse_not(self) -> Expression:
        if self._peek().type == TokenType.NotOp:
            self._consume(TokenType.NotOp)
            return Not(self._parse_not())
        return self._parse_primary()

    def _parse_and(self) -> Expression:
        left = self._parse_not()
        while self._peek().type == TokenType.AndOp:
            self._consume(TokenType.AndOp)
            right = self._parse_not()
            left = And(left, right)
        return left

    def _parse_or(self) -> Expression:
        left = self._parse_and()
        while self._peek().type == TokenType.OrOp:
            self._consume(TokenType.OrOp)
            right = self._parse_and()
            left = Or(left, right)
        return left

    def _parse_implies(self) -> Expression:
        left = self._parse_or()
        if self._peek().type == TokenType.ImpliesOp:
            self._consume(TokenType.ImpliesOp)
            right = self._parse_implies()
            left = Implies(left, right)
        return left

    def _parse_biconditional(self) -> Expression:
        left = self._parse_implies()
        while self._peek().type == TokenType.BiconditionalOp:
            self._consume(TokenType.BiconditionalOp)
            right = self._parse_implies()
            left = Biconditional(left, right)
        return left

    def parse(self) -> Expression:
        expr = self._parse_biconditional()
        if self._peek().type != TokenType.Eof:
            raise Exception("Parser error: Unexpected tokens remaining.")
        return expr
