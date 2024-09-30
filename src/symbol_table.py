

class Symbol:
    """
    Represents a symbol in the symbol table.
    This can be a variable, function, constant, or other identifier.

    Attributes:
        name (str): The identifier of the symbol (e.g., 'data', 'pi', 'isLevel').
        symbol (str): The symbol type (e.g., variable, constant or function)
        type (str): The data type of the symbol (e.g., u8, i16, char).
        scope_level (int): The scope in which the symbol is defined (e.g., global or local).
    """

    def __init__(self, name: str, symbol: str, type: str, scope_level: int, value=None):
        """
        Initializes a symbol with its name, symbol, type and scope.

        Args:
            name (str): The identifier name of the symbol.
            symbol (str): The symbol type or classification.
            type (str): The data type or bytes of the symbol.
            scope_level (int): The depth level of the current scope.
            value (optional): The value assigned to the symbol (if any).
        """
        self.name = name
        self.symbol = symbol
        self.type = type
        self.scope_level = scope_level

    def __repr__(self):
        return f"| name={self.name} | symbol={self.symbol} | type={self.type} | scope={self.scope_level} |\n"


class SymbolTable:
    """
    A symbol table that tracks variables, functions, constants, and other identifiers.
    It supports multiple scopes, allowing each scope to have its own set of defined symbols.

    Attributes:
        scopes (list): A list of dictionaries where each dictionary represents a scope.
                      The first scope is the global scope, and additional scopes are nested.
    """

    def __init__(self):
        """
        Initializes the symbol table with a single global scope (represented by an empty dictionary).
        """
        self.scopes = [
            {}]  # Start with the global scope as the initial (and only) scope.

    def enter_scope(self):
        """
        Enters a new scope by adding an empty dictionary to represent a new level of scope.
        This is typically called when entering a function, block, or new context.
        """
        self.scopes.append({})

    def exit_scope(self):
        """
        Exits the current scope by removing the most recent dictionary representing the current scope.
        Raises an error if trying to exit the global scope.
        """
        if len(self.scopes) > 1:
            self.scopes.pop()
        else:
            raise RuntimeError("Cannot exit the global scope.")

    def define(self, name: str, symbol: str, type: str):
        """
        Defines a new symbol in the current scope.

        Args:
            name (str): The identifier name of the symbol.
            symbol_type (str): The type of the symbol (e.g., u8, function, etc.).
            value (optional): The initial value of the symbol (if applicable).

        The symbol is added to the current (most recent) scope.
        """
        scope_level = len(self.scopes) - \
            1  # The scope level corresponds to the depth of the current scope.
        symbol = Symbol(name, symbol, type, scope_level)
        # Insert symbol into the current scope.
        self.scopes[scope_level][name] = symbol

    def lookup(self, name: str):
        """
        Looks up a symbol by its name, starting from the innermost scope and moving outward to global scope.

        Args:
            name (str): The identifier name of the symbol to look up.

        Returns:
            Symbol: The symbol if it is found, or None if it is not defined.
        """
        # Search from the innermost scope (most recent) to the global scope (first).
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def update(self, name: str, value):
        """
        Updates the value of an existing symbol, starting from the innermost scope.
        If the symbol is found, its value is updated.

        Args:
            name (str): The name of the symbol to update.
            value: The new value to assign to the symbol.

        Raises:
            RuntimeError: If the symbol is not defined in any scope.
        """
        # Search from the innermost scope to global scope.
        for scope in reversed(self.scopes):
            if name in scope:
                scope[name].value = value
                return
        # Raise an error if symbol is not found.
        raise RuntimeError(f"Symbol '{name}' not defined.")

    def __repr__(self):
        return f"SymbolTable(scopes={self.scopes})"
