#!/usr/bin/env python3
"""
Lispy: A Compact Lisp Interpreter in Python
Based on Peter Norvig's lispy.html with improvements
"""

import math
import operator as op
import functools as ft
import sys

Symbol = str

class Env(dict):
    def __init__(self, params=(), args=(), outer=None):
        super().__init__(zip(params, args))
        self.outer = outer
    
    def find(self, var):
        if var in self:
            return self
        if self.outer:
            return self.outer.find(var)
        raise NameError(f"undefined symbol: {var}")

class Proc:
    def __init__(self, params, body, env):
        self.params, self.body, self.env = params, body, env
    
    def __call__(self, *args):
        return evl(['begin', *self.body], Env(self.params, args, self.env))

def tokenize(s):
    return s.replace('(', ' ( ').replace(')', ' ) ').replace("'", " ' ").split()

def atom(t):
    try:
        return int(t)
    except ValueError:
        try:
            return float(t)
        except ValueError:
            return t

def read(ts):
    if not ts:
        raise SyntaxError("unexpected EOF")
    t = ts.pop(0)
    if t == '(':
        xs = []
        while True:
            if not ts:
                raise SyntaxError("missing ')'")
            if ts[0] == ')':
                ts.pop(0)
                return xs
            xs.append(read(ts))
    if t == ')':
        raise SyntaxError("unexpected ')'")
    if t == "'":
        return ['quote', read(ts)]
    return atom(t)

def parse(s):
    ts = tokenize(s)
    x = read(ts)
    if ts:
        raise SyntaxError("trailing tokens")
    return x

def prod(xs):
    return ft.reduce(op.mul, xs, 1)

def div(x, *xs):
    return ft.reduce(op.truediv, xs, x) if xs else 1 / x

def standard_env():
    e = Env()
    e.update(vars(math))
    e.update({
        '+': lambda *xs: sum(xs),
        '-': lambda x, *xs: x - sum(xs) if xs else -x,
        '*': lambda *xs: prod(xs),
        '/': div,
        '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq,
        'abs': abs, 'append': op.add, 'apply': lambda f, xs: f(*xs),
        'car': lambda x: x[0], 'cdr': lambda x: x[1:],
        'cons': lambda x, y: [x] + y,
        'eq?': op.is_, 'equal?': op.eq, 'length': len,
        'list': lambda *xs: list(xs), 'list?': lambda x: isinstance(x, list),
        'map': lambda f, xs: list(map(f, xs)),
        'max': max, 'min': min, 'not': op.not_,
        'null?': lambda x: x == [],
        'number?': lambda x: isinstance(x, (int, float)),
        'procedure?': callable,
        'round': round,
        'symbol?': lambda x: isinstance(x, str),
    })
    return e

GLOBAL = standard_env()

def evl(x, env=GLOBAL):
    while True:
        if isinstance(x, Symbol):
            return env.find(x)[x]
        if not isinstance(x, list):
            return x
        if not x:
            return []
        
        head = x[0]
        
        if head == 'quote':
            return x[1]
        if head == 'if':
            _, test, conseq, alt = x
            x = conseq if evl(test, env) else alt
        elif head == 'define':
            if isinstance(x[1], list):
                _, (name, *params), *body = x
                env[name] = Proc(params, body, env)
            else:
                _, name, exp = x
                env[name] = evl(exp, env)
            return None
        elif head == 'set!':
            _, name, exp = x
            env.find(name)[name] = evl(exp, env)
            return None
        elif head == 'lambda':
            _, params, *body = x
            return Proc(params, body, env)
        elif head == 'begin':
            for exp in x[1:-1]:
                evl(exp, env)
            x = x[-1]
        else:
            proc = evl(head, env)
            args = [evl(arg, env) for arg in x[1:]]
            return proc(*args)

def lispstr(x):
    return '(' + ' '.join(map(lispstr, x)) + ')' if isinstance(x, list) else str(x)

def run_tests():
    """Run comprehensive tests."""
    tests = [
        ("(+ 1 2 3 4)", 10),
        ("(* 2 3 4)", 24),
        ("(- 10 1 2 3)", 4),
        ("(/ 100 2 5)", 10),
        ("(- 5)", -5),
        ("(/ 2)", 0.5),
        ("'hello", "hello"),
        ("'(1 2 3)", [1, 2, 3]),
        ("(define (square x) (* x x))", None),
        ("(square 5)", 25),
        ("((lambda (x) (define y 10) (+ x y)) 5)", 15),
        ("(begin (define a 1) (define b 2) (+ a b))", 3),
        ("(define (fact n) (if (<= n 1) 1 (* n (fact (- n 1)))))", None),
        ("(fact 5)", 120),
        ("(fact 10)", 3628800),
        ("(map (lambda (x) (* x x)) '(1 2 3 4 5))", [1, 4, 9, 16, 25]),
        ("(define (make-adder n) (lambda (x) (+ x n)))", None),
        ("(define add5 (make-adder 5))", None),
        ("(add5 10)", 15),
        ("(car '(1 2 3))", 1),
        ("(cdr '(1 2 3))", [2, 3]),
        ("(cons 0 '(1 2))", [0, 1, 2]),
        ("(length '(a b c d))", 4),
        ("(define (sum lst) (if (null? lst) 0 (+ (car lst) (sum (cdr lst)))))", None),
        ("(sum '(1 2 3 4 5))", 15),
        ("(define (filter pred lst) (if (null? lst) '() (if (pred (car lst)) (cons (car lst) (filter pred (cdr lst))) (filter pred (cdr lst)))))", None),
        ("(filter (lambda (x) (> x 2)) '(1 2 3 4 5))", [3, 4, 5]),
    ]
    
    print("Running Lispy tests...\n")
    passed = 0
    failed = 0
    
    for code, expected in tests:
        try:
            result = evl(parse(code))
            if expected is None or result == expected:
                print(f"✓ {code}")
                if expected is not None:
                    print(f"  => {result}")
                passed += 1
            else:
                print(f"✗ {code}")
                print(f"  => {result} (expected {expected})")
                failed += 1
        except Exception as e:
            print(f"✗ {code}")
            print(f"  ERROR: {e}")
            failed += 1
    
    print(f"\n{passed} passed, {failed} failed")
    return failed == 0

def repl():
    print("Lispy v2 - Compact Lisp Interpreter")
    print("Type expressions or 'test' to run tests, Ctrl-C to exit\n")
    while True:
        try:
            line = input('lispy> ')
            if line.strip() == 'test':
                run_tests()
                print()
                continue
            v = evl(parse(line))
            if v is not None:
                print(lispstr(v))
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        success = run_tests()
        sys.exit(0 if success else 1)
    else:
        repl()
