def minicrt_print(s):
  """Runtime print function for strings"""
  print(s, end='')

def minicrt_print_int(n):
  """Runtime print function for integers"""
  print(n, end='')

def dll_main(hinst, reason, reserved):
  """DLL entry point"""
  return True