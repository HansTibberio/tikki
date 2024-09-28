import sys
import os

from generator import CodeGenerator
from scanner import Scanner
from parser import Parser
from error import TikkiError


class Tikki:
    """Creates a new instance for Tikki, The Innovative Kitty Kompiler Interface"""
    args = sys.argv[1:]
    had_runtime_error = False

    @classmethod
    def main(cls):
        os.system("cls" or "clear")
        if len(cls.args) > 1:
            print("Usage: python3 main.py [script]")
            sys.exit(64)
        elif len(cls.args) == 1:
            cls.run_file(cls.args[0])
        else:
            cls.run_prompt()

    @classmethod
    def run_file(cls, path):
        try:
            with open(path, 'rb') as file:
                bytes_content = file.read()
                cls.run(bytes_content.decode())

                # Indicate error in the exit code
                if TikkiError.had_error:
                    sys.exit(65)
                if Tikki.had_runtime_error:
                    sys.exit(70)

        except FileNotFoundError:
            print("File not found")

    @classmethod
    def run_prompt(cls):
        while True:
            try:
                line = input("> ")
                if line == "":
                    break
                cls.run(line)
                TikkiError.had_error = False
            except (EOFError, KeyboardInterrupt):
                print("\nExiting REPL...")
                break

    @classmethod
    def run(cls, source):
        error = TikkiError(source)
        Tikki_scanner = Scanner(source, error)
        tokens = Tikki_scanner.scan_tokens()
        Tikki_parser = Parser(tokens, error)
        statements = Tikki_parser.parse()

        # Stop if there was a syntax error.
        if TikkiError.had_error:
            return

        generator = CodeGenerator()
        instructions = generator.generate(statements)

        with open('file.as', 'w') as file:
            file.write("JMP .main\n\n.end\nHLT\n\n.main\n")
            for instruction in generator.instructions:
                file.write(instruction + '\n')
            file.write("\nJMP .end")


if __name__ == "__main__":
    Tikki.main()
