---
name: apple-hig
description: Apple Human Interface Guidelines reference for iOS/iPadOS/macOS app design. Covers typography (Dynamic Type sizes, SF Pro text styles), color system (semantic and system colors), layout (spacing, margins, safe areas), components (bars, buttons, sheets, alerts), navigation patterns, accessibility, and Liquid Glass (iOS 26). Use when building UI, choosing fonts/colors/spacing, or reviewing design compliance.
---

# Apple Human Interface Guidelines — Quick Reference

Precise specifications and decision rules for building HIG-compliant iOS apps
in SwiftUI.  Every value in this document comes from Apple's published
guidelines or measured from system defaults.  Use these numbers — do not guess.

---

## Part 1: Core Design Principles

Three pillars govern every Apple platform:

| Principle | Meaning |
|-----------|---------|
| **Clarity** | Text is legible at every size; icons are precise; adornments are subtle and appropriate; sharp focus on functionality motivates the design |
| **Deference** | Fluid motion and a crisp interface help people understand and interact with content without competing with it; content fills the screen |
| **Consistency** | Familiar standards and paradigms — system-provided controls, icons, text styles, uniform terminology — make the app feel integrated |

Additional principles: **Direct Manipulation** (rotate content with fingers, not dials), **Feedback** (acknowledge every action), **Metaphors** (virtual objects behave like real ones), **User Control** (people initiate and control actions).

---

## Part 2: Typography

### System font

**San Francisco (SF Pro)** is the system typeface.  Two optical sizes:

| Variant | Use for | Tracking behavior |
|---------|---------|-------------------|
| SF Pro Display | 20pt and above | Tighter tracking at large sizes |
| SF Pro Text | Below 20pt | Wider tracking for legibility |

SwiftUI selects the correct optical size automatically via `.font(.system(...))`.

### Text styles — default sizes (Large / default Dynamic Type)

| Text Style | SwiftUI | Size (pt) | Weight | Leading | Tracking |
|------------|---------|-----------|--------|---------|----------|
| Large Title | `.largeTitle` | 34 | Regular | 41 | +0.37 |
| Title 1 | `.title` | 28 | Regular | 34 | +0.36 |
| Title 2 | `.title2` | 22 | Regular | 28 | +0.35 |
| Title 3 | `.title3` | 20 | Regular | 24 | +0.38 |
| Headline | `.headline` | 17 | **Semi-Bold** | 22 | −0.41 |
| Body | `.body` | 17 | Regular | 22 | −0.41 |
| Callout | `.callout` | 16 | Regular | 21 | −0.32 |
| Subheadline | `.subheadline` | 15 | Regular | 20 | −0.24 |
| Footnote | `.footnote` | 13 | Regular | 18 | −0.08 |
| Caption 1 | `.caption` | 12 | Regular | 16 | 0.00 |
| Caption 2 | `.caption2` | 11 | Regular | 13 | +0.07 |

Headline is the only built-in style that defaults to semi-bold.

### Dynamic Type size categories

There are 12 size categories, from `xSmall` through `accessibility5`:

    xSmall → small → medium → large (DEFAULT) → xLarge → xxLarge → xxxLarge
    → accessibility1 → accessibility2 → accessibility3 → accessibility4 → accessibility5

The standard (non-accessibility) sizes scale text roughly ±2pt per step.
Accessibility sizes can reach 2-3× the default.  Key behavior:

- Small styles (Caption 2, Caption 1, Footnote) have a **floor** — they
  stop shrinking below their default size to stay legible.
- Large styles (Large Title) have a smaller scale factor — they grow less
  aggressively at accessibility sizes to avoid dominating the screen.

### Dynamic Type — representative sizes across categories

| Style | xSmall | Small | Medium | **Large** | xLarge | xxLarge | xxxLarge | AX1 | AX3 | AX5 |
|-------|--------|-------|--------|-----------|--------|---------|----------|-----|-----|-----|
| Large Title | 31 | 32 | 33 | **34** | 36 | 38 | 40 | 44 | 48 | 52 |
| Title 1 | 25 | 26 | 27 | **28** | 30 | 32 | 34 | 38 | 43 | 48 |
| Title 2 | 19 | 20 | 21 | **22** | 24 | 26 | 28 | 34 | 40 | 44 |
| Title 3 | 17 | 18 | 19 | **20** | 22 | 24 | 26 | 31 | 37 | 43 |
| Headline | 14 | 15 | 16 | **17** | 19 | 21 | 23 | 28 | 33 | 40 |
| Body | 14 | 15 | 16 | **17** | 19 | 21 | 23 | 28 | 33 | 40 |
| Callout | 13 | 14 | 15 | **16** | 18 | 20 | 22 | 26 | 32 | 38 |
| Subheadline | 12 | 13 | 14 | **15** | 17 | 19 | 21 | 25 | 30 | 36 |
| Footnote | 12 | 12 | 12 | **13** | 15 | 17 | 19 | 23 | 27 | 33 |
| Caption 1 | 11 | 11 | 11 | **12** | 14 | 16 | 18 | 22 | 26 | 32 |
| Caption 2 | 11 | 11 | 11 | **11** | 13 | 15 | 17 | 21 | 25 | 31 |

All sizes in points.  These are the sizes used when you apply a built-in text
style.  Always use built-in styles (`.font(.body)`) rather than hardcoding sizes.

### Typography rules

1. Prefer built-in text styles — they automatically support Dynamic Type.
2. Body text: minimum 11pt, recommended 17pt for comfortable reading.
3. Do not mix many font families — stick to SF Pro; add at most one brand font.
4. If using a custom font, call `.font(.custom("Name", size: ..., relativeTo: .body))`
   so it still scales with Dynamic Type.
5. Bold sparingly — only for emphasis. Headline style provides semi-bold.

---

## Part 3: Color System

### System colors (adaptable — auto-adjust for light/dark mode)

| SwiftUI | UIKit | Purpose |
|---------|-------|---------|
| `.red` | `.systemRed` | Destructive actions, errors |
| `.orange` | `.systemOrange` | Warnings |
| `.yellow` | `.systemYellow` | Caution, highlights |
| `.green` | `.systemGreen` | Success, confirmation |
| `.mint` | `.systemMint` | Fresh accent |
| `.teal` | `.systemTeal` | Secondary accent |
| `.cyan` | `.systemCyan` | Information |
| `.blue` | `.systemBlue` | Default tint, links, interactive elements |
| `.indigo` | `.systemIndigo` | Brand accent |
| `.purple` | `.systemPurple` | Premium, creative |
| `.pink` | `.systemPink` | Social, playful |
| `.brown` | `.systemBrown` | Earthy, organic |

**Always use `.system*` variants** (not `.red`, `.blue`, etc.) via UIKit, or
the SwiftUI named colors which already resolve to system colors.  These
automatically adjust brightness for dark mode and increased contrast.

### Semantic colors — foreground

| UIKit | Purpose |
|-------|---------|
| `.label` | Primary text |
| `.secondaryLabel` | Subtitle, less prominent text |
| `.tertiaryLabel` | Disabled text, placeholder-ish |
| `.quaternaryLabel` | Least prominent text |

### Semantic colors — backgrounds

| UIKit | Use for |
|-------|---------|
| `.systemBackground` | Primary background (white / near-black) |
| `.secondarySystemBackground` | Grouped content, cards |
| `.tertiarySystemBackground` | Nested content within secondary |
| `.systemGroupedBackground` | Grouped table/list background |
| `.secondarySystemGroupedBackground` | Cell within grouped list |
| `.tertiarySystemGroupedBackground` | Nested within grouped cell |

### Semantic colors — fills and separators

| UIKit | Use for |
|-------|---------|
| `.systemFill` | Thin overlays on backgrounds |
| `.secondarySystemFill` | Medium overlays |
| `.tertiarySystemFill` | Thick overlays |
| `.quaternarySystemFill` | Thickest overlays |
| `.separator` | Standard separator lines |
| `.opaqueSeparator` | Non-translucent separators |

### Grays

Six opaque system grays: `.systemGray` through `.systemGray6`.
`systemGray` is the most prominent; `systemGray6` is the most subtle
(near-white in light mode, near-black in dark mode).

### Color rules

1. **Never convey meaning through color alone** — pair with icons or text.
2. **Test both appearances** — verify in light mode, dark mode, AND increased
   contrast settings.
3. **Minimum contrast ratios**: 4.5:1 for normal text, 3:1 for large text
   (≥18pt regular or ≥14pt bold).
4. **Limit your palette**: use 1-2 brand colors + system semantic colors.
5. **Use tintColor** for interactive controls — it provides automatic pressed
   and disabled state adjustments.

---

## Part 4: Layout & Spacing

### Grid and spacing tokens

Apple's layout uses an **8pt grid**.  Standard spacing scale:

| Token | Value | Common use |
|-------|-------|------------|
| XS | 4pt | Icon-to-label gap, tight element spacing |
| S | 8pt | Between related items, compact padding |
| M | 16pt | Screen margins (iPhone), form field gaps, sheet padding |
| L | 24pt | Section gaps, group separation |
| XL | 32pt | Major section separation |
| XXL | 48pt | Visual breathing room between page regions |

### Screen margins

| Device | Standard horizontal margin |
|--------|---------------------------|
| iPhone | 16pt |
| iPad | 20pt |

These are the default `readableContentGuide` / list insets.  SwiftUI
`List`, `Form`, and `NavigationStack` apply these automatically.

### Component heights

| Component | Height (pt) | Notes |
|-----------|-------------|-------|
| Navigation bar | 44 | Plus status bar above + safe area |
| Large title (expanded) | 44 + 52 = 96 | Collapses to 44 on scroll |
| Tab bar | 49 | Plus safe area below |
| Toolbar | 44 | Bottom on iPhone, top or bottom on iPad |
| Standard list row | 44 | Minimum for comfortable tapping |
| Subtitle list row | 60 | Row with subtitle text |
| Text field / button | 44 | Minimum interactive height |
| Search bar | 36 | Inside navigation bar |

### Touch targets

**Minimum 44 × 44pt** for all interactive elements.  This is non-negotiable.

- If the visual element is smaller (e.g., a 24pt icon), extend the tap area
  with `.contentShape()` or padding.
- visionOS requires **60 × 60pt** minimum for hand interaction.

### Safe areas

- Use `safeAreaInset(edge:)` and `safeAreaPadding()` to respect system UI.
- Never clip content behind the status bar, home indicator, or Dynamic Island.
- SwiftUI `List` and `ScrollView` automatically adjust for safe areas.
- See the `device-geometry` skill for exact safe area values per device model.

### Layout rules

1. **Think in points, design in pixels.** All specs are in points; multiply by
   the device scale factor (@2x, @3x) for pixel rendering.
2. **Use system layout** (`NavigationStack`, `List`, `Form`) — they handle
   margins, separators, and safe areas correctly.
3. Align elements to the **8pt grid** where possible.
4. Never require horizontal scrolling for primary content.
5. Support both portrait and landscape unless the app has a strong reason not to.

---

## Part 5: Components Quick Reference

### Bars

| Component | Position | Key rules |
|-----------|----------|-----------|
| Navigation bar | Top | Shows title + back button. Use `.navigationTitle()` and `.toolbar {}`. Large title for root views, inline for pushed views. |
| Tab bar | Bottom | 3–5 tabs max (6+ triggers "More" on iPhone). Each tab is an SF Symbol + label. One tab always selected. Never hide programmatically. |
| Toolbar | Bottom (iPhone) / Top or bottom (iPad) | Action buttons for current context. Use `.toolbar { ToolbarItem(placement:) }`. |
| Search bar | Inside navigation bar | Use `.searchable(text:)`. Appears below navigation title. |

### Content

| Component | SwiftUI | Key rules |
|-----------|---------|-----------|
| List | `List` | Grouped or plain style. Rows ≥ 44pt. Supports swipe actions, selection. |
| Form | `Form` | Grouped list optimized for settings/input. Sections with headers/footers. |
| Table | `Table` | Multi-column (iPad/Mac). Not for iPhone — use List instead. |
| Label | `Label("text", systemImage:)` | Icon + text pair. Consistent alignment. |
| Text | `Text` | Apply text styles, not raw sizes: `.font(.body)`. |

### Controls

| Component | SwiftUI | Key rules |
|-----------|---------|-----------|
| Button | `Button` | Use `.buttonStyle(.bordered)` or `.borderedProminent` for emphasis. One prominent button per context. |
| Toggle | `Toggle` | For binary on/off. Label on left, switch on right. |
| Picker | `Picker` | Inline, wheel, segmented, or menu style. |
| Slider | `Slider` | Continuous value selection. Optional min/max labels. |
| Stepper | `Stepper` | Discrete increment/decrement. Small finite ranges. |
| DatePicker | `DatePicker` | Date and/or time selection. Compact, graphical, or wheel. |
| TextField | `TextField` | 44pt height. Use appropriate keyboard type (`.keyboardType()`). |
| SecureField | `SecureField` | Password input with masked text. |
| ProgressView | `ProgressView` | Determinate (bar) or indeterminate (spinner). |
| Gauge | `Gauge` | Display a value within a range. watchOS and widgets. |

### Presentation

| Component | SwiftUI | Key rules |
|-----------|---------|-----------|
| Sheet | `.sheet()` | Partial-height modal. Swipe-down to dismiss. For self-contained tasks. |
| Full-screen cover | `.fullScreenCover()` | Covers entire screen. Requires explicit dismiss button. |
| Popover | `.popover()` | Anchored to source. iPad/Mac — becomes sheet on iPhone. |
| Alert | `.alert()` | 1-2 buttons. Title + optional message. For critical decisions only. |
| Confirmation dialog | `.confirmationDialog()` | Action sheet replacement. Multiple options + cancel. |
| Menu | `Menu` | Contextual actions. Tap or long-press to reveal. |
| Context menu | `.contextMenu()` | Long-press on content for secondary actions. |

---

## Part 6: Navigation Patterns

### Structural patterns

| Pattern | Description | When to use | SwiftUI |
|---------|-------------|-------------|---------|
| **Hierarchical (drill-down)** | General → specific via cascading screens. Right = deeper, left = back. | Content with tree-like structure | `NavigationStack` / `NavigationSplitView` |
| **Flat (tab-based)** | Top-level sections in tab bar (iPhone) or sidebar (iPad). Each tab owns its own navigation state. | Apps with 3-5 distinct sections | `TabView` |
| **Content-driven** | Swipe between siblings at the same level. | Photo galleries, onboarding pages | `TabView(.page)` / `ScrollView(.paging)` |

### Overlay patterns

| Pattern | Description | When to use |
|---------|-------------|-------------|
| **Modal sheet** | Slides up from bottom. Blocks parent until dismissed. | Self-contained tasks (compose, add, edit) |
| **Full-screen modal** | Covers everything. Requires Done/Cancel. | Immersive experiences, media playback |
| **Popover** | Anchored floating view (iPad). Becomes sheet on iPhone. | Secondary content, configuration |
| **Alert** | Centered dialog with 1-2 buttons. | Critical decisions that need immediate attention |
| **Action sheet / confirmation dialog** | Bottom sheet with multiple options. | Choosing from several actions |

### Navigation rules

1. **Critical content within ≤ 3 taps** from launch.
2. **Always show where the user is** — navigation title, back button with
   parent label, highlighted tab.
3. **Support swipe-back** — never disable the edge-swipe gesture on
   `NavigationStack`.
4. **Minimize modality** — only present modally when a task must be completed
   or abandoned before continuing.
5. **Tab bar stays visible** unless covered by a modal sheet.  Never hide the
   tab bar within a navigation push.
6. **Max 5 tab bar items** on iPhone.  If you need more, use "More" tab or
   reorganize information architecture.
7. **Modal sheets need a clear dismiss** — "Done" / "Cancel" / "Save" button,
   plus swipe-down affordance.

---

## Part 7: App Icons

### Requirements

- **1024 × 1024px** single PNG, **RGB with no alpha channel**.
- Xcode 15+ / iOS 17+: a single `"idiom": "universal", "platform": "ios"` entry
  covers all iOS devices.  Mac Catalyst needs explicit 16–512pt @1x/@2x entries.
- The system applies the rounded superellipse mask — **never bake rounded corners
  into your icon artwork**.
- Icon should be recognizable at all sizes (down to 20pt in notifications).

### iOS 26 / Liquid Glass icons

From iOS 26, icons use an **automatic layered glass effect**.  Design with:
- Use **Icon Composer** (new Xcode tool) to define foreground, background, and
  optional middle layers.
- Keep the subject clearly separated from the background layer.
- Avoid text, fine details, and transparency in the foreground — the glass
  refraction effect will distort them.

### Dark mode & tinted icons (iOS 18+)

Provide three icon variants for the customizable home screen:
1. **Light** — standard appearance
2. **Dark** — adjusted for dark backgrounds
3. **Tinted** — monochromatic, adapts to user's chosen tint color

---

## Part 8: Accessibility Checklist

Every HIG-compliant app must support these:

### 1. Dynamic Type
- Use built-in text styles or `.relativeTo:` for custom fonts.
- Test at **every** size category, including accessibility sizes.
- Layouts must reflow — never truncate text at large sizes.

### 2. VoiceOver
- Every interactive element needs an accessibility label.
- Decorative images: `Image(...).accessibilityHidden(true)`.
- Meaningful images: `.accessibilityLabel("description")`.
- Custom controls: add `.accessibilityAddTraits(.isButton)`.

### 3. Color & contrast
- Minimum 4.5:1 for body text, 3:1 for large text.
- Never convey information through color alone — use icons, patterns, or text.
- Test with **Increase Contrast** setting enabled.

### 4. Reduce Motion
- Respect `@Environment(\.accessibilityReduceMotion)`.
- Replace sliding/bouncing animations with fades/dissolves.
- Disable auto-playing animations.

### 5. Touch accommodations
- All tap targets ≥ 44 × 44pt.
- Support both tap and long-press where appropriate.
- Test with **Switch Control** and **Voice Control**.

### 6. Smart Invert & Dark Mode
- Use semantic colors — they adapt automatically.
- Test that photos and full-color assets are not inverted.

---

## Part 9: Liquid Glass (iOS 26+)

Liquid Glass is Apple's new dynamic material introduced at WWDC25 (June 2025).
It refracts content below, reflects light around it, and has a lensing edge
effect.  All system controls adopt it automatically.

### Key design changes in iOS 26

| Element | Change |
|---------|--------|
| Tab bars | Shrink during scroll to prioritize content; expand fluidly on scroll-up |
| Navigation bars | Adopt translucent glass material with refraction |
| Controls / toolbars | Concentric with device rounded corners; grouped by function |
| App icons | Multi-layered with glass material; use Icon Composer for layers |
| Typography | SF Pro numerals dynamically scale weight/width on Lock Screen |
| Sidebars (iPad/Mac) | Refract background content, reflect wallpaper |

### Concentric design

Controls, windows, and UI elements now align concentrically with the device's
rounded hardware corners.  This means:
- Buttons inside cards should have smaller corner radii than their container.
- Nested rounded rectangles follow the rule: `inner_radius = outer_radius - padding`.
- This is the same math as in the `device-geometry` skill's squircle formula.

### Adopting Liquid Glass in code

- UIKit: use the new glass material APIs
- SwiftUI: system components adopt automatically; for custom views, use the
  new `.glassEffect()` modifier family
- Existing apps using standard components get the new look for free when
  compiled with the iOS 26 SDK

---

## Part 10: Platform Differences

| Aspect | iPhone | iPad | Mac (Catalyst / SwiftUI) |
|--------|--------|------|--------------------------|
| Navigation | Tab bar (bottom) | Sidebar + tab bar (adaptive) | Sidebar + toolbar |
| Margins | 16pt | 20pt | Varies with window size |
| Pointer | None | Optional (trackpad) | Primary input |
| Min tap target | 44 × 44pt | 44 × 44pt | 24 × 24pt (pointer precise) |
| Multitasking | None | Split View, Slide Over | Windows |
| Tab bar items | ≤ 5 | ≤ 7 | N/A (use sidebar) |
| Popover | Becomes sheet | Anchored popover | Anchored popover |
| Window size | Fixed (full screen) | Flexible (split) | Fully resizable |

---

## Part 11: What NOT To Do

These mistakes cause App Store rejections, bad reviews, or failed Apple Design
Award assessments.

1. **DO NOT hardcode font sizes** — use text styles (`.font(.body)`).
   Hardcoded sizes break Dynamic Type and accessibility.

2. **DO NOT make tap targets smaller than 44 × 44pt** — this is the single
   most common HIG violation and affects usability for millions of users.

3. **DO NOT use non-semantic colors** — `UIColor.red` is fixed; use
   `.systemRed` or SwiftUI's `.red` so it adapts to dark mode and accessibility.

4. **DO NOT convey information with color alone** — always pair with text, an
   icon, or a shape.  Color-blind users (8% of men) cannot rely on color.

5. **DO NOT hide the tab bar during navigation pushes** — it should remain
   visible at all times except behind modal sheets.

6. **DO NOT use custom navigation gestures that conflict with system gestures**
   — the left-edge swipe is for "back"; do not hijack it.

7. **DO NOT present alerts for non-critical information** — use inline messages,
   banners, or passive feedback instead.  Alerts interrupt flow and require action.

8. **DO NOT ignore safe areas** — content behind the notch, Dynamic Island,
   home indicator, or rounded corners is clipped or obscured.

9. **DO NOT skip dark mode** — if you use any custom colors, provide both
   light and dark variants.  Test thoroughly.

10. **DO NOT bake corner radius into app icon artwork** — the system applies
    the mask.  Including your own corners results in double-rounding.

11. **DO NOT rely on landscape-only or portrait-only** without good reason —
    support all orientations and let the user choose.

12. **DO NOT ignore Reduce Motion** — users who enable this setting may have
    vestibular disorders.  Respect `accessibilityReduceMotion`.

---

## Sources

- Apple Human Interface Guidelines: developer.apple.com/design/human-interface-guidelines
- Apple Design Tips: developer.apple.com/design/tips/
- WWDC24 HIG updates: createwithswift.com/wwdc24-whats-new-in-the-human-interface-guidelines/
- WWDC25 Liquid Glass: apple.com/newsroom/2025/06/apple-introduces-a-delightful-and-elegant-new-software-design/
- iOS navigation patterns: frankrausch.com/ios-navigation/
- Typography specs: learnui.design/blog/ios-font-size-guidelines.html
- Layout & spacing: gist.github.com/eonist/e79ca41b312362682343c41f63062734
