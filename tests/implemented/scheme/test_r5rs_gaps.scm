;; Integration tests for R5RS features not yet implemented.

(test-eq 5 (force (delay (+ 2 3))))

(test-eq 30
  (call-with-values (lambda () (values 10 20)) +))

(test-eq 4 (abs -4))

(test-eq #t (char-ci=? #\a #\A))

(test-eq #t (string-ci=? "foo" "FOO"))

(test-eq #(9 9)
  (begin
    (define v (vector 1 2))
    (vector-fill! v 9)
    v))
