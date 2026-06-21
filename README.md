# Lispy v2 - A Compact Lisp Interpreter in Python

A clean, compact implementation based on Peter Norvig's "How to Write a (Lisp) Interpreter (in Python)" with improvements for correctness and conciseness.

**Repository:** https://github.com/necat101/lispy-python

## What's New in v2

- **More compact**: ~140 lines (down from ~170)
- **Tail-call optimization**: `evl` uses a while loop for proper tail recursion
- **Quote syntax**: Support for `'x` as sugar for `(quote x)`
- **Variadic arithmetic**: `(+ 1 2 3 4)`, `(* 2 3 4)`, proper unary `-` and `/`
- **Multi-body functions**: Lambdas and defines can have multiple expressions
- **Better error handling**: Detects missing parens and trailing tokens
- **Improved `begin`**: Proper sequencing semantics

## Quick Start

```bash
# Clone and run
git clone https://github.com/necat101/lispy-python.git
cd lispy-python
python3 lis.py

# Run tests
python3 lis.py test
```

## Examples

### Basic Usage
```lisp
lispy> (+ 1 2 3 4)
10

lispy> (define (square x) (* x x))
lispy> (square 5)
25

lispy> '(1 2 3 4 5)
(1 2 3 4 5)
```

### Higher-Order Functions
```lisp
lispy> (map (lambda (x) (* x x)) '(1 2 3 4 5))
(1 4 9 16 25)

lispy> (define (filter pred lst)
         (if (null? lst)
             '()
             (if (pred (car lst))
                 (cons (car lst) (filter pred (cdr lst)))
                 (filter pred (cdr lst)))))
lispy> (filter (lambda (x) (> x 2)) '(1 2 3 4 5))
(3 4 5)
```

### Closures
```lisp
lispy> (define (make-counter)
         (define count 0)
         (lambda ()
           (set! count (+ count 1))
           count))
lispy> (define c (make-counter))
lispy> (c)
1
lispy> (c)
2
```

### Practical Examples
See `examples-advanced.lisp` for:
- Variadic arithmetic
- Map/filter/fold
- List utilities (length, append, reverse)
- Fibonacci (recursive and iterative)
- Function composition and currying
- Symbolic differentiation

## Implementation Highlights

The interpreter is built around a simple eval loop with explicit tail-call handling:

```python
def evl(x, env=GLOBAL):
    while True:  # Tail-call optimization
        if isinstance(x, Symbol): return env.find(x)[x]
        if not isinstance(x, list): return x
        # ... handle special forms ...
        # For tail positions, set x and continue loop instead of recursing
```

**Core components:**
1. **Parser**: Tokenize → read (recursive descent) → AST
2. **Environment**: Chain of dicts for lexical scoping
3. **Procedures**: Closures capturing params, body, and environment
4. **Evaluator**: Direct-style with proper tail calls

## Testing

```bash
$ python3 lis.py test
Running Lispy tests...

✓ (+ 1 2 3 4)
  => 10
✓ (map (lambda (x) (* x x)) '(1 2 3 4 5))
  => [1, 4, 9, 16, 25]
✓ (fact 10)
  => 3628800
...

28 passed, 0 failed
```

## Hacker News Context

This implementation was inspired by [HN discussion #48619831](https://news.ycombinator.com/item?id=48619831) on Norvig's tutorial. Key insights from the community:

- Writing interpreters remains a valuable learning exercise despite AI advances
- Lisp's minimal syntax makes it ideal for understanding language implementation
- The parentheses debate: formatting and tooling matter more than syntax
- MAL (Make-A-Lisp) mentioned as another excellent tutorial resource

## Files

- `lis.py` - The interpreter (~140 lines)
- `examples.lisp` - Basic examples
- `examples-advanced.lisp` - Advanced patterns and algorithms
- `README.md` - This file

## License

Public domain / MIT - Based on Peter Norvig's original code
