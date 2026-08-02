# dosiz

An MS-DOS emulator that runs DOS programs by emulating the DOS API itself —
trapping INT 21h / INT 31h (DPMI) / INT 67h (EMS) and translating them to C++
implementations on the host — on top of the in-tree
[emu88](https://github.com/avwohl/qxDOS) 386 CPU core. Same design as
[cpmemu](https://github.com/avwohl/cpmemu), which does the equivalent for
CP/M BDOS.

**Status:** real DOS programs run.  DOS-hosted toolchain binaries run.
Cross-compiler-produced binaries run.  DPMI 0.9 host complete (every
INT 31h sub-function implemented or stubbed, 25 DPMI fixtures green) — real
32-bit DJGPP programs run end-to-end (printf, argv, env, malloc, file I/O,
spawn, POSIX signals, C++ ctors/dtors).  LIM EMS 4.0 plus a VCPI detection
subset are provided on INT 67h.  LE (Linear Executable) loader loads, applies
fixups, installs LDT descriptors, and enters 32-bit protected mode end-to-end
on hand-crafted fixtures; real DOS4G-hosted Watcom binaries load their full
image + apply all fixups but stall on the runtime's DOS4G pre-entry
environment convention (a DPMI-host-compatibility gap).

	dosiz tests/EXE2BIN.EXE              → Open Watcom banner   (real DOS-hosted)
	dosiz tests/HELLO_W.EXE              → hello from watcom    (Watcom cross-compiled)
	dosiz tests/HELLO_B.COM              → hello from bcc       (bcc cross-compiled)
	dosiz tests/LE_MIN.EXE               → exit 0                (hand-crafted LE)
	echo F | dosiz xcopy.exe src dst     → copies src to dst    (FreeDOS xcopy)
	dosiz mTCP-FTP.EXE                   → prints usage banner  (Open Watcom 16-bit, real DOS)

	dosiz wd.exe / vi.exe                → enters 32-bit PM, runs ~0x135 bytes,
	                                        GP-faults on DOS4G pre-entry selector
	                                        setup we don't emulate

The emu88 386 core provides the CPU + memory + PC hardware, driven through a
thin DOSBox→emu88 compatibility shim (`src/compat/`). DOS INT 21h is handled
entirely by C++ host code. Currently implemented:

	01  stdin char+echo    0E  set drive          3E  close handle
	02  putchar            0B  stdin ready?       3F  read handle
	07  stdin char no-echo 19  get drive          40  write handle
	08  stdin char no-echo 1A  set DTA            41  unlink
	09  print string       25  set int vector     42  seek handle
	0A  buffered input     29  parse filename     43  get/set attr
	2A  get date           2C  get time           44  ioctl (basic)
	30  get DOS version    33  ctrl-break         47  get cwd
	35  get int vector     37  switchar           48  alloc (MCB)
	38  country info       39  mkdir              49  free + coalesce
	3A  rmdir              3B  chdir              4A  resize (MCB)
	3C  create handle      3D  open handle        4B  exec
	4C  exit               4E  findfirst          4F  findnext
	50  set PSP            51  get PSP            56  rename
	5D  network (stub)     62  get PSP            63  lead-byte (stub)
	6C  extended open

INT 2Fh AX=1687h reports DPMI 0.90 (32-bit capable).  INT 31h
implements the full DPMI 0.9 spec: LDT descriptor mgmt (AX=0000..000C),
DOS memory alloc (0100..0102), IVT get/set (0200..0201), PM exception
handlers (0202..0203, live dispatch via IDT gate), PM IDT gates
(0204..0205), simulate-RM-INT and call-RM-procedure (0300..0302),
RM callbacks (0303..0304, 16-bit + 32-bit PM), state save/restore
stubs (0305..0306), version (0400), memory info (0500), linear memory
alloc/free/resize (0501..0503) with a two-tier MCB-under-1MB /
pm_arena-above-1MB backing store, lock/unlock and paging stubs
(0600..0604, 0702..0703), physical mapping pass-through (0800..0801),
virtual IF state (0900..0902), and debug watchpoint stubs (0B00..0B03).

INT 67h provides a functional LIM EMS 4.0 manager (a host-side page pool
reached through a 16KB×4 page frame at 0xE000, allocate/map/realloc/move/
save-restore) plus a VCPI detection + page-count subset (DE00/DE02/DE03/DE0A);
the VCPI PM-transition functions return "unsupported" so extenders fall back
to dosiz's DPMI.

RM<->PM mode switching is full-fidelity: 16-bit and 32-bit client
entry both work, INT 21h from PM reflects to our host handler via
PM IDT gate, INT 21h AH=09h string output works from PM, and
per-vector reflection shims (`66 CF` IRETD) handle 32-bit-gate
frames for INT 10h/etc. dispatched back to real-mode BIOS.

LE binaries (the format Watcom's DOS4G and DOS4GW produce) are
loaded, fixed up (source types 0x05/0x07/0x08 fully, 0x02/0x03/0x06
with per-object LDT selectors), given one LDT descriptor per object
(base/limit/access/D-bit from object flags), and launched directly
into 32-bit PM at the LE header's entry_obj:entry_eip.  `LE_MIN.EXE`
runs end-to-end through PM INT 21h AH=4Ch to rc=0.  Real Watcom
binaries load + execute ~0.2s of PM code before hitting the DOS4G
pre-entry environment convention.

PSP:[2Ch] points at an env block populated with `COMSPEC`, `PATH`, and
whichever of `HOME`/`USER`/`TMPDIR`/`LANG` are set on the host, followed
by an `argc`/`argv[0]` record per DOS convention.

PSP command tail at offset 80h is populated from argv. Drive mounts and
per-file / per-pattern mappings come from a `.cfg` file:

	program        = PROG.EXE
	args           = /q /v
	drive_C        = /home/me/dos
	drive_D        = /mnt/sources
	default_mode   = text           # all files: CRLF<->LF
	HELLO.TXT      = /real/path/hello_long_name.txt text
	*.BAS          = text           # mode-only wildcard override

Text mode strips CR on write and expands LF to CRLF on read so files
live on the host in Unix format. No subprocess, no DOS shell, no config
files beyond the optional `.cfg`.

## Building

dosiz has **no required dependencies** beyond a C++20 compiler, CMake, and
libm — no glib, meson, or DOSBox. The emu88 backend is vendored in-tree. SDL2
is the one **optional** dependency: when present at build time it enables the
`--window` VGA display; without it the build is dependency-free and headless.

	# Debian/Ubuntu  (libsdl2-dev is optional, for --window)
	sudo apt install build-essential cmake libsdl2-dev

	# macOS  (sdl2 is optional, for --window)
	brew install cmake sdl2

	# build + smoke-test (all platforms)
	make                         # wrapper: cmake -S src -B build && cmake --build build
	build/dosiz --version        # → dosiz 0.1.0-dev (backend: emu88)
	build/dosiz tests/HELLO.COM  # → dosiz-hello-ok

`make clean` removes the build directory.

## Why

Most DOS emulators use native FAT disk images. When developing with a DOS
compiler that means shuffling files in and out of the disk image for every
build. dosiz makes the DOS program see host files directly, so you can:

- Run a DOS C compiler as if it were a native CLI tool
- Use long filenames on the host while presenting 8.3 names to DOS
- Run text-only programs with no window at all (the default)
- Or open a VGA window with `--window` (text + VGA/SVGA graphics)
- Redirect DOS printer / AUX I/O to host files

Because the syscall layer is native C++ and emu88 is self-contained, dosiz is
intended to run on Linux, macOS, Windows, iOS, iPadOS, and Android — the same
platform set cpmemu already covers.

## Architecture

	dosiz binary
		emu88 386 CPU + memory + PC hardware (vendored, in-tree)
		DOSBox→emu88 compatibility shim (src/compat/)
		host-side DOS: INT 21h/31h/67h handlers → C++ file / memory / process calls
		.cfg parser (cpmemu-style)

No subprocess, no config files beyond the optional `.cfg`. The guest sees a
DOS; the host implements what that DOS does.

## Usage

	dosiz [options] PROGRAM.EXE [args...]
	dosiz [options] config.cfg
	dosiz PROG                         # bare name -- search DOSIZ_PATH

`dosiz PROG` looks for `PROG.COM` (preferred) or `PROG.EXE` first in the
current directory, then in each `:`-separated entry of `DOSIZ_PATH`.
Matching is case-insensitive. If a sidecar `PROG.cfg` exists next to the
resolved executable, it is auto-loaded as configuration (drive mounts,
text-mode, file mappings) before the program runs:

	export DOSIZ_PATH=~/dos/bin:/usr/local/dos/bin
	dosiz tcc hello.c                  # finds tcc.exe + tcc.cfg (if any)

Options:

	--help              Show usage
	--version           Print version
	--window            Open a VGA window (needs SDL2 at build time)
	--memsize=N         DOS memory in MB (default: 16)
	--verbose, -v       Trace DOS syscalls

`--window` opens a window and renders VGA text, 320x200x256 graphics (mode 13h),
and SVGA/VESA VBE 2.0 modes (8/15/16/24/32-bpp up to 1280x1024) via an INT 10h
video BIOS, with keyboard input; it needs SDL2 at build time (otherwise it
prints a notice and runs headless). `DOSIZ_FRAME_DUMP=out.ppm` renders the final
screen to a PPM without needing a window. `--machine=NAME` and `--cpu=NAME` are
accepted but currently inert. Audio (Sound Blaster/AdLib), the mouse, and the
joystick are not yet wired on the emu88 backend.

## Example .cfg

See `examples/example.cfg` for a documented sample. Minimal:

	program  = PROG.EXE
	args     = /q /v
	drive_C  = ${HOME}/dos
	drive_D  = /mnt/sources
	memsize  = 16

## License

GPLv3. Parts of the CPU compatibility shim (`src/compat/`) and the INT 67h
EMS/VCPI provider are derived from dosbox-staging (GPLv2-or-later, compatible).
Third-party attributions in `docs/CREDITS.md`.

## Related Projects

- [cpmemu](https://github.com/avwohl/cpmemu) — CP/M 2.2 emulator; the
  translation-layer template and the origin of the `.cfg` format
- [qxDOS](https://github.com/avwohl/qxDOS) — iOS/Mac DOS emulator; source of
  the vendored emu88 CPU core
