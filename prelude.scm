(define fact 
    (lambda (n) (
        if (eq n 1)
        1 
        (* n (fact (- n 1)))
        )
    )
)


(define a 'global)

(let ()
    (define print-a (lambda () (print a)))
    (print-a)
    (setq a 'local)
    (print-a)
)


(define f (lambda (x) (+ (g x) 1)))
(define g (lambda (y) (* y 2)))


