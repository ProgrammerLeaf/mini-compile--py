import struct

class ELFBuilder:
  @staticmethod
  def build_elf(code, data, entry_point):
    elf = bytearray()
        
    # ELF头部 (64位)
    elf.extend(b'\x7fELF\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00')  # 标识
    elf.extend(struct.pack('<H', 0x03))  # 机器类型 (x86_64)
    elf.extend(struct.pack('<I', 0x01))  # 版本
    elf.extend(struct.pack('<Q', 0x400000))  # 入口点
    elf.extend(struct.pack('<Q', 0x40))  # 程序头偏移
    elf.extend(struct.pack('<Q', 0x00))  # 节头偏移（暂时0）
    elf.extend(struct.pack('<I', 0x00))  # 标志
    elf.extend(struct.pack('<H', 0x40))  # ELF头部大小
    elf.extend(struct.pack('<H', 0x38))  # 程序头表项大小
    elf.extend(struct.pack('<H', 2))     # 程序头表项数量
    elf.extend(struct.pack('<H', 0x00))  # 节头表项大小
    elf.extend(struct.pack('<H', 0x00))  # 节头表项数量
    elf.extend(struct.pack('<H', 0x00))  # 字符串表索引
        
    # 程序头表 - 代码段
    elf.extend(struct.pack('<I', 0x01))  # 类型 (LOAD)
    elf.extend(struct.pack('<I', 0x07))  # 标志 (RWE)
    elf.extend(struct.pack('<Q', len(elf)))  # 文件偏移
    elf.extend(struct.pack('<Q', 0x400000))  # 虚拟地址
    elf.extend(struct.pack('<Q', 0x400000))  # 物理地址
    elf.extend(struct.pack('<Q', len(code)))  # 文件大小
    elf.extend(struct.pack('<Q', len(code)))  # 内存大小
    elf.extend(struct.pack('<Q', 0x1000))    # 对齐
        
    # 程序头表 - 数据段
    elf.extend(struct.pack('<I', 0x01))  # 类型 (LOAD)
    elf.extend(struct.pack('<I', 0x06))  # 标志 (RW)
    elf.extend(struct.pack('<Q', len(elf) + len(code)))  # 文件偏移
    elf.extend(struct.pack('<Q', 0x401000))  # 虚拟地址
    elf.extend(struct.pack('<Q', 0x401000))  # 物理地址
    elf.extend(struct.pack('<Q', len(data)))  # 文件大小
    elf.extend(struct.pack('<Q', len(data)))  # 内存大小
    elf.extend(struct.pack('<Q', 0x1000))    # 对齐
        
    # 添加代码和数据
    elf.extend(code)
    elf.extend(data)
        
    return elf