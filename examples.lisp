;; Example Lisp programs for Lispy

;; Factorial
(define fact (lambda (n)
  (if (<= n 1)
      1
      (* n (fact (- n 1))))))

(fact 5)
; => 120

;; Fibonacci
(define fib (lambda (n)
  (if (< n 2)
      n
      (+ (fib (- n 1)) (fib (- n 2))))))

(fib 10)
; => 55

;; Higher-order functions
(define map (lambda (f lst)
  (if (null? lst)
      (quote ())
      (cons (f (car lst)) (map f (cdr lst))))))

(map (lambda (x) (* x x)) (list 1 2 3 4 5))
; => (1 4 9 16 25)

;; Closures - counter factory
(define make-counter (lambda ()
  (begin
    (define count 0)
    (lambda ()
      (begin
        (set! count (+ count 1))
        count)))))

(define c1 (make-counter))
(define c2 (make-counter))

(c1) ; => 1
(c1) ; => 2
(c2) ; => 1
(c1) ; => 3

;; List operations
(define range (lambda (a b)
  (if (> a b)
      (quote ())
      (cons a (range (+ a 1) b)))))

(range 1 10)
; => (1 2 3 4 5 6 7 8 9 10)

;; Using standard library
(define circle-area (lambda (r) (* pi (* r r))))
(circle-area 10)
; => 314.159...

(define circle-circumference (lambda (r) (* 2 pi r)))
(circle-circumference 10)
; => 62.831...
