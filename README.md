# Test 2 Document:
[TEST 2 RESUBMISSION DOC](https://docs.google.com/document/d/1781U41ydMz_0HRzeQnuIUyZ-tOFjqX5Bccd6j6syKh4/edit?usp=sharing)

LR(1) Parse Table for my language can be found at CuongHoang_LR(1)_Parser_Table.pdf

[Link to the Google document](https://docs.google.com/document/d/1s6JLctfnJl_DpSqcduSnPm9vLjd5eSziy10ILEjnQ80/edit?usp=sharing)

# Development Reference:
### Operations
| Name| Symbol |
|--|--|
| addition | + |
| subtraction | - |
| multiplication| * |
| division| / |
| modulo| % |
| less than | < |
| greater than | > |
| less or equal | <= |
| greater or equal | >= |
| not equal to | \|= |
| assignment | = |
| parenthese | ( ) |
| curly bracket | { } |

### Primitive data types: 
| Name | Description |
|--|--|
| oneb | stores 1 byte integer |
| twob | stores 2 bytes integer |
| fob | stores 4 bytes integer |
| ateb | stores 8 bytes integer |

### Character in number literal to express what they are in bytes:

| Format | Description |
|--|--|
|(number_literal).o | number will be stored in One byte |
|(number_literal).t | number will be stored in Two bytes |
|(number_literal).f | number will be stored in Fo (4) bytes |
|(number_literal).a | number will be stored in Ate (8) bytes |

### Keyword:
- Clear beginning and end:
```
BEGIN:
	<statement_list>
END
```
- Seperate multiple statements using a semicolon 
```
<statement>;
```
- Loop:
```
repeatif (<bool_expr>) {
	<codeblock>
}
```
- Selection Statement:
```
iffy (<bool_expr>) {
	<codeblock>
} ew {
	<codeblock>
}
```
- Variable Declarations:
```
<data type> <identifier>;
```
- Variable Assignment:
```
<identifier> = <value>;
```
  
## Grammar

```
<program> 		::= BEGIN <stmt_list>
<stmt_list> 	::= <stmt> <stmt_list> | END
<stmt>  		::= <declaration> | <assignment> | <cond> | <repeatif>

<declaration>  	::= <type> identifier `;`
<type> 			::= oneb | twob | fob | ateb

<assignment> 	::= identifier `=` <expr> `;`

<cond> 			::= iffy <bool_expr> `{` <codeblock> ew `{` <codeblock>
                | iffy <bool_expr> `{` <codeblock>
<repeatif> 		::= repeatif <bool_expr> ‘{‘ <codeblock>
<codeblock>  	::= <stmt> <codeblock> | `}`
<bool_expr>  	::= `(` <value> <comparison_op> <value> `)`

<comparison_op> ::= `<` | `<=’ | `>’ | `>=’ | `==’ | `|=`

### Enforce rule of non BODMAS
<expr>  		::= <sum>
<sum>  			::= <mod> `+` <sum> | <mod>
<mod>  			::= <div> `%` <mod> |  <div>
<div>  			::= <mul> `/` <div> | <mul>
<mul>  			::= <sub> `*` <mul> | <sub>
<sub>  			::= <factor> `-` <sub> | <factor>
<factor> 		::= `(` <expr> `)` | <value>
<value>  		::= LITERAL_INT_oneb
				| LITERAL_INT_twob
				| LITERAL_INT_fob
				| LITERAL_INT_ateb
				| identifier
```
@author: hvcuong201

