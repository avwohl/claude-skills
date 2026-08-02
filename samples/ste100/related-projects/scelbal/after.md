# SCELBAL - SCientific ELementary BAsic Language

A compact BASIC interpreter for CP/M systems, originally designed for 8080/Z80 microprocessors. This is a restored and debugged version with comprehensive test coverage.

## Overview

SCELBAL is a small BASIC interpreter that fits in less than 9KB of code. It provides essential BASIC functionality including:

- Integer and floating-point arithmetic
- Variables and arrays
- Built-in functions (INT, ABS, SGN, SQR, RND, TAB, CHR)
- Control structures (FOR/NEXT, IF/THEN, GOTO, GOSUB/RETURN)
- Input/Output (PRINT, INPUT)
- Program management (LIST, RUN, SAVE, LOAD)

**Current Status**: 38/39 tests passing (97% functional)

## Building

### Prerequisites

- `um80` - MACRO-80 compatible assembler
- `ul80` - MACRO-80 compatible linker
- 8080/Z80 emulator or CP/M system for testing

### Build Instructions

```bash
cd src
um80 scelbal.mac       # Assembles to scelbal.rel
ul80 scelbal.rel       # Links to scelbal.com
```

The output is a CP/M .COM file that can run on any CP/M-compatible system or emulator.

## Running

On a CP/M system or emulator:

```
A> scelbal
SCELBAL 1.0
READY
> 10 PRINT "HELLO WORLD"
> 20 END
> RUN
HELLO WORLD
READY
>
```

## Testing

Comprehensive test suite with 39 tests covering all language features:

```bash
cd src
bash quick_test.sh          # Run quick test suite
bash run_test_suite.sh      # Run full test suite with detailed output
```

Test categories:
- Basic arithmetic
- Parentheses and operator precedence
- Negative numbers
- Decimal numbers
- Built-in functions
- Comparison operators
- Complex expressions

## Documentation

- [Language Manual](docs/scelbal_language_manual.md) - Complete SCELBAL language reference
- [Bug Fixes](BUGS_FOUND.md) - History of bugs found and fixed
- [Test Documentation](src/README_TESTS.md) - Test suite documentation

## Recent Improvements

This version includes significant bug fixes:

1. **SQR Function Fix** - Fixed stack corruption in square root calculation
2. **FA Stack Fix** - Corrected function/array stack pointer management
3. **Decimal Arithmetic** - Fixed floating-point parsing and arithmetic
4. **Parentheses Precedence** - Fixed operator precedence in parenthesized expressions (11 tests fixed)

See [BUGS_FOUND.md](BUGS_FOUND.md) for complete fix history.

## Known Issues

- `PRINT((5))` without space returns empty (workaround: use `PRINT ((5))` with space)

This is a minor tokenization edge case that can be avoided with standard BASIC spacing.

## Project Structure

```
scelbal/
├── src/
│   ├── scelbal.mac          # Main assembly source
│   ├── scelbal.com          # Compiled CP/M binary
│   ├── quick_test.sh        # Quick test runner
│   ├── run_test_suite.sh    # Full test suite
│   └── trace_scelbal.cc     # C++ emulator for debugging
├── docs/
│   └── scelbal_language_manual.md
└── README.md
```

## History

SCELBAL was originally written for the Intel 8080 microprocessor and published in the late 1970s. This version has been restored from the original source and debugged using modern emulation and automated testing.

## License

Original public domain software, restored and improved.

## Contributing

Bug reports and fixes welcome! Please include:
- Minimal BASIC program that demonstrates the issue
- Expected vs actual output
- Test case that can be added to the test suite
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
- [uada80](https://github.com/avwohl/uada80) - Ada compiler for the Z80 processor and CP/M 2.2. It compiles a subset of Ada 2012 to CP/M .COM files.
- [uc80](https://github.com/avwohl/uc80) - C compiler for the Z80 processor and CP/M. It optimizes for small code size.
- [ucow](https://github.com/avwohl/ucow) - Cowgol compiler for the Z80 processor and CP/M. It runs on Linux in Python.
- [um80_and_friends](https://github.com/avwohl/um80_and_friends) - Linux toolchain that is compatible with Microsoft MACRO-80. It has an assembler, a linker, a librarian, and a disassembler.
- [upeepz80](https://github.com/avwohl/upeepz80) - Peephole optimizer for Z80 compilers that write lowercase Z80 assembly language. It shortens jumps to jr, builds djnz loops, and removes dead stores.
- [uplm80](https://github.com/avwohl/uplm80) - PL/M-80 compiler for the Z80 processor and CP/M. It writes Intel 8080 and Zilog Z80 assembly language.
- [z80cpmw](https://github.com/avwohl/z80cpmw) - Z80/CP/M emulator for Windows. It emulates the RomWBW HBIOS interface and boots CP/M from disk images.

