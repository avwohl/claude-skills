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
- [uc386](https://github.com/avwohl/uc386) - C23 compiler targeting Intel 386 (x86-32) and MS-DOS; consumer of uc_core
- [uc80](https://github.com/avwohl/uc80) - C23 compiler targeting Z80 processor and CP/M operating system; consumer of uc_core
- [ucow](https://github.com/avwohl/ucow) - Unix/Linux Cowgol to Z80 compiler
- [um80_and_friends](https://github.com/avwohl/um80_and_friends) - Microsoft MACRO-80 compatible toolchain for Linux: assembler, linker, librarian, disassembler
- [upeepz80](https://github.com/avwohl/upeepz80) - Z80 peephole optimizer
- [uplm80](https://github.com/avwohl/uplm80) - PL/M-80 compiler targeting Intel 8080 and Zilog Z80 assembly language
- [uplox](https://github.com/avwohl/uplox) - Parser/lexer-table generator that produces uc_core's C23 frontend (from `examples/c23.uplox`)
- [z80cpmw](https://github.com/avwohl/z80cpmw) - Z80 CP/M emulator for Windows (RomWBW)

## License

GPL-3.0-or-later. See `LICENSE`.
