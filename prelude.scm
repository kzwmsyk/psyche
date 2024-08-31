
(define atom? 
    (lambda (sexpr) 
        (and (not (pair? sexpr)) 
             (not (null? sexpr)))
    )
)

(define (length lst)
    (if (null? lst)
        0
        (+ 1 (length (cdr lst)))
    )
)

(define (list . x) x)

(define (list? lst)
    (if (null? lst)
        #t
        (and (pair? lst) (list? (cdr lst)))
    )
)

(define (append lst tail)
    (if (null? lst)
        tail
        (cons (car lst) (append (cdr lst) tail))
    )
)

(define (reverse lst)
    (if (null? lst)
        ()
        (append (reverse (cdr lst)) (list (car lst)))
    )
)

(define (caar cell) (car (car cell)))
(define (cadr cell) (car (cdr cell)))
(define (cdar cell) (cdr (car cell)))
(define (cddr cell) (cdr (cdr cell)))

(define (caaar cell) (car (car (car cell))))
(define (caadr cell) (car (car (cdr cell))))
(define (cadar cell) (car (cdr (car cell))))
(define (caddr cell) (car (cdr (cdr cell))))
(define (cdaar cell) (cdr (car (car cell))))
(define (cdadr cell) (cdr (car (cdr cell))))
(define (cddar cell) (cdr (cdr (car cell))))
(define (cdddr cell) (cdr (cdr (cdr cell))))

(define (caaaar cell) (car (car (car (car cell)))))
(define (caaadr cell) (car (car (car (cdr cell)))))
(define (caadar cell) (car (car (cdr (car cell)))))
(define (caaddr cell) (car (car (cdr (cdr cell)))))
(define (cadaar cell) (car (cdr (car (car cell)))))
(define (cadadr cell) (car (cdr (car (cdr cell)))))
(define (caddar cell) (car (cdr (cdr (car cell)))))
(define (cadddr cell) (car (cdr (cdr (cdr cell)))))
(define (cdaaar cell) (cdr (car (car (car cell)))))
(define (cdaadr cell) (cdr (car (car (cdr cell)))))
(define (cdadar cell) (cdr (car (cdr (car cell)))))
(define (cdaddr cell) (cdr (car (cdr (cdr cell)))))
(define (cddaar cell) (cdr (cdr (car (car cell)))))
(define (cddadr cell) (cdr (cdr (car (cdr cell)))))
(define (cdddar cell) (cdr (cdr (cdr (car cell)))))
(define (cddddr cell) (cdr (cdr (cdr (cdr cell)))))
