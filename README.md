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

Keyword:
- loop: 
    repeatif <condition> {
        code...;
    }
- selection statements:
    iffy <condition> {
        code...;
    } ew {
        code...;
    }
- data type declarations:
    <type> <variable_name>;
- BEGIN, END, and, or, not

Order or operation (high->low)
- atom: Identify literal integer type, LITERAL_INT_(oneb|twob|fob|ateb), Identifier
- atom: left and right parentheses
- factor: (PLUS|MINUS) factor
- term: factor ((MUL|DIV|MOD) factor)*
- arith-expr: term ((PLUS|MINUS) term)*
- comp-expr: arith-expr ((LESS|LESSEQ|GREATER|GREATEREQ|EQUAL|NOTEQ) arith-expr)*
- expr: not comp-expr, comp-expr ((KEYWORD: AND|KEYWORD: OR) comp-expr)*
- expr: declaration and assignment
