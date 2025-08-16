import os

def minicrt_print(s):
  """Linux下的打印函数，使用write系统调用"""
  os.write(1, s.encode('ascii') + b'\n')

def minicrt_print_int(n):
  """打印整数"""
  os.write(1, str(n).encode('ascii') + b'\n')