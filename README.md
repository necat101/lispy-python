# Lispy - A Lisp Interpreter in Python

A clean implementation of Peter Norvig's "How to Write a (Lisp) Interpreter (in Python)" from https://norvig.com/lispy.html

## Overview

This project implements a Scheme-like Lisp interpreter in Python, following Norvig's classic tutorial. The interpreter supports:

- Basic arithmetic: `+`, `-`, `*`, `/`
- Comparisons: `>`, `<`, `>=`, `<=`, `=`
- Control flow: `if`, `define`, `set!`, `lambda`
- List operations: `car`, `cdr`, `cons`, `list`, `append`
- Mathematical functions from Python's math module
- Recursive functions and lexical scoping
- Closures

## Usage

### Run the REPL
```bash
python3 lis.py
```

### Run tests
```bash
python3 lis.py test
```

### Examples

```lisp
;; Basic arithmetic
(+ 1 2 3)           ; => 6
(* 3 4)             ; => 12

;; Define variables
(define r 10)
(* pi (* r r))      ; => 314.159...

;; Define functions
(define square (lambda (x) (* x x)))
(square 5)          ; => 25

;; Recursion
(define fact (lambda (n)
  (if (<= n 1)
      1
      (* n (fact (- n 1))))))
(fact 10)           ; => 3628800

;; Lists
(list 1 2 3)        ; => (1 2 3)
(car (list 1 2 3))   ; => 1
(cdr (list 1 2 3))  ; => (2 3)
(cons 0 (list 1 2)) ; => (0 1 2)
```

## Implementation Details

The interpreter consists of:

1. **Parser** (`parse`, `tokenize`, `read_from_tokens`): Converts Lisp code to Python data structures
2. **Evaluator** (`eval`): Executes the parsed code in an environment
3. **Environment** (`Env`): Manages variable bindings with lexical scoping
4. **Procedures** (`Procedure`): Implements user-defined functions with closures

Total: ~150 lines of Python code (excluding tests and comments)

## Hacker News Discussion

This implementation was inspired by the Hacker News thread discussing Norvig's lispy tutorial. The community sentiment was overwhelmingly positive about:

- Lisp interpreters as excellent learning exercises
- The educational value of implementing languages
- Appreciation for Norvig's clear, minimal implementation
- The timeless nature of good programming tutorials despite AI advances

Key takeaways from the discussion:
- Writing a Lisp is a favorite "rite of passage" project
- Understanding parentheses and S-expressions changes how you view code structure
- The simplicity of Lisp syntax makes it ideal for learning interpreter concepts
- Good learning resources remain valuable regardless of AI tools

## Files

- `lis.py` - Main interpreter implementation
- `README.md` - This file
- `examples.lisp` - Example Lisp programs

## License

MIT - Based on Peter Norvig's public domain code
