---
name: watchos-hig
description: Apple Human Interface Guidelines reference for watchOS app design. Covers display specs (all Apple Watch sizes), typography (SF Compact text styles), layout (margins, spacing, round display considerations), navigation (watchOS 10 vertical TabView, NavigationSplitView), Digital Crown interaction, complications (WidgetKit families), notifications (short/long look), Always On display, Smart Stack, accessibility, and Liquid Glass (watchOS 26). Use when building watchOS UI, choosing fonts/layout, or reviewing watch app design compliance.
---

# Apple watchOS Human Interface Guidelines — Quick Reference

Precise specifications and decision rules for building HIG-compliant watchOS
apps in SwiftUI.  Every value in this document comes from Apple's published
guidelines or measured from system defaults.  Use these numbers — do not guess.

---

## Part 1: Core Design Philosophy

Apple Watch is a **personal, glanceable** device worn on the wrist.  Design
priorities differ fundamentally from iPhone/iPad:

| Principle | Meaning |
|-----------|---------|
| **Glanceable** | Interactions should take under 10 seconds. Show critical information immediately, single-screen when possible |
| **Actionable** | Every piece of information should lead to a clear, simple action |
| **Responsive** | Use on-device data (location, time, health) to anticipate needs and surface relevant content |
| **Lightweight** | Minimize navigation depth. One or two taps to accomplish a task |

### The "Apple Watch Moment"

Design your app around a single, focused interaction — the thing a user needs
most when they glance at their wrist.  Everything else is secondary.

### Input Methods

| Input | Use for |
|-------|---------|
| **Digital Crown** | Vertical scrolling, value selection, data inspection |
| **Tap** | Primary selection and activation |
| **Swipe** | Page navigation, dismiss, lateral movement |
| **Long press** | Secondary actions, context menus |
| **Action Button** (Ultra) | Quick-launch essential actions without looking |
| **Siri** | Voice input, shortcuts, hands-free interaction |

### Sensors Available for Context

GPS, heart rate, blood oxygen, altimeter, accelerometer, gyroscope,
ambient light, skin temperature, water temperature (Ultra).  Use sensor
data to make your app proactively relevant.

---

## Part 2: Display Specifications

### Current Apple Watch models (points @ 2x)

| Model | Case | Resolution (px) | PPI | Display area |
|-------|------|-----------------|-----|--------------|
| Series 4–6, SE (1st) | 40mm | 324 × 394 | 326 | 759 mm² |
| Series 4–6 | 44mm | 368 × 448 | 326 | 977 mm² |
| Series 7–9, SE (2nd/3rd) | 41mm | 352 × 430 | 326 | 904 mm² |
| Series 7–9 | 45mm | 396 × 484 | 326 | 1143 mm² |
| Series 10 | 42mm | 374 × 446 | 326 | 989 mm² |
| Series 10 | 46mm | 416 × 496 | 326 | 1220 mm² |
| Ultra 1–2 | 49mm | 410 × 502 | 338 | 1185 mm² |

### Legacy models (still supported by recent watchOS)

| Model | Case | Resolution (px) |
|-------|------|-----------------|
| Series 1–3 | 38mm | 272 × 340 |
| Series 1–3 | 42mm | 312 × 390 |

All current models feature Always-On LTPO OLED Retina displays.  Brightness
ranges from 1 nit (Always On dimmed) to 2000 nits (max outdoor).

### Display characteristics

- **Edge-to-edge**: No bezel gap — content extends to rounded display edges.
- **Rounded corners**: The display corners follow the case contour. Use system
  layout containers which respect this automatically.
- **Scale factor**: All current models are @2x.

---

## Part 3: Typography

### System font

**San Francisco Compact (SF Compact)** is the system typeface for watchOS.
Three variants:

| Variant | Use for |
|---------|---------|
| SF Compact Text | General UI text (below 20pt) |
| SF Compact Display | Large text (20pt and above) |
| SF Compact Rounded | Complications, gauges, informal contexts |

SF Compact shares features with SF Pro but has a more efficient, compact
design optimized for small sizes and narrow columns.  SwiftUI selects the
correct variant automatically.

### Text styles — watchOS default sizes

watchOS uses the same SwiftUI text style API as iOS, but sizes are smaller
to fit the watch display:

| Text Style | SwiftUI | watchOS Size (pt) | Weight |
|------------|---------|-------------------|--------|
| Large Title | `.largeTitle` | 28 | Regular |
| Title 1 | `.title` | 23 | Regular |
| Title 2 | `.title2` | 19 | Regular |
| Title 3 | `.title3` | 17 | Regular |
| Headline | `.headline` | 15 | **Semi-Bold** |
| Body | `.body` | 15 | Regular |
| Callout | `.callout` | 14 | Regular |
| Subheadline | `.subheadline` | 14 | Regular |
| Footnote | `.footnote` | 12 | Regular |
| Caption 1 | `.caption` | 13 | Regular |
| Caption 2 | `.caption2` | 13 | Regular |

Note: On watchOS, `.footnote` is **smaller** than `.caption` and `.caption2`,
which differs from the iOS ordering.

### Dynamic Type on watchOS

watchOS supports 7 Dynamic Type size categories (fewer than iOS):

    xSmall → small → medium → large (DEFAULT) → xLarge → xxLarge → xxxLarge

The largest Dynamic Type size on watchOS is approximately **150%** of the
default — significantly less range than iOS accessibility sizes.

### Typography rules

1. **Always use built-in text styles** (`.font(.body)`) — they support Dynamic Type
   and use SF Compact automatically.
2. **Tight leading** is applied system-wide on watchOS to maximize content density.
   Tight leading adjusts by ±1pt (vs ±2pt on iOS).
3. **Body text minimum**: 12pt for readability on the small display.
4. **Limit text**: Show essential information only. Long paragraphs are
   inappropriate for the watch — summarize and link to iPhone for details.
5. **SF Compact Rounded** for complications — it's the standard in that context.

---

## Part 4: Color & Materials

### Dark-first design

watchOS uses a **true black background** (OLED pixel-off) by default.  This
saves battery and emphasizes vibrancy.  All the system colors from iOS are
available and adapt to the dark context:

| SwiftUI | Use |
|---------|-----|
| `.red` | Destructive, health alerts, stop |
| `.orange` | Warnings, workout metrics |
| `.yellow` | Caution |
| `.green` | Success, start, activity rings |
| `.blue` | Default tint, interactive elements |
| `.cyan` | Information |
| `.teal` | Secondary accent |
| `.purple` | Premium |
| `.pink` | Heart rate, social |

### Background materials (watchOS 10+)

watchOS 10 introduced **background materials** that provide a sense of depth
and place.  Use the `.containerBackground()` modifier to set gradient or
color fills behind views.

```swift
NavigationStack {
    MyDetailView()
}
.containerBackground(.blue.gradient, for: .navigation)
```

Key behaviors:
- Background colors animate during push/pop transitions
- Each tab or detail view can have its own background
- System blur materials automatically adapt to content behind them

### Color rules

1. **True black background** — the default. Extend content edge-to-edge against it.
2. **Full-screen color** — watchOS 10+ celebrates the display shape with vivid
   background gradients. Use `.containerBackground()` to fill the screen.
3. **High contrast on dark** — ensure all text meets 4.5:1 contrast against
   the actual background (not just black).
4. **Activity ring colors** — red (Move), green (Exercise), cyan (Stand) are
   system-reserved. Avoid using them for unrelated purposes.
5. **Complications**: Use full-color mode for graphic complications. The system
   may render your complication in tinted or reduced-color modes.

---

## Part 5: Layout & Spacing

### Content area

watchOS extends content **edge-to-edge** across the round display.  The system
applies safe area insets for the curved corners automatically.

### Layout tokens

| Token | Value | Use |
|-------|-------|-----|
| XS | 2pt | Tight spacing between related elements |
| S | 4pt | Icon-to-label gap |
| M | 8pt | Between items in a group |
| L | 16pt | Section separation |

### Margins

The system provides automatic leading/trailing margins that account for the
rounded display.  Do not override them — content near the display edges will
be clipped by the physical corner radius.

### Touch targets

**Minimum 44pt height** for tappable elements (same as iOS).  On the small
watch display this is proportionally even more important.

- Buttons should span the **full width** of the display when possible
- Side-by-side buttons: **maximum 2–3** buttons per row
- Minimize padding between elements to maximize usable space

### Component heights

| Component | Height (pt) | Notes |
|-----------|-------------|-------|
| Navigation bar | ~36 | Automatically managed, includes time display |
| List row | 44 | Minimum comfortable tap target |
| Button (full-width) | 44 | Standard watchOS button height |
| Toolbar item | 36 | Top or bottom bar |

### Layout rules

1. **Edge-to-edge content** — fill the entire display. The system handles
   safe areas for the round corners.
2. **Single-column layout** — never attempt multi-column layouts on watch.
3. **Vertical scrolling only** — horizontal scrolling is reserved for
   system gestures (page navigation).
4. **Minimize scrolling** — if content requires extensive scrolling, consider
   splitting across vertical tabs instead.
5. **Full-width buttons** — buttons look best spanning the full width.
6. **No more than 2–3 side-by-side controls** in any row.

---

## Part 6: Navigation Patterns (watchOS 10+)

watchOS 10 redesigned navigation to be consistent and predictable.  Three
primary structures:

### NavigationSplitView (source list + detail)

Use when your app has a **list of items with detail views** (e.g., Weather
cities, stock tickers).

```swift
NavigationSplitView {
    List(cities) { city in
        NavigationLink(city.name, value: city)
    }
} detail: {
    CityDetailView(city: selectedCity)
}
```

Key behaviors:
- The source list is **tucked beneath the detail view** — scroll up past the
  top of the detail to reveal it
- App launches directly into the **detail view** (most relevant item)
- Digital Crown scrolls through the detail; scrolling past the top reveals
  the source list

### Vertical TabView (page-based)

Use when your app has **distinct sections** of equal importance (e.g., Activity
rings, heart rate, workout summary).

```swift
TabView {
    SummaryTab()
    HeartRateTab()
    ActivityTab()
}
.tabViewStyle(.verticalPage)
```

Key behaviors:
- **Digital Crown** drives vertical page switching
- Each tab is a **full-screen view** with a distinct purpose
- Individual tabs can expand and resize as needed (watchOS 10+)
- Page indicators appear on the trailing edge

### NavigationStack (hierarchical)

Use for **drill-down navigation** within a tab or detail view.

```swift
NavigationStack {
    List(items) { item in
        NavigationLink(item.title, value: item)
    }
    .navigationDestination(for: Item.self) { item in
        ItemDetailView(item: item)
    }
}
```

### Choosing a navigation pattern

| Pattern | When to use | Example apps |
|---------|-------------|--------------|
| NavigationSplitView | Source list → detail | Weather, Stocks, Mail |
| Vertical TabView | Distinct equal sections | Activity, Heart Rate |
| NavigationStack | Drill-down hierarchy | Settings, Messages |
| Single view | One-screen apps | Timer, Stopwatch |

### Navigation rules

1. **Land on the most useful view** — don't make users navigate to their goal.
2. **Minimize depth** — accomplish the "Apple Watch Moment" in 1–2 interactions.
3. **Digital Crown for vertical navigation** — scrolling within a view and
   switching between tabs.
4. **Swipe left from edge** for back navigation (system gesture — never override).
5. **Use `.containerBackground()`** on each view — different background colors
   help users orient across views.
6. **Toolbar items**: use `.toolbar { }` with `topBarLeading`, `topBarTrailing`,
   and `bottomBar` placements.

---

## Part 7: Digital Crown

The Digital Crown is the **primary input mechanism** for watchOS, alongside tap.

### Usage patterns

| Interaction | API | Use for |
|-------------|-----|---------|
| Scrolling | Automatic in `List`, `ScrollView` | Default vertical scroll |
| Page switching | `.tabViewStyle(.verticalPage)` | Switch between full-screen tabs |
| Value selection | `.digitalCrownRotation()` | Adjust numeric values, pick from ranges |
| Zooming | `.digitalCrownRotation()` with scale | Map zoom, image inspection |

### `.digitalCrownRotation()` modifier

```swift
@State private var value = 0.0

MyView()
    .digitalCrownRotation(
        $value,
        from: 0, through: 100,
        by: 1,                    // stride for haptic detents
        sensitivity: .medium,
        isContinuous: false,
        isHapticFeedbackEnabled: true
    )
```

Parameters:
- `from`/`through`: Value range
- `by`: Stride — provides haptic "clicks" at each step
- `sensitivity`: `.low`, `.medium`, `.high` — how fast values change per rotation
- `isContinuous`: If `true`, wraps from max back to min
- `isHapticFeedbackEnabled`: Haptic detent feedback (default `true`)

### Design rules

1. **Always provide haptic feedback** when Crown adjusts discrete values.
2. **Show the current value** prominently — users look at the screen, not the Crown.
3. **Crown scrolling should feel natural** — large lists scroll, small ranges click.
4. **Don't fight the system** — if a `List` or `ScrollView` is present, the Crown
   scrolls it. Don't also bind a Crown rotation to the same view.

---

## Part 8: Complications (WidgetKit)

Complications display information on the **watch face** — they are often the
primary way users interact with your app.

### Complication families (watchOS 9+ / WidgetKit)

| WidgetFamily | Shape | Content guidance |
|--------------|-------|-----------------|
| `accessoryCircular` | Circle | Brief info, gauges, progress rings, small icons |
| `accessoryCorner` | Corner arc | Curved text/gauge wrapping a circular icon |
| `accessoryRectangular` | Rectangle | Multiple lines of text, small charts, detailed info |
| `accessoryInline` | Single text line | One line of text, shown above the time on many faces |

### Legacy families (ClockKit — deprecated but still rendered)

The legacy 12 families (Modular Small/Large, Utilitarian Small/Flat/Large,
Circular Small, Extra Large, Graphic Circular/Corner/Rectangular/Bezel)
have been consolidated into the four WidgetKit families above.

### Complication design rules

1. **Show the most important single data point** — complications are glanceable.
2. **Update frequently** — stale data erodes trust. Use timeline entries.
3. **Design for all families** — support at least `accessoryCircular` and
   `accessoryRectangular` for maximum face compatibility.
4. **Full-color for Graphic faces** — use vivid colors on faces that support
   full-color rendering.
5. **Respect tinting** — the system may render your complication in the user's
   chosen tint color or in reduced color. Use `AccessoryWidgetGroup` to handle
   color adaptation.
6. **Tap opens your app** — tapping a complication always launches your app.
   Deep-link to the relevant context.
7. **SF Compact Rounded** is the standard font for complication text.

---

## Part 9: Notifications

### Short Look

Displayed briefly when a notification arrives and the user raises their wrist.

- **System-generated** — you cannot customize the layout
- Shows: app icon, app name, notification title
- Tapping or keeping wrist raised transitions to the Long Look

### Long Look

The expanded notification view. Customizable.

| Section | Source | Customizable? |
|---------|--------|---------------|
| Sash (header) | System | Color only (tint) |
| Content area | Your app | Yes — custom `WKUserNotificationHostingController` |
| Action buttons | Your app | Yes — define notification actions |
| Dismiss button | System | No (always present at bottom) |

### Notification design rules

1. **Timely and high-value** — only send notifications worth a wrist raise.
2. **Actionable** — include 1–2 action buttons (e.g., "Reply", "Archive").
3. **Concise content** — assume 2–3 seconds of reading time.
4. **Custom Long Look** — use a custom interface to show rich, relevant
   information. Include images or graphics when they add value.
5. **Maximum 4 action buttons** in the Long Look interface.
6. **Deep-link** — tapping the notification body should open the app to the
   relevant content.

---

## Part 10: Always On Display

Available on Series 5+ and Ultra.  Your app remains visible when the user
lowers their wrist, in a **dimmed state**.

### `isLuminanceReduced` environment property

```swift
@Environment(\.isLuminanceReduced) var isLuminanceReduced

var body: some View {
    MyView()
        .opacity(isLuminanceReduced ? 0.5 : 1.0)
}
```

### Design rules for Always On

1. **Highlight essential info** — when luminance is reduced, dim or hide
   secondary elements. Keep the most important data visible.
2. **Redact sensitive data** — account numbers, balances, personal health
   data should be obscured when the wrist is down.
3. **Reduce large color fills** — replace filled shapes with stroked outlines
   to save power and maintain visibility.
4. **Freeze animations** — reset to the first frame or resolve to a rested
   state. Do not leave animations mid-cycle.
5. **Remove transient elements** — tooltips, progress indicators, and ephemeral
   UI should be hidden in the dimmed state.
6. **Update sparingly** — the system limits updates in the dimmed state to
   save battery. Use `TimelineView` for time-based updates.

---

## Part 11: Smart Stack & Watch Faces (watchOS 10+)

### Smart Stack

The Smart Stack is accessed by **scrolling up from the watch face** with the
Digital Crown.  It shows a stack of widgets ordered by predicted relevance.

- Widgets use the same WidgetKit families as complications
- The system predicts which widgets to surface based on time, location,
  activity, and routine
- **watchOS 26**: Smart Stack Relevance API lets you provide signals for
  when your widget is most relevant

### Smart Stack Relevance API (watchOS 26)

```swift
// Points of Interest — surface widget near specific locations
RelevanceProvider {
    PointOfInterestRelevance(location: groceryStore)
}
```

### Control Widget API (watchOS 26)

Create custom controls that appear in Control Center, Action Button, or
Smart Stack:

- iOS controls automatically share to watchOS 26
- Use WidgetKit's `ControlWidget` API
- Controls perform single actions (toggle, launch, trigger)

---

## Part 12: App Lifecycle

### Background tasks

watchOS strictly limits background execution.  Use:
- `WKApplicationRefreshBackgroundTask` for periodic updates
- `WKURLSessionRefreshBackgroundTask` for network downloads
- `WKSnapshotRefreshBackgroundTask` for UI snapshot updates

### Workout sessions

For fitness apps, `HKWorkoutSession` provides extended background execution
during active workouts with access to:
- Heart rate streaming
- Location updates
- Motion data

### App states

| State | Behavior |
|-------|----------|
| Active | Full interaction, screen is on |
| Inactive | Screen on but not interactive (e.g., transitioning) |
| Background | Limited execution, no UI updates visible |
| Always On (dimmed) | Reduced luminance, limited updates |
| Suspended | No execution until next launch |

---

## Part 13: Accessibility

### watchOS-specific accessibility considerations

1. **Dynamic Type** — support all 7 size categories. Test at `xxxLarge`.
   Layouts must reflow, never truncate.

2. **VoiceOver** — label all interactive elements. The small screen makes
   VoiceOver critical for users with low vision. Digital Crown navigates
   between elements in VoiceOver mode.

3. **Reduce Motion** — respect `@Environment(\.accessibilityReduceMotion)`.
   Replace animations with fades. Especially important because watch
   motion can cause more discomfort than phone motion.

4. **Bold Text** — when the user enables Bold Text, all system text
   becomes bold. Test that your layouts accommodate the wider glyphs.

5. **Extra Large accessibility text style** — complications and widgets
   can use the `accessoryWidgetBackground` size when the user selects
   the Extra Large watch face.

6. **Touch accommodations** — maintain 44pt minimum tap targets despite
   the small screen. Full-width buttons are the safest choice.

7. **Haptic feedback** — supplement visual feedback with haptics for
   users who may not be looking at the screen. Use `WKInterfaceDevice.play()`
   or `.sensoryFeedback()` in SwiftUI.

---

## Part 14: Liquid Glass (watchOS 26)

Liquid Glass arrives on watchOS 26, bringing the new design language from
iOS 26 to the watch.

### Key changes

| Element | Change |
|---------|--------|
| Smart Stack | Rendered with Liquid Glass material |
| Control Center | Glass-effect controls |
| Navigation controls | Translucent glass bars and toolbars |
| App icons | Multi-layered glass effect (use Icon Composer) |
| Widgets & complications | Glass-tinted presentation in Smart Stack |

### Adopting Liquid Glass

- Apps using standard SwiftUI components get the new look automatically
  when compiled with the watchOS 26 SDK
- Use `.glassEffect()` modifiers for custom views
- Design app icons with multiple layers using Icon Composer
- Existing `containerBackground()` gradients work naturally with the
  glass material

---

## Part 15: What NOT To Do

These mistakes cause poor watchOS experiences and potential App Store issues.

1. **DO NOT port your iPhone app layout** — watch apps need completely
   different information architecture. Redesign for glanceability.

2. **DO NOT require extensive text input** — use preset replies, voice
   dictation, or scribble. Never present a full keyboard equivalent.

3. **DO NOT create deep navigation hierarchies** — more than 2–3 levels
   deep is too many for the watch. Flatten your structure.

4. **DO NOT ignore the Digital Crown** — it is the primary navigation
   device. Ensure scrolling and value selection work with it.

5. **DO NOT hardcode font sizes** — use text styles (`.font(.body)`).
   SF Compact is selected automatically.

6. **DO NOT use tap targets smaller than 44pt** — the small screen and
   imprecise wrist interaction make this even more critical than on iPhone.

7. **DO NOT send excessive notifications** — each notification demands a
   wrist raise. Only notify for timely, actionable information.

8. **DO NOT ignore Always On** — if your app displays sensitive data,
   you must redact it when `isLuminanceReduced` is true.

9. **DO NOT block the main thread** — watchOS has strict memory and
   execution limits. Heavy computation causes termination.

10. **DO NOT rely on continuous network connectivity** — the watch may
    be on Bluetooth relay, Wi-Fi, or cellular. Design for offline-first
    and sync when possible.

11. **DO NOT use horizontal scrolling** — it conflicts with system
    swipe-to-go-back and page navigation gestures.

12. **DO NOT ignore complications** — for many users, the complication
    IS your app. A watch app without complications misses the platform's
    primary interaction model.

---

## Sources

- Apple Human Interface Guidelines — Designing for watchOS: developer.apple.com/design/human-interface-guidelines/designing-for-watchos
- watchOS 10 UI guidance: developer.apple.com/documentation/watchos-apps/creating-an-intuitive-and-effective-ui-in-watchos-10
- WWDC23 — Design and build apps for watchOS 10: developer.apple.com/videos/play/wwdc2023/10138/
- WWDC25 — What's new in watchOS 26: developer.apple.com/videos/play/wwdc2025/334/
- Always On display design: developer.apple.com/documentation/watchos-apps/designing-your-app-for-the-always-on-state
- Creating complications with WidgetKit: developer.apple.com/documentation/widgetkit/creating-accessory-widgets-and-watch-complications
- Apple Watch technical specs: apple.com/apple-watch-series-10/specs/
- San Francisco font family: developer.apple.com/fonts/
