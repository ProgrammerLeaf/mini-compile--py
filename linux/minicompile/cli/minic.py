import sys
from ..frontend.lexer import Lexer
from ..frontend.parser import Parser
from ..backend.codegen import CodeGen
from ..backend.linux_target import generate_asm, TargetType
from ..runtime.minicrt import minicrt_print, minicrt_print_int
from ..backend.assembler import Assembler
from ..backend.elf_builder import ELFBuilder
from ..frontend.parser import NodeType
from ..frontend.lexer import TokenType

class OutputType:
  COMPILE_EXE = 0
  COMPILE_SO = 1
  COMPILE_A = 2
  COMPILE_RUN = 3

class CompilerConfig:
  def __init__(self):
    self.output_type = OutputType.COMPILE_EXE
    self.output_name = "a.exe"
    self.optimize_level = 0

def evaluate_ast(node):
  """Evaluate AST directly for --run option"""
    
  if node.type == NodeType.ND_PRINT:
    result = evaluate_ast(node.left)
    print(result, end='')
    return None
    
  elif node.type == NodeType.ND_EXPR:
    if node.token.type == TokenType.TOK_NUMBER:
      return int(node.token.start)
    elif node.token.type == TokenType.TOK_STRING:
      return node.token.start
    
  elif node.type == NodeType.ND_BINOP:
    left_val = evaluate_ast(node.left)
    right_val = evaluate_ast(node.right)
        
    if node.token.type == TokenType.TOK_PLUS:
      return left_val + right_val
    elif node.token.type == TokenType.TOK_MINUS:
      return left_val - right_val
    elif node.token.type == TokenType.TOK_MUL:
      return left_val * right_val
    elif node.token.type == TokenType.TOK_DIV:
      return left_val // right_val
    
  return 0

def compile_program(source, config):
  # Create lexer
  lexer = Lexer(source)
    
  # Create parser
  parser = Parser(lexer)
    
  # Parse AST
  ast = parser.parse()
    
  # Create code generator
  codegen = CodeGen()
    
  # Generate code
  codegen.generate(ast)
    
    # Determine output type
  if config.output_type == OutputType.COMPILE_RUN:
    # Evaluate directly
    evaluate_ast(ast)
    print()  # Add newline after output
  else:
    # Generate target file
    target = {
      OutputType.COMPILE_EXE: TargetType.TARGET_EXE,
      OutputType.COMPILE_SO: TargetType.TARGET_SO,
      OutputType.COMPILE_A: TargetType.TARGET_A
    }.get(config.output_type, TargetType.TARGET_EXE)
        

  # 生成目标文件
  target = {
    OutputType.COMPILE_EXE: TargetType.TARGET_EXE,
    OutputType.COMPILE_SO: TargetType.TARGET_SO,
    OutputType.COMPILE_A: TargetType.TARGET_A
    }.get(config.output_type, TargetType.TARGET_EXE)
    
    # 生成汇编代码
  asm_lines, strings = generate_asm(codegen, target, config.output_name)
    
    # 汇编为机器码
  assembler = Assembler()
  code, data = assembler.assemble(asm_lines, strings)
    
  # 生成PE文件
  entry_point = 0x1000  # .text节的虚拟地址
  pe_data = ELFBuilder.build_elf(code, data, entry_point)
    
  # 写入EXE文件
  with open(config.output_name, 'wb') as f:
    f.write(pe_data)

def main():
  config = CompilerConfig()
  source_file = None
    
  # Parse command line arguments
  i = 1
  while i < len(sys.argv):
    arg = sys.argv[i]
    if arg == "-o":
      if i + 1 < len(sys.argv):
        config.output_name = sys.argv[i+1]
        i += 1
    elif arg == "--so":
      config.output_type = OutputType.COMPILE_SO
    elif arg == "--a":
      config.output_type = OutputType.COMPILE_A
    elif arg == "--run":
      config.output_type = OutputType.COMPILE_RUN
    else:
      source_file = arg
    i += 1
    
  if not source_file:
    print("Error: No source file provided.", file=sys.stderr)
    return 1
    
  # Read source file
  try:
    with open(source_file, 'r') as f:
      source = f.read()
  except IOError as e:
    print(f"Error opening source file: {e}", file=sys.stderr)
    return 1
    
  # Compile program
  compile_program(source, config)
    
  return 0