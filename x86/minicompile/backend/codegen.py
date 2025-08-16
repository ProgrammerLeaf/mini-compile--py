from ..frontend.parser import NodeType
from ..frontend.lexer import TokenType

class CodeGen:
  def __init__(self):
    self.buffer = []
    self.strings = {}  # To store string constants
    
  def generate(self, node):
    if node.type == NodeType.ND_PRINT:
      self.generate_expr(node.left)
      self.buffer.append("call minicrt_print")
    else:
      self.generate_expr(node)
    
  def generate_expr(self, node):
    if node.type == NodeType.ND_EXPR:
      if node.token.type == TokenType.TOK_NUMBER:
        self.buffer.append(f"push qword {node.token.start}")
      elif node.token.type == TokenType.TOK_STRING:
        str_id = f"str_{id(node.token.start)}"
        self.strings[str_id] = node.token.start
        self.buffer.append(f"push offset {str_id}")
    elif node.type == NodeType.ND_BINOP:
      self.generate_expr(node.left)
      self.generate_expr(node.right)
            
      if node.token.type == TokenType.TOK_PLUS:
        self.buffer.append("pop ebx")
        self.buffer.append("pop eax")
        self.buffer.append("add eax, ebx")
        self.buffer.append("push eax")
      elif node.token.type == TokenType.TOK_MINUS:
        self.buffer.append("pop ebx")
        self.buffer.append("pop eax")
        self.buffer.append("sub eax, ebx")
        self.buffer.append("push eax")
      elif node.token.type == TokenType.TOK_MUL:
        self.buffer.append("pop ebx")
        self.buffer.append("pop eax")
        self.buffer.append("imul ebx")
        self.buffer.append("push eax")
      elif node.token.type == TokenType.TOK_DIV:
        self.buffer.append("pop ebx")
        self.buffer.append("pop eax")
        self.buffer.append("cqo")  # Sign extend rax to rdx:rax
        self.buffer.append("idiv ebx")
        self.buffer.append("push eax")
    
  def get_code(self):
    return "\n".join(self.buffer)
    
  def get_strings(self):
    return self.strings