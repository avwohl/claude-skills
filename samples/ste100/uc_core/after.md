# uc_core

Shared C23 frontend and AST-level optimizer for the `uc80` (Z80/CP/M) and
`uc386` (x86-32/MS-DOS) retro C compilers.

## What's in here

- **Lexer / parser** — C23 source to AST
- **Preprocessor** — C23 preprocessor with target-configurable predefined macros
- **AST** — node definitions shared across backends
- **AST optimizer** — target-independent expression simplification, constant
  folding, strength reduction, dead-code elimination at the AST level
- **Backend protocol** — the contract a target backend must implement

## Targets using uc_core

- [uc80](https://github.com/avwohl/uc80) — Z80 / CP/M
- [uc386](https://github.com/avwohl/uc386) — x86-32 / MS-DOS

## Install

```
pip install uc_core
```

Or from source:

```
pip install -e .
```

## Usage from a backend

```python
from uc_core.frontend import parse
from uc_core.preprocessor import Preprocessor
from uc_core.ast_optimizer import ASTOptimizer
from uc_core.backend import CodeGenerator  # Protocol

# Target-specific predefined macros
predefines = {
    "__UC80__": "1",
    "__Z80__": "1",
    "__CPM__": "1",
}

pp = Preprocessor(include_paths=["lib/include"], target_predefines=predefines)
source = pp.preprocess(open("hello.c").read(), "hello.c")
ast = parse(source, "hello.c")            # strict C23
# ast = parse(source, "hello.c", kr_prepass=True)  # pre-ANSI sources
ast = ASTOptimizer(opt_level=3).optimize(ast)

# Backend is provided by the target package (uc80, uc386, ...)
# It must implement uc_core.backend.CodeGenerator
```

The front-end is plox-driven: `uc_core/frontend.py` runs the lexer
+ LR(1) parser produced from `plox/examples/c23.plox` and lowers the
parse tree into `uc_core/ast.py` dataclasses. The pre-built tables
ship as `uc_core/data/c23.json`.

### K&R / implicit-int compatibility (`kr_prepass`)

The grammar is strict C23, which has no implicit-`int` and no K&R
old-style parameter lists. `parse(..., kr_prepass=True)` enables a
source-level recovery: the strict parse is attempted first, and
**only if it fails** are the two pre-ANSI shapes rewritten to
equivalent ANSI and the parse retried —

```c
main() { … }                 ->  int main() { … }
f(a, b) int a; char *b; { … } ->  int f(int a, char *b) { … }
```

The same opt-in also lowers the GNU **computed-goto / labels-as-values**
extension (`&&label`, `goto *expr`) into a `switch` dispatch over an
integer id-encoding of each function's address-taken labels — affine
label arithmetic (`&&a - &&b`, threaded code) stays consistent, and
the result uses only `switch`/`goto`/casts:

```c
void *t[] = {&&a, &&b}; goto *t[i];
  ->  void *t[]={(void*)0,(void*)1};
      switch((long)(t[i])){case 0: goto a; case 1: goto b; default:;}
```

Off by default, so modern code is parsed exactly once and never
reaches the rewriter (zero cost). Backends expose it as they see fit
(e.g. `uc386 --kr`); it is intended for legacy/pre-ANSI and GNU-C
codebases such as the gcc-c-torture corpus.

## Related Projects

- [80un](https://github.com/avwohl/80un) - Unpacker for the CP/M archive and compression formats LBR, ARC, squeeze, crunch, and CrLZH.
- [cpmdroid](https://github.com/avwohl/cpmdroid) - Z80/CP/M emulator for Android phones and tablets. It emulates the RomWBW HBIOS interface and a VT100 terminal.
- [cpmemu](https://github.com/avwohl/cpmemu) - Z80/CP/M emulator for Linux and Windows, with Z80 and 8080 CPU cores. It translates the BDOS and BIOS calls of CP/M 2.2 programs to the host file system.
- [ioscpm](https://github.com/avwohl/ioscpm) - Z80/CP/M emulator for iOS and macOS. It emulates the RomWBW HBIOS interface and runs CP/M 2.2 and CP/M 3.
- [learn-ada-z80](https://github.com/avwohl/learn-ada-z80) - Collection of more than 90 Ada example programs for uada80, the Ada compiler for the Z80 processor and CP/M.
- [mbasic](https://github.com/avwohl/mbasic) - Python interpreter for MBASIC 5.21, the Microsoft BASIC-80 for CP/M. Two compiler backends compile the programs to CP/M .COM files or to JavaScript.
- [mbasic2025](https://github.com/avwohl/mbasic2025) - Reconstruction of the lost source code of MBASIC 5.21, the Microsoft BASIC-80 for CP/M. The MACRO-80 source code assembles to a binary that matches mbasic.com byte for byte.
- [mbasicc](https://github.com/avwohl/mbasicc) - C++17 interpreter for MBASIC 5.21, the Microsoft BASIC-80 for CP/M. It runs on Linux and macOS.
- [mbasicc_web](https://github.com/avwohl/mbasicc_web) - Web browser interpreter for MBASIC 5.21, the Microsoft BASIC-80 for CP/M. Emscripten compiles the mbasicc interpreter to WebAssembly.
- [mpm2](https://github.com/avwohl/mpm2) - Z80 emulator for MP/M II, the multi-user CP/M operating system. Users connect over SSH, and SFTP clients transfer files.
- [romwbw_emu](https://github.com/avwohl/romwbw_emu) - Hardware-level Z80/CP/M emulator for Linux and macOS. It emulates the RomWBW HBIOS interface and switches banks in 512 KB of ROM and 512 KB of RAM.
- [scelbal](https://github.com/avwohl/scelbal) - Floating-point BASIC interpreter for the 8080 processor and CP/M. A translator converts the original 8008 source code to 8080 source code.
- [uada80](https://github.com/avwohl/uada80) - Ada compiler for the Z80 processor and CP/M 2.2. It compiles a subset of Ada 2012 to CP/M .COM files.
- [uc386](https://github.com/avwohl/uc386) - C23 compiler for the i386 processor and MS-DOS. It uses uc_core as its frontend.
- [uc80](https://github.com/avwohl/uc80) - C compiler for the Z80 processor and CP/M. It uses uc_core as its frontend.
- [ucow](https://github.com/avwohl/ucow) - Cowgol compiler for the Z80 processor and CP/M. It runs on Linux in Python.
- [um80_and_friends](https://github.com/avwohl/um80_and_friends) - Linux toolchain that is compatible with Microsoft MACRO-80. It has an assembler, a linker, a librarian, and a disassembler.
- [upeepz80](https://github.com/avwohl/upeepz80) - Peephole optimizer for Z80 compilers. It shortens jumps to jr, builds djnz loops, and removes dead stores.
- [uplm80](https://github.com/avwohl/uplm80) - PL/M-80 compiler for the Z80 processor and CP/M. It writes Intel 8080 and Zilog Z80 assembly language.
- [uplox](https://github.com/avwohl/uplox) - LR(1) and GLR parser generator. It writes the lexer and parser tables for the C23 frontend of uc_core from `examples/c23.uplox`.
- [z80cpmw](https://github.com/avwohl/z80cpmw) - Z80/CP/M emulator for Windows. It emulates the RomWBW HBIOS interface and boots CP/M from disk images.

## License

GPL-3.0-or-later. See `LICENSE`.
