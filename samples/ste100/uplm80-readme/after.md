# uplm80 - PL/M-80 Compiler

[![PyPI version](https://badge.fury.io/py/uplm80.svg)](https://pypi.org/project/uplm80/)
[![Tests](https://github.com/avwohl/uplm80/actions/workflows/pytest.yml/badge.svg)](https://github.com/avwohl/uplm80/actions/workflows/pytest.yml)
[![Pylint](https://github.com/avwohl/uplm80/actions/workflows/pylint.yml/badge.svg)](https://github.com/avwohl/uplm80/actions/workflows/pylint.yml)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

A modern PL/M-80 compiler targeting Zilog Z80 assembly language.

PL/M-80 was the primary systems programming language for CP/M and other 8080/Z80 operating systems. This compiler can rebuild original CP/M utilities from their PL/M source code.

**Repository:** https://github.com/avwohl/uplm80

## Features

- Compiles the full PL/M-80 language
- Targets the Z80 instruction set
- Compiles more than one file together, and optimizes across modules
- Runs more than one optimization pass (peephole, and tail merging after assembly)
- Generates relocatable object files for standard CP/M linkers
- Produces code that is comparable to the original Digital Research compiler

## Code Quality

The output of uplm80 is comparable to the output of the original Digital Research compiler:

| Program | DR PL/M-80 | uplm80 | Difference |
|---------|------------|--------|------------|
| PIP.COM | 7424 bytes | 7127 bytes | -4.0% |

## Installation

To install from PyPI, run this command:

```bash
pip install uplm80 um80 upeepz80
```

**Platform-specific guides:**
- **Raspberry Pi**: See [README_RASPBERRY_PI.md](README_RASPBERRY_PI.md)
- **General/Development**: See [INSTALL.md](INSTALL.md)

To install from source, do these steps:

```bash
git clone https://github.com/avwohl/uplm80.git
cd uplm80
pip install -e .
```

## Usage

### Compile PL/M-80 to Assembly

```bash
uplm80 input.plm -o output.mac
```

As an alternative, run the compiler as a module:

```bash
python -m uplm80.compiler input.plm -o output.mac
```

Options:
- `-m cpm` or `-m bare` - Runtime mode (default: cpm)
  - `cpm`: For new PL/M programs, maximum stack under BDOS
  - `bare`: Original Digital Research compatible (jump to start-3)
- `-o output.mac` - Output file name
- `-O 0|1|2|3` - Optimization level (default: 2)
- `-D SYMBOL` - Define conditional compilation symbol (you can repeat this option)

### Multi-File Compilation

To optimize across modules, compile more than one source file together:

```bash
uplm80 main.plm helper.plm library.plm -o output.mac
```

When you give more than one file to the compiler:
- The compiler parses all the files before it generates code.
- The compiler builds one call graph across all the modules.
- The compiler allocates the local variable storage (`??AUTO`). The allocation depends on which procedures can be active at the same time, across module boundaries.
- The compiler generates one combined output file.

This method produces better code than separate compilation. The compiler can share local variable storage between procedures in different modules that never call each other.

### Assemble and Link

Use your preferred Z80 assembler and linker. This example uses um80 and ul80:

```bash
um80 output.mac                              # Assemble to .rel
ul80 -o program.com output.rel runtime.rel   # Link to CP/M .com
```

## Language Reference

PL/M-80 is a typed systems programming language with:

- **Data types**: BYTE (8-bit), ADDRESS (16-bit)
- **Variables**: Scalars, arrays, structures, BASED variables (pointers)
- **Control flow**: DO/END, DO WHILE, DO CASE, IF/THEN/ELSE
- **Procedures**: With parameters, local variables, recursion
- **Built-in functions**: HIGH, LOW, DOUBLE, SHL, SHR, ROL, ROR, and others
- **I/O**: INPUT, OUTPUT for port access

Example:

```plm
hello: DO;
    DECLARE message DATA ('Hello, World!$');
    DECLARE i BYTE;

    print: PROCEDURE(addr) PUBLIC;
        DECLARE addr ADDRESS;
        /* CP/M BDOS print string */
        CALL mon1(9, addr);
    END print;

    CALL print(.message);
END hello;
```

For a complete working example, see [examples/hellocpm.plm](examples/hellocpm.plm).

A drop-in Makefile that drives the full `uplm80 → um80 → ul80` pipeline is
available at [docs/example.Makefile](docs/example.Makefile). The Makefile also
has optional `ud80` and `ux80` disassembly targets. Martin Homuth-Rosemann
([@Ho-Ro](https://github.com/Ho-Ro)) contributed it in issue #5.

For more information about CP/M BDOS usage, see [docs/BDOS_REFERENCE.md](docs/BDOS_REFERENCE.md).

## Conditional Compilation

PL/M-80 v4.0 added conditional compilation. The directives are **control lines**.
A control line has a `$` in column 1, exactly like `$INCLUDE` and `$TITLE`. Thus
one source file can target different configurations. For example, CP/M 2.2 or
CP/M 3, and single-user or MP/M. You do not have to enable this function first.

### Directives

| Directive | Description |
|-----------|-------------|
| `$SET (NAME)` | Define a symbol |
| `$RESET (NAME)` | Undefine a symbol |
| `$IF NAME` | Compile following code if NAME is defined |
| `$ELSEIF NAME` | Else-if branch |
| `$ELSE` | Else branch |
| `$ENDIF` | End conditional block |
| `$COND` / `$NOCOND` | Listing controls only (accepted as no-ops) |

The compiler also accepts a comment-wrapped form (`/** $if NAME **/`). This form
is for CP/M-3-style sources that put the same directives in comment syntax.

### Example

```plm
$set (CPM3)
DECLARE
$if CPM3
    VERSION LITERALLY '30H',
$else
    VERSION LITERALLY '22H',
$endif
    MAXFILES BYTE;
```

### Command Line

You can also define symbols on the command line:

```bash
uplm80 pip.plm -D CPM3 -D MPM -o pip.mac
```

## Runtime Library

The compiler generates calls to the runtime routines in the table that follows.
Supply these routines in a separate .rel file.

| Routine | Description |
|---------|-------------|
| `??MUL` | 16-bit unsigned multiply |
| `??DIV` | 16-bit unsigned divide |
| `??MOD` | 16-bit unsigned modulo |
| `??SHL` | 16-bit shift left |
| `??SHR` | 16-bit logical shift right |
| `??SHRS` | 16-bit arithmetic shift right |
| `??MOVE` | Block memory move |

## Runtime Modes

The operating system reserves the first 100H bytes of the memory of a CP/M
program (zero page, default FCB, default DMA buffer). All CP/M `.COM` programs
load at address 100H. Thus the contents of a CP/M binary start at offset 0 of the
file. The linker relocates the program to 100H.

> **CAUTION: DO NOT WRITE `100H:` IN A PL/M SOURCE FILE.**
> The assembler emits a `cseg org 100H`. The linker then obeys it and pads the
> binary with 256 zero bytes from 0 to FFH.

In `bare` mode there is one condition where a leading address constant is
meaningful. See the notes for `bare` mode below.

### CP/M Mode (default: `-m cpm`)

Use this mode for new PL/M-80 programs. The compiler emits a small entry
preamble. The preamble takes the maximum stack space under BDOS, and it returns
correctly to CP/M.

- The compiler emits the entry code at the start of the `.com` image.
  **Do not write `0100H:` in your source.** The linker (`ul80`) defaults to
  origin 100H, which is correct for CP/M.
- Entry preamble (auto-generated):

  ```asm
  ld   hl,(6)       ; load BDOS base from address 6
  ld   sp,hl        ; stack grows down from just below BDOS
  call MAIN         ; run your main procedure
  jp   0            ; warm-boot return to CP/M when MAIN returns
  ```
- Stack: the maximum available, which is all the memory between the end of the
  program and BDOS.
- Requires CP/M stubs in your runtime: `MON1`, `MON2`, `MON3`, `BOOT`.
- System variables: `BDISK`, `MAXB`, `FCB`, `BUFF`, `IOBYTE`.

### Bare Metal Mode (`-m bare`)

Use this mode to rebuild the original Digital Research utilities (PIP.PLM,
ED.PLM, and others) byte-compatibly. These programs obey the Intel PL/M-80
convention: they jump to *start − 3* to go past a local stack area.

- Entry preamble (auto-generated):

  ```asm
  jp   ??START      ; skip over the stack buffer
  ds   64           ; 64-byte local stack
  ??STACK:          ; top of stack
  ??START:
  ld   sp,??STACK   ; use the local stack
  jp   MAIN         ; jump (not call) into MAIN
  ```
- The program controls its own exit. There is no automatic warm boot. The
  original DR utilities reboot or chain when they write to memory directly.
- Custom entry points: the entry preamble is in the first bytes of the image.
  Thus the original programs sometimes put a `DECLARE … DATA(...)` block first,
  to make a different jump. PIP.PLM does this, and makes a JMP table at page 1.
  In `bare` mode the leading address constant (for example, `0100H:` or `0200H:`)
  *is* meaningful. It sets the assembler `org` for the bare image.
- Compatible with original Intel/DR PL/M-80 sources.

## Project Structure

```
uplm80/
├── compiler.py      # Main compiler driver / CLI
├── frontend.py      # plox-driven lexer + LR parse → AST
├── preprocess.py    # PL/M preprocessor ($INCLUDE, $if, LITERALLY, ...)
├── ast_nodes.py     # AST definitions
├── ast_optimizer.py # AST-level optimizations
├── codegen.py       # Z80 code generator
├── runtime.py       # Runtime helpers
├── symbols.py       # Symbol table
├── errors.py        # Diagnostic exception types
└── data/            # Pre-built plox grammar bundle (plm_full.json)
```

The external [upeepz80](https://github.com/avwohl/upeepz80) package does the
peephole optimization. The front-end comes from [plox](https://github.com/avwohl/plox)
grammars (`plm_pre` and `plm_full`). The compiler loads the front-end at import
time from the JSON bundle in `data/`.

## License

This project uses the GNU General Public License v3.0 or later.
For more information, see the [LICENSE](LICENSE) file.

## Contributing

Contributions are welcome. You can submit issues and pull requests.

## Related Projects

- [80un](https://github.com/avwohl/80un) - Unpacker for CP/M compression and archive formats (LBR, ARC, squeeze, crunch, CrLZH)
- [cpmdroid](https://github.com/avwohl/cpmdroid) - Z80/CP/M emulator for Android with RomWBW HBIOS compatibility and VT100 terminal
- [cpmemu](https://github.com/avwohl/cpmemu) - CP/M 2.2 emulator with Z80/8080 CPU emulation and BDOS/BIOS translation to Unix filesystem
- [ioscpm](https://github.com/avwohl/ioscpm) - Z80/CP/M emulator for iOS and macOS with RomWBW HBIOS compatibility
- [learn-ada-z80](https://github.com/avwohl/learn-ada-z80) - Ada programming examples for the uada80 compiler targeting Z80/CP/M
- [mbasic](https://github.com/avwohl/mbasic) - Modern MBASIC 5.21 Interpreter & Compilers
- [mbasic2025](https://github.com/avwohl/mbasic2025) - MBASIC 5.21 source code reconstruction - byte-for-byte match with original binary
- [mbasicc](https://github.com/avwohl/mbasicc) - C++ implementation of MBASIC 5.21
- [mbasicc_web](https://github.com/avwohl/mbasicc_web) - WebAssembly MBASIC 5.21
- [mpm2](https://github.com/avwohl/mpm2) - MP/M II multi-user CP/M emulator with SSH terminal access and SFTP file transfer
- [romwbw_emu](https://github.com/avwohl/romwbw_emu) - Hardware-level Z80 emulator for RomWBW with 512KB ROM + 512KB RAM banking and HBIOS support
- [scelbal](https://github.com/avwohl/scelbal) - SCELBAL BASIC interpreter - 8008 to 8080 translation
- [uada80](https://github.com/avwohl/uada80) - Ada compiler targeting Z80 processor and CP/M 2.2 operating system
- [uc80](https://github.com/avwohl/uc80) - ANSI C compiler targeting Z80 processor and CP/M 2.2 operating system
- [ucow](https://github.com/avwohl/ucow) - Unix/Linux Cowgol to Z80 compiler
- [um80_and_friends](https://github.com/avwohl/um80_and_friends) - Microsoft MACRO-80 compatible toolchain for Linux: assembler, linker, librarian, disassembler
- [upeepz80](https://github.com/avwohl/upeepz80) - Universal peephole optimizer for Z80 compilers
- [uplox](https://github.com/avwohl/uplox) - Compiler front-end generator (lexer DFA + LR parser + typed auto-AST) that uplm80 uses for PL/M-80 parsing
- [z80cpmw](https://github.com/avwohl/z80cpmw) - Z80 CP/M emulator for Windows (RomWBW)
