# pharo-headless-test

Run the full Pharo SUnit test suite headless, with a fake GUI that lets
you click menus, press buttons, and take screenshots — all without a
real display.

Works on any Spur VM: official Pharo VM (Cog JIT), interpreter VMs,
Mac Catalyst, etc. Tested on Pharo 13 and Pharo 14.

## What's in the box

**setup_fake_gui.st** — Creates a virtual Morphic display (1024x768
Form, WorldMorph, MorphicUIManager, UI process). Installs the `FakeGUI`
helper class for programmatic interaction:

    FakeGUI clickMenuItemNamed: 'Save'.
    FakeGUI clickButtonNamed: 'OK' in: aPresenter.
    FakeGUI allMorphsNamed: 'Tools'.
    FakeGUI findWidgetOfType: SpButtonMorph in: aPresenter.
    FakeGUI openPresenter: aPresenter.
    FakeGUI screenshot.                                "returns Display Form"
    FakeGUI screenshotToFile: '/tmp/screenshot.png'.   "saves PNG"
    FakeGUI screenshotOf: aMorph toFile: '/tmp/m.png'. "captures one morph"

Also patches `Morph>>activate`/`passivate` to skip nil submorphs, which
fixes ~350 "receiver of activate is nil" errors that occur headless.

**run_sunit_tests.st** — Batch SUnit runner that discovers and runs
every TestCase subclass in the image. Features:

- Per-test watchdog timeouts (Delay-based, configurable scale factor)
- Bail-out after consecutive timeouts per class
- Skip list for known hangers (Epicea file watchers, Athens/Cairo, etc.)
- Delay scheduler health checks between classes
- Auto-runs on image startup via SessionManager hook
- Tab-delimited detail log with pass/fail/error/skip/timeout per test
- Runs inside TestExecutionEnvironment for proper test isolation
- Trait-modifying tests sorted last to avoid corrupting shared state

## Quick start

    # Download a fresh Pharo image
    curl -sL https://get.pharo.org/64/140 | bash

    # Inject the scripts (--save bakes them into the image)
    ./pharo --headless Pharo.image eval --save \
      "'setup_fake_gui.st' asFileReference fileIn. \
       'run_sunit_tests.st' asFileReference fileIn"

    # Run — tests auto-execute on startup, results to /tmp
    ./pharo --headless Pharo.image

    # Check results
    cat /tmp/sunit_test_results.txt   # summary
    cat /tmp/sunit_test_detail.txt    # per-test detail

## Running without the test suite

If you just want the fake GUI for your own scripts (interactive testing,
CI screenshots, etc.), only inject `setup_fake_gui.st`:

    ./pharo --headless Pharo.image eval --save \
      "'setup_fake_gui.st' asFileReference fileIn"

Then in your own scripts:

    ./pharo --headless Pharo.image eval "
      FakeGUI openPresenter: SpSystemBrowser new.
      FakeGUI screenshotToFile: '/tmp/browser.png'.
      Smalltalk exitSuccess"

## Running a subset of tests

Write class names to `/tmp/sunit_class_names.txt` (one per line):

    echo 'SmallIntegerTest
    FloatTest
    ArrayTest' > /tmp/sunit_class_names.txt

    ./pharo --headless Pharo.image

Or use batch ranges in `/tmp/sunit_batch.txt`:

    echo '1 50' > /tmp/sunit_batch.txt

## Configuring timeouts

The default timeout scale is 5x (50 seconds per test). Interpreter VMs
without JIT compilation are slower, so increase the scale:

    echo '10' > /tmp/sunit_timeout_scale.txt

## GUI test results

Without `setup_fake_gui.st`, ~350 Spec presenter tests fail with
"receiver of activate is nil".

With it: 1054/1113 pass (94.6%) across 64 Spec GUI test classes.
The remaining failures are font metrics (FreeType not initialized
headless) and timing-sensitive tests.

## How it works

The fake GUI creates a real Morphic world that thinks it has a display:

1. A 1024x768 depth-32 `Form` is installed as `Display`
2. A `WorldMorph` is created and set as `World`/`ActiveWorld`
3. `MorphicUIManager` replaces `NonInteractiveUIManager`
4. The UI process starts the `MorphicRenderLoop`

From there, all standard Morphic operations work: opening windows,
building Spec presenters, rendering morphs, handling events. The
`FakeGUI` class sends synthetic `MouseButtonEvent`s to simulate clicks
and steps the world loop to process deferred actions.

Screenshots work because morphs render to the in-memory Display Form.
`writePNGFileNamed:` saves it as a standard PNG.

## Using with a non-standard VM

These scripts have no VM-specific dependencies. They were developed for
[iospharo](https://github.com/avwohl/iospharo) (a Pharo VM for iPad)
but work identically on the official Pharo VM. Any VM that runs a
standard Pharo 13+ Spur image will work.

For VMs without a `pharo` command-line launcher, inject the scripts
using whatever mechanism your VM provides, then launch the image. The
test runner registers a SessionManager startup hook at priority 90 and
runs automatically on image resume.

## Output files

    /tmp/sunit_test_results.txt   Summary with pass/fail/error/skip counts
    /tmp/sunit_test_detail.txt    Tab-delimited: run# class selector result
    /tmp/sunit_run_number.txt     Auto-incrementing run counter
    /tmp/sunit_run_completed.txt  Marker to prevent re-run on image resume

## Related

Other repos in this collection:

- **[smalltalk80-2026](https://github.com/avwohl/smalltalk80-2026)** — Smalltalk-80 VM implementation of the 1983 Blue Book Xerox virtual image, targeting macOS / Mac Catalyst, iOS, Windows, and Linux.
- **[iospharo](https://github.com/avwohl/iospharo)** — Pharo Smalltalk VM for iOS and Mac Catalyst (interpreter-only, low-bit oop encoding for ASLR compatibility).
- **[validate_smalltalk_image](https://github.com/avwohl/validate_smalltalk_image)** — Standalone validator and export tool for Spur-format Smalltalk image files (heap integrity, SHA-256 manifests, reference graphs).
- **[soogle](https://github.com/avwohl/soogle)** — Smalltalk code search engine that indexes packages across Pharo, Squeak, GemStone and more.
- **[claude-skills](https://github.com/avwohl/claude-skills)** — Open source skills for Claude Code: reusable knowledge and algorithms packaged as `.claude/skills/` markdown files.

## License

MIT. See LICENSE file.
