class Assembler:
  def __init__(self):
    self.mnemonics = {
      'push': self._assemble_push,
      'pop': self._assemble_pop,
      'add': self._assemble_add,
      'sub': self._assemble_sub,
      'imul': self._assemble_imul,
      'idiv': self._assemble_idiv,
      'call': self._assemble_call,
      'ret': self._assemble_ret,
      'mov': self._assemble_mov
    }
    self.labels = {}
    self.code = bytearray()
    self.data = bytearray()
    self.string_offsets = {}

  def _assemble_push(self, args):
    if args.startswith('qword '):
      val = int(args.split()[1])
      return b'\x68' + val.to_bytes(4, byteorder='little')  # 简化的32位push
    elif args.startswith('offset '):
      label = args.split()[1]
      # 暂存偏移，后续重定位
      self.labels[label] = len(self.code) + 1  # 指令长度1字节
      return b'\x68' + b'\x00\x00\x00\x00'  # 占位

  def _assemble_pop(self, args):
    regs = {'rbx': 0x5B, 'rax': 0x58}
    return bytes([0x58 + regs[args]])

  def _assemble_add(self, args):
    if args == 'rax, rbx':
      return b'\x48\x01\xD8'

  def _assemble_sub(self, args):
    if args == 'rax, rbx':
      return b'\x48\x29\xD8'

  def _assemble_imul(self, args):
    if args == 'rbx':
      return b'\x48\x0F\xAF\xC3'

  def _assemble_idiv(self, args):
    if args == 'rbx':
      return b'\x48\xF7\xFB'

  def _assemble_call(self, args):
    if args == 'minicrt_print':
      return b'\xE8\x00\x00\x00\x00'  # 占位

  def _assemble_ret(self, args):
    return b'\xC3'

  def _assemble_mov(self, args):
    if args == 'eax, 1':
      return b'\xB8\x01\x00\x00\x00'

  def assemble(self, asm_lines, strings):
    # 处理数据段
    for str_id, value in strings.items():
      self.string_offsets[str_id] = len(self.data)
      self.data.extend(value.encode('ascii') + b'\x00')

        # 处理代码段
    for line in asm_lines:
      line = line.strip()
      if not line:
        continue
      parts = line.split(maxsplit=1)
      if len(parts) < 1:
        continue
      mnemonic = parts[0]
      args = parts[1] if len(parts) > 1 else ''
      if mnemonic in self.mnemonics:
        self.code.extend(self.mnemonics[mnemonic](args))

    return self.code, self.data