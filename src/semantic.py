from error import ParseError


class SemanticAnalizer:
    def __init__(self, error, symbol_table):
        self.error = error
        self.symbol_table = symbol_table
        self.variables_defined = set()
        self.variables_initialized = set()
        self.variables_used = set()
        self.constants_defined = set()
        self.constants_used = set()

    def analyze(self, statements):
        try:
            for stmt in statements:
                self.visit(stmt)
        except Exception as error:
            return None

    def visit(self, node):
        method_name = f'visit_{type(node).__name__.lower()}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__.lower()} method')

    def visit_const(self, node):
        # Constant declaration: const <const> = <initializer>
        const_name = node.name.lexeme
        self.visit(node.initializer)
        self.constants_defined.add(const_name)

    def visit_var(self, node):
        # Variable declaration: let <var> = <initializer>
        var_name = node.name.lexeme
        self.variables_defined.add(var_name)
        if node.initializer:
            self.variables_initialized.add(var_name)
            self.visit(node.initializer)

    def visit_assign(self, node):
        # Variable assignment: <var> = <expr>
        var_name = node.name.lexeme
        self.variables_defined.add(var_name)
        self.visit(node.value)

    def visit_constant(self, node):
        # Usage of a constant: <const>
        const_name = node.name.lexeme
        self.constants_used.add(const_name)

    def visit_variable(self, node):
        # Usage of a variable: <var>
        if node.name.lexeme not in self.variables_initialized:
            raise ParseError(node.name,
                             f"Variables must be initialized before use '{node.name.lexeme}'.", self.error)
        var_name = node.name.lexeme
        self.variables_used.add(var_name)

    def visit_binary(self, node):
        # Binary operation: <left> <operator> <right>
        self.visit(node.left)
        self.visit(node.right)

    def visit_literal(self, node):
        # Literal value
        value = node.value
        return value

    def visit_block(self, node):
        # Block of statements
        for stmt in node.statements:
            self.visit(stmt)

    def visit_expression(self, node):
        self.visit(node.expression)

    def visit_if(self, node):
        # If statement: if (<condition>) { <then_branch> } else { <else_branch> }
        self.visit(node.condition)

        self.visit(node.then_branch)
        if node.else_branch:
            self.visit(node.else_branch)

    def visit_while(self, node):
        # While loop: while (<condition>) { <body> }

        self.visit(node.condition)
        self.visit(node.body)

    def visit_function(self, node):
        # Function definition: fn <name>(<params>) { <body> }

        self.visit(node.body)
