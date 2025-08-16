import string

class TokenType:
  TOK_EOF = 0
  TOK_IDENT = 1
  TOK_NUMBER = 2
  TOK_STRING = 3
  TOK_PRINT = 4
  TOK_PLUS = 5
  TOK_MINUS = 6
  TOK_MUL = 7
  TOK_DIV = 8
  TOK_LPAREN = 9
  TOK_RPAREN = 10
  TOK_SEMICOLON = 11

class Token:
  def __init__(self, type_, start, length, line, col):
    self.type = type_
    self.start = start
    self.length = length
    self.line = line
    self.col = col

  def __str__(self):
    types = {v: k for k, v in TokenType.__dict__.items() if not k.startswith('__')}
    return f"Token({types[self.type]}, '{self.start[:self.length]}', line={self.line}, col={self.col})"

class Lexer:
  def __init__(self, source):
    self.source = source
    self.position = 0
    self.line = 1
    self.col = 1
    self.length = len(source)
    
  def next_token(self):
    # Skip whitespace
    while self.position < self.length and self.source[self.position].isspace():
      if self.source[self.position] == '\n':
        self.line += 1
        self.col = 1
      else:
        self.col += 1
      self.position += 1

    if self.position >= self.length:
      return Token(TokenType.TOK_EOF, "", 0, self.line, self.col)

    start_pos = self.position
    current_char = self.source[self.position]
    line = self.line
    col = self.col

    # Numbers
    if current_char.isdigit():
      while self.position < self.length and self.source[self.position].isdigit():
        self.position += 1
        self.col += 1
      return Token(
        TokenType.TOK_NUMBER,
        self.source[start_pos:self.position],
        self.position - start_pos,
        line,
        col
      )

    # Strings
    if current_char == '"':
      self.position += 1
      self.col += 1
      start_pos = self.position

      while self.position < self.length and self.source[self.position] != '"':
        if self.source[self.position] == '\n':
          self.line += 1
          self.col = 1
        else:
          self.col += 1
        self.position += 1
            
      string_val = self.source[start_pos:self.position]
      length = self.position - start_pos

      if self.position < self.length and self.source[self.position] == '"':
        self.position += 1
        self.col += 1

      return Token(TokenType.TOK_STRING, string_val, length, line, col)
        
    # Identifiers and keywords
    if current_char.isalpha():
      while self.position < self.length and self.source[self.position].isalnum():
        self.position += 1
        self.col += 1
            
      identifier = self.source[start_pos:self.position]
      length = self.position - start_pos

      if identifier == "print":
          return Token(TokenType.TOK_PRINT, identifier, length, line, col)
            
      return Token(TokenType.TOK_IDENT, identifier, length, line, col)
        
    # Single character tokens
    self.position += 1
    self.col += 1
        
    if current_char == '+':
      return Token(TokenType.TOK_PLUS, current_char, 1, line, col)
    elif current_char == '-':
      return Token(TokenType.TOK_MINUS, current_char, 1, line, col)
    elif current_char == '*':
      return Token(TokenType.TOK_MUL, current_char, 1, line, col)
    elif current_char == '/':
        return Token(TokenType.TOK_DIV, current_char, 1, line, col)
    elif current_char == '(':
        return Token(TokenType.TOK_LPAREN, current_char, 1, line, col)
    elif current_char == ')':
        return Token(TokenType.TOK_RPAREN, current_char, 1, line, col)
    elif current_char == ';':
        return Token(TokenType.TOK_SEMICOLON, current_char, 1, line, col)
        
    # Unknown token, return EOF
    return Token(TokenType.TOK_EOF, current_char, 1, line, col)