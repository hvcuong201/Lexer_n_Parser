# Test 2 Document:
[Link to the Google document](https://docs.google.com/document/d/1781U41ydMz_0HRzeQnuIUyZ-tOFjqX5Bccd6j6syKh4/edit?usp=sharing)

# Development Reference:

Operations
addition: +
subtraction: -
multiplication: *
division: /
modulo: %
less than: <
greater than: >
less or equal: <=
greater or equal: >=
equal to: ==
not equal to: |=  
assignment: =
parenthese: ()

Primitive data types:
oneb:   stores 1 byte integer
twob:   stores 2 bytes integer
fob:    stores 4 bytes integer
ateb:   stores 8 bytes integer

Character in number literal to express what they are in bytes:
(number_literal).o :    number will be stored in One byte 
(number_literal).t :    number will be stored in Two bytes
(number_literal).f :    number will be stored in Fo (4) bytes
(number_literal).a :    number will be stored in Ate (8) bytes

Keyword:
- loop: 
    repeatif (bool_expr) {
        code...;
    }
- selection statements:
    iffy (bool_expr) {
        code...;
    } ew {
        code...;
    }
- data type declarations:
    (data type) (variable name);
- BEGIN, END

Order or operation (high->low)
- atom: Identify literal integer type, LITERAL_INT_(oneb|twob|fob|ateb), Identifier
- atom: left and right parentheses
- factor: (PLUS|MINUS) factor
- term: factor ((MUL|DIV|MOD) factor)*
- arith-expr: term ((PLUS|MINUS) term)*
- comp-expr: arith-expr ((LESS|LESSEQ|GREATER|GREATEREQ|EQUAL|NOTEQ) arith-expr)*
- expr: not comp-expr, comp-expr ((KEYWORD: AND|KEYWORD: OR) comp-expr)*
- expr: declaration and assignment
