---
name: how-to-make-a-leaderboard
description: Delta-based multi-device Game Center leaderboard system for iOS/Mac games. Covers local delta accumulation, async upload with exponential backoff, per-category score tracking, offline resilience, data versioning for smooth upgrades, and unsent-data UI. Use when adding leaderboards or score tracking to any Apple platform game.
---

# How to Make a Leaderboard

A battle-tested, delta-based leaderboard system for iOS/Mac games using Game
Center.  Handles multiple devices, offline play, network failures, and schema
upgrades without losing a single point.

---

## Why Delta-Based

The naive approach — submit the device's total score — breaks with multiple
devices.  If iPad has 500 and iPhone has 300, whichever submits last wins and
the other device's points are lost.

The delta approach: each device tracks only the *new points earned since the
last successful upload*.  On upload it reads the current Game Center score,
adds the delta, and submits the sum.  Every device contributes; nothing is
lost.

---

## Part 1: Architecture Overview

```
Device A (offline)          Device B (online)         Game Center
─────────────────          ─────────────────         ────────────
earn +50 → delta=50        earn +30 → delta=30
earn +20 → delta=70        upload: read GC=100
  (upload fails,                   submit 100+30=130
   back off)                       delta=0            score=130
  ...net returns...
upload: read GC=130
       submit 130+70=200
       delta=0                                        score=200
```

Key invariant: Game Center is the authoritative cumulative score.  Devices
only ever *add* to it.

---

## Part 2: Data Model

### PlayerStats

```swift
struct PlayerStats: Codable {
    // -- version envelope --
    var dataFormatVersion: Int = 0
    var lastAppVersion: String = ""

    // -- scores --
    var totalScore: Int = 0
    var scoresByCategory: [String: Int] = [:]   // e.g. "level1": 450

    // -- other stats --
    var puzzlesSolved: Int = 0
    var wordsFound: Int = 0
    var bonusWordsFound: Int = 0
    var currentStreak: Int = 0
    var longestStreak: Int = 0
    var lastPlayedDate: Date?

    static let currentDataFormatVersion = 1

    /// Authoritative overall score — always use this for Game Center.
    var computedTotalScore: Int {
        scoresByCategory.values.reduce(0, +)
    }
}
```

### Version-Safe Decoding

Every field uses `decodeIfPresent` with a sensible default so old data never
crashes:

```swift
extension PlayerStats {
    init(from decoder: Decoder) throws {
        let c = try decoder.container(keyedBy: CodingKeys.self)
        dataFormatVersion    = try c.decodeIfPresent(Int.self,    forKey: .dataFormatVersion) ?? 0
        lastAppVersion       = try c.decodeIfPresent(String.self, forKey: .lastAppVersion) ?? ""
        totalScore           = try c.decodeIfPresent(Int.self,    forKey: .totalScore) ?? 0
        scoresByCategory     = try c.decodeIfPresent([String: Int].self, forKey: .scoresByCategory) ?? [:]
        puzzlesSolved        = try c.decodeIfPresent(Int.self,    forKey: .puzzlesSolved) ?? 0
        wordsFound           = try c.decodeIfPresent(Int.self,    forKey: .wordsFound) ?? 0
        bonusWordsFound      = try c.decodeIfPresent(Int.self,    forKey: .bonusWordsFound) ?? 0
        currentStreak        = try c.decodeIfPresent(Int.self,    forKey: .currentStreak) ?? 0
        longestStreak        = try c.decodeIfPresent(Int.self,    forKey: .longestStreak) ?? 0
        lastPlayedDate       = try c.decodeIfPresent(Date.self,   forKey: .lastPlayedDate)
    }
}
```

This is the core of smooth upgrades: new fields arrive with defaults, old
fields decode even if removed from a future version.

---

## Part 3: StatsManager (Local Persistence)

```swift
@MainActor
final class StatsManager: ObservableObject {
    static let shared = StatsManager()
    @Published private(set) var stats = PlayerStats()

    private let defaults = UserDefaults.standard
    private let statsKey = "playerStats"

    private init() {
        if let data = defaults.data(forKey: statsKey),
           let decoded = try? JSONDecoder().decode(PlayerStats.self, from: data) {
            self.stats = decoded
        }
        repairIfNeeded()
    }

    // --- version stamping + save ---

    private func save() {
        stats.dataFormatVersion = PlayerStats.currentDataFormatVersion
        stats.lastAppVersion = Self.appVersionString
        if let data = try? JSONEncoder().encode(stats) {
            defaults.set(data, forKey: statsKey)
        }
    }

    static var appVersionString: String {
        let v = Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "?"
        let b = Bundle.main.infoDictionary?["CFBundleVersion"] as? String ?? "?"
        return "\(v) (\(b))"
    }

    // --- migration repair ---

    /// On schema changes, totalScore can be reset to 0 while
    /// scoresByCategory survives.  Sync it back up.
    private func repairIfNeeded() {
        let computed = stats.computedTotalScore
        if computed > stats.totalScore {
            stats.totalScore = computed
            save()
        }
    }

    // --- scoring API ---

    func addScore(_ points: Int, category: String) {
        stats.scoresByCategory[category, default: 0] += points
        stats.totalScore += points
        save()
    }

    func recordPuzzleCompleted(category: String) {
        stats.puzzlesSolved += 1
        save()
    }
}
```

### Why Two Score Fields

`scoresByCategory` is the authoritative source (it survives migrations).
`totalScore` is kept for fast display.  `computedTotalScore` derives the
real total.  Game Center submissions always use `computedTotalScore`.

### Future Migrations

When `currentDataFormatVersion` bumps from 1 to 2, add migration logic:

```swift
private func repairIfNeeded() {
    if stats.dataFormatVersion < 1 {
        // migrate from v0 → v1
    }
    if stats.dataFormatVersion < 2 {
        // migrate from v1 → v2
    }
    // ... always repair totalScore
    let computed = stats.computedTotalScore
    if computed > stats.totalScore {
        stats.totalScore = computed
        save()
    }
}
```

---

## Part 4: LeaderboardUploader

This is the core of the delta system.  iOS only (`#if os(iOS)`), since
watchOS delegates to the phone.

### Storage Keys

```swift
private let pendingKey             = "pendingLeaderboardScores"       // [String: Int]
private let unsentGamesKey         = "unsentLeaderboardGames"         // Int
private let failureCountKey        = "leaderboardUploadFailures"      // Int
private let puzzlesSinceAttemptKey = "puzzlesSinceUploadAttempt"      // Int
```

Total footprint: ~60 bytes in UserDefaults.

### Full Implementation

```swift
import GameKit

@MainActor
final class LeaderboardUploader: ObservableObject {
    static let shared = LeaderboardUploader()

    @Published private(set) var pendingDeltas: [String: Int] = [:]
    @Published private(set) var unsentGameCount: Int = 0

    private var consecutiveFailures: Int = 0
    private var puzzlesSinceLastAttempt: Int = 0
    private var isUploading = false
    private let defaults = UserDefaults.standard

    // -- keys --
    private let pendingKey             = "pendingLeaderboardScores"
    private let unsentGamesKey         = "unsentLeaderboardGames"
    private let failureCountKey        = "leaderboardUploadFailures"
    private let puzzlesSinceAttemptKey = "puzzlesSinceUploadAttempt"

    private init() {
        if let data = defaults.data(forKey: pendingKey),
           let decoded = try? JSONDecoder().decode([String: Int].self, from: data) {
            pendingDeltas = decoded
        }
        unsentGameCount         = defaults.integer(forKey: unsentGamesKey)
        consecutiveFailures     = defaults.integer(forKey: failureCountKey)
        puzzlesSinceLastAttempt = defaults.integer(forKey: puzzlesSinceAttemptKey)
    }

    // ── delta accumulation ──────────────────────────────────────

    var totalPendingDelta: Int { pendingDeltas.values.reduce(0, +) }
    var hasPendingScores: Bool { totalPendingDelta > 0 }

    func addPending(_ points: Int, for category: String) {
        pendingDeltas[category, default: 0] += points
        savePending()
    }

    // ── upload trigger ──────────────────────────────────────────

    func recordGameCompleted() {
        unsentGameCount += 1
        puzzlesSinceLastAttempt += 1
        defaults.set(unsentGameCount, forKey: unsentGamesKey)
        defaults.set(puzzlesSinceLastAttempt, forKey: puzzlesSinceAttemptKey)

        if shouldAttemptUpload() {
            Task { await upload() }
        }
    }

    /// Manual trigger — call from leaderboard view onAppear or game start.
    func attemptUpload() {
        guard !isUploading, totalPendingDelta > 0 else { return }
        Task { await upload() }
    }

    // ── exponential backoff ─────────────────────────────────────

    private func shouldAttemptUpload() -> Bool {
        guard consecutiveFailures > 0 else { return true }
        let interval = min(1 << consecutiveFailures, 16)   // 2, 4, 8, 16
        return puzzlesSinceLastAttempt >= interval
    }

    // ── core upload ─────────────────────────────────────────────

    private func upload() async {
        guard GKLocalPlayer.local.isAuthenticated else { return }
        guard totalPendingDelta > 0 else { return }
        guard !isUploading else { return }
        isUploading = true
        defer { isUploading = false }

        let snapshot = pendingDeltas
        let snapshotGameCount = unsentGameCount
        var sentDeltaTotal = 0
        var anyFailure = false

        // Per-category uploads
        for (category, delta) in snapshot where delta > 0 {
            let leaderboardID = leaderboardID(for: category)
            do {
                let current = try await loadCurrentScore(for: leaderboardID)
                try await submitScore(current + delta, to: [leaderboardID])

                // Immediately subtract and persist — atomic per category
                pendingDeltas[category, default: 0] -= delta
                if pendingDeltas[category, default: 0] <= 0 {
                    pendingDeltas.removeValue(forKey: category)
                }
                savePending()
                sentDeltaTotal += delta
            } catch {
                print("Leaderboard upload failed for \(category): \(error)")
                anyFailure = true
            }
        }

        // Overall leaderboard (sum of what was actually sent)
        if sentDeltaTotal > 0 {
            do {
                let current = try await loadCurrentScore(for: overallLeaderboardID)
                try await submitScore(current + sentDeltaTotal, to: [overallLeaderboardID])
            } catch {
                print("Overall leaderboard upload failed: \(error)")
                anyFailure = true
            }
        }

        // Bookkeeping
        if !anyFailure {
            unsentGameCount = max(0, unsentGameCount - snapshotGameCount)
            consecutiveFailures = 0
        } else if sentDeltaTotal == 0 {
            consecutiveFailures += 1
        }
        puzzlesSinceLastAttempt = 0
        savePending()
        saveBackoffState()
    }

    // ── Game Center helpers ─────────────────────────────────────

    private func loadCurrentScore(for leaderboardID: String) async throws -> Int {
        let boards = try await GKLeaderboard.loadLeaderboards(IDs: [leaderboardID])
        guard let board = boards.first else { return 0 }
        let (localEntry, _, _) = try await board.loadEntries(
            for: .global, timeScope: .allTime,
            range: NSRange(location: 1, length: 1))
        return localEntry?.score ?? 0
    }

    private func submitScore(_ score: Int, to ids: [String]) async throws {
        try await withCheckedThrowingContinuation { (cont: CheckedContinuation<Void, Error>) in
            GKLeaderboard.submitScore(score, context: 0, player: GKLocalPlayer.local,
                                      leaderboardIDs: ids) { error in
                if let error { cont.resume(throwing: error) }
                else { cont.resume() }
            }
        }
    }

    // ── persistence ─────────────────────────────────────────────

    private func savePending() {
        if let data = try? JSONEncoder().encode(pendingDeltas) {
            defaults.set(data, forKey: pendingKey)
        }
        defaults.set(unsentGameCount, forKey: unsentGamesKey)
    }

    private func saveBackoffState() {
        defaults.set(consecutiveFailures, forKey: failureCountKey)
        defaults.set(puzzlesSinceLastAttempt, forKey: puzzlesSinceAttemptKey)
    }

    // ── leaderboard IDs (customize per game) ────────────────────

    /// Replace this with your game's bundle-id-based leaderboard IDs.
    var overallLeaderboardID: String { "com.yourcompany.yourgame.leaderboard.overall" }

    func leaderboardID(for category: String) -> String {
        "com.yourcompany.yourgame.leaderboard.\(category)"
    }
}
```

---

## Part 5: Game Center Leaderboard Configuration

### Leaderboard Types

You need N+1 leaderboards in App Store Connect:

  Leaderboard              Score Type         Why
  ────────────────────     ─────────────      ──────────────────────────────
  Per-category (N)         Best Score          Competitive ranking per category
  Overall (1)              Most Recent Score   Must accept every submission

The overall leaderboard **must** be Most Recent Score.  If it were Best Score,
a device that was offline for a long time would read a stale baseline, add its
delta, and submit a value lower than the current best — Game Center would
silently discard it, losing those points.

### Leaderboard ID Convention

```
com.<company>.<game>.leaderboard.<category>
com.<company>.<game>.leaderboard.overall
```

---

## Part 6: Wiring Into the Game

### When a Round Scores Points

```swift
func recordScore(_ points: Int, category: String) {
    // 1. Update local stats (for display)
    StatsManager.shared.addScore(points, category: category)

    // 2. Accumulate delta (for upload)
    #if os(iOS)
    LeaderboardUploader.shared.addPending(points, for: category)
    #endif
}
```

### When a Round Completes

```swift
func roundCompleted(category: String) {
    StatsManager.shared.recordPuzzleCompleted(category: category)

    #if os(iOS)
    LeaderboardUploader.shared.recordGameCompleted()
    #endif
}
```

### On App Launch / Leaderboard View Open

```swift
#if os(iOS)
LeaderboardUploader.shared.attemptUpload()
#endif
```

This catches any deltas left over from a previous session.

---

## Part 7: Unsent-Data UI Indicator

Show a notice when the device has scores that haven't reached Game Center:

```swift
@ObservedObject private var uploader = LeaderboardUploader.shared

if uploader.unsentGameCount > 0 {
    HStack(spacing: 8) {
        Image(systemName: "icloud.and.arrow.up")
            .foregroundStyle(.secondary)
        Text("Results of \(uploader.unsentGameCount) "
             + "\(uploader.unsentGameCount == 1 ? "game" : "games") "
             + "not yet sent from this device")
            .font(.caption)
            .foregroundStyle(.secondary)
    }
    .padding(12)
    .frame(maxWidth: .infinity, alignment: .leading)
    .background(RoundedRectangle(cornerRadius: 12).fill(.ultraThinMaterial))
    .padding(.horizontal)
}
```

---

## Part 8: Data Versioning for Smooth Upgrades

The versioning system ensures players never lose data when the app updates.

### Principles

1. **Every persisted struct gets a `dataFormatVersion` field.**
   Old data without it decodes as 0.  Current version is a static constant.

2. **Every field uses `decodeIfPresent` with a default.**
   New fields appear silently.  Removed fields are ignored.  No crashes.

3. **Every save stamps the current version and app version.**
   This makes it possible to diagnose issues from the data alone.

4. **Repair runs on every launch.**
   `StatsManager.init()` checks invariants and fixes drift.  This catches
   problems from interrupted migrations or schema changes.

5. **Keep a derived authoritative field.**
   `computedTotalScore` (sum of per-category scores) is always correct even
   if `totalScore` gets reset during a migration.  Game Center submissions
   always use the derived value.

6. **Never downgrade.**
   Repair logic uses `if computed > stats.totalScore` — it only ratchets up.

### Migration Template

```swift
private func repairIfNeeded() {
    // Version-gated migrations
    if stats.dataFormatVersion < 1 {
        // e.g., populate scoresByCategory from legacy totalScore
    }
    if stats.dataFormatVersion < 2 {
        // future migration
    }

    // Invariant repairs (run every time)
    let computed = stats.computedTotalScore
    if computed > stats.totalScore {
        stats.totalScore = computed
        save()   // save() stamps currentDataFormatVersion
    }
}
```

### What Can Go Wrong Without Versioning

- Add a new field → old data decodes with Swift's zero-value → scores reset
  to 0.  Fix: `decodeIfPresent` with explicit default.
- Rename a field → old data's value is lost.  Fix: keep the old CodingKey
  and decode from it during migration, then save under the new key.
- Remove a field → future downgrades crash.  Fix: `decodeIfPresent` on all
  fields so unknown keys are silently ignored.

---

## Part 9: Exponential Backoff Schedule

Backoff is measured in *games completed*, not wall-clock time, because the
user may close the app for days.

  Consecutive Failures     Games Before Retry
  ────────────────────     ──────────────────
  0                        immediate
  1                        2
  2                        4
  3                        8
  4+                       16 (cap)

```swift
let interval = min(1 << consecutiveFailures, 16)
```

On full success: reset `consecutiveFailures` to 0.
On partial success (some categories sent): leave failure count unchanged.
On total failure: increment failure count.

---

## Part 10: watchOS / Multi-Platform Notes

watchOS cannot talk to Game Center directly.  The recommended pattern:

1. Watch writes pending deltas to **App Group** UserDefaults under a
   separate key (e.g., `watchPendingLeaderboardScores`).
2. iPhone checks the App Group key at upload time.
3. iPhone merges watch deltas into its own pending deltas before uploading.
4. iPhone clears the watch key after a successful upload.

The watch never submits to Game Center.  The phone is the single uploader.

---

## Part 11: Common Mistakes

**DO NOT submit the total score directly.**
This is the #1 mistake.  It causes data loss on multi-device.

**DO NOT use Best Score for the overall leaderboard.**
Use Most Recent Score.  Otherwise, a returning offline device submits a
value lower than the current best and Game Center silently discards it.

**DO NOT zero the delta table on success.**
Subtract the snapshot that was sent.  A game may finish during the upload,
adding new points.  Zeroing would lose those points.

**DO NOT retry on a tight timer.**
Back off by games played, not seconds.  A device in airplane mode for hours
should not queue up hundreds of retry attempts.

**DO NOT skip the version envelope.**
Without `dataFormatVersion` and `decodeIfPresent`, adding a single field to
`PlayerStats` can silently zero out every existing player's scores.

---

## Part 12: Testing Checklist

- [ ] Earn points, kill the app before upload, relaunch — delta survives
- [ ] Airplane mode: play several games, turn off airplane — all points upload
- [ ] Two devices: play offline on both, connect both — GC total = sum of both
- [ ] Play a game while an upload is in-flight — those points are not lost
- [ ] Unsent-games badge shows correct count and clears after upload
- [ ] Bump `currentDataFormatVersion`, add a field — old data loads without loss
- [ ] `computedTotalScore` always matches sum of `scoresByCategory`

---

## Part 13: File Layout

```
Shared/
├── Models/
│   └── GameModels.swift          # PlayerStats, category enum, constants
├── Services/
│   ├── StatsManager.swift        # Local stats, versioning, repair
│   └── LeaderboardUploader.swift # Delta tracking, upload, backoff
└── Views/
    └── LeaderboardView.swift     # GC display + unsent-data indicator
```

Total implementation: ~300 lines across three files.
