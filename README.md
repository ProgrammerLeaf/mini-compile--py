# Mini Compiler(py)

Mini Compiler(py) 是一个轻量级的编译器项目，支持将简单的自定义语言（.mini 文件）编译为不同平台的可执行文件、动态库或静态库，也可直接运行程序。目前支持 Linux、x86 Windows 和 x86_64 Windows 平台。

未来会有其他语言的版本，敬请期待。

目前有C语言版本[ProgrammerLeaf/mini-complie-C: 一个用C语言写的微型编译器](https://github.com/ProgrammerLeaf/mini-complie-C)

## 支持平台

- **Linux**：生成 ELF 格式的可执行文件（.out）、动态库（.so）、静态库（.a）
- **x86 Windows**：生成 32 位 PE 格式的可执行文件（.exe）、动态库（.dll）、静态库（.lib）
- **x86_64 Windows**：生成 64 位 PE 格式的可执行文件（.exe）、动态库（.dll）、静态库（.lib）

## 使用方法

该项目需要python3.6或更高版本。

编译器命令行工具为 `python run.py`，支持以下参数：

| 参数          | 功能说明                       | 平台支持    |
| ----------- | -------------------------- | ------- |
| `[file]`    | 指定输入的 .mini 源文件（必选）        | 所有平台    |
| `-o [name]` | 指定输出文件名称（默认：a.exe 或 a.out） | 所有平台    |
| `--run`     | 直接运行程序（不生成目标文件）            | 所有平台    |
| `--so`      | 生成动态库                      | Linux   |
| `--a`       | 生成静态库                      | Linux   |
| `--dll`     | 生成动态库                      | Windows |
| `--lib`     | 生成静态库                      | Windows |

**语法**：

plaintext

```plaintext
python run.py file [--so|--a|--dll|--lib] [-o name] [--run]
```

### 示例

1. **编译为可执行文件并运行**（Linux）：
   
   ```bash
   minic examples/hello.mini -o hello
   ./hello
   ```

2. **直接运行程序**（Windows）：
   
   ```cmd
   minic.exe examples/hello.mini --run
   ```

3. **生成动态库**（Linux）：
   
   ```bash
   minic examples/calc.mini --so -o libcalc.so
   ```

4. **生成静态库**（Windows）：
   
   ```cmd
   minic.exe examples/calc.mini --lib -o calc.lib
   ```

## 支持的语法

目前 Mini Compiler 支持简单的语法特性，包括：

- 打印语句（如 `print "Hello, World!"`）
- 基本算术表达式（+、-、*、/）
- 整数和字符串常量

## 注意事项

- 本项目为简化的编译器实现，仅支持基础语法，不适合生产环境。
- 不同平台的目标文件格式和库类型存在差异，使用时需注意参数与平台匹配。
- 示例程序位于 `examples/`，可直接用于测试。
