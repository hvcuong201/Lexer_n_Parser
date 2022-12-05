import re
###################################################
                ##### TOKENS #####
###################################################

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
DATATYPES    = ['oneb', 'twob', 'fob', 'ateb']
#               1byte,  2bytes, 4bytes  8bytes
identifier_pattern = "^[A-Za-z_]{6,8}$"


class Token:
    def __init__(self, _type, value=None) -> None:
        self.type = _type
        self.value = value
    
    # representation method to return a string with the token's value and type
    def __repr__(self) -> str:
        if self.value:
            return f"{self.type}:{self.value}"
        return f"{self.type}"
    
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Token):
            return (self.type == other.type and self.value == other.value) if (other.value and self.value) else (self.type == other.type)
        return False
    
    def __hash__(self):
        return hash((self.type, self.value))


    
###################################################
                ##### POSITION #####
###################################################
# Keep track of the line number, column number, index for easier traceability
class Position:
    def __init__(self, idx, line, col) -> None:
        self.idx = idx
        self.line = line
        self.col = col
        
    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1 
    
        if current_char == '\n': 
            # new line -> increase the line counter and reset the column counter
            self.line += 1  
            self.col = 0
        return self
    
    def pos_snapshot(self):
        return Position(self.idx, self.line, self.col)
    
    def __str__(self) -> str:
        return f"line: {self.line + 1}"
    

###################################################
                ##### LEXER #####
###################################################

class LexicalAnalyzer:
    def __init__(self, data) -> None:
        self.data = data
        self.pos = Position(0, 0, 0) # current position
        self.current_char = self.data[self.pos.idx]
        
    def advance(self):
        # advance the 'pos' pointer 
        self.pos.advance(self.current_char)
        # set the current character
        if self.pos.idx < len(self.data):
            self.current_char = self.data[self.pos.idx]
        else:
            self.current_char = None #End of Input
            
    def create_multi_digit_integer(self):
        # create an integer  that formed by multiple digits
        number = ''
        while self.current_char != None and self.current_char.isdigit():
            number += self.current_char
            self.advance()
        return int(number)
    
    def create_identifier_token(self):
        string = ''
        while self.current_char != None and (self.current_char.isalpha() or self.current_char == '_' or self.current_char.isdigit()):
            string += self.current_char
            self.advance()
        if string in KEYWORDS:
            return Token(KEYWORD, string)
        if string in DATATYPES:
            return Token(DATATYPE, string)
        if not bool(re.match(identifier_pattern, string)):
            start_pos = self.pos.pos_snapshot()
            print(f"LEX_ERROR: Identifier can only contains letters and underscores, at {start_pos}.")
            #exit()
        if len(string) < 6 and len(string) > 8:
            start_pos = self.pos.pos_snapshot()
            print(f"LEX_ERROR: Identifier can only be within 6-8 letters, at {start_pos}.")
            #exit()
        return Token(IDENTIFIER, string)
    
        
    def tokenize(self):
        tokens = []
        
        while self.current_char != None:
            # skip if the current character is a blank space characters
            if self.current_char in ' \t\n':
                self.advance()
            ### operators
            elif self.current_char == '+':
                tokens.append(Token(PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(RPAREN))
                self.advance()
            ### comparision operators <, >, <=, >=, |=, ==    
            elif self.current_char == '|': # only if follows by a =, then it's valid
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(NOTEQ))
                    self.advance()
                else:
                    start_pos = self.pos.pos_snapshot()
                    print(f"LEX_ERROR: at {start_pos}, it has to be '|=' bruh.")
                    self.advance()
                    exit()
            elif self.current_char == '=': # might be == or =
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(EQUAL))
                    self.advance()
                else:
                    tokens.append(Token(ASSIGN))
            elif self.current_char == '<': # might be < or <=
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(LESSEQ))
                    self.advance()
                else:
                    tokens.append(Token(LESS))
            elif self.current_char == '>': # might be > or >=
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(GREATEREQ))
                    self.advance()
                else:
                    tokens.append(Token(GREATER))
            ### integer
            elif self.current_char.isdigit():
                number = self.create_multi_digit_integer()
                if number <= 255:
                    tokens.append(Token(LITERAL_INT_oneb, number))
                elif number <= 65535:
                    tokens.append(Token(LITERAL_INT_twob, number))
                elif number <= 4294967295:
                    tokens.append(Token(LITERAL_INT_fob, number))
                else:
                    tokens.append(Token(LITERAL_INT_ateb, number))
            ### identifier and keyword
            elif self.current_char.isalpha() or self.current_char == '_':
                tokens.append(self.create_identifier_token())
            ### punctuation
            elif self.current_char == ';':
                tokens.append(Token(SEMICOLON))
                self.advance()
            elif self.current_char == '{':
                tokens.append(Token(LCBRACKET))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token(RCBRACKET))
                self.advance()
            # the character is unregconized
            else:
                start_pos = self.pos.pos_snapshot()
                print(f"LEX_ERROR: Character is illegal {self.current_char} at {start_pos}.")
                self.advance()
                exit()
                
        return tokens
    
    
# """
# PART F START HERE
# """
# symbol_table = {} #key=var_name, value=var_value
# ###################################################
#             ##### SYNTAX TREE NODES #####
# ###################################################
    
# class NumberNode:
#     def __init__(self, token) -> None:
#         self.token = token
    
#     def __repr__(self) -> str:
#         return f'{self.token}'
    
# class BinaryOperationNode:
#     def __init__(self, left_node, op_token, right_node) -> None:
#         self.left_node = left_node
#         self.op_token = op_token
#         self.right_node = right_node
        
#     def __repr__(self) -> str:
#         return f'({self.left_node}, {self.op_token}, {self.right_node})'
    
# class UnaryOperationNode:
#     def __init__(self, op_token, node) -> None:
#         self.op_token = op_token
#         self.node = node
    
#     def __repr__(self) -> str:
#         return f'({self.op_token}, {self.node})'
    
# class VarAccessNode:
#     def __init__(self, var_name_token) -> None:
#         self.var_name_token = var_name_token
        
# class VarAssignNode:
#     def __init__(self, var_name_token, value_node) -> None:
#         self.var_name_token = var_name_token
#         self.value_node = value_node
    
# ###################################################
#                 ##### PARSER #####
# ###################################################

# class Parser2:
#     def __init__(self, tokens) -> None:
#         self.tokens= tokens
#         self.token_idx = 0
#         self.current_token = self.tokens[self.token_idx]
        
#     def advance(self):
#         self.token_idx += 1
#         if self.token_idx < len(self.tokens):
#             self.current_token = self.tokens[self.token_idx]
#         return self.current_token
    
#     def parse(self):
#         res = self.expr()
#         return res
    
#     #######################################################
#     def atom(self):
#         token = self.current_token
        
#         ### literal integer
#         if token.type in (LITERAL_INT_oneb, LITERAL_INT_twob, LITERAL_INT_fob, LITERAL_INT_ateb):
#             self.advance()
#             return NumberNode(token)
#         ### identifier 
#         if token.type == IDENTIFIER:
#             self.advance()
#             return VarAccessNode(token)
#         ### open parenthese and close parenthese
#         elif token.type == LPAREN:
#             self.advance()
#             expr = self.expr()
#             if self.current_token.type == RPAREN:
#                 self.advance()
#                 return expr
#             else:  
#                 print("SYNTAX ERROR: Expected ')'")
    
#     def factor(self): 
#         token = self.current_token
#         ### negative|positive integer
#         if token.type in (PLUS, MINUS):
#             self.advance()
#             factor = self.factor()
#             return UnaryOperationNode(token, factor)
#         ### literal integer
#         elif token.type in (LITERAL_INT_oneb, LITERAL_INT_twob, LITERAL_INT_fob, LITERAL_INT_ateb):
#             self.advance()
#             return NumberNode(token)
#         ### open parenthese and close parenthese
#         elif token.type == LPAREN:
#             self.advance()
#             expr = self.expr()
#             if self.current_token.type == RPAREN:
#                 self.advance()
#                 return expr
#             else:  
#                 print("SYNTAX ERROR: Expected ')'")
    
#     def term(self):
#         return self.binary_op(self.factor, (MUL, DIV, MOD))
    
#     def arith_expr(self):
#         return self.binary_op(self.term, (PLUS, MINUS))
    
#     def comp_expr(self):
#         if self.current_token.type == KEYWORD and self.current_token.vaue == 'not':
#             op_token = self.current_token
#             self.advance()
            
#             node = self.comp_expr()
#             return UnaryOperationNode(op_token=op_token, node=node)
#         node = self.binary_op(self.arith_expr(), (LESS,LESSEQ,GREATER,GREATEREQ,EQUAL,NOTEQ))
#         return node
    
#     def expr(self):
#         # Variable declaration: twob varname;
#         if self.current_token.type == DATATYPE and self.current_token.value in DATATYPES:
#             self.advance() # to find the variable name
#             if self.current_token.type != IDENTIFIER:
#                 print("SYNTAX ERROR: Expected Identifier.")
#             elif self.current_token.type == IDENTIFIER:
#                 var_name = self.current_token
#                 self.advance() # look for ';'
#                 if self.current_token.type != SEMICOLON:
#                     self.advance()
#                     print("SYNTAX ERROR: Expected ';'")
#                 else:
#                     self.advance()
#                     # Variable Declaration in Symbol Table
#                     return VarAssignNode(var_name_token=var_name, value_node=None)
                    
        
#         if self.current_token.type == IDENTIFIER:
#             var_name = self.current_token
#             self.advance() 
#             if self.current_token.type == ASSIGN:
#                 self.advance()
#                 expr = self.expr()
#                 if self.current_token.type != SEMICOLON:
#                     self.advance()
#                     print("SYNTAX ERROR: Expected ';'")
#                 else:
#                     self.advance()
#                     return VarAssignNode(var_name_token=var_name, value_node=expr)
#         #return self.binary_op(self.term, (PLUS, MINUS))        
#         return self.binary_op(self.comp_expr, ((KEYWORD, "and"), (KEYWORD, "or")))
        
#     def binary_op(self, func, ops):
#         left = func()
        
#         while self.current_token.type in ops or (self.current_token.type, self.current_token.value) in ops:
#             op_token = self.current_token
#             self.advance()
#             right = func()
#             left = BinaryOperationNode(left, op_token, right)
            
#         return left
    
# ###################################################
#                 ##### INTEGER #####
# ###################################################
# class Number:
#     def __init__(self, value) -> None:
#         self.value = value
#     def __repr__(self) -> str:
#         return str(self.value)
        
#     ### Math Operation
#     def added_to(self, other):   
#         if isinstance(other, Number):
#             return Number(self.value + other.value)
        
#     def subtracted_by(self, other):   
#         if isinstance(other, Number):
#             return Number(self.value - other.value)
        
#     def multiplied_by(self, other):   
#         if isinstance(other, Number):
#             return Number(self.value * other.value)
        
#     def divided_by(self, other):   
#         if isinstance(other, Number):
#             if other.value == 0:
#                 print(f'SYNTAX ERROR: {self.value} division by zero')
#             return Number(self.value // other.value)
    
#     def modded_by(self, other):   
#         if isinstance(other, Number):
#             if other.value == 0:
#                 print(f'SYNTAX ERROR: {self.value} division by zero')
#             return Number(self.value % other.value)
        
#     def get_comparison_eq(self, other):
#         if isinstance(other, Number):
#             return Number(int(self.value == other.value))
    
#     def get_comparison_ne(self, other):
#         if isinstance(other, Number):
#             return Number(int(self.value != other.value))
    
#     def get_comparison_lt(self, other):
#         if isinstance(other, Number):
#             return Number(int(self.value < other.value))

#     def get_comparison_gt(self, other):
#         if isinstance(other, Number):
#             return Number(int(self.value > other.value))
        
#     def get_comparison_lte(self, other):
#         if isinstance(other, Number):
#             return Number(int(self.value <= other.value))
        
#     def get_comparison_gte(self, other):
#         if isinstance(other, Number):
#             return Number(int(self.value >= other.value))
        
#     def and_with(self, other):
#         if isinstance(other, Number):
#             return Number(int(self.value and other.value))
        
#     def or_with(self, other):
#         if isinstance(other, Number):
#             return Number(int(self.value or other.value))
        
#     def not_ed(self):
#         return Number(1 if self.value == 0 else 0)
        

# ###################################################
#             ##### INTERPRETER #####
# ###################################################

# class Interpreter:
#     def visit(self, node):
#         method_name = f'visit_{type(node).__name__}'
#         method = getattr(self, method_name, self.no_visit_method)
#         return method(node)
    
#     def no_visit_method(self, node):
#         pass
#         #raise Exception(f'No visit_{type(node).__name__} method defined.')
    
#     ################################
#     def visit_NumberNode(self, node):
#         return Number(node.token.value)
    
#     def visit_VarAccessNode(self, node):
#         var_name = node.var_name_token.value
#         if var_name in symbol_table.keys:
#             value = symbol_table[var_name]
#             if value is None:
#                 print(f'Syntax Error: {var_name} has not been initialized.')
#                 return None
#             elif value is not None:
#                 return value
#         else:
#             print(f'Syntax Error: {var_name} is not defined')
#         return value

#     def visit_VarAssignNode(self, node):
#         var_name = node.var_name_token.value
#         value = self.visit(node.value_node)
#         symbol_table[var_name] = value
#         return value
    
#     def visit_BinaryOperationNode(self, node):
#         left = self.visit(node.left_node)
#         right = self.visit(node.right_node)
        
#         if node.op_token.type == PLUS:
#             result = left.added_to(right)
#         elif node.op_token.type == MINUS:
#             result = left.subtracted_by(right)
#         elif node.op_token.type == MUL:
#             result = left.multiplied_by(right)
#         elif node.op_token.type == DIV:
#             result = left.divided_by(right)    
#         elif node.op_token.type == MOD:
#             result = left.modded_by(right)
#         elif node.op_token.type == EQUAL:
#             result = left.get_comparison_eq(right)
#         elif node.op_token.type == NOTEQ:
#             result = left.get_comparison_ne(right)
#         elif node.op_token.type == LESS:
#             result = left.get_comparison_lt(right)  
#         elif node.op_token.type == GREATER:
#             result = left.get_comparison_gt(right)
#         elif node.op_token.type == LESSEQ:
#             result = left.get_comparison_lte(right)
#         elif node.op_token.type == GREATEREQ:
#             result = left.get_comparison_gte(right)
#         elif node.op_token.type == KEYWORD and node.op_token.value == 'AND':
#             result = left.and_with(right)
#         elif node.op_token.type == KEYWORD and node.op_token.value == 'OR':
#             result = left.or_with(right)
    
#         return result  
    
#     def visit_UnaryOperationNode(self, node):
#         number = self.visit(node.node) #visit its child node
        
#         if node.op_token.type == MINUS:
#             number = number.multiplied_by(Number(-1))
#         elif node.op_token.type == KEYWORD and node.op_token.value == 'not':
#             number = number.not_ed()
#         return number

# if __name__ == "__main__":
    
#     text_file = open("test_no_error_1.txt", "r")
#     #read whole file to a string
#     data = text_file.read()
#     #close file
#     text_file.close()
#     print(data)
#     lexer = LexicalAnalyzer(data)
#     tokens = lexer.tokenize()
#     print(tokens)
#     print(len(tokens)) 
    
    
#     math = 'ateb big_num;'
#     lexer = LexicalAnalyzer(math)
#     tokens = lexer.tokenize()
#     parser = Parser2(tokens)
#     syntax_tree = parser.parse()
#     print("Data: "+math)
#     print("Tokens List: " + str(tokens))    
#     print("Parser" + str(syntax_tree))
    
#     inter = Interpreter()
#     result = inter.visit(syntax_tree)
#     print(symbol_table)
    
    