
# <div align="center"> The Innovative Kitty Kompiler Interface </div>

<div align="center">

[![License][license-badge]][license-link]

</div>


**TIKKI** is a new and lightweight compiler for Tiny Kitten Instructions (`.tki`), designed to compile down to assembly language targeting the [BatPU-2](https://github.com/mattbatwings/BatPU-2) 8-bit instruction set architecture.
## Overview
The `.tki` instructions are loosely based on the [Lox](https://github.com/munificent/craftinginterpreters) language from Crafting Interpreters but adapted to the BatPU-2's architecture. **TIKKI** supports various basic expressions and operators, including unary, arithmetic, comparison, and bitwise operations. The language also provides fundamental statements such as control flow (`if`, `for`, `while`), function declaration, and usage.
## Roadmap
- [x]  ***Lexer***.
- [x]  ***Parser***.
- [x]  ***AST*** Abstract Syntax Tree representation.
- [x]  ***Basic Error Handling***
- [x]  ***Constants***. Add support for constants. Constants must be declared before use, cannot be reassigned, and should be immutable.
- [ ]  ***Functions***. Add support for functions.
- [ ]  ***Data type declarations***:  Support for variable types `u8`, `i8`, `u16`, `i16`, `char`
- [ ]  ***Semantic Analysis***: Add semantic rules and type-checking to the compiler.
- [ ]  ***Comments***: Improve documentation across functions and methods.
- [ ]  ***Error Reporting Improvements***: Enhance error messages to provide more clarity and context.
- [ ]  ***Intermediate Representation (IR)***: Implement an intermediate representation of the code to facilitate optimizations and easier translation to assembly.
- [ ]  ***Symbol Table***: Add a symbol table to track variable declarations, types, functions, and scope throughout the program.
- [ ]  ***Assembly Backend***: Finalize the backend to ensure efficient generation of BatPU-2 assembly code, including register management and instruction optimizations.


## Contributing

Feel free to contribute and enhance the project!


[license-link]:https://github.com/hanstibberio/tikki/blob/master/LICENSE
[license-badge]:https://img.shields.io/github/license/hanstibberio/tikki?style=for-the-badge&label=license&color=success