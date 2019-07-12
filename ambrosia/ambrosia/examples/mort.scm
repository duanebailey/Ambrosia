;; Our friend Mort, the headless TinkerToy guy.
;; (c) 1996, 1999 duane a. bailey
;;
; By placing the mouse to the right of the command below, and hitting enter
; you can get "default-camera" to tell you the types of messages it will accept.
;(default-camera (methods))

; A cylinder that is 1" tall and 1" in diameter
(object unit-cylinder part
    (addchild cylinder)
    ; note the scale command is not part of the addchild - it scales everything added
    (scale 0.005 0.005 0.005)
)


(object unit-cube part
    (addchild cube)
    (scale 0.005 0.005 0.005)
)

; yellow stick is 2.25" long, and 1/4" diameter
(object yellow-stick part
    (addchild unit-cylinder)
    (scale 0.25 2.25 0.25)
    (setmaterial yellow-mat)
)

; blue stick is longer, but just as wide
(object blue-stick part
    (addchild unit-cylinder)
    (scale 0.25 3.333 0.25)
    (setmaterial blue-mat)
)

; orange (red) caps are 3/8" in diameter, 1/2" long
(object orange-cap part
    (addchild unit-cylinder)
    (scale 0.375 0.5 0.375)  ; stumpy cap
    (setmaterial red-mat)       ; later we'll figure out orange
)

; the double-male connector piece
(object connector part
    (addchild unit-cylinder (scale 0.25 1.25 0.25))
    (addchild unit-cube (scale 0.75 0.0625 0.75))
    (setmaterial white-mat)
)

; astonishing engineering: the octagon connector
(object wheel part
    (addchild unit-cylinder)         ; lying flat in the x-z plane
    (scale 1.375 .625 1.375)   ; golden tinker toy ratios
    (x-rot -90)                 ; rotate it up so that it sits upright
    (setmaterial white-mat)     ; well, white wood, really
)


; Now, put the pieces together

; First, a blue piece with a cap.
;    1. blue stick is added
;    2. add on orange cap 1.6666 inches below origin
(object capped-blue-stick part
    (addchild blue-stick)
    (addchild orange-cap (translate 0 -1.6666 0))
)

; Second, build the bottom & feet
(object bottom part
    (addchild wheel)
    (addchild blue-stick (compose (translate 0 -2 0) (z-rot -45)))
    (addchild capped-blue-stick (compose (translate 0 -2 0) (z-rot 45)))
)

; headless shoulders
(object top part
    (addchild bottom (x-rot 180))
    (addchild connector (translate 0 1 0))
)

; headless torso
(object body part
    (addchild top (compose (y-rot 30) (translate 0 1.5 0)))
    (addchild yellow-stick)
    (addchild bottom (translate 0 -1.5 0))
)


(object scene part
    (addchild body)
    (scale 10 10 10)
)

(shade (setbackcolor white))
(default-camera (setrenderer ray))