from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Abstraction:
    bound: str
    body: Abstraction | Application | str

    def get_children(self):
        return [self.body]

    def binding_substitute(self, var: str, new_expr: Abstraction | Application | str):
        if self.bound == var:
            raise ValueError("Bound variable in an abstraction!")
        else:
            if type(self.body) == str:
                if self.body == var:
                    self.body = new_expr
            else:
                self.body.binding_substitute(var, new_expr)

    def reverse_substitute(self, var: str, new_expr: Abstraction | Application | str):
        if self.body == new_expr:
            self.body = var

        if not isinstance(self.body, str):
            self.body.reverse_substitute(var, new_expr)

    def __str__(self):
        return f"lambda {self.bound} . ({self.body})"


@dataclass(slots=True)
class Application:
    expr1: Abstraction | Application | str
    expr2: Abstraction | Application | str

    def get_children(self):
        return [self.expr2, self.expr1]

    def binding_substitute(self, var: str, new_expr: Abstraction | Application | str):
        if type(self.expr1) == str:
            if self.expr1 == var:
                self.expr1 = new_expr
        else:
            self.expr1.binding_substitute(var, new_expr)

        if type(self.expr2) == str:
            if self.expr2 == var:
                self.expr2 = new_expr
        else:
            self.expr2.binding_substitute(var, new_expr)

    def reverse_substitute(self, var: str, new_expr: Abstraction | Application | str):
        if self.expr1 == new_expr:
            self.expr1 = var
        elif self.expr2 == new_expr:
            self.expr2 = var

        if not isinstance(self.expr1, str):
            self.expr1.reverse_substitute(var, new_expr)
        if not isinstance(self.expr2, str):
            self.expr2.reverse_substitute(var, new_expr)

    def __str__(self):
        return f"({self.expr1} {self.expr2})"


# @dataclass(slots=True)
# class Expression:
#     root_expr: Abstraction | Application | str
#
#     def __iter__(self):
#         pass