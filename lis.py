#!/usr/bin/env python3
"""
Lispy: A Simple Lisp Interpreter in Python
Based on Peter Norvig's "How to Write a (Lisp) Interpreter (in Python)"
https://norvig.com/lispy.html

This implementation follows Norvig's design with improvements for clarity.
"""

import math
import operator as op
from typing import Union, List, Any, Dict

# Types
Symbol = str
Number = Union[int, float]
Atom = Union[Symbol, Number]
Exp = Union[Atom, List]

def tokenize(chars: str) -> List[str]:
    """Convert a string of characters into a list of tokens."""
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()

def parse(program: str) -> Exp:
    """Read a Scheme expression from a string."""
    return read_from_tokens(tokenize(program))

def read_from_tokens(tokens: List[str]) -> Exp:
    """Read an expression from a sequence of tokens."""
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF')
    token = tokens.pop(0)
    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0)  # pop off ')'
        return L
    elif token == ')':
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

def atom(token: str) -> Atom:
    """Numbers become numbers; every other token is a symbol."""
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)

class Env(dict):
    """An environment: a dict of {'var': val} pairs, with an outer Env."""
    def __init__(self, params=(), args=(), outer=None):
        self.update(zip(params, args))
        self.outer = outer

    def find(self, var: str) -> 'Env':
        """Find the innermost Env where var appears."""
        if var in self:
            return self
        elif self.outer is not None:
            return self.outer.find(var)
        else:
            raise NameError(f"Undefined symbol: {var}")

class Procedure:
    """A user-defined Scheme procedure."""
    def __init__(self, params, body, env):
        self.params = params
        self.body = body
        self.env = env

    def __call__(self, *args):
        env = Env(self.params, args, self.env)
        return eval(self.body, env)

def standard_env() -> Env:
    """An environment with some Scheme standard procedures."""
    env = Env()
    env.update(vars(math))
    env.update({
        '+': op.add,
        '-': op.sub,
        '*': op.mul,
        '/': op.truediv,
        '>': op.gt,
        '<': op.lt,
        '>=': op.ge,
        '<=': op.le,
        '=': op.eq,
        'abs': abs,
        'append': op.add,
        'apply': lambda proc, args: proc(*args),
        'begin': lambda *x: x[-1],
        'car': lambda x: x[0],
        'cdr': lambda x: x[1:],
        'cons': lambda x, y: [x] + y,
        'eq?': op.is_,
        'equal?': op.eq,
        'length': len,
        'list': lambda *x: list(x),
        'list?': lambda x: isinstance(x, list),
        'map': lambda proc, lst: list(map(proc, lst)),
        'max': max,
        'min': min,
        'not': op.not_,
        'null?': lambda x: x == [],
        'number?': lambda x: isinstance(x, Number),
        'procedure?': callable,
        'round': round,
        'symbol?': lambda x: isinstance(x, Symbol),
    })
    return env

global_env = standard_env()

def eval(x: Exp, env=global_env) -> Any:
    """Evaluate an expression in an environment."""
    if isinstance(x, Symbol):
        return env.find(x)[x]
    elif not isinstance(x, list):
        return x
    elif x[0] == 'quote':
        return x[1]
    elif x[0] == 'if':
        (_, test, conseq, alt) = x
        exp = conseq if eval(test, env) else alt
        return eval(exp, env)
    elif x[0] == 'define':
        if isinstance(x[1], list):
            (_, (name, *params), body) = x
            env[name] = Procedure(params, body, env)
        else:
            (_, var, exp) = x
            env[var] = eval(exp, env)
    elif x[0] == 'set!':
        (_, var, exp) = x
        env.find(var)[var] = eval(exp, env)
    elif x[0] == 'lambda':
        (_, params, body) = x
        return Procedure(params, body, env)
    else:
        proc = eval(x[0], env)
        args = [eval(arg, env) for arg in x[1:]]
        return proc(*args)

def repl(prompt='lis.py> '):
    """A prompt-read-eval-print loop."""
    while True:
        try:
            val = eval(parse(input(prompt)))
            if val is not None:
                print(lispstr(val))
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

def lispstr(exp) -> str:
    """Convert a Python object back into a Lisp-readable string."""
    if isinstance(exp, list):
        return '(' + ' '.join(map(lispstr, exp)) + ')'
    else:
        return str(exp)

def run_tests():
    """Run basic tests to verify the interpreter works."""
    tests = [
        ("(+ 1 2)", 3),
        ("(* 3 4)", 12),
        ("(define r 10)", None),
        ("(* pi (* r r))", 314.1592653589793),
        ("(if (> 10 5) 1 0)", 1),
        ("(if (< 10 5) 1 0)", 0),
        ("(define circle-area (lambda (r) (* pi (* r r))))", None),
        ("(circle-area 3)", 28.274333882308138),
        ("(define fact (lambda (n) (if (<= n 1) 1 (* n (fact (- n 1))))))", None),
        ("(fact 5)", 120),
        ("(fact 10)", 3628800),
        ("(list 1 2 3)", [1, 2, 3]),
        ("(car (list 1 2 3))", 1),
        ("(cdr (list 1 2 3))", [2, 3]),
        ("(cons 0 (list 1 2))", [0, 1, 2]),
    ]
    
    print("Running Lispy tests...")
    passed = 0
    failed = 0
    
    for code, expected in tests:
        try:
            result = eval(parse(code))
            if expected is None or (abs(result - expected) < 1e-10 if isinstance(expected, float) else result == expected):
                print(f"✓ {code} => {result}")
                passed += 1
            else:
                print(f"✗ {code} => {result} (expected {expected})")
                failed += 1
        except Exception as e:
            print(f"✗ {code} => ERROR: {e}")
            failed += 1
    
    print(f"\nTests complete: {passed} passed, {failed} failed")
    return failed == 0

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        success = run_tests()
        sys.exit(0 if success else 1)
    else:
        print("Lispy: A Simple Lisp Interpreter")
        print("Type 'test' as argument to run tests, or start REPL")
        repl()
