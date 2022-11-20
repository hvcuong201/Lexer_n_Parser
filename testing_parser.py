# DEFINE TOKEN TYPE
## operators
PLUS        = 'PLUS'        
MINUS       = 'MINUS'
MUL         = 'MUL'
DIV         = 'DIV'
MOD         = 'MOD'
LESS        = 'LESS'
LESSEQ      = 'LESSEQ'
GREATER     = 'GREATER'
GREATEREQ   = 'GREATEREQ'
EQUAL       = 'EQUAL'       # ==
NOTEQ       = 'NOTEQ'       # |=
ASSIGN      = 'ASSIGN'      # =
LPAREN      = 'LPAREN'      # (
RPAREN      = 'RPAREN'      # )
##Integer Literals
LITERAL_INT_oneb    = 'LITERAL_INT_oneb'
LITERAL_INT_twob    = 'LITERAL_INT_twob'
LITERAL_INT_fob     ='LITERAL_INT_fob' 
LITERAL_INT_ateb    ='LITERAL_INT_ateb'
## Data type
DATATYPE    = 'DATATYPE'
## Punctuation
SEMICOLON   = 'SEMICOLON'   # ;
LCBRACKET   = 'LCBRACKET'   # {
RCBRACKET   = 'RCBRACKET'   # }
## Identifier
IDENTIFIER  = 'IDENTIFIER'
## keywords
KEYWORD     = 'KEYWORD'

KEYWORDS    = ['iffy', 'ew', 'repeatif', 'BEGIN', 'END', 'and', 'or', 'not']
#               if,     else, while loop
DATATYPES    = ['oneb', 'twob', 'fob', 'ateb']
#               1byte,  2bytes, 4bytes  8bytes

from lexer_n_parser import *

text_file = open("test_no_error_1.txt", "r")
#read whole file to a string
data = text_file.read()
#close file
text_file.close()
print(data)
lexer = LexicalAnalyzer(data)
tokens = lexer.tokenize()
print(tokens)
symbol_table = []

class variable:
    def __init__(self, data_type, id, value) -> None:
        self.data_type = data_type
        self.id = id
        self.value = value
        
    def __repr__(self) -> str:
        return f'{self.data_type}, {self.id}, {self.value}'

def match(token, type, value=None):
    return True if token.type == type and token.value == value else False

i = 0
while i < len(tokens):
    token = tokens[i]
    if i == 0 and not match(token, KEYWORD, 'BEGIN'):
        print("Syntactic Error: the program is supposed to start with 'BEGIN'")
        
    if i != 0 and match(token, DATATYPE):
        print("Hi")
        data_type = token.value
        i+=1
        # Declaration
        if match(token, IDENTIFIER) and match(token[i+1], SEMICOLON):
            symbol_table[token.value] = variable(data_type, token.value, None)
            
    i+=1
            
print(symbol_table)
            

        