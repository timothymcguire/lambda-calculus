from __future__ import annotations

from lark import Lark, Transformer, UnexpectedEOF
from expression import Abstraction, Application


class LambdaTransformer(Transformer):
    def decl(self, bindings):
        return {name: expr for name, expr in bindings}

    def expr(self, items):
        return items[0]

    def bind(self, bind):
        return (bind[0], bind[1])

    def application(self, items):
        return Application(items[0], items[1])

    def abstraction(self, items):
        return Abstraction(items[0], items[1])

    def VARIABLE(self, var):
        return var.value


def _substitute(expr, var, new_expr):
    if isinstance(expr, str):
        if expr == var:
            return new_expr
        else:
            return expr
    elif isinstance(expr, Application):
        return Application(
            _substitute(expr.expr1, var, new_expr),
            _substitute(expr.expr2, var, new_expr)
        )
    elif isinstance(expr, Abstraction):
        if expr.bound == var:
            return Abstraction(
                expr.bound,
                expr.body
            )
        else:
            return Abstraction(
                expr.bound,
                _substitute(expr.body, var, new_expr)
            )


def b_reduction(expr):
    if isinstance(expr, Application):
        if isinstance(expr.expr1, Application):
            expr.expr1 = b_reduction(expr.expr1)
            return expr
        elif isinstance(expr.expr1, Abstraction):
            return _substitute(expr.expr1.body, expr.expr1.bound, expr.expr2)
        else:
            return expr.expr1


def binding_substitute(expr, var, new_expr):
    if type(expr) == str:
        if expr == var:
            return new_expr
        else:
            return expr
    else:
        expr.binding_substitute(var, new_expr)
        return expr


def reverse_substitute(expr, var, new_expr):
    if expr == new_expr:
        return var

    if isinstance(expr, str):
        return expr
    else:
        expr.reverse_substitute(var, new_expr)
        return expr


class LambdaInterpreter:
    with open("lambda.lark", "r") as f:
        grammar = f.read()

    expr_parser = Lark(grammar, start="expr")
    decl_parser = Lark(grammar, start="decl")
    transformer = LambdaTransformer()

    def __init__(self, filenames: [str] | str | None = None):
        self.bindings = {}

        if type(filenames) == list:
            for filename in filenames:
                self.parse_file(filename)
        elif type(filenames) == str:
            self.parse_file(filenames)

    def parse_file(self, filename: str):
        with open(filename, "r") as f:
            decl = LambdaInterpreter.decl_parser.parse(f.read())

        for key, value in LambdaInterpreter.transformer.transform(decl).items():
            self.bindings[key] = value

    def replace_bindings(self, expr: Abstraction | Application | str):
        old_expr = None
        while old_expr != expr:
            old_expr = expr
            for binding, new_expr in self.bindings.items():
                expr = binding_substitute(expr, binding, new_expr)
        return expr

    def add_bindings(self, expr: Abstraction | Application | str):
        new = expr
        for binding, bind_expr in self.bindings.items():
            new = reverse_substitute(new, binding, bind_expr)
        return new

    def eval(self, string: str) -> Abstraction | Application | str:
        p = LambdaInterpreter.expr_parser.parse(string)
        expr = LambdaInterpreter.transformer.transform(p)
        expr = self.replace_bindings(expr)

        # Beta reduction
        while isinstance(expr, Application):
            expr = b_reduction(expr)

        expr = self.add_bindings(expr)
        return expr

    def eval_steps(self, string):
        p = LambdaInterpreter.expr_parser.parse(string)
        expr = LambdaInterpreter.transformer.transform(p)
        expr = self.replace_bindings(expr)
        yield f"     => {expr}"

        i = 1
        while isinstance(expr, Application):
            expr = b_reduction(expr)
            yield f"B, {i} => {str(expr)}"
            i += 1

        expr = self.add_bindings(expr)
        yield f"     => {expr}"



if __name__ == '__main__':
    i = LambdaInterpreter("declarations.lambda")
    print(i.eval("(lambda x . x x) (lambda x . x x)"))
