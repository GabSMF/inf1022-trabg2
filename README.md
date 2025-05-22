# Custom Grammar to C Transpiler

## Overview

This project implements a transpiler that converts programs written in a domain‑specific language (DSL) into equivalent C code. The DSL is defined by a formal grammar (see **Grammar** below) and supports variable declarations, arithmetic expressions, loops, conditionals, and monitored output.

The transpiler is built in **Python** using the **PLY** (Python Lex & Yacc) library and produces a `saida.c` file, which can then be compiled and executed with a standard C compiler.

## Features

* **Lexical analysis and parsing** via PLY
* **Grammar-driven code generation** targeting C
* **Variable initialization** with optional monitoring (via `MONITOR` keyword)
* **Control structures**: descending `for` loops (`EVAL`), `while`, `if`/`else`
* **Arithmetic operations**: addition, multiplication
* **Zeroing and equality assignments**

## Grammar

```
programa        → INICIO varlist monitor_varlist EXECUTE cmds TERMINO
monitor_varlist → MONITOR varlist
varlist         → ID (COMMA ID)*
cmds            → cmd+
cmd             → while | if | ifelse | plus | times | eval | zero | equal
while           → ENQUANTO ID FACA cmds FIM
if              → IF ID THEN cmd
ifelse          → IF ID THEN cmd ELSE cmd
eval            → EVAL LPAREN ID COMMA ID COMMA cmds RPAREN
plus            → (ID | NUM) PLUS exp
times           → (ID | NUM) TIMES exp
exp             → ID | NUM | plus | times
zero            → ZERO LPAREN ID RPAREN
equal           → ID EQUAL exp
```

## Installation

1. Install Python 3.x
2. Install the PLY library:

   ```bash
   pip install ply
   ```

## Usage

1. Place your source program in a file named `ex.provol` (or modify the script to read another filename).
2. Run the transpiler:

   ```bash
   python main.py
   ```
3. On success, a `saida.c` file is generated.
4. Compile and run the generated C code:

   ```bash
   gcc -o output saida.c
   ./output
   ```

## Implementation Details

* **Lexer and Parser** are defined in `main.py`, combining token definitions (`t_…`) and grammar rules (`p_…`).
* **Reserved words** and tokens are managed via a dictionary and PLY conventions.
* **Monitored variables**: any variable listed after `MONITOR` is printed via `printf` each time it is assigned or updated.
* **Loop translation**: `EVAL(X, Y, cmds)` is rendered as a C `for (int i = X; i > Y; i--) { cmds }`.
* **Error handling**: illegal characters and syntax errors are reported to the console; no C file is produced on parse failure.

## Limitations

* `EVAL` loops only support **descending** iteration; no ascending loops.
* `if` statements check only for non-zero vs. zero; no explicit comparison operators like `==` or `>`.
* No operator precedence beyond the recursive grammar for `plus` and `times` (no parentheses nesting).
* Generated `printf` calls do not include newline characters, so output may appear concatenated.
* No code formatting or indentation beyond basic newlines.

## Example

Given `ex2.provol`:

```provol
INICIO X, Y, B
MONITOR Z
EXECUTE
X = 5
Y = 2
B = 0
EVAL(X, Y,
  IF B THEN Z = Z + 2
  ELSE Z = Z + 1
)
TERMINO
```

The transpiler produces `saida.c` with:

```c
#include <stdio.h>

int main() {
  int X = 0;
  int Y = 0;
  int B = 0;
  int Z = 0;
  printf("Z = %d", Z);

  X = 5;
  Y = 2;
  B = 0;

  for (int i = X; i > Y; i--) {
    if (B) {
      Z = Z + 2;
      printf("Z = %d", Z);
    } else {
      Z = Z + 1;
      printf("Z = %d", Z);
    }
  }

  return 0;
}
```

## Test Cases

Three sample inputs and their generated behavior are described in `relatorio.pdf` under **Casos de Teste**.

## Authors

* Gabriel da Silva Marques Ferreira
* Rafael Chaves Bayão Ribeiro

## License

This project is released under the MIT License. Feel free to use and modify!
