---
name: how-to-in-app-purchase
description: Complete guide to consumable in-app purchases (coins/gems) for iOS/watchOS games using StoreKit 2. Covers App Store Connect setup, coin balance architecture with monotonic counters to prevent double-spending, iCloud KVS sync, WatchConnectivity, review metadata, and common mistakes. Use when adding IAP or virtual currency to any Apple platform app.
---

# How to Do In-App Purchases Right the First Time

A complete guide for adding consumable IAP (coins, gems, tokens) to an
iOS/watchOS game using StoreKit 2.  Covers every layer from App Store Connect
setup through multi-device sync, with a double-spend-proof coin balance
architecture.

---

## Part 1: What You Need Before Writing Code

Before touching Xcode, set up everything in App Store Connect.  Missing any
of these causes "Missing Resources" errors that block submission.

### App Store Connect Checklist

For EACH consumable product you need ALL of the following:

  1. Product ID               e.g. com.company.app.coins.small
  2. Reference Name            Human-readable name for ASC dashboard
  3. Price Schedule             At least one price point selected
  4. Localization (per locale)  Display name AND description
  5. Review Note                Tells the reviewer how to test the purchase
  6. Review Screenshot          Shows the purchase UI in context

Missing any of items 5-6 causes the "Missing Resources" or "Missing
Metadata" warning that prevents submission to App Review.

### Product ID Convention

```
com.<company>.<app>.coins.small     100 coins
com.<company>.<app>.coins.medium    500 coins
com.<company>.<app>.coins.large    2000 coins
```

Keep product IDs short and hierarchical.  The bundle ID prefix keeps them
globally unique.

### Pricing Tiers

Apple has fixed price tiers.  Pick tiers that feel like good value at each
level but give a volume discount for larger packs:

  Pack       Coins    Price     Coins per Dollar
  ────────   ─────    ──────    ────────────────
  Small      100      $1.99     50
  Medium     500      $4.99     100
  Large      2000     $9.99     200

The volume discount incentivizes larger purchases.

---

## Part 2: Review Metadata (The Part Everyone Forgets)

App Review requires a review note and a screenshot for each IAP product.
Without them, the submission is rejected or the product shows as
"Missing Resources" in the dashboard.

### Review Note Template

Write a note that tells the reviewer exactly what the product does and how
to find the purchase UI:

```
Consumable purchase of 100 coins. Coins are used to buy hints
during puzzles. Tap the Shop tab to see coin packs, then tap
the price button to purchase.
```

### Review Screenshot

The screenshot must be a real screenshot (or realistic mock) of your purchase
UI at iPhone resolution (1290x2796 for iPhone 15 Pro Max).  It should show:

- The purchase button with the price visible
- The product name and coin count
- Enough surrounding UI for context

If you need to generate screenshots programmatically (e.g. for CI or to
avoid manual screenshotting), use the App Store Connect API:

```python
# 1. Reserve the upload
reservation = api_post("/v1/inAppPurchaseAppStoreReviewScreenshots", {
    "data": {
        "type": "inAppPurchaseAppStoreReviewScreenshots",
        "attributes": {
            "fileName": "review_screenshot.png",
            "fileSize": file_size,
        },
        "relationships": {
            "inAppPurchaseV2": {
                "data": {"type": "inAppPurchases", "id": iap_id}
            }
        }
    }
})

# 2. Upload the image chunks per the returned uploadOperations
for op in reservation["data"]["attributes"]["uploadOperations"]:
    requests.put(op["url"], headers=op["requestHeaders"],
                 data=image_bytes[op["offset"]:op["offset"]+op["length"]])

# 3. Commit the upload
api_patch(f"/v1/inAppPurchaseAppStoreReviewScreenshots/{screenshot_id}", {
    "data": {
        "type": "inAppPurchaseAppStoreReviewScreenshots",
        "id": screenshot_id,
        "attributes": {
            "uploaded": True,
            "sourceFileChecksum": md5_hex,
        }
    }
})
```

### Setting Review Notes via API

```python
api_patch(f"/v2/inAppPurchases/{iap_id}", {
    "data": {
        "type": "inAppPurchases",
        "id": iap_id,
        "attributes": {
            "reviewNote": "Consumable purchase of 100 coins. ..."
        }
    }
})
```

Note the v2 endpoint for IAP patches.  The v1 endpoint returns 404 for
review note updates.

---

## Part 3: Entitlements

IAP itself requires no special entitlement (StoreKit is available by
default).  But if you sync coin balances across devices, you need:

### iCloud Key-Value Store

```xml
<key>com.apple.developer.ubiquity-kvstore-identifier</key>
<string>$(TeamIdentifierPrefix)$(CFBundleIdentifier)</string>
```

Add this to both your iOS and watchOS entitlements.  This gives you
NSUbiquitousKeyValueStore for syncing small values (like coin counters)
across devices.

### App Groups (for watchOS)

```xml
<key>com.apple.security.application-groups</key>
<array>
    <string>group.com.company.app</string>
</array>
```

Required for sharing UserDefaults between the iOS app and watchOS extension.

---

## Part 4: StoreKit 2 Purchase Flow

StoreKit 2 (async/await) is dramatically simpler than the original
StoreKit.  Here is the complete purchase flow:

### Product Loading

```swift
import StoreKit

private let productIDs = [
    "com.company.app.coins.small",
    "com.company.app.coins.medium",
    "com.company.app.coins.large"
]

@State private var products: [Product] = []

private func loadProducts() async {
    do {
        products = try await Product.products(for: Set(productIDs))
    } catch {
        print("Failed to load products: \(error)")
    }
}
```

Call this in a `.task` modifier when the shop view appears.

### Purchase Execution

```swift
private func purchase(productID: String, coins: Int) async {
    guard let product = products.first(where: { $0.id == productID }) else { return }

    do {
        let result = try await product.purchase()
        switch result {
        case .success(let verification):
            let transaction: StoreKit.Transaction
            switch verification {
            case .verified(let t):
                transaction = t
            case .unverified(let t, _):
                // Accept unverified in sandbox; in production you may
                // want to reject or log these
                transaction = t
            }
            coinManager.purchaseCoins(coins)
            await transaction.finish()    // CRITICAL: must call finish()
        case .userCancelled:
            break
        case .pending:
            break
        @unknown default:
            break
        }
    } catch {
        print("Purchase failed: \(error)")
    }
}
```

### Critical Rules

1. **Always call `transaction.finish()`** after delivering the content.
   Unfinished transactions will re-appear on next launch.

2. **Handle `.unverified` in sandbox.**  The sandbox environment often
   returns unverified transactions.  In production, decide whether to
   accept or reject them based on your security requirements.

3. **Use `Product.displayPrice`** for the button label, never hardcode
   prices.  StoreKit returns the localized price for the user's region.

4. **Disable the button during purchase** to prevent double-taps.

### Displaying Prices

```swift
Button {
    Task { await purchase(productID: pack.id, coins: pack.coins) }
} label: {
    Text(product?.displayPrice ?? "$--")
}
.disabled(purchaseInProgress || product == nil)
```

---

## Part 5: Coin Balance Architecture (The Hard Part)

This is where most implementations go wrong.  The naive approach — storing
a single `balance` integer — creates a double-spend vulnerability on
multi-device.

### The Problem with a Single Balance

```
iPhone: balance = 100
Watch:  balance = 100  (synced)

iPhone: spend 50 → balance = 50
Watch:  spend 50 → balance = 50   (before sync arrives)

Sync: max(50, 50) = 50

Result: User spent 100 coins but only lost 50.  Free coins.
```

Even worse with iCloud KVS, where sync can be delayed by minutes.

### The Solution: Two Monotonic Counters

Track two counters that only ever increase:

```
totalEarned: all coins ever received (purchases + rewards + daily)
totalSpent:  all coins ever spent on hints

balance = totalEarned - totalSpent
```

Since both counters only go up, syncing with `max(local, remote)` per
counter is mathematically safe:

```
iPhone: earned=200, spent=50  → balance=150
Watch:  earned=200, spent=50  → balance=150  (synced)

iPhone: spend 30 → spent=80  → balance=120
Watch:  spend 40 → spent=90  → balance=110  (before sync)

Sync: earned=max(200,200)=200, spent=max(80,90)=90

Result: balance=110.  User spent 70 total, lost 70.  Correct.
```

No double-spend is possible because spent only ratchets upward.

### Implementation

```swift
@MainActor
final class CoinManager: ObservableObject {
    static let shared = CoinManager()

    private let earnedKey = "coinTotalEarned"
    private let spentKey  = "coinTotalSpent"

    private let defaults = UserDefaults(suiteName: "group.com.company.app")
                           ?? .standard
    private let cloud = NSUbiquitousKeyValueStore.default

    private var totalEarned: Int { didSet { persist() } }
    private var totalSpent:  Int { didSet { persist() } }

    @Published private(set) var balance: Int

    private init() {
        // Load local counters
        var localEarned = defaults.integer(forKey: earnedKey)
        var localSpent  = defaults.integer(forKey: spentKey)

        // Merge with iCloud (max per counter — always safe)
        let remoteEarned = Int(cloud.longLong(forKey: earnedKey))
        let remoteSpent  = Int(cloud.longLong(forKey: spentKey))
        self.totalEarned = max(localEarned, remoteEarned)
        self.totalSpent  = max(localSpent, remoteSpent)
        self.balance = self.totalEarned - self.totalSpent

        // Observe iCloud changes
        NotificationCenter.default.addObserver(
            self,
            selector: #selector(icloudChanged(_:)),
            name: NSUbiquitousKeyValueStore.didChangeExternallyNotification,
            object: cloud
        )
        cloud.synchronize()
        persist()
    }

    private func persist() {
        balance = totalEarned - totalSpent

        defaults.set(totalEarned, forKey: earnedKey)
        defaults.set(totalSpent, forKey: spentKey)
        cloud.set(Int64(totalEarned), forKey: earnedKey)
        cloud.set(Int64(totalSpent), forKey: spentKey)

        #if os(iOS)
        SyncManager.shared.pushCoinCounters(
            earned: totalEarned, spent: totalSpent)
        #endif
    }

    @objc private func icloudChanged(_ notification: Notification) {
        Task { @MainActor in
            mergeRemote(
                earned: Int(cloud.longLong(forKey: earnedKey)),
                spent:  Int(cloud.longLong(forKey: spentKey))
            )
        }
    }

    /// Merge remote counters.  Each counter only ratchets upward.
    func mergeRemote(earned: Int, spent: Int) {
        var changed = false
        if earned > totalEarned { totalEarned = earned; changed = true }
        if spent > totalSpent   { totalSpent = spent;   changed = true }
        if changed { balance = totalEarned - totalSpent }
    }

    func spend(_ amount: Int) -> Bool {
        guard balance >= amount else { return false }
        totalSpent += amount
        return true
    }

    func award(_ amount: Int) {
        totalEarned += amount
    }

    func purchaseCoins(_ amount: Int) {
        totalEarned += amount
    }
}
```

### Migration from a Single Balance

If you already shipped with a single `balance` key, migrate on first launch:

```swift
// In init(), before iCloud merge:
if localEarned == 0 && localSpent == 0 {
    let legacyBalance = defaults.integer(forKey: "coinBalance")
    if legacyBalance > 0 {
        // Use stats history to reconstruct earned, or fall back
        // to using the balance as a floor
        let statsEarned = StatsManager.shared.stats.totalCoinsEarned
        localEarned = max(statsEarned, legacyBalance)
        localSpent = localEarned - legacyBalance
    }
}
```

The key insight: you need to reconstruct what `totalEarned` should be.
If you have a stats tracker that recorded total coins earned historically,
use it.  Otherwise, treat the legacy balance as a lower bound for earned
and set spent to zero.

---

## Part 6: iCloud KVS Sync

NSUbiquitousKeyValueStore gives you automatic cross-device sync for small
values (up to 1 MB total, 1024 keys max).  Perfect for coin counters.

### Setup

1. Add the `com.apple.developer.ubiquity-kvstore-identifier` entitlement
2. Read and write via `NSUbiquitousKeyValueStore.default`
3. Observe `didChangeExternallyNotification` for remote changes
4. Call `synchronize()` on launch to pull pending changes

### Why `Int64` for iCloud

`NSUbiquitousKeyValueStore` has `set(_:forKey:)` overloads for `Int64` but
not `Int`.  Always use `Int64` when writing and convert back:

```swift
cloud.set(Int64(totalEarned), forKey: earnedKey)
let remote = Int(cloud.longLong(forKey: earnedKey))
```

### Merge Strategy

With monotonic counters, the merge is trivially safe:

```swift
newEarned = max(local, remote)
newSpent  = max(local, remote)
```

No conflict resolution needed.  No vector clocks.  No CRDTs.

---

## Part 7: WatchConnectivity Sync

If your app has a watchOS companion, sync coin counters via
WatchConnectivity's application context.  Application context is queued
and delivered even when the companion app isn't running.

### iOS Side (Push)

```swift
func pushCoinCounters(earned: Int, spent: Int) {
    guard WCSession.default.activationState == .activated,
          WCSession.default.isPaired else { return }
    do {
        var ctx = WCSession.default.applicationContext
        ctx["coinEarned"] = earned
        ctx["coinSpent"] = spent
        try WCSession.default.updateApplicationContext(ctx)
    } catch {
        print("Failed to push coin counters: \(error)")
    }
}
```

### watchOS Side (Receive)

```swift
func session(_ session: WCSession,
             didReceiveApplicationContext ctx: [String: Any]) {
    Task { @MainActor in
        if let earned = ctx["coinEarned"] as? Int,
           let spent = ctx["coinSpent"] as? Int {
            CoinManager.shared.mergeRemote(earned: earned, spent: spent)
        }
    }
}
```

Also merge from `session.receivedApplicationContext` on activation,
to pick up context sent while the watch app wasn't running.

### Why Not `sendMessage`?

`sendMessage` requires both apps to be running and reachable.
`updateApplicationContext` is queued — the latest values are always
delivered when the companion app launches, even if the phone was in
airplane mode when the update was sent.  For coin balances (latest state,
not a stream of events), application context is the right choice.

---

## Part 8: Shop UI

The shop view needs these components:

1. **Balance display** — current coin count
2. **Daily allowance indicator** — if your economy has free daily coins
3. **Product cards** — one per IAP, showing name, coin count, and price
4. **Loading state** — products may take a moment to load from StoreKit

### Key UI Principles

- Use `Product.displayPrice` for prices (localized by Apple)
- Show "$--" while products are loading
- Disable purchase buttons during a transaction
- Show a coin icon consistently (SF Symbol `circle.fill` in yellow)
- Give feedback on purchase (haptic, animation, sound)

### Injecting CoinManager

Make CoinManager a `@StateObject` in your app entry point and inject it
into the environment:

```swift
@main
struct MyApp: App {
    @StateObject private var coinManager = CoinManager.shared

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(coinManager)
        }
    }
}
```

---

## Part 9: App Store Connect API Endpoints

The API has v1 and v2 endpoints for IAP.  The v2 endpoints are required
for most IAP operations.

  Operation                       Endpoint
  ──────────────────────────────  ────────────────────────────────────────
  List IAPs for an app            GET /v1/apps/{id}/inAppPurchasesV2
  Get IAP details                 GET /v2/inAppPurchases/{id}
  Update IAP (review note, etc.)  PATCH /v2/inAppPurchases/{id}
  Get IAP localizations           GET /v2/inAppPurchases/{id}/inAppPurchaseLocalizations
  Get review screenshot           GET /v2/inAppPurchases/{id}/appStoreReviewScreenshot
  Upload review screenshot        POST /v1/inAppPurchaseAppStoreReviewScreenshots
  Commit screenshot upload        PATCH /v1/inAppPurchaseAppStoreReviewScreenshots/{id}
  Get price schedule              GET /v2/inAppPurchases/{id}/iapPriceSchedule

Note that listing IAPs uses the v1 apps endpoint with `inAppPurchasesV2`,
but patching an individual IAP uses the v2 endpoint.  Using v1 for patches
returns 404.

### Authentication

App Store Connect API uses JWT (ES256) with the key from your App Store
Connect API key:

```python
payload = {
    "iss": ISSUER_ID,
    "iat": now,
    "exp": now + 1200,   # 20 minutes max
    "aud": "appstoreconnect-v1",
}
token = jwt.encode(payload, private_key, algorithm="ES256",
                   headers={"kid": KEY_ID})
```

---

## Part 10: Common Mistakes

**DO NOT store a single balance integer.**
This is the #1 mistake.  A single balance synced with max() across devices
allows double-spending.  Use two monotonic counters (earned/spent).

**DO NOT forget review metadata.**
Each IAP product needs a review note AND a review screenshot.  Without
them, App Store Connect shows "Missing Resources" and your submission
is blocked.  This is the most common surprise for first-time IAP setups.

**DO NOT hardcode prices.**
Always use `Product.displayPrice` from StoreKit.  Prices vary by region,
and Apple handles currency conversion.

**DO NOT skip `transaction.finish()`.**
Unfinished transactions persist and will trigger again on next launch.
Always call `finish()` after delivering the purchased content.

**DO NOT sync a raw balance via iCloud KVS.**
Sync the earned and spent counters separately.  The balance is derived.

**DO NOT use `sendMessage` for coin sync to watchOS.**
Use `updateApplicationContext`.  It's queued and delivered reliably even
when the companion app isn't running.

**DO NOT use Int for iCloud KVS.**
NSUbiquitousKeyValueStore requires Int64.  Write with `set(Int64(...))`,
read with `longLong(forKey:)`.

**DO NOT forget the iCloud KVS entitlement.**
Without `com.apple.developer.ubiquity-kvstore-identifier`,
NSUbiquitousKeyValueStore silently fails.  No error, no sync.  Add it to
both iOS and watchOS entitlements.

**DO NOT merge coin data before checking for migration.**
If migrating from a legacy single-balance system, reconstruct the earned
and spent counters from historical stats BEFORE merging with iCloud.
Otherwise the migration data gets overwritten by stale iCloud values.

**DO NOT store the daily allowance date only in UserDefaults.**
If your economy has a daily coin allowance, the "last granted" date MUST
be synced to iCloud KVS alongside the coin counters.  UserDefaults is
deleted on uninstall, so a local-only date lets users farm infinite coins
by reinstalling.  On grant, write the date to both local and iCloud.
On check, read both and use the most recent:

```swift
let localDate = defaults.object(forKey: lastAllowanceDateKey) as? Date
let cloudDate = cloud.object(forKey: lastAllowanceDateKey) as? Date
let lastDate = [localDate, cloudDate].compactMap { $0 }.max()
```

---

## Part 11: Testing Checklist

- [ ] Products load and display localized prices in the shop
- [ ] Purchase completes and coins are awarded
- [ ] Transaction.finish() is called (check with Transaction.currentEntitlements)
- [ ] Balance persists across app restart
- [ ] Balance syncs to another device via iCloud KVS
- [ ] Balance syncs to watchOS via WatchConnectivity
- [ ] Spending on two devices simultaneously cannot double-spend
- [ ] Daily allowance awards once per calendar day, not more
- [ ] App Store Connect shows no "Missing Resources" warnings
- [ ] Review note and screenshot are visible for each IAP product
- [ ] Sandbox purchases work with a sandbox Apple ID
- [ ] Offline purchase (airplane mode) is handled gracefully

---

## Part 12: File Layout

```
Shared/
├── Services/
│   ├── CoinManager.swift        # Monotonic counters, iCloud KVS, balance
│   └── SyncManager.swift        # WatchConnectivity (push/receive counters)
ArcWord/
└── Views/
    └── ShopView.swift           # StoreKit 2 product loading, purchase UI
scripts/
├── audit_app_store.py           # Audit ASC for missing metadata
└── fix_iap_metadata.py          # Set review notes + upload screenshots
```

Total implementation: ~350 lines across three Swift files, plus optional
Python scripts for ASC automation.

---

## Part 13: Order of Operations

When adding IAP to a new app, do things in this order to avoid backtracking:

  1. Create products in App Store Connect (IDs, names, prices)
  2. Add localizations for each product (display name, description)
  3. Add review notes for each product
  4. Add review screenshots for each product
  5. Add entitlements (iCloud KVS, App Groups) in Xcode
  6. Implement CoinManager with monotonic counters
  7. Implement shop UI with StoreKit 2
  8. Wire up WatchConnectivity sync (if watchOS companion)
  9. Run audit_app_store.py to verify no missing metadata
  10. Test in sandbox with a sandbox Apple ID
