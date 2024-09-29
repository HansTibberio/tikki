from src.token_type import TokenType
from src.expr import *
from src.stmt import *
from src.error import ParseError


class Parser:
    def __init__(self, tokens, error):
        self.error = error
        self.tokens = tokens
        self.current = 0
        self.literal_pool = []

    def parse(self):
        statements = []
        try:
            while not self.is_at_end():
                statements.append(self.declaration())
            return statements
        except ParseError as error:
            return None

    def declaration(self):
        try:
            if self.match(TokenType.FN):
                return self.function("function")
            if self.match(TokenType.LET):
                return self.var_declaration()
            return self.statement()
        except ParseError as error:
            self.synchronize()

    def statement(self):
        if self.match(TokenType.FOR):
            return self.for_statement()
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.PRINT):
            return self.print_statement()
        if self.match(TokenType.WHILE):
            return self.while_statement()
        if self.match(TokenType.LEFT_BRACE):
            return Block(self.block())
        return self.expression_statement()

    def for_statement(self):

        self.consume(TokenType.LEFT_PAREN, "Expected '(' after 'for'.")

        initializer = None
        if self.match(TokenType.SEMICOLON):
            initializer = None
        if self.match(TokenType.LET):
            initializer = self.var_declaration()
        else:
            initializer = self.expression_statement()

        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after loop condtion.")

        increment = None
        if not self.check(TokenType.RIGHT_PAREN):
            increment = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expected ')' after for clauses.")

        if self.check(TokenType.LEFT_BRACE):
            pass
        else:
            raise ParseError(
                self.peek(), "Expected '{' after for statement.", self.error)

        body = self.statement()

        if increment is not None:
            body = Block([body, Expression(increment)])

        if condition is None:
            condition = Literal(True)
        body = While(condition, body)

        if initializer is not None:
            body = Block([initializer, body])

        return body

    def if_statement(self):
        """Parses an if statement in the source code.
        The structure of an if statement includes a condition inside parentheses, followed by
        a block of statements inside curly braces for the 'then' branch. Optionally, it can be followed
        by an 'else' branch with its own block of statements."""
        self.consume(TokenType.LEFT_PAREN, "Expected '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expected ')' after if condition.")

        if self.check(TokenType.LEFT_BRACE):
            pass
        else:
            raise ParseError(
                self.peek(), "Expected '{' after if condition.", self.error)

        then_branch = self.statement()

        else_branch = None
        if self.match(TokenType.ELSE):
            if self.check(TokenType.LEFT_BRACE):
                pass
            else:
                raise ParseError(
                    self.peek(), "Expected '{' before else branch.", self.error)
            else_branch = self.statement()

        return If(condition, then_branch, else_branch)

    def print_statement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after value.")
        return Print(value)

    def var_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expected variable name.")

        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()

        self.consume(TokenType.SEMICOLON,
                     "Expected ';' after variable declaration.")
        return Var(name, initializer)

    def while_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expected '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expected ')' after condition.")

        if self.check(TokenType.LEFT_BRACE):
            pass
        else:
            raise ParseError(
                self.peek(), "Expected '{' after while condition.", self.error)

        body = self.statement()

        return While(condition, body)

    def expression_statement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after expression.")
        return Expression(expr)

    def function(self, kind):
        name = self.consume(TokenType.IDENTIFIER,
                            "Expected " + kind + " name.")
        self.consume(TokenType.LEFT_PAREN,
                     "Expected '(' after " + kind + " name.")

        parameters = []
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                if len(parameters) >= 255:
                    raise ParseError(
                        self.peek(), "Can't have more than 255 parameters.", self.error)
                parameters.append(self.consume(
                    TokenType.IDENTIFIER, "Expected parameter name."))
                if not self.match(TokenType.COMMA):
                    break
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")
        self.consume(TokenType.LEFT_BRACE, f"Expect '{{' before {kind} body.")
        body = self.block()

        return Function(name, parameters, body)

    def block(self):
        """A block is a (possibly empty) series of statements or declarations surrounded by curly braces.
        A block is itself a statement and can appear anywhere a statement is allowed. """

        opening_token = self.previous()

        statements = []

        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())

        if self.is_at_end():
            raise ParseError(
                opening_token, "Unclosed delimiter.", self.error)

        self.consume(TokenType.RIGHT_BRACE,
                     "Unclosed delimiter. Expected '}' after block.")

        return statements

    def expression(self):
        return self.assigment()

    def assigment(self):
        expr = self.or_expr()

        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assigment()

            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)

            raise ParseError(equals, "Invalid assigment target.", self.error)

        return expr

    def or_expr(self):
        expr = self.and_expr()

        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.and_expr()
            expr = Logical(expr, operator, right)

        return expr

    def and_expr(self):
        expr = self.equality()

        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.equality()
            expr = Logical(expr, operator, right)

        return expr

    def equality(self):
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self):
        expr = self.inclusive()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.inclusive()
            expr = Binary(expr, operator, right)

        return expr

    def inclusive(self):
        expr = self.exclusive()

        while self.match(TokenType.PIPE):
            operator = self.previous()
            right = self.exclusive()
            expr = Binary(expr, operator, right)

        return expr

    def exclusive(self):
        expr = self.conjunction()

        while self.match(TokenType.CARET):
            operator = self.previous()
            right = self.conjunction()
            expr = Binary(expr, operator, right)

        return expr

    def conjunction(self):
        expr = self.shift()

        while self.match(TokenType.AMPERSAND):
            operator = self.previous()
            right = self.shift()
            expr = Binary(expr, operator, right)

        return expr

    def shift(self):
        expr = self.term()

        while self.match(TokenType.LEFT_SHIFT, TokenType.RIGHT_SHIFT):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self):
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self):
        expr = self.unary()

        while self.match(TokenType.MODULO, TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.call()

    def finish_call(self, callee):
        arguments = []

        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                if len(arguments) >= 255:
                    raise ParseError(
                        self.peek(), "Can't have more than 255 arguments.", self.error)
                arguments.append(self.expression())
                if not self.match(TokenType.COMMA):
                    break
        paren = self.consume(TokenType.RIGHT_PAREN,
                             "Expected ')' after arguments.")

        return Call(callee, paren, arguments)

    def call(self):
        expr = self.primary()

        while True:
            if self.match(TokenType.LEFT_PAREN):
                expr = self.finish_call(expr)
            else:
                break

        return expr

    def primary(self):
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NULL):
            return Literal(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            self.literal_pool.append(self.previous().literal)
            return Literal(self.previous().literal)

        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN,
                         "Expected ')' after expression.")
            return Grouping(expr)

        raise ParseError(self.peek(), "Expected expression.", self.error)

    def match(self, *types):
        """This checks to see if the current token has any of the given types.
        If so, it consumes the token and returns true.
        Otherwise, it returns false and leaves the current token alone."""
        for type_ in types:
            if self.check(type_):
                self.advance()
                return True

        return False

    def consume(self, type, message):
        """It’s similar to match() in that it checks to see if the next token is of the expected type.
        If so, it consumes the token and everything is groovy.
        If some other token is there, then we’ve hit an error."""
        if self.check(type):
            return self.advance()

        raise ParseError(self.peek(), message, self.error)

    def check(self, type_):
        """The check() method returns true if the current token is of the given type.
        Unlike match(), it never consumes the token, it only looks at it."""
        if self.is_at_end():
            return False
        return self.peek().type == type_

    def advance(self):
        """The advance() method consumes the current token and returns it."""
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        """Checks if we’ve run out of tokens to parse."""
        return self.peek().type == TokenType.EOF

    def peek(self):
        """Returns the current token we have yet to consume."""
        return self.tokens[self.current]

    def previous(self):
        """Returns the most recently consumed token."""
        return self.tokens[self.current - 1]

    def synchronize(self):
        """If we encounter an error, discard tokens until we find the
        beginning of the next statement
        """
        self.advance()

        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return

            if self.peek().type in {TokenType.CONST, TokenType.CLASS, TokenType.FN, TokenType.LET,
                                    TokenType.FOR, TokenType.IF, TokenType.WHILE,
                                    TokenType.PRINT, TokenType.RETURN}:
                return

            self.advance()
