---
name: ios-app-scaffold
description: Complete recipe for creating a new iOS/Mac Catalyst app from scratch using XcodeGen. Covers project.yml, Config.xcconfig, code signing (private vs public repo), asset catalog with icon generation, Info.plist keys, and CLAUDE.md. Use when creating a new iOS or Mac app project.
---

# iOS App Scaffold

Step-by-step recipe for creating a new SwiftUI iOS/Mac Catalyst app using
XcodeGen.  Covers every file needed to pass App Store validation on first
upload.

---

## Part 1: Directory Layout

```
<appname>/
├── project.yml              # XcodeGen source of truth
├── Config.xcconfig          # Build config (includes Local.xcconfig)
├── Local.xcconfig           # Team ID + signing (gitignored for public repos)
├── CLAUDE.md                # Developer instructions
├── .gitignore
└── <appname>/
    ├── <appname>App.swift   # @main entry point
    ├── Models/
    ├── Services/
    ├── ViewModels/
    ├── Views/
    │   └── ContentView.swift
    └── Assets.xcassets/
        ├── Contents.json
        ├── AccentColor.colorset/
        │   └── Contents.json
        └── AppIcon.appiconset/
            ├── Contents.json
            └── icon_*.png   # Generated icons (NO alpha channel)
```

---

## Part 2: Code Signing — Private vs Public Repo

**Ask the user two questions:**
1. "Is this repo currently private or public?"
2. "Will it stay that way, or might it go public later?"

If the repo **will ever be public** (even if private now), use the
Local.xcconfig pattern.  Only put the team ID directly in project.yml if the
repo is private AND will stay private forever.

### Private forever — team ID in project.yml

```yaml
settings:
  base:
    DEVELOPMENT_TEAM: 644N5FNKG2
```

### Public (or might go public) — team ID in Local.xcconfig (gitignored)

**Config.xcconfig:**
```
#include? "Local.xcconfig"
```

**Local.xcconfig:**
```
DEVELOPMENT_TEAM = 644N5FNKG2
```

**.gitignore must include:**
```
Local.xcconfig
```

**project.yml must NOT set DEVELOPMENT_TEAM** — it comes from the xcconfig.

---

## Part 3: project.yml Template

```yaml
name: <appname>
options:
  bundleIdPrefix: com.awohl
  deploymentTarget:
    iOS: "17.0"
  xcodeVersion: "16.0"
settings:
  base:
    SUPPORTS_MACCATALYST: YES
    SWIFT_VERSION: "5.9"
targets:
  <appname>:
    type: application
    platform: iOS
    sources:
      - path: <appname>
    configFiles:
      Debug: Config.xcconfig
      Release: Config.xcconfig
    settings:
      base:
        # DEVELOPMENT_TEAM: 644N5FNKG2    # only if private repo
        MARKETING_VERSION: "0.1.0"
        CURRENT_PROJECT_VERSION: 1
        PRODUCT_BUNDLE_IDENTIFIER: com.awohl.<appname>
        INFOPLIST_KEY_CFBundleDisplayName: <DisplayName>
        ASSETCATALOG_COMPILER_APPICON_NAME: AppIcon
        INFOPLIST_KEY_CFBundleIconName: AppIcon
        INFOPLIST_KEY_ITSAppUsesNonExemptEncryption: NO
        INFOPLIST_KEY_UILaunchScreen_Generation: YES
        INFOPLIST_KEY_UISupportedInterfaceOrientations: >-
          UIInterfaceOrientationPortrait
          UIInterfaceOrientationLandscapeLeft
          UIInterfaceOrientationLandscapeRight
          UIInterfaceOrientationPortraitUpsideDown
        INFOPLIST_KEY_UIRequiresFullScreen: NO
        GENERATE_INFOPLIST_FILE: YES
```

### Required Info.plist keys checklist

| Key | Purpose | Value |
|-----|---------|-------|
| `ASSETCATALOG_COMPILER_APPICON_NAME` | Tells Xcode which icon set | `AppIcon` |
| `INFOPLIST_KEY_CFBundleIconName` | CFBundleIconName in Info.plist | `AppIcon` |
| `INFOPLIST_KEY_ITSAppUsesNonExemptEncryption` | Skip export compliance dialog | `NO` |
| `INFOPLIST_KEY_UILaunchScreen_Generation` | Auto-generate launch screen | `YES` |
| `GENERATE_INFOPLIST_FILE` | Let Xcode generate Info.plist | `YES` |

If the app uses location:
```yaml
        INFOPLIST_KEY_NSLocationWhenInUseUsageDescription: "<App> uses your location to ..."
```

---

## Part 4: App Icon Generation

**CRITICAL**: iOS icons must be **RGB with NO alpha channel**.  RGBA icons
will be rejected by App Store Connect with "Invalid Image Asset" errors.

### Icon generation script

Use `tools/generate_ios_icon.py` from this repo, or inline:

```python
from PIL import Image, ImageDraw

SIZE = 1024
# RGB mode — NOT RGBA. No alpha channel.
img = Image.new('RGB', (SIZE, SIZE), (R, G, B))
draw = ImageDraw.Draw(img)

# Draw your icon content here...

# Save the 1024 master
img.save('icon_1024.png')

# Generate all required sizes
SIZES = [16, 20, 29, 32, 40, 58, 60, 64, 76, 80, 87,
         120, 128, 152, 167, 180, 256, 512]
for s in SIZES:
    img.resize((s, s), Image.LANCZOS).save(f'icon_{s}.png')
```

### AppIcon.appiconset/Contents.json

```json
{
  "images" : [
    {
      "filename" : "icon_1024.png",
      "idiom" : "universal",
      "platform" : "ios",
      "size" : "1024x1024"
    },
    { "filename": "icon_16.png",   "idiom": "mac", "scale": "1x", "size": "16x16" },
    { "filename": "icon_32.png",   "idiom": "mac", "scale": "2x", "size": "16x16" },
    { "filename": "icon_32.png",   "idiom": "mac", "scale": "1x", "size": "32x32" },
    { "filename": "icon_64.png",   "idiom": "mac", "scale": "2x", "size": "32x32" },
    { "filename": "icon_128.png",  "idiom": "mac", "scale": "1x", "size": "128x128" },
    { "filename": "icon_256.png",  "idiom": "mac", "scale": "2x", "size": "128x128" },
    { "filename": "icon_256.png",  "idiom": "mac", "scale": "1x", "size": "256x256" },
    { "filename": "icon_512.png",  "idiom": "mac", "scale": "2x", "size": "256x256" },
    { "filename": "icon_512.png",  "idiom": "mac", "scale": "1x", "size": "512x512" },
    { "filename": "icon_1024.png", "idiom": "mac", "scale": "2x", "size": "512x512" }
  ],
  "info" : { "author" : "xcode", "version" : 1 }
}
```

The single `icon_1024.png` with `"idiom": "universal", "platform": "ios"` is
sufficient for all iOS devices (Xcode 15+ / iOS 17+).  The mac entries with
explicit scale factors are required for Mac Catalyst.

### Size reference

| Size | Used for |
|------|----------|
| 1024 | App Store, iOS universal |
| 512 | Mac 512@1x, 256@2x |
| 256 | Mac 256@1x, 128@2x |
| 180 | iPhone @3x (60pt) |
| 167 | iPad Pro @2x (83.5pt) |
| 152 | iPad @2x (76pt) |
| 128 | Mac 128@1x |
| 120 | iPhone @2x (60pt), @3x (40pt) |
| 87  | Settings @3x (29pt) |
| 80  | Spotlight @2x (40pt) |
| 76  | iPad @1x (76pt) |
| 64  | Mac 32@2x |
| 60  | Spotlight @3x (20pt) |
| 58  | Settings @2x (29pt) |
| 40  | Spotlight @2x (20pt) |
| 32  | Mac 32@1x, 16@2x |
| 29  | Settings @1x (29pt) |
| 20  | Notification @1x (20pt) |
| 16  | Mac 16@1x |

---

## Part 5: Asset Catalog Boilerplate

**Assets.xcassets/Contents.json:**
```json
{
  "info" : { "author" : "xcode", "version" : 1 }
}
```

**AccentColor.colorset/Contents.json** — adapt the RGB values:
```json
{
  "colors" : [
    {
      "color" : {
        "color-space" : "srgb",
        "components" : { "alpha": "1.000", "red": "0.910", "green": "0.408", "blue": "0.227" }
      },
      "idiom" : "universal"
    }
  ],
  "info" : { "author" : "xcode", "version" : 1 }
}
```

---

## Part 6: .gitignore

```
# Xcode
*.xcodeproj/
xcuserdata/
*.xcworkspace/
DerivedData/
build/
*.pbxuser
*.perspectivev3
*.mode1v3
*.mode2v3
*.moved-aside
*.hmap
*.ipa

# Local config (public repos)
Local.xcconfig

# macOS
.DS_Store
*.swp
*~

# SPM
.build/
```

---

## Part 7: CLAUDE.md Template

```markdown
# <appname> Project Instructions

## Build

After modifying `project.yml` or adding/removing source files, regenerate:
\```
xcodegen && open <appname>.xcodeproj
\```
Always run this before telling the user to rebuild.

## Xcode Project Regeneration

When any of these change, run `xcodegen` automatically:
- `project.yml`
- Files added to or removed from `<appname>/`
- Build settings, deployment target, or entitlements
```

---

## Part 8: Minimal App Entry Point

```swift
import SwiftUI

@main
struct <appname>App: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

---

## Part 9: Complete Setup Sequence

1. Create directory: `mkdir -p <appname>/<appname>/{Models,Services,ViewModels,Views,Assets.xcassets/{AccentColor.colorset,AppIcon.appiconset}}`
2. Ask: **"Private or public repo?"**
3. Write `project.yml` (with or without DEVELOPMENT_TEAM)
4. Write `Config.xcconfig` with `#include? "Local.xcconfig"`
5. If public repo: write `Local.xcconfig` with `DEVELOPMENT_TEAM = 644N5FNKG2`
6. Write `.gitignore` (include `Local.xcconfig` for public repos)
7. Write `CLAUDE.md`
8. Write asset catalog JSON files (Contents.json, AccentColor, AppIcon)
9. Generate icons using Python/Pillow — **RGB mode, no alpha**
10. Write `<appname>App.swift` and `ContentView.swift`
11. Run `xcodegen && xcodebuild -project <appname>.xcodeproj -scheme <appname> -destination 'generic/platform=iOS Simulator' build`
12. `git init && git add -A && git commit`
13. Create GitHub repo: `gh repo create <org>/<appname> --private --source=. --push`

---

## What NOT To Do

1. **DO NOT use RGBA for icons** — App Store rejects icons with alpha channel.
   Always `Image.new('RGB', ...)` never `Image.new('RGBA', ...)`.

2. **DO NOT forget ASSETCATALOG_COMPILER_APPICON_NAME and CFBundleIconName** —
   without both, Xcode won't embed the icon and App Store validation fails with
   "Missing required icon file" and "Missing Info.plist value".

3. **DO NOT put DEVELOPMENT_TEAM in project.yml for public repos** — the team
   ID is a secret-adjacent value. Use Local.xcconfig (gitignored) instead.

4. **DO NOT omit ITSAppUsesNonExemptEncryption** — without it, every upload
   prompts for export compliance in App Store Connect.

5. **DO NOT skip Mac icon sizes for Catalyst apps** — iOS universal icon covers
   phones/tablets, but Mac Catalyst needs explicit 16-512pt @1x/@2x entries.

6. **DO NOT use `#include` (without `?`) for Local.xcconfig** — the `?` makes
   the include optional so builds don't fail when the file doesn't exist (CI,
   new clones).

7. **DO NOT leave .xcodeproj in git** — XcodeGen regenerates it.  Only
   `project.yml` belongs in version control.
