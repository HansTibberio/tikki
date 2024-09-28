from token_type import TokenType
import expr
import stmt
from registers import Registers
import libraries


class CodeGenerator(expr.Visitor, stmt.Visitor):

    def __init__(self) -> None:
        self.registers = Registers()
        self.instructions = []

    def generate(self, statements):
        for stmt in statements:
            self.execute(stmt)

    def visit_expression_stmt(self, stmt):
        self.evaluate(stmt.expression)
        return None

    def evaluate(self, expr):
        return expr.accept(self)

    def execute(self, statement):
        statement.accept(self)

    def visit_literal_expr(self, expr):
        reg = self.registers.pop()
        self.instructions.append(f"LDI {reg} {expr.value}")
        return reg

    def visit_binary_expr(self, expr):

        left_register = self.evaluate(expr.left)
        right_register = self.evaluate(expr.right)
 
        match expr.operator.type:
            case TokenType.GREATER_EQUAL:
                libraries.greater_than_or_equal_function(
                    self, left_register, right_register)
            case TokenType.PIPE:
                libraries.or_function(self, left_register, right_register)
            case TokenType.CARET:
                self.instructions.append(
                    f"XOR {left_register} {right_register} {left_register}")
            case TokenType.AMPERSAND:
                self.instructions.append(
                    f"AND {left_register} {right_register} {left_register}")
            case TokenType.LEFT_SHIFT:
                libraries.left_shift(self, left_register,
                                     right_register)
            case TokenType.RIGHT_SHIFT:
                libraries.right_shift(self, left_register,
                                      right_register)
            case TokenType.PLUS:
                self.instructions.append(
                    f"ADD {left_register} {right_register} {left_register}")
            case TokenType.MINUS:
                self.instructions.append(
                    f"SUB {left_register} {right_register} {left_register}")
            case TokenType.STAR:
                libraries.multiply_function(
                    self, left_register, right_register)

        self.registers.push(right_register)
        return left_register
