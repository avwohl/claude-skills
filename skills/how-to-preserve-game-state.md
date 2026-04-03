---
name: how-to-preserve-game-state
description: Preserve game progress across uninstall/reinstall and sync across iPhone, iPad, and Apple Watch using iCloud KVS. Covers the monotonic-counter merge strategy for stats, level progression, settings, and coin balances. Includes audit methodology for finding unprotected state, migration from local-only storage, and the distinction between what Game Center stores vs what you must sync yourself. Use when game state is lost on reinstall or when adding cross-device sync to any Apple platform game.
---

# How to Preserve Game State Across Reinstalls

A complete guide to making game progress survive uninstall/reinstall and stay
in sync across iPhone, iPad, Mac, and Apple Watch.

---

## Part 1: What Game Center Does and Does Not Store

Game Center provides two kinds of durable storage, both tied to the player's
Apple ID:

  What                Storage Model         Survives Reinstall
  ──────────────────  ────────────────────  ──────────────────
  Leaderboard scores  Cumulative integer    YES
  Achievements        Binary (earned/not)   YES

Game Center does NOT provide:
- Arbitrary key-value storage
- Saved game state (GKSavedGame exists but is deprecated-in-spirit and
  unreliable)
- Level progression, stats, settings, or any other structured data

If your game has stats, level progression, coin balances, or settings that
you want to preserve across reinstalls, you must sync them yourself.

---

## Part 2: iCloud Key-Value Store (The Right Tool)

NSUbiquitousKeyValueStore is Apple's lightweight key-value sync service:

- 1 MB total storage, 1024 keys max
- Automatic sync across all devices on the same iCloud account
- Survives uninstall/reinstall (tied to iCloud account, not app install)
- No server setup required
- Works on iOS, watchOS, macOS, tvOS

For a game with stats, levels, and coins, you will use ~2-5 KB.  The 1 MB
limit is not a concern.

### Entitlement Required

```xml
<key>com.apple.developer.ubiquity-kvstore-identifier</key>
<string>$(TeamIdentifierPrefix)$(CFBundleIdentifier)</string>
```

Add this to BOTH your iOS and watchOS entitlements.  Without it,
NSUbiquitousKeyValueStore silently fails -- no errors, no sync, no data
preserved.

---

## Part 3: Audit Your Persisted State

Before writing any sync code, catalog every piece of state your app
persists.  Search for:

- `UserDefaults` (both `.standard` and any suite like App Groups)
- `@AppStorage`
- `NSUbiquitousKeyValueStore`
- File writes (Documents, Caches, Application Support)
- Keychain
- Game Center (leaderboards, achievements)

For each item, classify it:

  Classification              Merge Strategy      Example
  ────────────────────────    ────────────────    ──────────────────────
  Monotonically increasing    max(local, remote)  puzzlesSolved, level
  High-water mark             max(local, remote)  longestStreak, highScore
  Resettable counter          see Part 6          currentStreak
  Timestamp                   max(local, remote)  lastPlayedDate
  User preference             last-write-wins     language, theme
  Derived value               don't sync          balance = earned - spent
  Ephemeral / cache           don't sync          recentPuzzleWords

Most game stats are monotonically increasing.  This is the key insight that
makes iCloud KVS sync safe and simple.

---

## Part 4: The Monotonic Counter Pattern

Any value that only increases can be safely synced across devices using
`max(local, remote)`.  This is the same pattern used for coin counters
(see how-to-in-app-purchase skill).

### Why max() Works for Monotonic Values

```
Device A: puzzlesSolved = 50
Device B: puzzlesSolved = 50  (synced)

Device A: solve 3 puzzles → puzzlesSolved = 53
Device B: solve 5 puzzles → puzzlesSolved = 55  (before sync)

Sync: max(53, 55) = 55
```

This undercounts by 3 -- Device A's 3 puzzles are lost.  But this is
the fundamental trade-off: iCloud KVS is eventually consistent, and without
a delta-based system (like the leaderboard uploader), some increments
from the slower device can be lost.

For leaderboard scores, use the delta-based LeaderboardUploader (see
how-to-make-a-leaderboard skill) which never loses points.  For stats
displayed only locally (puzzlesSolved, wordsFound, etc.), max-merge is
acceptable -- slight undercounting is far better than losing everything
on reinstall.

### Implementation Pattern

```swift
private let cloud = NSUbiquitousKeyValueStore.default

// Write
cloud.set(Int64(value), forKey: key)

// Read
let remote = Int(cloud.longLong(forKey: key))
let merged = max(local, remote)
```

Always use `Int64` / `longLong` -- NSUbiquitousKeyValueStore has no `Int`
overload.

---

## Part 5: What to Sync (Prioritized)

### Tier 1: Must Sync (player loses real progress without these)

  Data                        Key Pattern               Type
  ────────────────────────    ────────────────────────  ──────────
  Level per difficulty        cloudLevel_level1 .. _6   Int64
  Coin earned counter         coinTotalEarned           Int64
  Coin spent counter          coinTotalSpent            Int64
  Total puzzles solved        cloudPuzzlesSolved        Int64
  Total score                 cloudTotalScore           Int64
  Scores by difficulty        cloudScore_level1 .. _6   Int64
  Puzzles by difficulty       cloudPuzzles_level1 .._6  Int64
  Longest streak              cloudLongestStreak        Int64

### Tier 2: Should Sync (annoying to lose, easy to add)

  Data                        Key Pattern               Type
  ────────────────────────    ────────────────────────  ──────────
  Words found                 cloudWordsFound           Int64
  Bonus words found           cloudBonusWordsFound      Int64
  Hints used                  cloudHintsUsed            Int64
  Puzzles without hints       cloudPuzzlesNoHints       Int64
  Highest puzzle score        cloudHighestPuzzleScore   Int64
  Watch puzzles solved        cloudWatchPuzzles         Int64
  Daily allowances claimed    cloudAllowancesClaimed    Int64
  Max bonus words in puzzle   cloudMaxBonusWords        Int64
  Total coins earned (stats)  cloudTotalCoinsEarned     Int64
  Last played date            cloudLastPlayed           Double (timeInterval)
  Current streak              see Part 6                Int64 + Date

### Tier 3: Nice to Sync (settings)

  Data                        Key Pattern               Type
  ────────────────────────    ────────────────────────  ──────────
  Selected language           cloudLanguage             String
  Selected difficulty         cloudDifficulty           String
  Background theme            cloudBackgroundTheme      String
  Sound/music volumes         cloudMusicVolume, etc.    Double

Settings use last-write-wins: just read the cloud value on first launch
after reinstall and apply it if local has no value.

---

## Part 6: Handling Non-Monotonic Values

### Current Streak

Current streak can reset to 1 (if the player misses a day).  You cannot
use max() blindly because a stale remote value of 30 would overwrite a
legitimate local reset to 1.

Solution: sync the streak alongside its anchor date.

```swift
// Write both together
cloud.set(Int64(currentStreak), forKey: "cloudCurrentStreak")
cloud.set(lastPlayedDate.timeIntervalSince1970, forKey: "cloudLastPlayed")

// Merge: only accept the remote streak if its date is newer
let remoteStreak = Int(cloud.longLong(forKey: "cloudCurrentStreak"))
let remoteDate = Date(timeIntervalSince1970: cloud.double(forKey: "cloudLastPlayed"))

if remoteDate > localLastPlayed {
    // Remote is more recent -- use its streak
    currentStreak = remoteStreak
    lastPlayedDate = remoteDate
} else {
    // Local is more recent -- keep local streak
}

// longestStreak is always max()
longestStreak = max(localLongest, remoteLongest)
```

### Per-Difficulty Dictionaries

scoresByDifficulty, puzzlesByDifficulty, etc. are dictionaries where each
value is monotonic.  Sync each key independently:

```swift
for difficulty in DifficultyLevel.allCases {
    let key = "cloudScore_\(difficulty.rawValue)"
    let remote = Int(cloud.longLong(forKey: key))
    let local = stats.scoresByDifficulty[difficulty.rawValue] ?? 0
    let merged = max(local, remote)
    stats.scoresByDifficulty[difficulty.rawValue] = merged
    cloud.set(Int64(merged), forKey: key)
}
```

---

## Part 7: Architecture

### Where Sync Lives

Add iCloud KVS sync to StatsManager alongside the existing local
persistence:

```swift
@MainActor
final class StatsManager: ObservableObject {
    static let shared = StatsManager()

    private let defaults = UserDefaults.standard
    private let cloud = NSUbiquitousKeyValueStore.default
    private let statsKey = "playerStats"

    @Published var stats: PlayerStats

    private init() {
        // 1. Load local
        var stats: PlayerStats
        if let data = defaults.data(forKey: statsKey),
           let decoded = try? JSONDecoder().decode(PlayerStats.self, from: data) {
            stats = decoded
        } else {
            stats = PlayerStats()
        }

        // 2. Merge with iCloud (per-field max)
        stats = Self.mergeWithCloud(local: stats, cloud: cloud)

        self.stats = stats

        // 3. Observe remote changes
        NotificationCenter.default.addObserver(
            self, selector: #selector(cloudChanged(_:)),
            name: NSUbiquitousKeyValueStore.didChangeExternallyNotification,
            object: cloud)
        cloud.synchronize()

        // 4. Persist merged values back to both stores
        save()
    }

    private static func mergeWithCloud(
        local: PlayerStats,
        cloud: NSUbiquitousKeyValueStore
    ) -> PlayerStats {
        var s = local
        s.puzzlesSolved = max(s.puzzlesSolved,
            Int(cloud.longLong(forKey: "cloudPuzzlesSolved")))
        s.wordsFound = max(s.wordsFound,
            Int(cloud.longLong(forKey: "cloudWordsFound")))
        // ... repeat for each monotonic field ...
        return s
    }

    private func save() {
        // Stamp version
        stats.dataFormatVersion = PlayerStats.currentDataFormatVersion

        // Save local
        if let data = try? JSONEncoder().encode(stats) {
            defaults.set(data, forKey: statsKey)
        }

        // Save to iCloud (per-field, not a JSON blob)
        cloud.set(Int64(stats.puzzlesSolved), forKey: "cloudPuzzlesSolved")
        cloud.set(Int64(stats.wordsFound), forKey: "cloudWordsFound")
        // ... repeat for each field ...
    }

    @objc private func cloudChanged(_ notification: Notification) {
        Task { @MainActor in
            stats = Self.mergeWithCloud(local: stats, cloud: cloud)
            save()  // persist merged values locally
        }
    }
}
```

### Per-Field vs JSON Blob

Store each stat as its own iCloud KVS key, NOT as a JSON blob.  Reasons:

1. Per-field max() merge is safe.  A JSON blob requires last-write-wins,
   which loses the slower device's increments.
2. Individual keys are more debuggable (you can inspect them in Console).
3. The 1024-key limit is not a concern (you'll use ~30-40 keys total).

### Level Progression

Level sync follows the same pattern but lives in GameViewModel:

```swift
// On level change
let key = "cloudLevel_\(difficulty.rawValue)"
cloud.set(Int64(level), forKey: key)

// On init (merge with cloud)
let remoteLevel = Int(cloud.longLong(forKey: key))
let localLevel = defaults.integer(forKey: "currentLevel_\(difficulty.rawValue)")
let merged = max(max(localLevel, remoteLevel), 1)
self.level = merged
```

---

## Part 8: Initialization Order

On a fresh install (reinstall), local UserDefaults are empty.  The init
sequence must be:

```
1. Read local UserDefaults           → all zeros (fresh install)
2. Read iCloud KVS                   → has the real values
3. Merge: max(local, remote) per field
4. Write merged values back to local  → local is now restored
5. Write merged values to iCloud      → ensures cloud has latest
6. Observe didChangeExternallyNotification for ongoing sync
```

On a normal launch (no reinstall), step 3 is a no-op because local values
are already >= remote.

### The Critical Mistake: Overwriting Cloud with Zeros

If you write to iCloud KVS on every save without merging first, a fresh
install will read local zeros and then push those zeros to iCloud,
destroying the cloud data.  Always merge before writing.

---

## Part 9: What Game Center Can Reconstruct

After reinstall, you can read back some data from Game Center to seed
local stats:

```swift
// Restore achievement reporting state
let achievements = try await GKAchievement.loadAchievements()
var reported = Set<String>()
for a in achievements where a.percentComplete >= 100 {
    reported.insert(a.identifier)
}
// Save to reportedAchievements UserDefaults
```

```swift
// Restore approximate scores from leaderboards
let boards = try await GKLeaderboard.loadLeaderboards(IDs: leaderboardIDs)
for board in boards {
    let (entry, _, _) = try await board.loadEntries(
        for: .global, timeScope: .allTime, range: NSRange(1, 1))
    if let score = entry?.score {
        // Use as a floor for the corresponding stat
    }
}
```

This is a useful fallback but not a replacement for iCloud KVS sync:
- Leaderboard scores are cumulative totals, not per-field stats
- You cannot derive puzzlesSolved, wordsFound, etc. from a score
- Level progression is not stored in Game Center at all

---

## Part 10: WatchConnectivity Integration

If you sync stats to Apple Watch via WatchConnectivity, extend the
existing application context to include stats alongside coins:

```swift
// iOS: push stats to watch
func pushStats(stats: PlayerStats) {
    guard WCSession.default.activationState == .activated else { return }
    do {
        var ctx = WCSession.default.applicationContext
        ctx["puzzlesSolved"] = stats.puzzlesSolved
        ctx["wordsFound"] = stats.wordsFound
        ctx["longestStreak"] = stats.longestStreak
        // ... key fields only, not everything ...
        try WCSession.default.updateApplicationContext(ctx)
    } catch {
        print("Failed to push stats: \(error)")
    }
}
```

Application context is last-write-wins (only latest value delivered),
which is fine since we're pushing max-merged values.

---

## Part 11: Common Mistakes

**DO NOT rely on Game Center for game state.**
Game Center stores leaderboard scores and achievements.  That's it.
Level progression, stats, settings, and coin balances must be synced
separately via iCloud KVS.

**DO NOT store stats as a JSON blob in iCloud KVS.**
Per-field storage allows safe max() merging.  A JSON blob means
last-write-wins, which loses increments from the slower device.

**DO NOT write to iCloud KVS before merging.**
On a fresh install, local values are zero.  Writing zeros to iCloud
before reading the existing cloud values destroys the player's data.
Always read + merge + write.

**DO NOT forget the entitlement.**
Without `com.apple.developer.ubiquity-kvstore-identifier`, iCloud KVS
silently does nothing.  No error, no sync, no data preserved.  Add it
to both iOS and watchOS targets.

**DO NOT assume iCloud is enabled.**
Some users disable iCloud.  Your game must function correctly with
local-only storage.  iCloud sync is a bonus, not a requirement.
Never crash or degrade if iCloud KVS returns zeros.

**DO NOT sync derived values.**
`balance = totalEarned - totalSpent` -- sync the two counters, not the
balance.  `computedTotalScore = sum(scoresByDifficulty)` -- sync the
per-difficulty scores, not the total.

**DO NOT sync ephemeral state.**
Recent puzzle words (for repetition avoidance), pending leaderboard
deltas, and UI animation state are per-device and per-session.
Syncing them adds complexity with no benefit.

**DO NOT use UserDefaults alone for important data.**
UserDefaults (both standard and App Group suites) are deleted on
uninstall.  Any data stored only in UserDefaults will be lost.
Always mirror important state to iCloud KVS.

**DO NOT store the daily allowance date only in UserDefaults.**
If your game grants a daily coin allowance, the "last granted" date is
critical state that must be synced to iCloud KVS.  If it lives only in
local UserDefaults, uninstalling and reinstalling resets the date to nil,
which the code interprets as "first time" and grants another allowance.
Users can farm infinite coins this way.  On grant, write the date to
both local and iCloud.  On check, read both and use the most recent:

```swift
let localDate = defaults.object(forKey: lastAllowanceDateKey) as? Date
let cloudDate = cloud.object(forKey: lastAllowanceDateKey) as? Date
let lastDate = [localDate, cloudDate].compactMap { $0 }.max()
```

---

## Part 12: Testing Checklist

- [ ] Install app, play several puzzles, verify stats and level are correct
- [ ] Uninstall app completely, reinstall, verify stats and level restored
- [ ] Play on iPhone, check iPad shows updated stats (and vice versa)
- [ ] Play on iPhone, check Watch shows updated coin balance
- [ ] Turn off iCloud, play, turn on iCloud -- data merges correctly
- [ ] Play on two devices simultaneously, verify no data loss on sync
- [ ] Fresh install with iCloud disabled -- app works normally with zeros
- [ ] Level progression on reinstall matches what it was before
- [ ] Achievements re-sync from Game Center on reinstall
- [ ] Coin balance survives reinstall (iCloud KVS)
- [ ] Settings survive reinstall (language, theme, difficulty)

---

## Part 13: Key Prefix Convention

Use a `cloud` prefix for all iCloud KVS keys to distinguish them from
local UserDefaults keys:

```
cloudPuzzlesSolved
cloudWordsFound
cloudBonusWordsFound
cloudTotalScore
cloudScore_level1 ... cloudScore_level6
cloudPuzzles_level1 ... cloudPuzzles_level6
cloudLevel_level1 ... cloudLevel_level6
cloudLongestStreak
cloudCurrentStreak
cloudLastPlayed
cloudHighestPuzzleScore
cloudHintsUsed
cloudPuzzlesNoHints
cloudWatchPuzzles
cloudAllowancesClaimed
cloudMaxBonusWords
cloudTotalCoinsEarned
cloudLanguage
cloudDifficulty
cloudBackgroundTheme
coinTotalEarned        (already in use -- no prefix change)
coinTotalSpent         (already in use -- no prefix change)
```

Total: ~35 keys.  Well within the 1024-key limit.

---

## Part 14: Migration Plan for Existing Apps

If your app already has local-only persistence and you're adding iCloud
KVS sync:

1. Add the iCloud KVS entitlement to all targets
2. On first launch after the update, local values are populated from
   prior sessions -- these become the seed values
3. Merge local with cloud (cloud will be empty for existing users)
4. Write merged values to both local and cloud
5. From now on, every save writes to both stores

No user action required.  Existing users get their current stats pushed
to iCloud on the first launch of the updated version.  Future reinstalls
will restore from iCloud.

---

## Part 15: iCloud KVS Limits

  Limit              Value
  ─────────────────  ─────────
  Total storage      1 MB
  Maximum keys       1024
  Max key length     64 bytes
  Sync frequency     ~every few minutes (not instant)

For a game with 35 keys averaging 8 bytes each, total usage is ~280 bytes.
The limits are not a concern.

Sync is not instant -- changes propagate within minutes, not seconds.
For real-time multiplayer sync, use WatchConnectivity (immediate between
paired devices) or CloudKit.  For game state preservation, the eventual
consistency of iCloud KVS is fine.
