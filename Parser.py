from LexicalAnalyzer import Token 

class NumberNode:
    def __init__(self, token) -> None:
        self.token = token
    
    def __repr__(self) -> str:
        return f'{self.token}'
    
class BinaryOperationNode:
    def __init__(self, left_node, op_token, right_node) -> None:
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node
        
    def __repr__(self) -> str:
        return f'{self.left_node}, {self.op_token}, {self.right_node}'
    
###################################################
                ##### PARSER #####
###################################################

class Parser:
    def __init__(self, tokens) -> None:
        self.tokens= tokens
        self.token_idx = 1
        self.advance()
        
    def advance(self):
        self.token_idx += 1
        if self.token_idx < len(self.tokens):
            self.current_token = self.tokens[self.token_idx]
        return self.current_token
    
    def factor(self):
        token = self.current_token
        
        if token.type
        
        