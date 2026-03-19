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

## Part 2: Code Signing via Local.xcconfig

Always use the Local.xcconfig pattern. It keeps the team ID out of version
control and works for both private and public repos.

**Config.xcconfig** (checked into git):
```
#include? "Local.xcconfig"
```

The `?` makes the include optional — builds won't fail if the file is missing
(CI, fresh clones). Config.xcconfig is referenced by **every target** in
project.yml via `configFiles:`.

**Local.xcconfig** (gitignored, never committed):
```
DEVELOPMENT_TEAM = 644N5FNKG2
```

**.gitignore must include:**
```
Local.xcconfig
```

**project.yml must reference Config.xcconfig on every target:**
```yaml
  MyApp:
    configFiles:
      Debug: Config.xcconfig
      Release: Config.xcconfig
  MyAppTests:
    configFiles:
      Debug: Config.xcconfig
      Release: Config.xcconfig
```

**project.yml must NOT set DEVELOPMENT_TEAM** — it comes from the xcconfig.

---

## Part 3: project.yml Template

```yaml
name: <appname>
options:
  xcodeVersion: "16.0"
  deploymentTarget:
    iOS: "17.0"
  defaultConfig: Release
  groupSortPosition: top
  generateEmptyDirectories: true

settings:
  base:
    SWIFT_VERSION: "5.9"
    MARKETING_VERSION: "0.1.0"
    SUPPORTS_MAC_DESIGNED_FOR_IPHONE_IPAD: false

configs:
  Debug: debug
  Release: release

targets:
  <appname>:
    type: application
    platform: iOS
    configFiles:
      Debug: Config.xcconfig
      Release: Config.xcconfig
    sources:
      - path: <appname>
      - path: Shared     # optional, for shared code
    settings:
      base:
        PRODUCT_BUNDLE_IDENTIFIER: com.awohl.<appname>
        GENERATE_INFOPLIST_FILE: true
        INFOPLIST_GENERATION_MODE: GeneratedFile
        CURRENT_PROJECT_VERSION: 1
        ASSETCATALOG_COMPILER_APPICON_NAME: AppIcon
        SUPPORTED_PLATFORMS: "iphoneos iphonesimulator"
        SUPPORTS_MACCATALYST: true
        DERIVE_MACCATALYST_PRODUCT_BUNDLE_IDENTIFIER: false
        TARGETED_DEVICE_FAMILY: "1,2,6"
        INFOPLIST_KEY_UILaunchScreen_Generation: true
        INFOPLIST_KEY_ITSAppUsesNonExemptEncryption: NO
        INFOPLIST_KEY_UISupportedInterfaceOrientations_iPhone: >-
          UIInterfaceOrientationPortrait
          UIInterfaceOrientationLandscapeLeft
          UIInterfaceOrientationLandscapeRight
        INFOPLIST_KEY_UISupportedInterfaceOrientations_iPad: >-
          UIInterfaceOrientationPortrait
          UIInterfaceOrientationPortraitUpsideDown
          UIInterfaceOrientationLandscapeLeft
          UIInterfaceOrientationLandscapeRight

  <appname>Tests:
    type: bundle.unit-test
    platform: iOS
    configFiles:
      Debug: Config.xcconfig
      Release: Config.xcconfig
    sources:
      - path: <appname>Tests
    dependencies:
      - target: <appname>
    settings:
      base:
        GENERATE_INFOPLIST_FILE: true
        PRODUCT_BUNDLE_IDENTIFIER: com.awohl.<appname>.tests
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

### Which sizes are needed

- **iOS (17+)**: One single 1024x1024 image with `"idiom": "universal",
  "platform": "ios"`. Xcode auto-generates all device sizes from this.
- **Mac Catalyst**: Explicit sizes at 16, 32, 64, 128, 256, 512, 1024.
  Mac icons need specific @1x/@2x entries — Xcode does NOT auto-derive them.

If the app is iOS-only (no Mac Catalyst), you only need the 1024.
If it supports Mac Catalyst, you need all 7 sizes.

### Icon generation script (Pillow)

```python
from PIL import Image, ImageDraw, ImageFont
import math

SIZE = 1024
output_dir = "<appname>/Assets.xcassets/AppIcon.appiconset"

# RGB mode — NOT RGBA. No alpha channel.
img = Image.new("RGB", (SIZE, SIZE))
draw = ImageDraw.Draw(img)

# Example: gradient background
for y in range(SIZE):
    t = y / SIZE
    r = int(58 + t * 30)
    g = int(98 + t * 40)
    b = int(191 + t * 50)
    draw.line([(0, y), (SIZE, y)], fill=(r, g, b))

# Draw your icon content here (text, shapes, etc.)
# Use ImageFont.truetype("/System/Library/Fonts/SFCompactRounded.ttf", size)
# for SF fonts on macOS

# Optional: vignette (darken corners)
for y in range(SIZE):
    for x in range(SIZE):
        dx = (x - SIZE / 2) / (SIZE / 2)
        dy = (y - SIZE / 2) / (SIZE / 2)
        dist = math.sqrt(dx * dx + dy * dy)
        if dist > 0.7:
            darken = min(int((dist - 0.7) * 180), 120)
            px = img.getpixel((x, y))
            img.putpixel((x, y), tuple(max(0, c - darken) for c in px))

# Save 1024 master + all Mac Catalyst sizes
MAC_SIZES = [16, 32, 64, 128, 256, 512, 1024]
for s in MAC_SIZES:
    resized = img.resize((s, s), Image.LANCZOS)
    resized.save(f"{output_dir}/icon_{s}.png", "PNG")
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

The `"universal"` + `"platform": "ios"` entry covers ALL iOS/iPadOS devices
(Xcode 15+). The `"mac"` entries with explicit scale factors are required
for Mac Catalyst — without them, the Mac app has no icon.

Note: some `"mac"` sizes reuse the same file (e.g., `icon_32.png` serves as
both 32@1x and 16@2x). This is correct — the pixel dimensions match.

### Size reference (Mac Catalyst icons)

- 16px  — Mac 16@1x
- 32px  — Mac 32@1x, 16@2x
- 64px  — Mac 32@2x
- 128px — Mac 128@1x
- 256px — Mac 256@1x, 128@2x
- 512px — Mac 512@1x, 256@2x
- 1024px — App Store, iOS universal, Mac 512@2x

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
## Xcode
xcuserdata/
*.xcscmblueprint
*.xccheckout
build/
DerivedData/
*.moved-aside
*.pbxuser
!default.pbxuser
*.mode1v3
!default.mode1v3
*.mode2v3
!default.mode2v3
*.perspectivev3
!default.perspectivev3
*.hmap
*.ipa
*.dSYM.zip
*.dSYM
*.xcodeproj/project.xcworkspace/
*.xcodeproj/xcuserdata/

## Local config (team signing)
Local.xcconfig

## Swift Package Manager
.build/
Packages/
Package.resolved

## macOS
.DS_Store
.AppleDouble
.LSOverride
```

Note: `*.xcodeproj/project.pbxproj` and `*.xcodeproj/xcshareddata/` ARE
committed. Only user-specific data (xcuserdata, workspace) is ignored.
XcodeGen regenerates the pbxproj, but having it in git means the project
opens without running xcodegen first.

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

1. Create directories:
   ```
   mkdir -p <appname>/{<appname>/Views,<appname>/Assets.xcassets/{AccentColor.colorset,AppIcon.appiconset},Shared/{Models,Services,Views},<appname>Tests}
   ```
2. Write `project.yml` — never put DEVELOPMENT_TEAM here
3. Write `Config.xcconfig` with `#include? "Local.xcconfig"`
4. Write `Local.xcconfig` with `DEVELOPMENT_TEAM = 644N5FNKG2`
5. Write `.gitignore` (must include `Local.xcconfig`)
6. Write `CLAUDE.md`
7. Write asset catalog JSON files (Contents.json, AccentColor, AppIcon)
8. Generate icons using Python/Pillow — **RGB mode, no alpha**, all Mac sizes
9. Write `<appname>App.swift` and initial views
10. Run `xcodegen` to generate .xcodeproj
11. Build: `xcodebuild build -project <appname>.xcodeproj -scheme <appname> -destination 'platform=iOS Simulator,name=iPhone 16' -quiet`
12. Run tests: `xcodebuild test -project <appname>.xcodeproj -scheme <appname> -destination 'platform=iOS Simulator,name=iPhone 16' -only-testing:<appname>Tests -quiet`
13. `git init && git add .gitignore CLAUDE.md project.yml Config.xcconfig <appname>/ <appname>Tests/ Shared/ <appname>.xcodeproj/project.pbxproj <appname>.xcodeproj/xcshareddata/`
14. `git commit -m "Initial commit"`
15. Create GitHub repo: `gh repo create <org>/<appname> --private` then `git remote add origin ... && git push -u origin main`

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

7. **DO NOT commit xcuserdata or project.xcworkspace** — those are
   user-specific.  DO commit `project.pbxproj` and `xcshareddata/` so the
   project opens without running xcodegen first.

8. **DO NOT forget `configFiles:` on the test target** — without it, the
   test target won't inherit DEVELOPMENT_TEAM from Local.xcconfig and
   code signing will fail when running tests.
