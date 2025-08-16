from .lexer import TokenType, Lexer, Token

class NodeType:
  ND_PRINT = 0
  ND_EXPR = 1
  ND_BINOP = 2

class ASTNode:
  def __init__(self, node_type):
    self.type = node_type
    self.left = None
    self.right = None
    self.token = None

class Parser:
  def __init__(self, lexer):
    self.lexer = lexer
    self.current_token = self.lexer.next_token()
    
  def eat(self, expected_type):
    if self.current_token.type == expected_type:
      self.current_token = self.lexer.next_token()
    
  def parse(self):
    node = ASTNode(NodeType.ND_EXPR)
        
    if self.current_token.type == TokenType.TOK_PRINT:
      node.type = NodeType.ND_PRINT
      self.eat(TokenType.TOK_PRINT)
            
      if self.current_token.type == TokenType.TOK_STRING:
        node.left = ASTNode(NodeType.ND_EXPR)
        node.left.token = self.current_token
        self.eat(TokenType.TOK_STRING)
      else:
        node.left = self.parse_expr()
            
      self.eat(TokenType.TOK_SEMICOLON)
      return node
        
    return self.parse_expr()
    
  def parse_expr(self):
    node = self.parse_term()
        
    while (self.current_token.type == TokenType.TOK_PLUS or 
      self.current_token.type == TokenType.TOK_MINUS):
      binop = ASTNode(NodeType.ND_BINOP)
      binop.token = self.current_token
      binop.left = node
            
      if self.current_token.type == TokenType.TOK_PLUS:
        self.eat(TokenType.TOK_PLUS)
      else:
        self.eat(TokenType.TOK_MINUS)
            
      binop.right = self.parse_term()
      node = binop
        
    return node
    
  def parse_term(self):
    node = self.parse_factor()
        
    while (self.current_token.type == TokenType.TOK_MUL or 
      self.current_token.type == TokenType.TOK_DIV):
      binop = ASTNode(NodeType.ND_BINOP)
      binop.token = self.current_token
      binop.left = node
            
      if self.current_token.type == TokenType.TOK_MUL:
        self.eat(TokenType.TOK_MUL)
      else:
        self.eat(TokenType.TOK_DIV)
            
      binop.right = self.parse_factor()
      node = binop
        
    return node
    
  def parse_factor(self):
    node = ASTNode(NodeType.ND_EXPR)
        
    if self.current_token.type == TokenType.TOK_NUMBER:
      node.token = self.current_token
      self.eat(TokenType.TOK_NUMBER)
      return node
    elif self.current_token.type == TokenType.TOK_LPAREN:
      self.eat(TokenType.TOK_LPAREN)
      node = self.parse_expr()
      self.eat(TokenType.TOK_RPAREN)
      return node
        
    # Default to 0 if nothing matches
    node.token = Token(TokenType.TOK_NUMBER, "0", 1, 0, 0)
    return node