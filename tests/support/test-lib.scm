;; Minimal test helpers for Scheme-side integration tests.
;; Loaded by tests/support/harness.py before test files.

(define *test-failures* 0)

(define (test-eq expected actual)
  (if (equal? expected actual)
      #t
      (begin
        (print (list 'fail expected actual))
        (set! *test-failures* (+ *test-failures* 1))
        #f)))

(define (test-assert expr)
  (if expr
      #t
      (begin
        (print (list 'assert-fail expr))
        (set! *test-failures* (+ *test-failures* 1))
        #f)))
