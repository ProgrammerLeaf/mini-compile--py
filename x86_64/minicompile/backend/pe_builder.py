import struct

class PEBuilder:
  @staticmethod
  def build_exe(code, data, entry_point):
    pe = bytearray()
        
    # DOS头
    pe.extend(b'MZ' + b'\x00' * 58 + b'\x40\x00\x00\x00')
        
    # NT头 (简化版)
    pe.extend(b'PE\x00\x00')
    pe.extend(struct.pack('<H', 0x8664))  # 机器类型 (x64)
    pe.extend(struct.pack('<H', 2))       # 节数量
    pe.extend(b'\x00' * 8)                # 时间戳等
    pe.extend(struct.pack('<L', 0x1000))  # 可选头大小
    pe.extend(struct.pack('<H', 0x010F))  # 特性
        
    # 可选头
    pe.extend(struct.pack('<H', 0x020B))  # 魔术数 (PE32+)
    pe.extend(b'\x00' * 90)               # 其余字段
    pe.extend(struct.pack('<L', 2))       # 节数量
    pe.extend(struct.pack('<L', entry_point))  # 入口点
        
    # 代码节
    pe.extend(b'.text\x00\x00\x00')
    pe.extend(struct.pack('<L', len(code)))  # 虚拟大小
    pe.extend(struct.pack('<L', 0x1000))     # 虚拟地址
    pe.extend(struct.pack('<L', len(code)))  # 原始大小
    pe.extend(struct.pack('<L', len(pe)))    # 原始偏移
    pe.extend(b'\x00' * 16)
    pe.extend(struct.pack('<L', 0x60000020)) # 特性
    pe.extend(code)
        
    # 数据节
    pe.extend(b'.data\x00\x00\x00')
    pe.extend(struct.pack('<L', len(data)))  # 虚拟大小
    pe.extend(struct.pack('<L', 0x2000))     # 虚拟地址
    pe.extend(struct.pack('<L', len(data)))  # 原始大小
    pe.extend(struct.pack('<L', len(pe)))    # 原始偏移
    pe.extend(b'\x00' * 16)
    pe.extend(struct.pack('<L', 0xC0000040)) # 特性
    pe.extend(data)
        
    return pe