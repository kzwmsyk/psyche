(test-eq (list 2 4 6) (map (lambda (x) (* x 2)) (list 1 2 3)))

(test-eq (list 2 3) (filter (lambda (x) (> x 1)) (list 1 2 3)))
