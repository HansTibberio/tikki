from src.token_type import TokenType
from src.tokens import Token


class Scanner:
    """Docstring for Scanner"""

    def __init__(self, source, error):
        self.source = source
        self.error = error
        self.tokens = []  # Empty token list
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1  # Track the current column in the line
        self.start_column = 0  # Track where the current token started
        self.keywords = {
            "and": TokenType.AND,
            "break": TokenType.BREAK,
            "const": TokenType.CONST,
            "continue": TokenType.CONTINUE,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "fn": TokenType.FN,
            "for": TokenType.FOR,
            "if": TokenType.IF,
            "in": TokenType.IN,
            "not": TokenType.NOT,
            "null": TokenType.NULL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "self": TokenType.SELF,
            "super": TokenType.SUPER,
            "true": TokenType.TRUE,
            "let": TokenType.LET,
            "while": TokenType.WHILE
        }

    def scan_tokens(self):
        while not self.is_at_end():
            # We are at the beginning of the next lexeme.
            self.start = self.current
            self.start_column = self.column
            self.scan_token()

        self.tokens.append(
            Token(TokenType.EOF, "", None, self.line, self.column))
        return self.tokens

    def scan_token(self):
        c = self.advance()
        match c:
            case '(':
                self.add_token(TokenType.LEFT_PAREN)
            case ')':
                self.add_token(TokenType.RIGHT_PAREN)
            case '{':
                self.add_token(TokenType.LEFT_BRACE)
            case '}':
                self.add_token(TokenType.RIGHT_BRACE)
            case '[':
                self.add_token(TokenType.LEFT_BRACKET)
            case ']':
                self.add_token(TokenType.RIGHT_BRACKET)
            case ',':
                self.add_token(TokenType.COMMA)
            case '.':
                self.add_token(TokenType.DOT)
            case '-':
                self.add_token(TokenType.MINUS)
            case '%':
                self.add_token(TokenType.MODULO)
            case '+':
                self.add_token(TokenType.PLUS)
            case '&':
                self.add_token(TokenType.AMPERSAND)
            case '^':
                self.add_token(TokenType.CARET)
            case '|':
                self.add_token(TokenType.PIPE)
            case ';':
                self.add_token(TokenType.SEMICOLON)
            case '*':
                self.add_token(TokenType.STAR)
            case '!':
                self.add_token(TokenType.BANG_EQUAL if self.match(
                    '=') else TokenType.BANG)
            case '=':
                self.add_token(TokenType.EQUAL_EQUAL if self.match(
                    '=') else TokenType.EQUAL)
            case '<':
                if self.match('='):
                    self.add_token(TokenType.LESS_EQUAL)
                elif self.match('<'):
                    self.add_token(TokenType.LEFT_SHIFT)
                else:
                    self.add_token(TokenType.LESS)
            case '>':
                if self.match('='):
                    self.add_token(TokenType.GREATER_EQUAL)
                elif self.match('>'):
                    self.add_token(TokenType.RIGHT_SHIFT)
                else:
                    self.add_token(TokenType.GREATER)
            case '/':
                if self.match('*'):
                    # Block comments
                    self.block_comment()
                elif self.match('/'):
                    # A comment goes until the end of the line.
                    while self.peek() != '\n' and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            case ' ' | '\r' | '\t':
                # Ignore whitespace.
                pass
            case '\n':
                self.line += 1
                self.column = 1
            case '"':
                self.string()
            case _:
                if self.is_digit(c):
                    self.number()
                elif self.is_alpha(c):
                    self.identifier()
                else:
                    self.error.report(Token(TokenType.NULL, c, None, self.line,
                                      self.start_column), f"Unexpected character: '{c}'.")

    def identifier(self):
        while self.is_alpha_numeric(self.peek()):
            self.advance()

        text = self.source[self.start:self.current]
        token_type = self.keywords.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type)

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        self.add_token(TokenType.NUMBER, self.source[self.start:self.current])

    def string(self):
        initial_line = self.line
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.is_at_end():
            self.error.report(Token(TokenType.NULL, None, None, initial_line,
                                    self.start_column), "Unterminated string.")
            return

        # The closing ".
        self.advance()

        # Trim the surrounding quotes.
        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)

    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def block_comment(self):
        initial_line = self.line
        while not (self.peek() == '*' and self.peek_next() == '/') and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1  # Updates the line number
            self.advance()

        if self.is_at_end():
            self.error.report(Token(TokenType.NULL, None, None, initial_line,
                                    self.start_column), "Unterminated block comment.")
            return

        self.advance()
        self.advance()

    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def is_alpha(self, c):
        return ('a' <= c <= 'z') or ('A' <= c <= 'Z') or c == '_'

    def is_alpha_numeric(self, c):
        return self.is_alpha(c) or self.is_digit(c)

    def is_digit(self, c):
        return '0' <= c <= '9'

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        c = self.source[self.current]
        self.current += 1
        self.column += 1
        return c

    def add_token(self, type: TokenType, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(
            Token(type, text, literal, self.line, self.start_column))
