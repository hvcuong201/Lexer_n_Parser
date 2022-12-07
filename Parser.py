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

KEYWORDS    = ['iffy', 'ew', 'repeatif', 'BEGIN', 'END']
#               if,     else, while loop
DATATYPES   = ['oneb', 'twob', 'fob', 'ateb']
#               1byte,  2bytes, 4bytes  8bytes
COMP_OPS    = [LESS, LESSEQ, GREATER, GREATEREQ, EQUAL, NOTEQ]
import random

from Lexer import *

start_token = None

class variable:
    def __init__(self, id, data_type) -> None:
        self.data_type = data_type
        self.id = id
        
    def __repr__(self) -> str:
        return f'(Var_ID: {self.id}, Var_DataType: {self.data_type})'
    

def match(token, type, value=None):
    if value:
        return (token.type == type and token.value == value)
    return token.type == type

class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[self.position]
        
        ### Stack to keep track of the proper usage of iffy/ew: 
        self.iffyew_stack = []
        
        ### Stack to keep track of the parentheses, brackets. 
        self.bra_stack = []
        
        ### For keeping track of variable declaration
        self.symbol_table = {}
        
        ### List of syntactic errors 
        self.syntax_error = []
    
    def advance(self): 
        if self.position < len(self.tokens):
            self.position += 1
        self.current_token = self.tokens[self.position] if self.position < len(self.tokens) else None
        
    def get_current_token(self):
        return self.tokens[self.position]
    
    def get_next_token(self):
        return self.tokens[self.position + 1] if self.position + 1 < len(self.tokens) else None
    
    def check_BEGIN_END(self):
        return (self.tokens[0].type == KEYWORD and self.tokens[0].value == 'BEGIN') and (self.tokens[len(self.tokens)-1].type == KEYWORD and self.tokens[len(self.tokens)-1].value == 'END')
    
    def check_bool_expr(self):
        if not match(self.current_token, LPAREN):
            self.syntax_error.append(f"{self.current_token.value}: expect a '('")
        else:
            bool_expr_st = []
            bool_expr_st.append(RPAREN) # need to look for a right parenthese ')'
            # Look at bool_expr
            self.advance()
            comp_op_found = False
            while (not match(self.current_token, KEYWORD, 'END')):
                if match(self.current_token, RPAREN): # ')'
                    bool_expr_st.pop() 
                    if len(bool_expr_st) == 0:
                        if not comp_op_found:
                            self.syntax_error.append(f"{self.current_token.value}: invalid boolean expression")
                        if len(bool_expr_st) != 0:
                            self.syntax_error.append(f"{self.current_token.value}: missing {len(bool_expr_st)} ')'")
                        self.advance()
                        break 
                
                if match(self.current_token, LPAREN): # '('
                    bool_expr_st.append(RPAREN)
                    
                if self.current_token.type in COMP_OPS:
                    comp_op_found = True
                
                if match(self.current_token, KEYWORD):
                    self.syntax_error.append(f"{self.current_token.value}: illegal start of expression")
                    
                if match(self.current_token, ASSIGN):
                    self.syntax_error.append(f"{self.current_token.value}: illegal start of assignment")
                
                if match(self.current_token, DATATYPE):
                    self.syntax_error.append(f"{self.current_token.value}: illegal start of declaration")
                
                if match(self.get_next_token(), KEYWORD, 'END'):
                    self.syntax_error.append(f"{self.current_token.value}: missing a ')'")
                    break
                    
                self.advance()
    
    def run(self):
        if not self.check_BEGIN_END():
            self.syntax_error.append(f"{self.current_token.value}: the program is supposed to start with 'BEGIN' and end with 'END'")
        self.advance()
        self.execute_stm_list(end='END', scope='global')
        #print(self.bra_stack)
        print(f"\nList of Syntatic Errors: \n{self.syntax_error}")
    
    # Execute the code block until met an ending token (param: end)
    def execute_stm_list(self, end, scope=None):
        while self.current_token.value != end:
            #print(self.current_token)
            
            if match(self.current_token, end):
                if end == RCBRACKET:
                    if (len(self.bra_stack) == 0):
                        self.syntax_error.append("Missin an opening curly brace '{'")
                    else:
                        self.bra_stack.pop()
                break
            
            # Declaration
            if match(self.current_token, DATATYPE): 
                # Syntactic Errors
                if not match(self.get_next_token(), IDENTIFIER):
                    self.syntax_error.append(f"{self.current_token.value}: not a Statement")
                    if match(self.get_next_token(), KEYWORD):
                        self.syntax_error.append(f"{self.current_token.value}: missing a Semicolon ';'")
                # Declaration
                else:
                    var_datatype = self.current_token
                    self.advance() #to identifier
                    
                    if not match(self.get_next_token(), SEMICOLON):
                        self.syntax_error.append(f"{self.current_token.value}: missing a Semicolon ';'")
                    else: 
                        # Register the declared variable into the symbol table
                        self.symbol_table[self.current_token] = variable(self.current_token.value, var_datatype.value)
                        #print(self.symbol_table)
                        self.advance()
            
            # Initialization or Assign
            if match(self.current_token, IDENTIFIER) and match(self.get_next_token(), ASSIGN):
                # Synctactics Errors:
                if self.symbol_table.get(self.current_token) == None:
                    self.syntax_error.append(f"{self.current_token.value}: undeclared variable name")
                else:
                    self.advance() #to assign
                    self.advance() #to factor
                    pa_stack = []
                    token_start_of_assign = self.current_token
                    while (not match(self.current_token, SEMICOLON)):
                        if match(self.current_token, KEYWORD):
                            self.syntax_error.append(f"{self.current_token.value}: illegal start of expression")
                        
                        if match(self.current_token, 'END'):
                            self.syntax_error.append(f"{self.current_token.value}: missing a Semicolon ';'")
                            
                        if match(self.current_token, LPAREN):
                            pa_stack.append(')')
                        
                        if match(self.current_token, RPAREN):
                            if len(pa_stack) == 0:
                                self.syntax_error.append(f"{token_start_of_assign.value}: missing an open parenthese '('")
                            else:
                                pa_stack.pop()
                        self.advance()
                    if len(pa_stack) > 0:
                        self.syntax_error.append(f"{token_start_of_assign.value}: missing {len(pa_stack)} close parenthese ')'")
                        
            # Checking grammar rule for repeatif loop
            if match(self.current_token, KEYWORD, 'repeatif'):
                #print("loooooooooooooooooooooooooooooooooooooooooooooooooooop")
                self.advance()
                self.check_bool_expr()
                if (not match(self.current_token, LCBRACKET)):
                    self.syntax_error.append("repeatif: expected an opening curly brace")
                
            # Checking grammar rule for iffy/ew selection statement   
            if match(self.current_token, KEYWORD, 'iffy'):
                #print("ifffffffffffffffffffffffffffffffffffffffffffffffffffffffy") 
                self.iffyew_stack.append(self.current_token)
                self.advance()
                self.check_bool_expr()
                if (not match(self.current_token, LCBRACKET)):
                    self.syntax_error.append("iffy: expected an opening curly brace")
                
            if match(self.get_next_token(), KEYWORD, 'ew'):
                if not match(self.current_token, RCBRACKET):
                    self.syntax_error.append(f"{self.current_token.value}: invalid use of 'ew'")
            
            # Checking { code block }
            if match(self.current_token, LCBRACKET):
                self.bra_stack.append(RCBRACKET) # need to look '}'
                self.advance()
                starttt = random.randint(0,100)
                print(f"start of recursion {starttt}")
                start_token = 'iffy'
                self.execute_stm_list(end=RCBRACKET, scope=starttt) # recursion to the code block
                #print("OUUUUUUUUUUUUUUUUUUUUUUUUUUT")
                if (self.current_token == None):
                    self.syntax_error.append("missing a '}'")
                #print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                
            self.advance()
            if (self.current_token == None):
                break
        
        print(f"end of recursion {scope}")
            
if __name__ == "__main__":
    pass
    # print("\n--------Test file 1 with 0 errors--------: \n")
    # text_file = open("test_no_error_1.txt", "r")
    # #read whole file to a string
    # data = text_file.read()
    # #close file
    # text_file.close()
    # print(data)
    # lexer = Lexer(data)
    # tokens = lexer.tokenize()
    # print(f"\nList of tokens: \n{tokens}")
    # parser = Parser(tokens)
    # parser.run()
    
    # print("\n--------Test file 2 with 0 errors--------: \n")
    # text_file = open("test_no_error_2.txt", "r")
    # #read whole file to a string
    # data = text_file.read()
    # #close file
    # text_file.close()
    # print(data)
    # lexer = Lexer(data)
    # tokens = lexer.tokenize()
    # print(f"\nList of tokens: \n{tokens}")
    # parser = Parser(tokens)
    # parser.run()
    
    # print(f"\n--------Test file with 5 syntax errors--------: \n")
    # text_file = open("test_syn_error.txt", "r")
    # #read whole file to a string
    # data = text_file.read()
    # #close file
    # text_file.close()
    # print(data)
    # lexer = Lexer(data)
    # tokens = lexer.tokenize()
    # print(f"\nList of tokens: \n{tokens}")
    # parser = Parser(tokens)
    # parser.run()

    # print("\n--------Test file with 5 lexical errors--------: \n")
    # text_file = open("test_lex_error.txt", "r")
    # #read whole file to a string
    # data = text_file.read()
    # #close file
    # text_file.close()
    # print(data)
    # lexer = Lexer(data)
    # tokens = lexer.tokenize()
    # print(f"\nList of tokens: \n{tokens}")
    # parser = Parser(tokens)
    # parser.run()
    



        