from enum import Enum


class TokenType(Enum):
    # Single-character tokens.
    LEFT_PAREN = 1
    RIGHT_PAREN = 2
    LEFT_BRACE = 3
    RIGHT_BRACE = 4
    LEFT_BRACKET = 5
    RIGHT_BRACKET = 6
    COMMA = 7
    DOT = 8
    MINUS = 9
    MODULO = 10
    PLUS = 11
    AMPERSAND = 12
    CARET = 13
    PIPE = 14
    SEMICOLON = 15
    SLASH = 16
    STAR = 17

    # One or two character tokens.
    BANG = 18
    BANG_EQUAL = 19
    EQUAL = 20
    EQUAL_EQUAL = 21
    GREATER = 22
    GREATER_EQUAL = 23
    LESS = 24
    LESS_EQUAL = 25
    LEFT_SHIFT = 26
    RIGHT_SHIFT = 27

    # Literals.
    IDENTIFIER = 28
    STRING = 29
    NUMBER = 30

    # Keywords.
    AND = 31
    BREAK = 32
    CONST = 33
    CONTINUE = 34
    CLASS = 35
    ELSE = 36
    FALSE = 37
    FN = 38
    FOR = 39
    IF = 40
    IN = 41
    NOT = 42
    NULL = 43
    OR = 44
    RETURN = 45
    SELF = 46
    SUPER = 47
    TRUE = 48
    LET = 49
    WHILE = 50

    # Data.
    EOF = 51
