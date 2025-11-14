# S3 Scenario 6: Mobile App Instant Search (iOS/Android In-App Search)

**Company Profile**: Mobile-first consumer app (social, productivity, e-commerce, content)
**Search Volume**: 100K documents (posts, products, users, content), 500K searches/month
**Budget**: $100-1K/month for mobile search
**Priority**: <50ms latency, offline capability, battery efficiency, small SDK size, network optimization

---

## Business Context

### Company Details
- **Stage**: Seed to Series B
- **Team Size**: 10-100 employees, 5-30 engineers (50% mobile, 50% backend)
- **Users**: 100K-5M monthly active users (MAU)
- **Revenue**: $500K-20M ARR
- **Growth**: 100-300% YoY (mobile-first, viral growth)
- **Business Model**: Freemium, subscription, in-app purchases, or ads

### Technical Environment
- **Platform**: iOS (Swift/SwiftUI) + Android (Kotlin/Jetpack Compose)
- **Content**: 100K-500K documents (user profiles, posts, products, places, content)
- **Search Patterns**:
  - **User search** (40%): "Find friends", "Search profiles"
  - **Content search** (40%): "Posts about travel", "Videos on cooking"
  - **Product search** (20%): "Shoes", "iPhone cases" (if e-commerce)
- **Search Traffic**: 500K-2M searches/month (mobile-only, no web)
- **User Behavior**: 80% mobile data (3G/4G/5G), 20% WiFi, offline usage common
- **Geographic Distribution**: Global (50% US, 30% emerging markets with slower networks, 20% Europe/APAC)

### Mobile Search Requirements
- **Latency**: <50ms p95 (instant search UX, no perceived delay)
- **Offline Capability**: Search cached data when offline (last 100-500 results)
- **Battery Efficiency**: Minimize network requests (debouncing, caching, prefetching)
- **Network Optimization**: Small payloads (<10KB per query), gzip compression
- **SDK Size**: <2MB SDK (mobile apps are size-sensitive)
- **Native SDKs**: iOS (Swift), Android (Kotlin), React Native, Flutter
- **Autocomplete**: Query suggestions (<10ms, on-device if possible)
- **Faceting**: 5-15 facets (category, location, date, user type)
- **Cost**: $100-1K/month (mobile apps are cost-sensitive)

---

## Search Platform Evaluation

### Evaluation Criteria

| Criterion | Weight | Algolia | Meilisearch | Typesense | AWS Amplify | Firebase | Notes |
|-----------|--------|---------|-------------|-----------|------------|----------|-------|
| **Mobile SDKs** | 25% | 10/10 | 7/10 | 8/10 | 8/10 | 9/10 | Algolia best (iOS, Android, RN, Flutter) |
| **Performance (<50ms)** | 25% | 10/10 | 9/10 | 9/10 | 7/10 | 6/10 | Algolia/Meili/Type sub-50ms |
| **Offline Support** | 20% | 8/10 | 5/10 | 5/10 | 7/10 | 9/10 | Firebase best (Firestore offline) |
| **Cost Efficiency** | 15% | 5/10 | 9/10 | 10/10 | 7/10 | 6/10 | Typesense cheapest ($20/month) |
| **SDK Size** | 10% | 7/10 | 8/10 | 8/10 | 6/10 | 5/10 | Algolia 1.5MB, Firebase 3MB |
| **Battery Efficiency** | 5% | 9/10 | 8/10 | 8/10 | 8/10 | 7/10 | All good, Algolia best (caching) |
| **Total Score** | 100% | **8.7/10** | **7.7/10** | **8.1/10** | **7.4/10** | **7.3/10** | Algolia wins for mobile |

### Winner: Algolia (best mobile SDKs, performance, offline caching)
### Alternative: Typesense (cost-conscious, good performance, <$100/month)
### Offline-First: Firebase Firestore (best offline support, but limited search features)

---

## Platform Deep Dive

### Option 1: Algolia (Recommended for Mobile Apps)

**Pricing**: **$0-245/month** (Free: 10K records, 10K searches; Grow: 100K records, 1M searches)

**500K searches/month pricing**: Grow plan = **$245/month** (base) + overage = **$245-500/month**

**Pros**:
- ✅ **Best mobile SDKs** (iOS Swift, Android Kotlin, React Native, Flutter, all official)
- ✅ **10-20ms latency** (70+ PoPs, global CDN, mobile-optimized)
- ✅ **InstantSearch Mobile** (pre-built UI components: search bar, hits, facets, filters)
- ✅ **Offline caching** (SDK caches last 100-500 results, search offline)
- ✅ **Battery optimization** (automatic debouncing, request batching, smart caching)
- ✅ **Small SDK** (1.5MB iOS, 1.8MB Android, minimal impact)
- ✅ **Network optimization** (gzip compression, small JSON payloads <5KB)
- ✅ **Query suggestions** (server-side, <10ms, or on-device cache)
- ✅ **Proven mobile-first** (Twitch, Medium, Stripe use Algolia for mobile)

**Cons**:
- ⚠️ **Usage-based pricing** ($245/month base, overages if >1M searches)
- ⚠️ **Vendor lock-in** (proprietary SDK, hard to migrate)
- ⚠️ **Offline limited** (caches last N results, not full offline search)

**TCO (3-year, 100K docs, 500K searches/month)**:
- License: $245/month × 36 months = **$8,820**
- Engineering (setup 40h + maintenance 5h/month): 40 + (5 × 36) = 220 hours × $100 = **$22,000**
- **Total TCO**: **$30,820** (3-year)

**When to Choose Algolia**:
- Mobile-first app (iOS + Android + React Native/Flutter)
- Need <50ms latency (instant search UX, global users)
- Budget $245-1K/month (acceptable for mobile apps with MAU >100K)
- Want pre-built mobile UI (InstantSearch Mobile, save 80-160 hours)
- Offline caching important (search last results when offline)

**Mobile Integration** (iOS Swift):
```swift
import InstantSearchSwiftUI
import AlgoliaSearchClient

struct SearchView: View {
  @StateObject var searcher = HitsSearcher(appID: "APP_ID", apiKey: "SEARCH_KEY", indexName: "products")
  @StateObject var queryInputController = TextFieldController()

  var body: some View {
    VStack {
      SearchBar(textFieldController: queryInputController)
        .padding()

      HitsList(searcher) { hit in
        VStack(alignment: .leading) {
          Text(hit.object["title"].stringValue)
            .font(.headline)
          Text("$\(hit.object["price"].stringValue)")
            .font(.subheadline)
        }
      }
    }
    .onAppear {
      searcher.connectController(queryInputController)
      searcher.search()
    }
  }
}
```

---

### Option 2: Typesense (Cost-Optimized for Mobile)

**Pricing**: **$20-120/month** (Hobby: $20, Growth: $120)

**500K searches/month pricing**: Growth plan = **$120/month** (fixed, unlimited searches)

**Pros**:
- ✅ **Cheapest** ($120/month vs Algolia $245-500/month, 2-4× cheaper)
- ✅ **Good mobile SDKs** (iOS, Android, React Native, Flutter, community-supported)
- ✅ **10-20ms latency** (excellent performance, comparable to Algolia)
- ✅ **Predictable pricing** ($120/month fixed, no overage surprises)
- ✅ **Small SDK** (1.2MB iOS, 1.5MB Android, smaller than Algolia)
- ✅ **InstantSearch compatible** (can reuse Algolia's InstantSearch UI)

**Cons**:
- ⚠️ **No official offline caching** (need to implement manually, 20-40 hours)
- ⚠️ **Community SDKs** (iOS/Android SDKs community-maintained, not official)
- ⚠️ **No pre-built mobile UI** (need to build search UI, 40-80 hours)

**TCO (3-year, 100K docs, 500K searches/month)**:
- License: $120/month × 36 months = **$4,320**
- Engineering (setup 80h + UI 60h + offline 30h + maintenance 5h/month): 80 + 60 + 30 + (5 × 36) = 350 hours × $100 = **$35,000**
- **Total TCO**: **$39,320** (3-year)

**When to Choose Typesense**:
- Budget-conscious ($120/month vs Algolia $245-500/month)
- Engineering team comfortable building mobile UI (40-80 hours)
- Don't need official SDKs (community SDKs acceptable)
- Offline caching not critical (or can DIY)

**Mobile Integration** (iOS Swift):
```swift
import Typesense

let client = Client(config: Configuration(
  nodes: [Node(host: "xxx.a1.typesense.net", port: "443", protocol: "https")],
  apiKey: "SEARCH_KEY"
))

// Search function
func search(query: String) async throws -> [Hit] {
  let searchParameters = SearchParameters(
    q: query,
    queryBy: "title,description",
    filterBy: "category:electronics"
  )

  let results = try await client.collection(name: "products").documents().search(searchParameters)
  return results.hits ?? []
}

// Usage in SwiftUI
struct SearchView: View {
  @State private var query = ""
  @State private var results: [Hit] = []

  var body: some View {
    VStack {
      TextField("Search...", text: $query)
        .onChange(of: query) { newQuery in
          Task {
            results = try await search(query: newQuery)
          }
        }

      List(results, id: \.document.id) { hit in
        VStack(alignment: .leading) {
          Text(hit.document["title"] as? String ?? "")
            .font(.headline)
          Text("$\(hit.document["price"] as? Double ?? 0)")
            .font(.subheadline)
        }
      }
    }
  }
}
```

---

### Option 3: Meilisearch (Alternative to Typesense)

**Pricing**: **$30/month** (Build: 100K docs, 10M API calls)

**Pros**:
- ✅ **Best DX** (9.0/10, fastest to production)
- ✅ **Hybrid search included** ($30/month for AI features)
- ✅ **Good mobile SDKs** (iOS, Android, React Native, community-supported)
- ✅ **15-25ms latency** (excellent performance)

**Cons**:
- ⚠️ **No official mobile SDKs** (community-maintained)
- ⚠️ **No pre-built mobile UI** (DIY, 40-80 hours)
- ⚠️ **No official offline support** (DIY, 20-40 hours)

**TCO (3-year)**: Similar to Typesense ($35K-40K)

**When to Choose Meilisearch**: Prioritize backend DX (fastest API integration), mobile UI DIY acceptable

---

### Option 4: Firebase Firestore (Best Offline, Limited Search)

**Pricing**: **$25-100/month** (Firestore: reads + writes, small for 500K searches)

**Pros**:
- ✅ **Best offline support** (full offline-first, Firestore caches all data locally)
- ✅ **Native mobile SDKs** (iOS, Android, Flutter, official Firebase SDKs)
- ✅ **Real-time sync** (live updates, push notifications)
- ✅ **Google ecosystem** (Analytics, Auth, Cloud Functions, integrated)

**Cons**:
- ❌ **Limited search** (no full-text search, only exact match or prefix)
- ❌ **No typo tolerance** (must use Algolia/Typesense/Meilisearch on top)
- ❌ **No faceting** (complex filters require composite indexes)
- ❌ **50-150ms latency** (slower than Algolia/Typesense for search)

**When to Choose Firebase**: Offline-first app (chat, notes, todo lists), basic search (user names, IDs, not full-text)

**Hybrid Approach**: Firebase (offline data storage) + Algolia (search index) = best of both worlds

---

## Architecture Pattern: Mobile Instant Search

### Phase 1: Basic Mobile Search (Algolia)

**Architecture**:
```
┌─────────────────────────────────────────────────────────────────┐
│                   Mobile App (iOS / Android)                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ InstantSearch Mobile UI                                   │   │
│  │  - SearchBar (debounced 100ms, prevent battery drain)     │   │
│  │  - Results List (InfiniteScrollView, lazy loading)        │   │
│  │  - Filters (Category, Price, Rating)                      │   │
│  │  - Offline indicator (show if cached results)             │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Algolia SDK (1.5MB, native Swift/Kotlin)                  │   │
│  │  - Request batching (combine multiple queries)            │   │
│  │  - Offline cache (last 100-500 results, 7-day TTL)        │   │
│  │  - Gzip compression (reduce network payload 70%)          │   │
│  │  - Smart debouncing (100ms delay, cancel previous request)│   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                          │
                          │ HTTPS requests (gzipped, <5KB per query)
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Algolia (70+ PoPs, Global CDN)                 │
│  - Nearest PoP (10-20ms latency, auto-routing)                   │
│  - Index: products (100K docs)                                   │
│  - Searchable: title, description, category                      │
│  - Facets: category, price_range, rating                         │
│  - Ranking: relevance + popularity + conversion                  │
└─────────────────────────────────────────────────────────────────┘
```

**Data Flow**:
1. **User types query** → SearchBar debounces (100ms, cancel previous request)
2. **SDK checks cache** → If offline or cached, return cached results (0ms, instant)
3. **SDK sends request** → HTTPS to nearest Algolia PoP (gzip compressed, <5KB)
4. **Algolia responds** → 10-20ms, returns top 20 results (gzipped, <10KB)
5. **SDK caches results** → Store in local cache (SQLite or CoreData/Room)
6. **UI updates** → Display results (lazy loading, smooth scrolling)

---

### Phase 2: Offline Support (Hybrid Firebase + Algolia)

**Architecture**:
```
┌─────────────────────────────────────────────────────────────────┐
│                   Mobile App (iOS / Android)                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Search UI (Custom or InstantSearch)                       │   │
│  │  - Offline mode: Search local Firebase cache (0ms)        │   │
│  │  - Online mode: Search Algolia (10-20ms)                  │   │
│  │  - Indicator: "Searching offline" or "Searching online"   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Firebase SDK (Firestore)                                  │   │
│  │  - Offline persistence (all data cached locally)          │   │
│  │  - Real-time sync (when online, sync changes)             │   │
│  │  - Limited search (exact match, prefix, no full-text)     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Algolia SDK (Full-text search)                            │   │
│  │  - Online only (requires network)                         │   │
│  │  - Full-text search, typo tolerance, faceting             │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                          │
                          │ Online requests
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Firebase Firestore (Data Storage)              │
│  - Primary data store (posts, users, products)                   │
│  - Real-time sync (live updates)                                 │
│  - Offline-first (full cache)                                    │
└─────────────────────────────────────────────────────────────────┘
                          │
                          │ Cloud Function (on write)
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Algolia (Search Index)                         │
│  - Secondary index (search-optimized)                            │
│  - Full-text search, typo tolerance, faceting                    │
│  - Synced from Firestore (via Cloud Functions)                   │
└─────────────────────────────────────────────────────────────────┘
```

**Hybrid Search Logic** (iOS Swift):
```swift
import Firebase
import InstantSearch

class HybridSearch {
  let algoliaSearcher = HitsSearcher(appID: "APP_ID", apiKey: "SEARCH_KEY", indexName: "products")
  let firestoreDB = Firestore.firestore()

  func search(query: String) async -> [Product] {
    // Check network connectivity
    if isOnline() {
      // Online: Use Algolia (full-text, typo tolerance)
      return await searchAlgolia(query: query)
    } else {
      // Offline: Use Firestore local cache (exact match, prefix only)
      return await searchFirestore(query: query)
    }
  }

  func searchAlgolia(query: String) async -> [Product] {
    let results = try? await algoliaSearcher.search(Query(query))
    return results?.hits.compactMap { hit in
      Product(
        id: hit["objectID"] as? String ?? "",
        title: hit["title"] as? String ?? "",
        price: hit["price"] as? Double ?? 0
      )
    } ?? []
  }

  func searchFirestore(query: String) async -> [Product] {
    // Basic prefix search (Firestore limitation, no full-text)
    let snapshot = try? await firestoreDB.collection("products")
      .whereField("title", isGreaterThanOrEqualTo: query)
      .whereField("title", isLessThanOrEqualTo: query + "\u{f8ff}") // Prefix search trick
      .getDocuments()

    return snapshot?.documents.compactMap { doc in
      Product(
        id: doc.documentID,
        title: doc["title"] as? String ?? "",
        price: doc["price"] as? Double ?? 0
      )
    } ?? []
  }

  func isOnline() -> Bool {
    // Use NetworkMonitor or Reachability to check connectivity
    return NetworkMonitor.shared.isConnected
  }
}
```

---

## Implementation Guide

### Step 1: Algolia Mobile SDK Setup (iOS)

**Install SDK**:
```ruby
# Podfile
pod 'InstantSearch', '~> 7.0'
pod 'AlgoliaSearchClient', '~> 8.0'
```

**Configure index**:
```swift
import InstantSearch
import AlgoliaSearchClient

struct ContentView: View {
  @StateObject var searcher = HitsSearcher(
    appID: "YOUR_APP_ID",
    apiKey: "YOUR_SEARCH_API_KEY",
    indexName: "products"
  )

  @StateObject var queryInputController = TextFieldController()
  @StateObject var hitsController = HitsObservableController<Product>()

  var body: some View {
    VStack {
      SearchBar(textFieldController: queryInputController)
        .padding()

      List(hitsController.hits) { hit in
        ProductRow(product: hit.object)
      }
    }
    .onAppear {
      searcher.connectController(queryInputController)
      searcher.connectController(hitsController)
      searcher.search()
    }
  }
}

struct Product: Codable {
  let objectID: String
  let title: String
  let price: Double
  let thumbnail: String
}

struct ProductRow: View {
  let product: Product

  var body: some View {
    HStack {
      AsyncImage(url: URL(string: product.thumbnail)) { image in
        image.resizable().frame(width: 60, height: 60)
      } placeholder: {
        ProgressView()
      }

      VStack(alignment: .leading) {
        Text(product.title).font(.headline)
        Text("$\(product.price, specifier: "%.2f")").font(.subheadline)
      }
    }
  }
}
```

---

### Step 2: Offline Caching (Algolia SDK)

**Enable offline caching** (automatic in Algolia SDK):
```swift
import AlgoliaSearchClient

let client = SearchClient(appID: "APP_ID", apiKey: "SEARCH_KEY")
let index = client.index(withName: "products")

// Configure offline caching (automatic, last 500 queries cached)
// Cache TTL: 7 days (default)
// Cache size: 10MB (default)

// Search (SDK handles online/offline automatically)
index.search(Query("running shoes")) { result in
  switch result {
  case .success(let response):
    // Response from server (if online) or cache (if offline)
    print("Results: \(response.hits.count)")
  case .failure(let error):
    print("Error: \(error)")
  }
}
```

---

## Testing & Validation

### Performance Testing (Mobile)

**Latency benchmarks** (target: <50ms p95, mobile network):
```swift
import XCTest
import AlgoliaSearchClient

class SearchPerformanceTests: XCTestCase {
  func testSearchLatency() async throws {
    let client = SearchClient(appID: "APP_ID", apiKey: "SEARCH_KEY")
    let index = client.index(withName: "products")

    var latencies: [Double] = []

    // Run 100 searches
    for _ in 0..<100 {
      let start = Date()
      let response = try await index.search(Query("laptop"))
      let latency = Date().timeIntervalSince(start) * 1000 // Convert to ms

      latencies.append(latency)
    }

    let p50 = latencies.sorted()[49]
    let p95 = latencies.sorted()[94]

    print("p50 latency: \(p50)ms")
    print("p95 latency: \(p95)ms")

    XCTAssertLessThan(p95, 50, "p95 latency should be <50ms")
  }
}
```

**Expected results**:
- **Algolia (WiFi)**: 10-20ms p50, 30-40ms p95 ✅
- **Algolia (4G)**: 20-30ms p50, 40-60ms p95 ✅
- **Algolia (3G)**: 50-100ms p50, 150-200ms p95 (acceptable for 3G)

---

### Battery Impact Testing

**Measure battery drain**:
```swift
import XCTest

class BatteryImpactTests: XCTestCase {
  func testBatteryDrain() async throws {
    // Measure battery drain from 100 searches over 10 minutes
    let startBattery = UIDevice.current.batteryLevel
    UIDevice.current.isBatteryMonitoringEnabled = true

    // Simulate 100 searches (1 search every 6 seconds)
    for _ in 0..<100 {
      let _ = try await index.search(Query("random query"))
      try await Task.sleep(nanoseconds: 6_000_000_000) // 6 seconds
    }

    let endBattery = UIDevice.current.batteryLevel
    let batteryDrain = startBattery - endBattery

    print("Battery drain: \(batteryDrain * 100)% over 10 minutes (100 searches)")

    XCTAssertLessThan(batteryDrain, 0.05, "Battery drain should be <5% for 100 searches")
  }
}
```

**Expected results**:
- **Algolia (with caching, debouncing)**: <3% battery drain (100 searches, 10 minutes) ✅
- **No optimization**: 10-15% battery drain (excessive network requests)

---

## Cost-Benefit Analysis (3-Year)

### Scenario: Mobile App (500K MAU, 500K searches/month)

**Baseline (No Search or Basic SQLite Full-Text Search)**:
- Engagement: 20% of users search (basic full-text, slow, no typo tolerance)
- Conversion: 5% (poor search quality → low conversion)

**With Algolia Mobile Search**:
- Engagement: 40% of users search (2× improvement from instant search UX)
- Conversion: 12% (2.4× improvement from typo tolerance, relevance)
- **Incremental engagement**: 500K MAU × (40% - 20%) = 100K more users searching
- **Incremental conversions**: 500K MAU × 40% × (12% - 5%) = 14K more conversions/month

**Revenue Impact** (subscription app, $10/month):
- Incremental conversions: 14K × $10 = **$140K/month**
- **3-year value**: $140K × 36 = **$5.04M**

**TCO**:
- Algolia: $30,820 (3-year)
- Typesense: $39,320 (3-year, higher engineering cost)

**ROI**:
- **Algolia**: ($5.04M - $30.8K) / $30.8K = **163× ROI**
- **Typesense**: ($5.04M - $39.3K) / $39.3K = **128× ROI**

**Winner**: Algolia (best mobile SDKs, pre-built UI, offline caching, highest ROI)

---

## Final Recommendation

### For Mobile-First Apps (iOS + Android, budget $245-1K/month):

**Choose Algolia**:
- ✅ Best mobile SDKs (iOS Swift, Android Kotlin, React Native, Flutter, official)
- ✅ InstantSearch Mobile (pre-built UI, save 80-160 hours)
- ✅ Offline caching (search last results when offline)
- ✅ Battery optimization (automatic debouncing, request batching)
- ✅ <50ms latency (global CDN, 70+ PoPs)
- ✅ 163× ROI (3-year, massive engagement lift)

### For Cost-Conscious Mobile Apps (budget <$120/month):

**Choose Typesense**:
- ✅ 2-4× cheaper than Algolia ($120/month vs $245-500/month)
- ✅ Good performance (<50ms latency)
- ✅ Community mobile SDKs (iOS, Android, Flutter)
- ✅ 128× ROI (3-year, slightly lower due to DIY UI)

### For Offline-First Apps (chat, notes, todo lists):

**Choose Firebase + Algolia Hybrid**:
- ✅ Best offline support (Firestore full offline cache)
- ✅ Real-time sync (live updates)
- ✅ Algolia for full-text search (when online)

---

**Last Updated**: November 14, 2025
**Scenario**: Mobile App Instant Search (iOS/Android)
**Recommended Platform**: Algolia (mobile-first) or Typesense (cost-conscious)
**Expected ROI**: 128-163× (3-year, engagement + conversion lift)
