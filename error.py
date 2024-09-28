from colorama import Fore, Style
from token_type import TokenType


class RuntimeError(Exception):
    def __init__(self, token, message, reporter, phase="Runtime"):
        super().__init__(message)
        self.token = token
        self.reporter = reporter
        self.phase = phase

        self.reporter.report(token, message, phase)


class DivisionByZeroError(RuntimeError):
    def __init__(self, token, reporter):
        super().__init__(token, "Division by zero is not allowed.", reporter)
        self.phase = "Arithmetic"


class ModuloByZeroError(RuntimeError):
    def __init__(self, token, reporter):
        super().__init__(token, "Modulo by zero is not allowed.", reporter)
        self.phase = "Arithmetic"


class InvalidOperandError(RuntimeError):
    def __init__(self, token, operand, reporter):
        message = f"Invalid operand: '{operand}'."
        super().__init__(token, message, reporter)
        self.phase = "Type"


class InvalidOperandsError(RuntimeError):
    def __init__(self, token, left, right, reporter):
        message = f"Invalid operands: '{left}' and '{right}'."
        super().__init__(token, message, reporter)
        self.phase = "Type"


class UndefinedVariableError(RuntimeError):
    def __init__(self, token, variable_name, reporter):
        message = f"Undefined variable '{variable_name}'."
        super().__init__(token, message, reporter)
        self.phase = "Resolution"


class TypeMismatchError(RuntimeError):
    def __init__(self, token, expected, actual, reporter):
        message = f"Expected type {expected}, but got {actual}."
        super().__init__(token, message, reporter)
        self.phase = "Type"


class ParseError(Exception):
    def __init__(self, token, errordescription, reporter):
        self.token = token
        self.reporter = reporter
        phase = "Parse"

        if token.type == TokenType.EOF:
            message = f"at end: {errordescription}"
            TikkiError.had_error = True
        else:
            message = f" at '{token.lexeme}': {errordescription}"
            TikkiError.had_error = True

        self.reporter.report(token, message, phase)
        super().__init__(message)


class TikkiError:
    had_error = False

    def __init__(self, source_code) -> None:
        self.source_code = source_code.splitlines()

    def report(self, token, message, phase="Syntax"):
        line_number = token.line - 1
        column = token.column
        source_line = self.source_code[line_number]
        self.display_error(source_line, token.line, column, message, phase)

    def display_error(self, source_line, line, column, message, phase):
        max_line_number_digits = len(str(line + 1))
        line_marker_format = f"{{:>{max_line_number_digits}}} | "
        prefix = ''.join(
            ['\t' if char == '\t' else ' ' for char in source_line[:column-1]])

        print(Fore.RED + Style.BRIGHT +
              f"[{phase}Error]" + Fore.WHITE + f" in line {line}:{column}:" + Style.RESET_ALL)
        print(Fore.CYAN + Style.BRIGHT + line_marker_format.format(""))
        print(f"{line} | " + Fore.WHITE + Style.NORMAL +
              source_line.rstrip() + Style.RESET_ALL)
        print(Fore.CYAN + Style.BRIGHT + line_marker_format.format("") + Fore.RED + Style.BRIGHT + prefix +
              '^ ' + message + Style.RESET_ALL)

    @staticmethod
    def error(line, where, source_line, message):
        TikkiError.had_error = True
        TikkiError.report(line, where, source_line, message)
