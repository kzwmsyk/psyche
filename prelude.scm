
(define atom? 
    (lambda (sexpr) 
        (and (not (pair? sexpr)) 
             (not (null? sexpr)))
    )
)

(define (length ls)
    (if (null? ls)
        0
        (+ 1 (length (cdr ls)))
    )
)

(define (list . x) x)

(define (list? ls)
    (if (null? ls)
        #t
        (and (pair? ls) (list? (cdr ls)))
    )
)

(define (append ls tail)
    (if (null? ls)
        tail
        (cons (car ls) (append (cdr ls) tail))
    )
)

(define (reverse ls)
    (if (null? ls)
        ()
        (append (reverse (cdr ls)) (list (car ls)))
    )
)

(define (list-copy obj)
    (if (null? obj)
        nil
        (cons (car obj) (list-copy (cdr obj)))
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
