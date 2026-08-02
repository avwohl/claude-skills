# uc386

C23 compiler targeting the Intel 386 (i386 / x86-32) processor under a
DOS extender — specifically the **flat 32-bit Watcom / DOS/4GW-era** C
that early-to-mid-1990s PC games were written in.

**Status: working — in testing ahead of a general release.** Measured
against two reference suites under our DOS emulator (compile →
assemble → run → diff): **215 / 220**
[c-testsuite](https://github.com/c-testsuite/c-testsuite) and, with
the `--kr` pre-pass (see below), **1397 / 1514**
[gcc-c-torture](https://github.com/llvm/llvm-test-suite) executable
tests passing. The frontend defaults to **strict C23**; the
gcc-c-torture corpus is pre-ANSI and GNU-heavy, so it is run with
`--kr` enabled. The remaining ~117 are GCC extensions that need a
static-chain ABI / closure conversion (nested functions, `__label__`),
a fragmented backlog of unimplemented codegen features (C99 VLA /
variably-modified types, vectors, designated initializers, `_Complex`,
offsetof designators, …), and a few large-frame / file-I/O edges —
tracked, not claimed as passing. The standard-C codegen-corner
miscompiles have been driven out (see `STANDARD_C_BACKLOG.md`).

**K&R / implicit-int compatibility (`--kr`).** Pre-ANSI sources —
implicit-`int` returns (`main() { … }`) and K&R old-style parameter
lists (`f(a, b) int a; char *b; { … }`) — are not valid C23 and the
strict grammar rejects them — as is the GNU **computed-goto /
labels-as-values** extension (`&&label`, `goto *expr`). Passing
`--kr` enables a source-level pre-pass (in
[uc_core](https://github.com/avwohl/uc_core)) that rewrites these
shapes into equivalent standard C before parsing (computed goto
lowers to a `switch` dispatch). It is **off by default and only
engages on files that fail the strict parse**, so modern code is
parsed exactly once and pays zero cost. Use it for legacy/pre-ANSI
or GNU-C codebases; the conformance runners enable it for the
K&R-heavy torture corpus.

The frontend (parsing, preprocessing, AST-level optimization) lives
in [uc_core](https://github.com/avwohl/uc_core); this repo owns the
driver, the x86-32 NASM emitter, and the DOS runtime bindings.

**Highlights** — beyond the reference suites, uc386 compiles real
third-party C programs into runnable DOS executables:

- **Real `.exe` output.** Produces self-contained, PMODE/W-bound DOS
  `.exe` files (not just flat binaries), boot-tested under DOSBox in
  CI: correct errorlevels, command-line argument parsing, and
  `printf`/file I/O through genuine DOS handles.
- **DOOM** (id Software's 1993 shooter) compiles and boots
  end-to-end, running through engine startup until it exits cleanly
  on the expected "WAD file not found".
- **MicroPython** (a small Python interpreter) compiles into a
  working DOS Python REPL — expressions, functions, classes, list
  comprehensions, exceptions, and the common builtins. Packaged
  separately as
  [freedos_micro_python](https://github.com/avwohl/freedos_micro_python).
  It is our toughest end-to-end test of the compiler.
- **awk** — Kernighan's "one true awk" runs arithmetic, regexes,
  aggregation, and string functions.
- **GNU utilities** — 16 in-tree coreutils-style programs (`cat`,
  `wc`, `true`, …) build and pass parametrized regression tests.

See `addons/STATUS.md` for the full per-addon report and
`docs/path-a-mz-le.md` for the `.exe` build path.

## Size — measured, not asserted

The "tiny output" claim, checked against the period reference
compiler instead of asserted. Every column below was **reproduced
on one macOS/arm64 host** by `python -m addons.harness.compare`
(Open Watcom V2 has no native macOS build, so its DOS-hosted
`wcc386`/`wlink` run under DOSBox-X via `addons/harness/
watcom_dosbox.py`; DJGPP is the gcc-12.2 osx cross under Rosetta).
Bytes of the on-disk executable; full table in
[`addons/results.md`](addons/results.md):

| program | uc386 .bin | uc386 .exe | Watcom | DJGPP |
|---------|-----------:|-----------:|-------:|------:|
| true    |         18 |     16,907 |  5,420 | 147,914 |
| echo    |        148 |     16,915 | 11,286 | 150,212 |
| factor  |      1,858 |     16,989 | 20,538 | 179,614 |
| wc      |      1,529 |     16,928 | 20,158 | 179,092 |

Reading this honestly:

- **`.bin` is not a DOS program.** It has no MZ header and runs
  only under `uc386.dos_emu`/a custom loader. It is the right
  metric for *codegen+DCE tightness* (and there uc386 is in a
  class of its own — tens of bytes), but it is not what you ship.
- **`.exe` is what you ship**, and it carries a ~17 KB PMODE/W
  extender floor. Against that real-DOS artifact, **Open Watcom
  is ~2–3× smaller on tiny programs** (its DOS/4GW clib + mature
  linker beat our extender floor); the two converge as real code
  grows. uc386 beats **DJGPP ~9×** and host **gcc ~2×**.
- So: uc386's *code generation* is extremely compact; its current
  *DOS packaging* (PMODE/W) is not yet competitive with Watcom's
  on small binaries. Both statements are true and the table shows
  which is which — no single "390× smaller" headline.

## Goal

Compile representative public-source DOS games **unmodified**:

- Descent (Parallax, 1995 — Watcom)
- Duke Nukem 3D / Build engine (3D Realms, 1996 — Watcom)
- Rise of the Triad (Apogee, 1994 — Watcom)
- Heretic / Hexen (Raven, 1994–95 — Watcom)

These all share one compiler (Watcom C/C++) and one memory model
(flat 32-bit under DOS/4GW). That's the target.

**Non-goals:** 16-bit real-mode with near/far/huge memory models
(Wolf3D-era code). uc386 will *parse* the 16-bit keywords so that
shared period headers don't choke, but won't honor their semantics —
all pointers are 32-bit flat.

## Design

The uc80/uc386 family shares a single C23 frontend
([uc_core](https://github.com/avwohl/uc_core), itself uplox-driven).
This project contributes only:

- `main.py` — driver (CLI, I/O, embedding, post-processing)
- `codegen.py` — x86-32 NASM code generator
- `peephole.py` — NASM-text peephole optimizer
- `asm_dce.py` — assembly-level dead-code elimination from `_start` / `_main`
- `libc_split.py` — selective inclusion of `lib/i386_dos_libc.asm` symbols
- `runtime.py` — MS-DOS runtime library bindings (INT 21h wrappers, stubs)
- `dos_emu.py` — i386 emulator harness for testing flat-binary output
- `dos_emu_netsim.py` — simulated network for the INT 0x83 packet-driver shim

Every front-end improvement (new C23 feature, AST optimization, DOS-era
syntax tolerance) lands in uc_core and benefits both targets
automatically.

## Install

> **Note:** not yet ready on PyPI — install from the GitHub repository for now.

From PyPI:

```
pip install uc386
```

That gets you the `uc386` driver, the bundled `i386_dos_libc.asm`,
and the `lib/include/` headers. To assemble + run the output you
also need `nasm` (system package) and, for the `dos_emu` test
harness, `pip install unicorn`.

Source checkout for development:

```
sudo apt-get install -y python3 python3-venv nasm    # Debian/Ubuntu
python3 -m venv .venv && . .venv/bin/activate
pip install pytest unicorn "uc_core @ git+https://github.com/avwohl/uc_core@main" -e .
pytest tests/
```

macOS (Homebrew) and Fedora/RHEL (dnf) instructions, plus the
optional toolchains for addon builds (bison/flex) and the
DJGPP / OpenWatcom comparison columns, are documented in
[`docs/INSTALL.md`](docs/INSTALL.md).

## Related Projects

- [cpmdroid](https://github.com/avwohl/cpmdroid) - Z80/CP/M emulator for Android phones and tablets. It emulates the RomWBW HBIOS interface and a VT100 terminal.
- [cpmemu](https://github.com/avwohl/cpmemu) - Z80/CP/M emulator for Linux and Windows, with Z80 and 8080 CPU cores. It translates the BDOS and BIOS calls of CP/M 2.2 programs to the host file system.
- [dosemu](https://github.com/avwohl/dosiz) - MS-DOS emulator for Linux. It uses the dosbox-staging CPU core and translates system calls in the manner of cpmemu. It is the intended test host for uc386.
- [qxDOS](https://github.com/avwohl/qxDOS) - DOS emulator app for iOS and macOS with a SwiftUI interface. DOSBox Staging supplies the emulated i386 hardware.
- [uc80](https://github.com/avwohl/uc80) - C compiler for the Z80 processor and CP/M. This sibling backend shares the C23 frontend of uc_core.
- [uc_core](https://github.com/avwohl/uc_core) - Shared C23 frontend and AST optimizer for the uc80 and uc386 compilers.
- [um80_and_friends](https://github.com/avwohl/um80_and_friends) - Linux toolchain that is compatible with Microsoft MACRO-80. It has an assembler, a linker, a librarian, and a disassembler. It is the Z80 equivalent of what uc386 needs for i386.
- [upeepz80](https://github.com/avwohl/upeepz80) - Peephole optimizer for Z80 compilers. It is the template for a future upeep386.
- [uplox](https://github.com/avwohl/uplox) - LR(1) and GLR parser generator. It writes the lexer and parser tables for the C23 frontend of uc_core from `examples/c23.uplox`.

## License

GPL-3.0-or-later.
