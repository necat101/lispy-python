;; Advanced Lisp Examples for Lispy v2
;; These examples demonstrate the improved interpreter features

;; ============================================
;; 1. VARIADIC ARITHMETIC
;; ============================================

(+ 1 2 3 4 5 6 7 8 9 10)  ; => 55
(* 1 2 3 4 5)             ; => 120
(- 100 10 20 30)          ; => 40
(/ 1000 2 5 10)           ; => 10.0

;; ============================================
;; 2. QUOTE SYNTAX SUGAR
;; ============================================

'(hello world)            ; => (hello world)
'(1 2 3 4 5)             ; => (1 2 3 4 5)
'()                      ; => ()

;; Nested quotes
'(a (b c) d)             ; => (a (b c) d)

;; ============================================
;; 3. MULTI-BODY FUNCTIONS
;; ============================================

;; Functions can now have multiple expressions in body
(define (factorial n)
  (define (fact-iter product counter)
    (if (> counter n)
        product
        (fact-iter (* counter product) (+ counter 1))))
  (fact-iter 1 1))

(factorial 5)   ; => 120
(factorial 10)  ; => 3628800

;; ============================================
;; 4. HIGHER-ORDER FUNCTIONS
;; ============================================

;; Map
(define (map f lst)
  (if (null? lst)
      '()
      (cons (f (car lst)) (map f (cdr lst)))))

(map (lambda (x) (* x x)) '(1 2 3 4 5))
; => (1 4 9 16 25)

;; Filter
(define (filter pred lst)
  (if (null? lst)
      '()
      (if (pred (car lst))
          (cons (car lst) (filter pred (cdr lst)))
          (filter pred (cdr lst)))))

(filter (lambda (x) (> x 3)) '(1 2 3 4 5 6))
; => (4 5 6)

;; Fold/reduce
(define (foldr f init lst)
  (if (null? lst)
      init
      (f (car lst) (foldr f init (cdr lst)))))

(foldr + 0 '(1 2 3 4 5))        ; => 15
(foldr * 1 '(1 2 3 4 5))        ; => 120
(foldr cons '() '(1 2 3))       ; => (1 2 3)

;; ============================================
;; 5. CLOSURES AND LEXICAL SCOPING
;; ============================================

;; Counter factory
(define (make-counter)
  (define count 0)
  (lambda ()
    (set! count (+ count 1))
    count))

(define c1 (make-counter))
(define c2 (make-counter))

(c1)  ; => 1
(c1)  ; => 2
(c2)  ; => 1
(c1)  ; => 3

;; Adder factory
(define (make-adder n)
  (lambda (x) (+ x n)))

(define add10 (make-adder 10))
(define add100 (make-adder 100))

(add10 5)    ; => 15
(add100 5)   ; => 105

;; ============================================
;; 6. RECURSIVE DATA STRUCTURES
;; ============================================

;; List utilities
(define (length lst)
  (if (null? lst)
      0
      (+ 1 (length (cdr lst)))))

(length '(a b c d e))  ; => 5

(define (append lst1 lst2)
  (if (null? lst1)
      lst2
      (cons (car lst1) (append (cdr lst1) lst2))))

(append '(1 2 3) '(4 5 6))  ; => (1 2 3 4 5 6)

(define (reverse lst)
  (define (rev-iter lst acc)
    (if (null? lst)
        acc
        (rev-iter (cdr lst) (cons (car lst) acc))))
  (rev-iter lst '()))

(reverse '(1 2 3 4 5))  ; => (5 4 3 2 1)

;; ============================================
;; 7. PRACTICAL ALGORITHMS
;; ============================================

;; Fibonacci (inefficient but clear)
(define (fib n)
  (if (< n 2)
      n
      (+ (fib (- n 1)) (fib (- n 2)))))

(fib 10)  ; => 55

;; Fibonacci (efficient iterative)
(define (fib-fast n)
  (define (fib-iter a b count)
    (if (= count 0)
        b
        (fib-iter (+ a b) a (- count 1))))
  (fib-iter 1 0 n))

(fib-fast 10)  ; => 55
(fib-fast 30)  ; => 832040

;; ============================================
;; 8. FUNCTIONAL PROGRAMMING PATTERNS
;; ============================================

;; Currying
(define (curry f)
  (lambda (x)
    (lambda (y)
      (f x y))))

(define add (curry +))
(define add5 ((curry +) 5))
(add5 10)  ; => 15

;; Composition
(define (compose f g)
  (lambda (x)
    (f (g x))))

(define (square x) (* x x))
(define (inc x) (+ x 1))
(define square-after-inc (compose square inc))

(square-after-inc 4)  ; => 25  (since (4+1)² = 25)

;; ============================================
;; 9. USING MATH LIBRARY
;; ============================================

(define pi 3.141592653589793)

(define (circle-area r)
  (* pi (* r r)))

(define (circle-circumference r)
  (* 2 pi r))

(circle-area 10)           ; => 314.159...
(circle-circumference 10)  ; => 62.831...

;; Trigonometry
(sin (/ pi 2))  ; => 1.0
(cos 0)         ; => 1.0
(sqrt 2)        ; => 1.414...
