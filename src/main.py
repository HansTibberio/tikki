import sys
import os

from semantic import SemanticAnalizer
from lexer import Scanner
from parser import Parser
from error import TikkiError
from symbol_table import SymbolTable


class Tikki:
    """Creates a new instance for Tikki, The Innovative Kitty Kompiler Interface"""
    args = sys.argv[1:]

    @classmethod
    def main(cls):
        os.system("cls" or "clear")
        if len(cls.args) > 1:
            print("Usage: python3 main.py [script]")
            sys.exit(64)
        elif len(cls.args) == 1:
            cls.run_file(cls.args[0])
        else:
            sys.exit(1)

    @classmethod
    def run_file(cls, path):
        try:
            with open(path, 'rb') as file:
                bytes_content = file.read()
                cls.run(bytes_content.decode())

                # Indicate error in the exit code
                if TikkiError.had_error:
                    sys.exit(1)

        except FileNotFoundError:
            print("File not found")

    @classmethod
    def run(cls, source):
        error = TikkiError(source)
        symbol_table = SymbolTable()

        Tikki_scanner = Scanner(source, error)
        tokens = Tikki_scanner.scan_tokens()

        Tikki_parser = Parser(tokens, error, symbol_table)
        statements = Tikki_parser.parse()

        analyzer = SemanticAnalizer(error, symbol_table)
        analyzer.analyze(statements)

        print("Defined Variables:", analyzer.variables_defined)
        print("Initialized Variables:", analyzer.variables_initialized)
        print("Used Variables:", analyzer.variables_used)
        print("Defined Constants:", analyzer.constants_defined)
        print("Used Constants:", analyzer.constants_used)

        # Stop if there was a syntax error.
        if TikkiError.had_error:
            return


"""
    generator = CodeGenerator()
    instructions = generator.generate(statements)

    with open('file.as', 'w') as file:
        tkcode.header(file)
        tkcode.stater(file)
        for instruction in generator.instructions:
            file.write(instruction + '\n')
        file.write("\nJMP .end")
    """


if __name__ == "__main__":
    Tikki.main()
