# freedos_git

A **FreeDOS / i386 port of [git](https://github.com/git/git)**, built
end-to-end through the [uc386](https://pypi.org/project/uc386/) C23
compiler — the same toolchain and approach as its sibling project
[freedos_micro_python](https://github.com/avwohl/freedos_micro_python)
(which also carries the working DOS networking + SSH/TLS stack this
port will eventually borrow for `clone`/`fetch`/`push`).

> **Status: pre-alpha bring-up — `git --version` runs through git's
> real command dispatch on DOS.** A binary built end-to-end through
> uc386 runs `git --version` via git's *verbatim* `cmd_main` →
> `handle_options` → `run_argv` → `handle_builtin` → `run_builtin`
> path (only `commands[]` is trimmed and `init_git` reduced, both via
> idempotent `fetch.sh` patches) and prints byte-identical `git
> version 2.50.1` under `uc386.dos_emu` (exit 0); `git` with no args
> prints git's real usage banner. Next milestone is `git init`.
> Porting git — a large deeply-POSIX-coupled C codebase — to 32-bit
> DOS is an incremental multi-stage effort tracked frankly in
> [`NOTES.md`](NOTES.md), the development diary.

## License

git is **GPLv2** (with LGPLv2.1 for some components such as `xdiff`).
This port links against and derives from the official git sources, so
the port as a whole is distributed under git's license. The repo
[`LICENSE`](LICENSE) is a verbatim copy of upstream git's `COPYING`;
`vendor/git/LGPL-2.1` covers the LGPL parts. The integration glue
(scripts, port shim, CLI) is contributed under that same GPLv2.

## How it's built

There is **no DJGPP and no `make`**. uc386 is a pure-Python C23
compiler that emits NASM, linked flat for PMODE/W — exactly the
pipeline the sibling project uses. The official git source is the
pinned **`vendor/git`** submodule (git `v2.50.1`).

```
pip install -e .            # pulls uc386 (the compiler)
mkdir work && cd work
freedos-git fetch           # materialise pinned git src + zlib + gen headers
freedos-git build           # per-TU triage pass — the bring-up workhorse
freedos-git port            # multi-TU build → build/git.bin (once green)
```

- **`vendor/git`** — official git, pinned (submodule, shallow at the tag).
- **`src/freedos_git/scripts/`** — `fetch.sh` (materialise + vendor zlib +
  run git's own generated-header generators + DOS patches), `build.sh`
  (per-TU triage matrix), `build_port.sh` (multi-TU → `build/git.bin`),
  `_common.sh` (the uc386 invocation, NO_* portability knob set, and
  the bring-up source frontier).
- **`src/freedos_git/port/`** — the DOS port shim: `gitdos.h`
  (force-included portability policy), real `opendir`/`readdir` over
  DOS FindFirst/FindNext (uc386 ships those as NULL stubs), a
  `time()`/`gettimeofday()` backed by the DOS RTC, `vsnprintf`, and
  the stub system headers (`pwd.h`, `utime.h`, `sys/utsname.h`, …)
  that git's `compat/posix.h` expects but uc386's libc doesn't have.
- **`src/freedos_git/cli.py`** — the `freedos-git` CLI wrapper.

## Approach

git assumes POSIX (fork/exec, mmap, symlinks, pthreads, sockets, a
users/groups DB, a real `/`-rooted filesystem). DOS has none of that.
The strategy mirrors freedos_micro_python's bring-up:

1. Drive git's own portability fallbacks (`NO_MMAP`, `NO_PTHREADS`,
   `NO_SYMLINK_HEAD`, `NO_REGEX`, … → its `compat/*.c`).
2. Fill the remaining gaps with the DOS shim in `port/`.
3. Take the smallest real command first (`git --version`, then
   `git init`), grow the source frontier in `_common.sh`, clear each
   triage layer, and log every pass in `NOTES.md`.

Networking commands (`clone`/`fetch`/`push`) come later, on top of the
lwIP + axtls stack already proven in the sibling project.

## Related projects

- [freedos_micro_python](https://github.com/avwohl/freedos_micro_python)
  — sibling port; source of the toolchain pattern and the DOS
  networking/TLS stack.
- [uc386](https://github.com/avwohl/uc386) — the C23 compiler + the
  `dos_emu` test harness.
- [git](https://github.com/git/git) — upstream (vendored, pinned).
