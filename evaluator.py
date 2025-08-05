from parser import Expression, Var, Not, And, Or, Implies, Biconditional


class Evaluator:
    def __init__(self, assignments: dict[str, bool]) -> None:
        self._assignments = assignments

    def evaluate(self, expr: Expression) -> bool:
        match expr:
            case Var(name):
                return self._assignments[name]
            case Not(expression):
                return not self.evaluate(expression)
            case And(left, right):
                return self.evaluate(left) and self.evaluate(right)
            case Or(left, right):
                return self.evaluate(left) or self.evaluate(right)
            case Implies(left, right):
                return not self.evaluate(left) or self.evaluate(right)
            case Biconditional(left, right):
                return self.evaluate(left) == self.evaluate(right)
            case _:
                raise Exception("Evaluation error: Unknown expression type.")


class VariableExtractor:
    def get_variables(self, expr: Expression) -> list[str]:
        variables: set[str] = set()
        self._extract(expr, variables)
        return sorted(list(variables))

    def _extract(self, expr: Expression, variables: set[str]) -> None:
        if isinstance(expr, Var):
            variables.add(expr.name)
        elif isinstance(expr, Not):
            self._extract(expr.expression, variables)
        elif isinstance(expr, (And, Or, Implies, Biconditional)):
            self._extract(expr.left, variables)
            self._extract(expr.right, variables)


class TruthTableGenerator:
    def __init__(self, expr: Expression, formula: str) -> None:
        self._expr = expr
        self._formula = formula
        self._variables = VariableExtractor().get_variables(self._expr)
        self._num_variables = len(self._variables)

    def generate_and_print(self) -> None:
        var_headers = " | ".join(self._variables)
        print(f"{var_headers} | {self._formula}")

        separator_length = len(var_headers) + 3 + len(self._formula)
        print("-" * separator_length)

        assignments = self._generate_assignments(0, {})
        for assignment in assignments:
            var_values = [("T" if assignment[v] else "F") for v in self._variables]
            formatted_var_values = " | ".join(var_values)
            result = Evaluator(assignment).evaluate(self._expr)
            result_str = "T" if result else "F"
            print(f"{formatted_var_values} | {result_str}")

    def _generate_assignments(
        self, index: int, current: dict[str, bool]
    ) -> list[dict[str, bool]]:
        if index == self._num_variables:
            return [current.copy()]

        var = self._variables[index]
        results: list[dict[str, bool]] = []
        current[var] = True
        results.extend(self._generate_assignments(index + 1, current))
        current[var] = False
        results.extend(self._generate_assignments(index + 1, current))

        return results
