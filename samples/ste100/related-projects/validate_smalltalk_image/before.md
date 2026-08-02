# validate_smalltalk_image

Standalone validator and export tool for Spur-format Smalltalk image files.
Walks the entire heap and checks structural integrity, class table consistency,
method validity, and more. Reports errors (fatal corruption) and warnings
(suspicious but non-fatal conditions).

Also supports exporting image contents in diff-friendly formats: per-object
SHA-256 manifests (for change detection), full object catalogs, class hierarchy
trees, and object reference graphs.

## Supported Image Formats

    Format    Description                  Dialect
    68021     Spur 64-bit                  Pharo 5+, Squeak 5.3+, Cuis 6+
    68533     Spur 64-bit + Sista V1       Pharo 9+ (Sista bytecodes)
    6521      Spur 32-bit                  Squeak 5.x (32-bit), Cuis 5.x
    6505      Spur 32-bit + Sista V1       (if used)

Also supports the iOS-variant immediate tag encoding used by
[iospharo](https://github.com/avwohl/iospharo) at runtime — see
[iOS Tag Variant](#ios-tag-variant) below.

## Building

Requires CMake 3.16+ and a C++17 compiler.

    mkdir build && cd build
    cmake .. -DCMAKE_BUILD_TYPE=Release
    cmake --build .

## Usage

    validate_smalltalk_image [options] <image-file>

    Options:
      --ios-tags       Use iOS tag variant (see below)
      --reachability   Run reachability analysis (finds unreachable objects)
      --json           Output JSON instead of human-readable text
      --verbose        Print findings as they are discovered
      --max-errors N   Stop after N errors (default: unlimited)
      --help           Show help

    Export options (mutually exclusive):
      --export-shasum      Per-object SHA-256 manifest (for diff)
      --export-catalog     Full object metadata catalog
      --export-hierarchy   Class inheritance tree
      --export-graph       Object reference graph

    Export modifiers:
      --csv                CSV output (with --export-catalog)
      --filter-class NAME  Restrict to instances of named class
      --graph-root OFFSET  Hex offset of subgraph root (with --export-graph)
      --graph-depth N      Max traversal depth (with --export-graph)

    Exit codes:
      0  No errors (or export succeeded)
      1  Errors found (image has structural problems)
      2  Usage error

Export output goes to stdout; progress and validation messages go to stderr.
This lets you pipe or redirect exports cleanly:

    validate_smalltalk_image --export-shasum image.image > shasums.txt

## Validation Checks

### Errors (structural corruption, exit code 1)

    Check                         Description
    heap.objectOverflow           Object extends past end of heap
    alignment.misaligned          Object header not 8-byte aligned
    classIndex.outOfRange         Class index exceeds 22-bit maximum
    forwarded.inSavedImage        Forwarded object (classIndex=8) found in saved image
    oop.invalidPointer            Pointer slot contains invalid Oop (not immediate, not in heap)
    oop.misalignedPointer         Pointer slot contains unaligned heap address
    oop.notObjectStart            Pointer targets mid-object, not a header
    classTable.missingClass       Object references class index not in class table
    classTable.badPage            Class table page pointer invalid
    classHierarchy.nonPointer     Class object has non-pointer format
    classHierarchy.tooFew         Class has fewer than 3 slots
    classHierarchy.superCycle     Cycle detected in superclass chain
    classHierarchy.badSuper       Superclass is not a valid Oop
    classHierarchy.badMethodDict  Method dictionary is not a valid pointer
    specialObjects.outOfRange     Special objects Oop outside heap
    specialObjects.notStart       Special objects Oop not an object start
    specialObjects.badFormat      Special objects array is not pointer format
    specialObjects.tooSmall       Special objects array has < 60 entries
    specialObjects.badEntry       Critical special object is not a heap pointer
    method.badHeader              Method header (slot 0) is not a SmallInteger
    method.literalOverflow        numLiterals exceeds available slots
    method.literalPastBody        Literal frame extends past method body
    slot.pastHeap                 Object slot data extends past heap end

### Warnings (suspicious but valid)

    Check                         Description
    format.reserved               Object uses reserved format (6, 7, or 8)
    format.zeroWithSlots          ZeroSized format but has > 0 slots
    format.bytePadding            Byte object with 0 slots but non-zero unused count
    freeChunk.nonZeroFormat       Free chunk (classIndex=0) with non-zero format
    overflow.smallCount           Overflow header with slot count < 255
    overflow.veryLarge            Object larger than 100 MB
    classTable.unexpectedFormat   hiddenRootsObj has unexpected format
    classHierarchy.deepChain      Superclass chain depth >= 200
    classHierarchy.badInstSpec    Instance specification is not a SmallInteger
    classHierarchy.badName        Class name is not a byte or IndexableFixed object
    classHierarchy.mdBadFormat    Method dictionary has non-pointer format
    classHierarchy.mdTooSmall     Method dictionary has < 2 slots
    method.argsVsTemps            numArgs > numTemps in method header
    method.badPrimBytecode        hasPrimitive set but first byte is not 248
    method.primOutOfRange         Primitive index > 8191
    header.veryLargeImage         Image > 4 GB
    image.truncated               File is shorter than header claims
    reachability.unreachable      Objects not reachable from roots (with --reachability)
    specialObjects.nilMismatch    nil slot doesn't point to first heap object
    specialObjects.falseMismatch  false slot doesn't point to second heap object
    specialObjects.trueMismatch   true slot doesn't point to third heap object

### Statistics (always reported)

    Statistic                     Description
    Total objects                 Count of non-free heap objects
    Total size                    Sum of all non-free object sizes
    Free chunks / bytes           Count and size of free space
    Heap utilization              Percentage of heap that is live objects
    Pointer/Byte/Word objects     Breakdown by format category
    Compiled methods              Count of CompiledMethod objects
    Weak objects                  Count of weak/ephemeron objects
    Overflow headers              Objects with > 254 slots
    Pinned / Immutable            Count of flagged objects
    Max slot count / object size  Largest object in the heap
    Class table entries           Number of classes in the class table
    Top 20 classes                Most-instantiated classes by count
    Reachable / unreachable       Object reachability (with --reachability)

## Export Features

### SHA-256 Manifest (`--export-shasum`)

One line per non-free object: heap offset, identity hash, class name, and
SHA-256 of the object's content bytes. Designed for `diff`:

    validate_smalltalk_image --export-shasum before.image > before.txt
    # ... run tests in Pharo VM ...
    validate_smalltalk_image --export-shasum after.image > after.txt
    diff before.txt after.txt

Output format:

    0000000000000000 0f4d32 UndefinedObject                          b73a37ba...
    0000000000000010 063372 False                                    59dcf714...

The content hash covers the stable header (classIndex, format, identity hash,
slot count — excluding mutable GC flags) plus all body bytes. Objects with
changed content produce different hashes. New or deleted objects appear as
added or removed lines.

Use `--filter-class NAME` to restrict output to instances of a specific class.

### Object Catalog (`--export-catalog`)

Full metadata for every non-free object. Default output is aligned text;
use `--json` for JSON or `--csv` for CSV.

    validate_smalltalk_image --export-catalog image.image
    validate_smalltalk_image --export-catalog --json image.image
    validate_smalltalk_image --export-catalog --csv image.image

Fields: offset, classIndex, className, format, slots, bytes, identityHash,
contentHash, flags (immutable, pinned, overflow).

### Class Hierarchy (`--export-hierarchy`)

Prints the full class inheritance tree with method counts and instance
variable counts. Default is indented text; use `--json` for a flat JSON array.

    validate_smalltalk_image --export-hierarchy image.image

Sample output:

    ProtoObject (classIndex=3129, methods=51, instVars=0)
      Object (classIndex=3161, methods=446, instVars=0)
        Collection (classIndex=135, methods=112, instVars=0)
          ...

### Object Graph (`--export-graph`)

Adjacency list of object references. Each pointer object gets one line showing
the offsets of all objects it references. Non-pointer objects (bytes, words)
are omitted since they have no outgoing references.

    validate_smalltalk_image --export-graph image.image

Use `--graph-root OFFSET` and `--graph-depth N` to export a subgraph rooted
at a specific object:

    validate_smalltalk_image --export-graph --graph-root 1a340 --graph-depth 3 image.image

### Performance

On a 52 MB Pharo 13 image (740K objects):

    --export-shasum:     ~0.7s
    --export-catalog:    ~0.7s
    --export-hierarchy:  ~0.4s
    --export-graph:      ~0.4s (full), varies for subgraphs

## iOS Tag Variant

The `--ios-tags` flag is for validating the **in-memory** representation used
by [iospharo](https://github.com/avwohl/iospharo), not a separate image file
format. Saved `.image` files are always standard Spur format, interchangeable
with any Pharo VM.

### Why different tags?

Standard Spur 64-bit uses single-bit tag positions to distinguish immediates:

    Tag bits   Value   Meaning
    000        0x0     Object pointer (heap address)
    001        0x1     SmallInteger
    010        0x2     Character
    100        0x4     SmallFloat

On iOS, ASLR can place the heap at arbitrary addresses, so a fast
"is this an immediate?" check cannot rely on specific high-address patterns.
iospharo shifts the tag encoding so that **all immediates have bit 0 set**:

    Tag bits   Value   Meaning
    000        0x0     Object pointer (heap address)
    001        0x1     SmallInteger
    011        0x3     Character
    101        0x5     SmallFloat

This makes the immediate check a single bit test: `(oop & 1) != 0`.

### Image file format is unchanged

iospharo does not define a new image format. The conversion happens at
load/save time:

  - **Load**: `ImageLoader` reads a standard Spur `.image` and converts
    standard tags (0x2, 0x4) to iOS tags (0x3, 0x5) as objects enter memory.
  - **Save**: `ImageWriter` converts iOS tags back to standard tags before
    writing. The resulting `.image` is byte-identical in format to one saved
    by the reference Pharo VM.

A freshly downloaded Pharo image has standard tags. A running iospharo process
has iOS tags in memory. A saved image from iospharo has standard tags again.

### When to use `--ios-tags`

Use `--ios-tags` only if you are validating a **raw memory dump** from a
running iospharo process (e.g., captured via a debugger). For normal `.image`
files — whether saved by iospharo or any other Pharo VM — use the default
(standard) tag mode.

## How It Works

The validator loads the image file and processes it in phases:

 1. Parse and validate the Spur image header
 2. Linear heap walk: scan every object from start to end
 3. Per-object structural checks: format, alignment, overflow headers
 4. Pointer slot validation: every Oop in every pointer object is checked
    against the set of known object starts
 5. Class table: validate hiddenRootsObj pages and cross-reference all
    objects' class indices
 6. Special objects array: check critical entries (nil, false, true,
    SmallInteger class, etc.)
 7. Class hierarchy: superclass chains (cycle detection), method
    dictionaries, instance specifications, class names
 8. Compiled methods: header decoding, literal frames, primitive indices
 9. Reachability (optional): BFS from roots to find unreachable objects

The validator works on raw file offsets — it does NOT relocate pointers. All
Oop validation uses the original `startOfMemory` base address as stored in the
image header.

## Spur Object Header Layout

All Spur variants (32-bit and 64-bit) use a 64-bit object header:

    Bits 0-21:   Class index (22 bits, index into class table)
    Bit 23:      Immutable flag
    Bits 24-28:  Object format (5 bits, 0-31)
    Bit 29:      Remembered flag
    Bit 30:      Pinned flag
    Bit 31:      Grey flag (GC)
    Bits 32-53:  Identity hash (22 bits)
    Bit 55:      Marked flag (GC)
    Bits 56-63:  Slot count (0-254, or 255 = overflow header)

Objects with > 254 slots have a two-word header: the preceding 64-bit word
contains the actual slot count in its low 56 bits.

## Performance

On a 52 MB Pharo 13 image (740K objects):

    Validation only:       ~0.3s
    With reachability:     ~0.9s
    SHA-256 export:        ~0.7s
    Catalog export:        ~0.7s
    Hierarchy export:      ~0.4s
    Graph export:          ~0.4s

## Related

Other repos in this collection:

- **[smalltalk80-2026](https://github.com/avwohl/smalltalk80-2026)** — Smalltalk-80 VM implementation of the 1983 Blue Book Xerox virtual image, targeting macOS / Mac Catalyst, iOS, Windows, and Linux.
- **[iospharo](https://github.com/avwohl/iospharo)** — Pharo Smalltalk VM for iOS and Mac Catalyst (interpreter-only, low-bit oop encoding for ASLR compatibility).
- **[pharo-headless-test](https://github.com/avwohl/pharo-headless-test)** — Headless Pharo test runner with a fake GUI; clicks menus, takes screenshots, runs SUnit without a display.
- **[soogle](https://github.com/avwohl/soogle)** — Smalltalk code search engine that indexes packages across Pharo, Squeak, GemStone and more.
- **[claude-skills](https://github.com/avwohl/claude-skills)** — Open source skills for Claude Code: reusable knowledge and algorithms packaged as `.claude/skills/` markdown files.

## License

MIT License. See [LICENSE](LICENSE).
