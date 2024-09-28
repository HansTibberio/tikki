class Token:
    """A token represents a unit of code at a specific place in the source text."""

    def __init__(self, token_type, lexeme, literal, line, column):
        self.type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
        self.column = column

    def __str__(self):
        return f"{self.type} {self.lexeme} {self.literal}"
