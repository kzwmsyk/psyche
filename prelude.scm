
(define atom? 
    (lambda (sexpr) 
        (and (not (pair? sexpr)) 
             (not (null? sexpr)))
    )
)