# Related Projects — before / after

Every README in the account that carries a **Related Projects** list, before and after the
entries were rewritten in Simplified Technical English.

Produced with [`skills/simplified-technical-english.md`](../../../skills/simplified-technical-english.md).

## What changed

- **32 repositories**, **420 list entries**
- Those 420 entries reduce to **56 distinct texts** — 19 were the same line
  copy-pasted into 6 or more READMEs, and 28 were one-off entries hand-written for a
  single README.
- In every repository, **only the Related Projects section changed.** This is verified
  mechanically: the file with that section excised is byte-identical before and after.

## Why this was not a regeneration

These lists look machine-generated, and an earlier assumption in this work was that a
generator produced them from the GitHub repo description fields. **That was wrong.**
Checking 151 entries against the descriptions found only 46 percent matched. The other
54 percent had been hand-edited — correcting `mbasic` to `MBASIC`, dropping a stale
parenthetical, or adding a relationship the description does not carry, such as
*sibling backend sharing the uc_core frontend*.

No generator exists in any repository, and no `BEGIN/END GENERATED` markers are present.
So this pass re-authored the entries deliberately rather than regenerating them, and the
hand-written context had to survive the rewrite. Every number, file name, test result and
inline code span in an original was checked against its replacement.

## Repositories

| Repository | Entries | Before | After |
|---|---:|---|---|
| `uc80` | 21 | [before](uc80/before.md) | [after](uc80/after.md) |
| `uc_core` | 21 | [before](uc_core/before.md) | [after](uc_core/after.md) |
| `uplm80` | 19 | [before](uplm80/before.md) | [after](uplm80/after.md) |
| `80un` | 18 | [before](80un/before.md) | [after](80un/after.md) |
| `cpmdroid` | 18 | [before](cpmdroid/before.md) | [after](cpmdroid/after.md) |
| `cpmemu` | 18 | [before](cpmemu/before.md) | [after](cpmemu/after.md) |
| `ioscpm` | 18 | [before](ioscpm/before.md) | [after](ioscpm/after.md) |
| `learn-ada-z80` | 18 | [before](learn-ada-z80/before.md) | [after](learn-ada-z80/after.md) |
| `mbasic` | 18 | [before](mbasic/before.md) | [after](mbasic/after.md) |
| `mbasic2025` | 18 | [before](mbasic2025/before.md) | [after](mbasic2025/after.md) |
| `mbasicc` | 18 | [before](mbasicc/before.md) | [after](mbasicc/after.md) |
| `mbasicc_web` | 18 | [before](mbasicc_web/before.md) | [after](mbasicc_web/after.md) |
| `mpm2` | 18 | [before](mpm2/before.md) | [after](mpm2/after.md) |
| `romwbw_emu` | 18 | [before](romwbw_emu/before.md) | [after](romwbw_emu/after.md) |
| `scelbal` | 18 | [before](scelbal/before.md) | [after](scelbal/after.md) |
| `uada80` | 18 | [before](uada80/before.md) | [after](uada80/after.md) |
| `ucow` | 18 | [before](ucow/before.md) | [after](ucow/after.md) |
| `um80_and_friends` | 18 | [before](um80_and_friends/before.md) | [after](um80_and_friends/after.md) |
| `upeepz80` | 18 | [before](upeepz80/before.md) | [after](upeepz80/after.md) |
| `z80cpmw` | 18 | [before](z80cpmw/before.md) | [after](z80cpmw/after.md) |
| `uc386` | 9 | [before](uc386/before.md) | [after](uc386/after.md) |
| `iospharo` | 5 | [before](iospharo/before.md) | [after](iospharo/after.md) |
| `pharo-headless-test` | 5 | [before](pharo-headless-test/before.md) | [after](pharo-headless-test/after.md) |
| `soogle` | 5 | [before](soogle/before.md) | [after](soogle/after.md) |
| `validate_smalltalk_image` | 5 | [before](validate_smalltalk_image/before.md) | [after](validate_smalltalk_image/after.md) |
| `claude-skills` | 4 | [before](claude-skills/before.md) | [after](claude-skills/after.md) |
| `freedos_micro_python` | 4 | [before](freedos_micro_python/before.md) | [after](freedos_micro_python/after.md) |
| `smalltalk80-2026` | 4 | [before](smalltalk80-2026/before.md) | [after](smalltalk80-2026/after.md) |
| `uplox` | 4 | [before](uplox/before.md) | [after](uplox/after.md) |
| `freedos_git` | 3 | [before](freedos_git/before.md) | [after](freedos_git/after.md) |
| `hearzork` | 3 | [before](hearzork/before.md) | [after](hearzork/after.md) |
| `dosiz` | 2 | [before](dosiz/before.md) | [after](dosiz/after.md) |

## The 56 distinct texts

Sorted by how many READMEs each appeared in.

### Copy-paste entries

**`cpmdroid`** — appears in 20 READMEs

> **before:** Z80/CP/M emulator for Android with RomWBW HBIOS compatibility and VT100 terminal
>
> **after:** Z80/CP/M emulator for Android phones and tablets. It emulates the RomWBW HBIOS interface and a VT100 terminal.

**`cpmemu`** — appears in 20 READMEs

> **before:** CP/M 2.2 emulator with Z80/8080 CPU emulation and BDOS/BIOS translation to Unix filesystem
>
> **after:** Z80/CP/M emulator for Linux and Windows, with Z80 and 8080 CPU cores. It translates the BDOS and BIOS calls of CP/M 2.2 programs to the host file system.

**`80un`** — appears in 19 READMEs

> **before:** Unpacker for CP/M compression and archive formats (LBR, ARC, squeeze, crunch, CrLZH)
>
> **after:** Unpacker for the CP/M archive and compression formats LBR, ARC, squeeze, crunch, and CrLZH.

**`ioscpm`** — appears in 19 READMEs

> **before:** Z80/CP/M emulator for iOS and macOS with RomWBW HBIOS compatibility
>
> **after:** Z80/CP/M emulator for iOS and macOS. It emulates the RomWBW HBIOS interface and runs CP/M 2.2 and CP/M 3.

**`learn-ada-z80`** — appears in 19 READMEs

> **before:** Ada programming examples for the uada80 compiler targeting Z80/CP/M
>
> **after:** Collection of more than 90 Ada example programs for uada80, the Ada compiler for the Z80 processor and CP/M.

**`mbasic`** — appears in 19 READMEs

> **before:** Modern MBASIC 5.21 Interpreter & Compilers
>
> **after:** Python interpreter for MBASIC 5.21, the Microsoft BASIC-80 for CP/M. Two compiler backends compile the programs to CP/M .COM files or to JavaScript.

**`mbasic2025`** — appears in 19 READMEs

> **before:** MBASIC 5.21 source code reconstruction - byte-for-byte match with original binary
>
> **after:** Reconstruction of the lost source code of MBASIC 5.21, the Microsoft BASIC-80 for CP/M. The MACRO-80 source code assembles to a binary that matches mbasic.com byte for byte.

**`mbasicc`** — appears in 19 READMEs

> **before:** C++ implementation of MBASIC 5.21
>
> **after:** C++17 interpreter for MBASIC 5.21, the Microsoft BASIC-80 for CP/M. It runs on Linux and macOS.

**`mbasicc_web`** — appears in 19 READMEs

> **before:** WebAssembly MBASIC 5.21
>
> **after:** Web browser interpreter for MBASIC 5.21, the Microsoft BASIC-80 for CP/M. Emscripten compiles the mbasicc interpreter to WebAssembly.

**`mpm2`** — appears in 19 READMEs

> **before:** MP/M II multi-user CP/M emulator with SSH terminal access and SFTP file transfer
>
> **after:** Z80 emulator for MP/M II, the multi-user CP/M operating system. Users connect over SSH, and SFTP clients transfer files.

**`romwbw_emu`** — appears in 19 READMEs

> **before:** Hardware-level Z80 emulator for RomWBW with 512KB ROM + 512KB RAM banking and HBIOS support
>
> **after:** Hardware-level Z80/CP/M emulator for Linux and macOS. It emulates the RomWBW HBIOS interface and switches banks in 512 KB of ROM and 512 KB of RAM.

**`scelbal`** — appears in 19 READMEs

> **before:** SCELBAL BASIC interpreter - 8008 to 8080 translation
>
> **after:** Floating-point BASIC interpreter for the 8080 processor and CP/M. A translator converts the original 8008 source code to 8080 source code.

**`uada80`** — appears in 19 READMEs

> **before:** Ada compiler targeting Z80 processor and CP/M 2.2 operating system
>
> **after:** Ada compiler for the Z80 processor and CP/M 2.2. It compiles a subset of Ada 2012 to CP/M .COM files.

**`ucow`** — appears in 19 READMEs

> **before:** Unix/Linux Cowgol to Z80 compiler
>
> **after:** Cowgol compiler for the Z80 processor and CP/M. It runs on Linux in Python.

**`um80_and_friends`** — appears in 19 READMEs

> **before:** Microsoft MACRO-80 compatible toolchain for Linux: assembler, linker, librarian, disassembler
>
> **after:** Linux toolchain that is compatible with Microsoft MACRO-80. It has an assembler, a linker, a librarian, and a disassembler.

**`uplm80`** — appears in 19 READMEs

> **before:** PL/M-80 compiler targeting Intel 8080 and Zilog Z80 assembly language
>
> **after:** PL/M-80 compiler for the Z80 processor and CP/M. It writes Intel 8080 and Zilog Z80 assembly language.

**`z80cpmw`** — appears in 19 READMEs

> **before:** Z80 CP/M emulator for Windows (RomWBW)
>
> **after:** Z80/CP/M emulator for Windows. It emulates the RomWBW HBIOS interface and boots CP/M from disk images.

**`uc80`** — appears in 18 READMEs

> **before:** ANSI C compiler targeting Z80 processor and CP/M 2.2 operating system
>
> **after:** C compiler for the Z80 processor and CP/M. It optimizes for small code size.

**`upeepz80`** — appears in 17 READMEs

> **before:** Universal peephole optimizer for Z80 compilers
>
> **after:** Peephole optimizer for Z80 compilers that write lowercase Z80 assembly language. It shortens jumps to jr, builds djnz loops, and removes dead stores.

**`iospharo`** — appears in 5 READMEs

> **before:** Pharo Smalltalk VM for iOS and Mac Catalyst (interpreter-only, low-bit oop encoding for ASLR compatibility).
>
> **after:** Virtual machine for Pharo Smalltalk on iOS and macOS. The C++ interpreter runs Pharo 13 and Pharo 14 images without a just-in-time compiler, and it uses low-bit oop encoding to work with ASLR.

**`soogle`** — appears in 5 READMEs

> **before:** Smalltalk code search engine that indexes packages across Pharo, Squeak, GemStone and more.
>
> **after:** Search engine for Smalltalk source code. It indexes packages and labels each one with its dialect, such as Pharo, Squeak, or GemStone.

**`validate_smalltalk_image`** — appears in 5 READMEs

> **before:** Standalone validator and export tool for Spur-format Smalltalk image files (heap integrity, SHA-256 manifests, reference graphs).
>
> **after:** Standalone validator and export tool for Spur-format Smalltalk images. It checks the heap, and it writes SHA-256 manifests and reference graphs.

**`claude-skills`** — appears in 4 READMEs

> **before:** Open source skills for Claude Code: reusable knowledge and algorithms packaged as `.claude/skills/` markdown files.
>
> **after:** Collection of open source skills for Claude Code. Each skill is a Markdown file in `.claude/skills/` that holds reusable knowledge and algorithms.

**`pharo-headless-test`** — appears in 4 READMEs

> **before:** Headless Pharo test runner with a fake GUI; clicks menus, takes screenshots, runs SUnit without a display.
>
> **after:** Headless test runner for Pharo Smalltalk with a fake GUI. It clicks menus, takes screenshots, and runs the SUnit suite without a display.

**`smalltalk80-2026`** — appears in 4 READMEs

> **before:** Smalltalk-80 VM implementation of the 1983 Blue Book Xerox virtual image, targeting macOS / Mac Catalyst, iOS, Windows, and Linux.
>
> **after:** C++17 virtual machine for Smalltalk-80 on macOS, Mac Catalyst, Linux, and Windows. It boots the 1983 Xerox virtual image to the desktop.

**`uplox`** — appears in 3 READMEs

> **before:** Parser/lexer-table generator that produces uc_core's C23 frontend (from `examples/c23.uplox`)
>
> **after:** LR(1) and GLR parser generator. It writes the lexer and parser tables for the C23 frontend of uc_core from `examples/c23.uplox`.

**`uc_core`** — appears in 2 READMEs

> **before:** Shared C23 frontend and AST optimizer used by uc80 and uc386
>
> **after:** Shared C23 frontend and AST optimizer for the uc80 and uc386 compilers.

**`upeepz80`** — appears in 2 READMEs

> **before:** Z80 peephole optimizer
>
> **after:** Peephole optimizer for Z80 compilers. It shortens jumps to jr, builds djnz loops, and removes dead stores.

### Context-carrying entries

Each of these was written for one README and states a relationship the generic entry does
not. The `kept` line records what had to survive.

**`FreeDOS`** — in `freedos_micro_python`

> **before:** the target OS.
>
> **after:** The target operating system. This port runs on FreeDOS on i386.

> 
> *kept:* count 1, hand-written for freedos_micro_python. The "target operating system" relationship survives, the abbreviation is expanded, and the shared target phrase "FreeDOS on i386" is used

**`MicroPython`** — in `freedos_micro_python`

> **before:** upstream.
>
> **after:** The upstream project. This repository is its port for FreeDOS on i386.

> 
> *kept:* count 1, in freedos_micro_python only. The upstream relationship survives and the port target is named as FreeDOS on i386

**`cpmemu`** — in `dosiz`

> **before:** CP/M 2.2 emulator; the translation-layer template and the origin of the `.cfg` format
>
> **after:** Z80/CP/M emulator that translates the BDOS and BIOS calls of CP/M 2.2 programs to the host file system. It is the template for the translation layer and the origin of the `.cfg` format.

> 
> *kept:* count 1, hand-written for dosiz. The template for the translation layer, the origin of the `.cfg` format (code span kept), and the CP/M 2.2 version number all survive. The semicolon is gone, and "CP/M 2.2 emulator" becomes the glossary head noun with the BDOS and BIOS translation that makes it the template

**`dosemu`** — in `uc386`

> **before:** MS-DOS emulator for Linux: dosbox-staging CPU + cpmemu-style syscall translation (intended test host for uc386)
>
> **after:** MS-DOS emulator for Linux. It uses the dosbox-staging CPU core and translates system calls in the manner of cpmemu. It is the intended test host for uc386.

> 
> *kept:* count 1, hand-written for uc386. The dosbox-staging CPU core, the cpmemu-style system call translation, and the intended test host relationship to uc386 all survive

**`freedos_micro_python`** — in `freedos_git`

> **before:** sibling port; source of the toolchain pattern and the DOS networking/TLS stack.
>
> **after:** Sibling MicroPython port for FreeDOS on i386. It is the source of the toolchain pattern and of the network and TLS stack.

> 
> *kept:* count 1, hand-written for freedos_git. The sibling port role, the source of the toolchain pattern, and the source of the network and TLS stack all survive. The semicolon is gone and "DOS" becomes the shared target phrase FreeDOS on i386

**`git`** — in `freedos_git`

> **before:** upstream (vendored, pinned).
>
> **after:** The upstream project. This port includes a copy of its source code and pins it to one version.

> 
> *kept:* count 1, hand-written for freedos_git. git is the upstream project, and freedos_git carries it vendored and pinned. The two parenthetical adjectives become active verbs with the named agent "This port"

**`pharo-headless-test`** — in `iospharo`

> **before:** Headless Pharo test runner with a fake GUI; clicks menus, takes screenshots, runs SUnit without a display. Extracted from this project; included here as a submodule at `scripts/pharo-headless-test/`.
>
> **after:** Headless test runner for Pharo Smalltalk with a fake GUI. It clicks menus, takes screenshots, and runs the SUnit suite without a display. This project extracted it and includes it as a submodule at `scripts/pharo-headless-test/`.

> 
> *kept:* count 1, hand-written for iospharo. The fake GUI, the three actions, SUnit, the provenance (extracted from this project), and the submodule path `scripts/pharo-headless-test/` all survive. Both semicolons are gone and "Pharo" becomes the head term "Pharo Smalltalk". Over 200 characters because the provenance and the submodule path are unique context

**`qxDOS`** — in `dosiz`

> **before:** iOS/Mac DOS emulator; source of the vendored emu88 CPU core
>
> **after:** DOS emulator app for iOS and macOS. It supplies the emu88 CPU core that dosiz includes.

> 
> *kept:* count 1, in dosiz only. The load-bearing relationship "source of the vendored emu88 CPU core" and the emu88 name survive

**`qxDOS`** — in `uc386`

> **before:** DOS emulator for iPad and Mac — DOSBox-based with SwiftUI interface
>
> **after:** DOS emulator app for iOS and macOS with a SwiftUI interface. DOSBox Staging supplies the emulated i386 hardware.

> 
> *kept:* count 1, hand-written for uc386. The DOSBox basis (named as DOSBox Staging, with the active verb "supplies") and the SwiftUI interface survive. Devices are renamed by operating system, so iPad and Mac become iOS and macOS. "DOS" is kept because qxDOS boots three DOS versions

**`uada80`** — in `uplox`

> **before:** Ada 2012 → Z80 / CP/M 2.2 (+ MP/M II `.prl`). Consumes `ada_full.uplox`. 100% on ACATS A/C/D/E/L (2846/2846) and 97.8% on the GNAT runtime (1072/1096); see [WIP.md](WIP.md) for the corpus-by-corpus numbers.
>
> **after:** Ada compiler for the Z80 processor and CP/M 2.2. It compiles a subset of Ada 2012, writes MP/M II `.prl` files, and reads `ada_full.uplox`. It scores 100 percent on ACATS A/C/D/E/L (2846/2846) and 97.8 percent on the GNAT run time (1072/1096). [WIP.md](WIP.md) gives the numbers for each corpus.

> 
> *kept:* count 1, in uplox only. Ada 2012, CP/M 2.2, MP/M II `.prl`, the `ada_full.uplox` input, 100 percent on ACATS A/C/D/E/L (2846/2846), 97.8 percent on the GNAT run time (1072/1096), and the [WIP.md](WIP.md) link all survive

**`uc386`** — in `freedos_git`

> **before:** the C23 compiler + the `dos_emu` test harness.
>
> **after:** C23 compiler for the i386 processor and MS-DOS. It hosts the `dos_emu` test harness.

> 
> *kept:* count 1, hand-written for freedos_git. The `dos_emu` test harness code span and the C23 compiler role survive

**`uc386`** — in `freedos_micro_python`

> **before:** the C23 compiler that builds this port. Hosts the `dos_emu` test harness.
>
> **after:** C23 compiler for the i386 processor and MS-DOS. It builds this port and hosts the `dos_emu` test harness.

> 
> *kept:* count 1, hand-written for freedos_micro_python. uc386 builds the port and hosts the `dos_emu` test harness. The code span is unchanged

**`uc386`** — in `uc80`

> **before:** C23 compiler targeting Intel 386 (x86-32) and MS-DOS; sibling backend sharing the uc_core frontend
>
> **after:** C23 compiler for the i386 processor and MS-DOS. This sibling backend shares the uc_core frontend.

> 
> *kept:* count 1, hand-written for uc80. The sibling backend relationship and the shared uc_core frontend survive, and "Intel 386 (x86-32)" becomes the glossary term i386. The two gerunds and the semicolon are gone

**`uc386`** — in `uc_core`

> **before:** C23 compiler targeting Intel 386 (x86-32) and MS-DOS; consumer of uc_core
>
> **after:** C23 compiler for the i386 processor and MS-DOS. It uses uc_core as its frontend.

> 
> *kept:* count 1, in uc_core only. "Consumer of uc_core" becomes an active clause, and C23, i386, and MS-DOS survive

**`uc386`** — in `uplox`

> **before:** C23 → i386 / MS-DOS. 100% on `gcc-c-torture` (1514 tests) and `c-testsuite` (220 tests); produces real DOS `.exe` files via NASM + PMODE/W.
>
> **after:** C23 compiler for the i386 processor and MS-DOS. It scores 100 percent on `gcc-c-torture` (1514 tests) and `c-testsuite` (220 tests), and it writes real DOS `.exe` files with NASM and PMODE/W.

> 
> *kept:* count 1, in uplox only. Both test results with exact counts (100 percent on `gcc-c-torture`, 1514 tests, `c-testsuite`, 220 tests), the real DOS `.exe` file output, and the NASM and PMODE/W toolchain all survive. "via" becomes "with", the semicolon and the arrow are gone, and "produces" becomes the glossary verb "writes"

**`uc80`** — in `uc386`

> **before:** C23 compiler targeting Z80 processor and CP/M; sibling backend sharing the uc_core frontend
>
> **after:** C compiler for the Z80 processor and CP/M. This sibling backend shares the C23 frontend of uc_core.

> 
> *kept:* count 1, hand-written for uc386. The sibling backend relationship, the shared uc_core frontend, and the C23 fact from the original all survive. The head noun follows the verified uc80 description

**`uc80`** — in `uc_core`

> **before:** C23 compiler targeting Z80 processor and CP/M operating system; consumer of uc_core
>
> **after:** C compiler for the Z80 processor and CP/M. It uses uc_core as its frontend.

> 
> *kept:* count 1, in uc_core only. The consumer of uc_core relationship survives as an active clause, and it is exactly parallel with the uc386 entry in the same list

**`uc80`** — in `uplox`

> **before:** C23 → Z80 / CP/M.
>
> **after:** C compiler for the Z80 processor and CP/M. It is the Z80 backend on this C23 frontend.

> 
> *kept:* count 1, in uplox only, nested under the uc_core entry. The Z80 and CP/M target and the C23 fact survive, and the "targets that ride on top" relationship becomes "the Z80 backend on this C23 frontend"

**`uc_core`** — in `freedos_micro_python`

> **before:** shared C23 frontend used by uc386 (and the Z80 sibling, uc80).
>
> **after:** Shared C23 frontend and AST optimizer that the uc386 compiler and its Z80 sibling uc80 both use.

> 
> *kept:* count 1, hand-written for freedos_micro_python. Both consumers uc386 and uc80 and the Z80 sibling relationship survive, the passive "used by" becomes an active clause, and the verified AST optimizer role is added

**`uc_core`** — in `uplox`

> **before:** shared C23 frontend and AST-level optimizer. Consumes `c23.uplox`. The backend protocol is target-agnostic; the targets that ride on top are:
>
> **after:** Shared C23 frontend and AST optimizer. It reads `c23.uplox`. The backend protocol is independent of the target, and these targets use it:

> 
> *kept:* count 1, in uplox only. The `c23.uplox` code span, the target-independent backend protocol, and the trailing colon that introduces the nested target list all survive

**`ucow`** — in `uplox`

> **before:** Cowgol → Z80 / CP/M. Consumes `cowgol.uplox` via an emitted-Python parser module (`uplox_cowgol.py`).
>
> **after:** Cowgol compiler for the Z80 processor and CP/M. It reads `cowgol.uplox` through the Python parser module `uplox_cowgol.py` that uplox writes.

> 
> *kept:* count 1, in uplox only. The full uplox relationship survives: it consumes `cowgol.uplox` through the Python parser module `uplox_cowgol.py` that uplox writes. Both code spans are unchanged, "via" becomes "through", and "emitted" becomes the glossary verb "writes"

**`um80_and_friends`** — in `uc386`

> **before:** Microsoft MACRO-80 compatible toolchain for Linux: assembler, linker, librarian, disassembler (the Z80 analogue of what uc386 needs for i386)
>
> **after:** Linux toolchain that is compatible with Microsoft MACRO-80. It has an assembler, a linker, a librarian, and a disassembler. It is the Z80 equivalent of what uc386 needs for i386.

> 
> *kept:* count 1, hand-written for uc386. The four tools (assembler, linker, librarian, disassembler) and the relationship as the Z80 equivalent of what uc386 needs for i386 all survive

**`upeepz80`** — in `uc386`

> **before:** Z80 peephole optimizer (template for an eventual upeep386)
>
> **after:** Peephole optimizer for Z80 compilers. It is the template for a future upeep386.

> 
> *kept:* count 1, hand-written for uc386. The template for upeep386 relationship and the exact name upeep386 survive

**`uplm80`** — in `uplox`

> **before:** PL/M-80 → Z80 / 8080. Consumes `plm_pre.uplox` (the LITERALLY / `$`-directive preprocessor) followed by `plm_full.uplox`. Can rebuild original CP/M utilities (BDOS etc.) from their PL/M source.
>
> **after:** PL/M-80 compiler for the Z80 processor and CP/M. It writes 8080 and Z80 assembly language. It reads `plm_pre.uplox`, the preprocessor for LITERALLY and the `$` directives, and then `plm_full.uplox`. It rebuilds original CP/M utilities such as the BDOS from their PL/M-80 source code.

> 
> *kept:* count 1, in uplox only. It consumes `plm_pre.uplox` (the LITERALLY and `$` directive preprocessor) and then `plm_full.uplox`, writes Z80 and 8080 output, and rebuilds original CP/M utilities such as the BDOS from PL/M-80 source code. "etc." becomes "such as" and "PL/M source" becomes "PL/M-80 source code". Over 200 characters because the entry carries two file names and a unique toolchain

**`uplox`** — in `uplm80`

> **before:** Compiler front-end generator (lexer DFA + LR parser + typed auto-AST) that uplm80 uses for PL/M-80 parsing
>
> **after:** LR(1) and GLR parser generator. It writes a lexer DFA, an LR parser, and a typed automatic AST, and uplm80 uses it to parse PL/M-80.

> 
> *kept:* count 1, hand-written for uplm80. The lexer DFA, the LR parser, the typed AST, and the relationship "uplm80 uses it to parse PL/M-80" all survive. Under rule 8 the verified description head noun "LR(1) and GLR parser generator" replaces "compiler front-end generator", the "+" list becomes a written list with articles, and the "parsing" gerund becomes "to parse"

**`z2js`** — in `hearzork`

> **before:** Z-machine to JavaScript compiler
>
> **after:** Python compiler for interactive fiction. It compiles Z-machine story files to JavaScript, and it supports versions 1 through 8.

> 
> *kept:* count 1, in hearzork only. The Z-machine to JavaScript compile path survives, with the glossary range form "versions 1 through 8" from the description

**`zorkie`** — in `hearzork`

> **before:** ZIL/ZILF compiler producing Z-machine story files
>
> **after:** Python compiler for the Infocom ZIL language and the ZILF dialect. It writes Z-machine story files.

> 
> *kept:* count 1, in hearzork only. ZIL and ZILF as the input languages and Z-machine story files as the output survive. The "producing" gerund becomes the glossary verb "writes", and Z-machine takes the lowercase m

**`zwalker`** — in `hearzork`

> **before:** Z-machine test runner and game walker
>
> **after:** Walkthrough generator and test runner for Z-machine interactive fiction. It has a CZECH-compliant interpreter, an AI solver, and a replay harness.

> 
> *kept:* count 1, in hearzork only. Both roles survive: "game walker" becomes walkthrough generator and the test runner is kept, with the three verified parts from the description

## Facts the consistency pass restored

- CP/M 2.2 restored to both cpmemu entries. Both agent rewrites had dropped the version number while replacing the banned head noun "CP/M 2.2 emulator". The glossary bans that head noun, not the fact. Both entries now read "the BDOS and BIOS calls of CP/M 2.2 programs", which also sets up the contrast with the ioscpm entry (CP/M 2.2 and CP/M 3) in the same list.
- C23 restored to the three uc80 entries whose originals stated it, after the head noun was corrected to "C compiler" under rule 8. It survives as "the C23 frontend of uc_core" (uc386 README) and "the Z80 backend on this C23 frontend" (uplox README). The uc_core README entry does not repeat it because uc_core is described as the C23 frontend in the same README.
- "removes dead stores" restored to the 17-README upeepz80 entry, which had listed only two of the three verified actions while its 2-README twin listed three.
- Full script check of all 56 pairs: every inline code span in an original appears unchanged in its rewrite (`.cfg`, `dos_emu`, `c23.uplox`, `cowgol.uplox`, `uplox_cowgol.py`, `ada_full.uplox`, `plm_pre.uplox`, `plm_full.uplox`, `$`, `.prl`, `.exe`, `gcc-c-torture`, `c-testsuite`, `examples/c23.uplox`, `.claude/skills/`, `scripts/pharo-headless-test/`, [WIP.md](WIP.md)). Every number survives except three deliberate cases listed under flags.
- All hand-written relationships from the count-1 entries verified present: sibling backend and shared uc_core frontend, consumer of uc_core, source of the vendored emu88 CPU core, translation-layer template and origin of the .cfg format, intended test host for uc386, template for an eventual upeep386, Z80 analogue of what uc386 needs for i386, extracted from this project and included as a submodule, upstream and vendored and pinned, the target operating system, builds this port, and the trailing colon that introduces uplox's nested target list.

## Open judgment calls

- Three entries exceed 200 characters, all count-1 and all carrying unique technical context: uada80 in uplox (295 chars, two test corpora with four numbers, two file names, and the WIP.md link), uplm80 in uplox (283 chars, two .uplox file names, the LITERALLY and $ directive preprocessor, and the CP/M utility rebuild), pharo-headless-test in iospharo (229 chars, provenance plus submodule path). Nothing can be cut from any of them without deleting a fact.
- uc80 rule 8 call, please confirm. The verified description is "A C compiler for the Z80 processor and CP/M", so "ANSI" and "CP/M 2.2" from the 18-README original are dropped and the head is "C compiler" in all four entries. If you would rather claim C23 in the head, change all four together, since three of the four originals said C23 and uc_core is verified as "a shared C23 frontend ... for the uc80 and uc386 compilers".
- smalltalk80-2026 drops iOS and Mac Catalyst. The original claimed macOS, Mac Catalyst, iOS, Windows, and Linux; the verified description lists only macOS, Linux, and Windows. Rule 8 applied.
- cpmemu drops "Unix filesystem" in favor of the host file system on Linux and Windows, per the verified description. ucow drops "Unix" from "Unix/Linux" for the same reason.
- Platform renamings mandated by the glossary: qxDOS "iPad and Mac" becomes iOS and macOS, iospharo "Mac Catalyst" becomes macOS, uc386 "Intel 386 (x86-32)" becomes i386. The literal token x86-32 is therefore gone from two entries.
- Spelling split that the glossary does not cover: the dosemu entry keeps lowercase "dosbox-staging" (the upstream repository name, as its original wrote it) while the two qxDOS entries use "DOSBox Staging" (as the verified qxDOS description writes it). Say the word if you want one spelling in both places.
- The literal word "Consumes" no longer appears anywhere. It is now "reads" in the four uplox-family entries. The relationship and every file name are intact, but flagging it in case you want the original verb kept.
- Clean on all mechanical checks, script-verified over all 56: no semicolons, no "via", no e.g. / i.e. / etc. / vs., no contractions, no gerund heads, no entry beginning with its own target name, no percent signs. The only -ing words present are the approved fixed terms (operating system, floating-point, just-in-time) and the adjective "Sibling".
- uc80 in the uplox README says "this C23 frontend" because it sits nested under the uc_core entry, which ends with the colon introducing the target list. If that nesting is ever flattened, that entry needs "the uc_core C23 frontend" instead.
- The uc386 entry in freedos_git says only "It hosts the `dos_emu` test harness", while its freedos_micro_python twin says "It builds this port and hosts ...". That asymmetry is deliberate: only the freedos_micro_python original claimed the build relationship.

## Corrections made while passing through

- `uc386` linked to `avwohl/dosemu`, which GitHub now resolves only by redirect. The
  repository was renamed to `dosiz`, and the link is updated.
- `smalltalk80-2026` nearly lost **Mac Catalyst**. Its README states that it runs natively
  on macOS, Mac Catalyst, Linux and Windows and ships a Catalyst App Store frontend, so
  the entry was corrected before the commit. iOS stays dropped, because the README lists
  it as a future target and not as a shipped platform.

