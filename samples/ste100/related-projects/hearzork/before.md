# HearZork

A voice-controlled Z-machine interpreter for iOS and macOS, designed for visually impaired players. Play classic interactive fiction games like Zork entirely by voice.

## Overview

HearZork is a full Z-machine interpreter with on-device speech recognition and text-to-speech. No touch, keyboard, or screen required — though a large-text console is available when you want it.

The app includes a built-in game catalog with 20 classic and community games ready to download and play. You can also import your own `.z3`, `.z5`, `.z8` files from the local file system or a URL.

## Features

- **Full voice control**: Speak commands, hear the game read aloud. On-device speech recognition via Apple's Neural Engine — no data leaves your device.
- **Game vocabulary boosting**: Extracts the Z-machine dictionary table and feeds it to the speech recognizer, dramatically improving recognition of game-specific words.
- **Edit-distance correction**: Post-processes recognized speech against the game vocabulary to fix near-misses.
- **Adjustable large-text console**: Monospaced text output with font sizes up to 72pt.
- **Voice-only mode**: Hide the console entirely for a fully audio experience.
- **Meta voice commands**: "repeat", "louder", "quieter", "faster", "slower", "bigger text", "smaller text", "show console", "hide console".
- **Built-in game catalog**: Browse and download 20 games (Zork I–III, Enchanter, Planetfall, Curses, Photopia, and more).
- **Import from anywhere**: Local file picker or paste a URL.
- **Z-machine versions 1–5, 7, 8**: All versions except V6 (graphics-dependent).

## Status

**Interpreter (solid):**
- Passes the Czech compliance test suite on all four versions (V3/V4/V5/V8) — 0 failures
- Runs Zork I, Curses, Anchorhead, Dreamhold, and many other games
- Full opcode coverage: arithmetic, logic, objects, text, I/O, indirect references, undo
- Correct Z-text decoding with abbreviations, custom alphabets, and ZSCII escapes

**Voice (working):**
- SFSpeechRecognizer with `requiresOnDeviceRecognition` (A12+ Neural Engine)
- AVSpeechSynthesizer with configurable rate, pitch, and volume
- Dictionary-boosted `contextualStrings` for game vocabulary
- Levenshtein edit-distance post-correction

**UI (complete):**
- SwiftUI, cross-platform iOS 17+ and macOS 14+
- Game catalog with one-tap download and SHA-256 verification
- Status bar, upper window, scrollable output, text input
- Full VoiceOver accessibility labels and hints throughout

## Building

### Prerequisites

```bash
# Xcode 15+ with iOS 17 / macOS 14 SDK
xcode-select --install

# XcodeGen (project generation)
brew install xcodegen
```

### Build

```bash
git clone https://github.com/avwohl/hearzork.git
cd hearzork
xcodegen generate
open HearZork.xcodeproj
```

Select **HearZork_iOS** or **HearZork_macOS** and build. The first build takes about a minute.

### Running tests

```bash
xcodebuild test -project HearZork.xcodeproj -scheme HearZorkTests \
  -destination 'platform=iOS Simulator,name=iPhone 16'
```

25 tests covering memory, text encoding, dictionary lookup, game execution, and the Czech compliance suite.

## Project Structure

```
hearzork/
├── HearZork/
│   ├── App/              Entry point (HearZorkApp.swift)
│   ├── ZMachine/         Z-machine interpreter core
│   │   ├── Memory.swift       Memory model, packed addresses, save/restore
│   │   ├── Header.swift       64-byte header parsing
│   │   ├── TextDecoder.swift  Z-text decoding and encoding
│   │   ├── ObjectTable.swift  Object tree, attributes, properties
│   │   ├── Dictionary.swift   Dictionary parsing, tokenization, lookup
│   │   ├── Instruction.swift  Instruction decoder (all four forms)
│   │   ├── Processor.swift    Execution engine, all opcodes
│   │   └── IOSystem.swift     I/O protocol and test harness
│   ├── Voice/            Speech recognition and text-to-speech
│   │   ├── SpeechInput.swift  SFSpeechRecognizer, vocabulary boosting
│   │   └── SpeechOutput.swift AVSpeechSynthesizer, rate/pitch control
│   ├── Model/            Game catalog, downloader, storage
│   └── UI/               SwiftUI views
│       ├── LibraryView.swift  Catalog browser, import, game list
│       ├── ConsoleView.swift  Game console, voice indicator
│       ├── AboutView.swift    About screen with GitHub link
│       └── GameViewModel.swift Bridges Z-machine, UI, and voice
├── Tests/                Unit and compliance tests
├── games.xml             Game catalog manifest (20 games)
├── project.yml           XcodeGen project definition
├── PRIVACY.md            Privacy policy
└── LICENSE               GPL-3.0
```

## Game Catalog

The built-in catalog includes freely distributable games:

**Infocom Classics** (released as freeware)
- Zork I: The Great Underground Empire (1980)
- Zork II: The Wizard of Frobozz (1981)
- Zork III: The Dungeon Master (1982)
- Enchanter (1983)
- Planetfall (1983)
- Ballyhoo (1986)
- Cutthroats (1984)

**Community Favorites**
- Adventure (Colossal Cave) — Will Crowther, Don Woods (1977)
- Curses — Graham Nelson (1993)
- Photopia — Adam Cadre (1998)
- Spider and Web — Andrew Plotkin (1998)
- Shade — Andrew Plotkin (2000)
- 9:05 — Adam Cadre (2000)
- The Dreamhold — Andrew Plotkin (2004)
- Anchorhead — Michael Gentry (1998)
- and more

Games are hosted as GitHub release assets with SHA-256 checksums in `games.xml`.

## Related Projects

- [zorkie](https://github.com/avwohl/zorkie) — ZIL/ZILF compiler producing Z-machine story files
- [z2js](https://github.com/avwohl/z2js) — Z-machine to JavaScript compiler
- [zwalker](https://github.com/avwohl/zwalker) — Z-machine test runner and game walker

## License

GPL-3.0 — see [LICENSE](LICENSE).

## Privacy

HearZork does not collect any personal data. Speech recognition runs entirely on-device. See [PRIVACY.md](PRIVACY.md).

## Acknowledgments

- Z-Machine Standards Document v1.1 by Graham Nelson
- Czech test suite by Amir Karger
- Games sourced from the [Interactive Fiction Archive](https://ifarchive.org)
- The Interactive Fiction community at [intfiction.org](https://intfiction.org)
