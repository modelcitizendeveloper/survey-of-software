# Use Case: Mobile Application
## Error Tracking for iOS/Android Apps

**Pattern**: Native or cross-platform mobile application
**Stack**: iOS (Swift), Android (Kotlin), React Native, Flutter
**Example**: Consumer mobile app, mobile-first SaaS, hybrid app

---

## Scenario Description

### Who This Is For

- Mobile app developers (iOS, Android, React Native, Flutter)
- Consumer apps with 1K-1M+ users
- Mobile-first SaaS products
- Hybrid apps with native + web views
- Apps in TestFlight/Google Play beta testing

### Typical Architecture

```
Mobile App → REST/GraphQL API
    ↓
  Device Storage (SQLite, Core Data, Room)
    ↓
  Push Notifications (FCM, APNs)
    ↓
  Third-party SDKs (Analytics, Auth, Payment)
```

### Pain Points to Solve

1. Crash reports from app stores (vague, no context)
2. Device-specific bugs (works on iPhone 15, crashes on Android 12)
3. Network errors (offline mode, timeouts, API failures)
4. Third-party SDK crashes (Firebase, Facebook SDK, payment libs)
5. Memory leaks and performance issues
6. Release-specific regressions (new version breaks feature)
7. Unable to reproduce user-reported crashes

---

## Requirements Profile

### Must-Have Features

- **Native SDKs** for iOS (Swift/Objective-C), Android (Kotlin/Java)
- **Crash reporting** with full stack traces and symbolication
- **Session tracking** to measure crash-free sessions rate
- **Breadcrumbs** showing user actions, network calls, screen views
- **Device context** (OS version, device model, memory, battery, network)
- **Release tracking** to correlate crashes with app versions
- **Symbol upload** for deobfuscation (ProGuard, R8, dSYM)

### Nice-to-Have Features

- ANR detection (Application Not Responding on Android)
- Network monitoring (API call performance)
- Custom events and user properties
- Real-time alerting (critical crash spikes)
- Integration with app stores (auto-fetch dSYMs)
- Stability scores (prioritize by user impact)
- User feedback in-app widget

### Budget Reality

- Side project: $0/month (free tier)
- Indie developer: $0-50/month
- Startup: $50-200/month
- Scale-up: $200-1,000/month
- Enterprise: $1,000+/month

### Session Volume Estimate

- Early (1K MAU): 10K-50K sessions/month
- Growth (10K MAU): 100K-500K sessions/month
- Scale (100K MAU): 1M-5M sessions/month
- Viral (1M+ MAU): 10M+ sessions/month

---

## Provider Fit Analysis

### Bugsnag (Score: 95/100)

**Strengths:**
- Mobile-first product (best iOS/Android SDKs)
- Stability scores (crash-free session rate)
- Session tracking (errors per session)
- Excellent symbolication (auto dSYM upload)
- Release health dashboard
- ANR detection on Android
- React Native first-class support

**Pricing for Mobile:**
- Free: 7,500 events/month, 1M spans
- Lite ($18/mo): 50K events/month, 3M spans
- Standard ($59/mo): 200K events/month, 10M spans

**SDK Size:** Small (<500KB impact on app size)

**TCO (12 months):**
- Early (10K MAU): $0 (free tier)
- Growth (50K MAU): $216/year (Lite)
- Scale (200K MAU): $708/year (Standard)

**Integration Effort:** 2 hours (CocoaPods/Gradle + symbol upload)

### Sentry (Score: 92/100)

**Strengths:**
- Excellent iOS/Android native SDKs
- Performance monitoring (slow frame rates, startup time)
- Session replay (for mobile web views)
- Release health tracking
- Source context (code snippets in stack traces)
- Attachment support (screenshots, logs)

**Pricing for Mobile:**
- Free: 5K errors/month
- Team ($26/mo): 50K errors/month
- Business ($80/mo): 500K errors/month + performance

**SDK Size:** Medium (~1MB impact)

**TCO (12 months):**
- Early (10K MAU): $0 (free tier)
- Growth (50K MAU): $312/year (Team)
- Scale (200K MAU): $960/year (Business)

**Integration Effort:** 3 hours (SPM/Gradle + debug symbol upload)

### Rollbar (Score: 85/100)

**Strengths:**
- Good iOS/Android SDKs
- People tracking (crashes per user)
- Telemetry (events before crash)
- Spike protection
- RQL for custom queries

**Pricing for Mobile:**
- Free: 5K errors/month
- Essentials ($24.17/mo): 50K errors/month
- Advanced ($99/mo): 500K errors/month

**SDK Size:** Medium (~800KB impact)

**TCO (12 months):**
- Early (10K MAU): $0 (free tier)
- Growth (50K MAU): $290/year (Essentials)
- Scale (200K MAU): $1,188/year (Advanced)

**Integration Effort:** 3 hours (CocoaPods/Gradle + config)

### Firebase Crashlytics (Score: 88/100)

**Strengths:**
- Free (no usage limits)
- Deeply integrated with Firebase ecosystem (Analytics, Remote Config, etc.)
- Automatic symbol upload (no manual dSYM management)
- Real-time crash reporting
- Velocity alerts (crash spikes)
- Crash-free users metric

**Weaknesses:**
- Locked into Google ecosystem
- Less feature-rich than Bugsnag/Sentry
- Limited querying capabilities
- No performance monitoring built-in

**Pricing for Mobile:**
- Free: Unlimited (part of Firebase free tier)

**SDK Size:** Large (~2MB with Firebase SDK)

**TCO (12 months):**
- All stages: $0/year

**Integration Effort:** 2 hours (Firebase setup + Crashlytics plugin)

### Datadog Mobile (Score: 78/100)

**Strengths:**
- Full mobile observability (crashes + performance + logs)
- User session tracking
- Real User Monitoring (RUM)
- Best for teams using Datadog backend

**Weaknesses:**
- Expensive for mobile-only use case
- Overkill for simple crash tracking
- Complex pricing model

**Pricing for Mobile:**
- Mobile RUM: $1.50 per 1,000 sessions
- Typical: 100K sessions/month = $150/month

**SDK Size:** Large (~2MB+ impact)

**TCO (12 months):**
- Early (50K sessions): $900/year
- Growth (500K sessions): $9,000/year
- Scale (2M sessions): $36,000/year

**Integration Effort:** 4 hours (SDK + RUM config)

### Honeybadger (Score: 72/100)

**Strengths:**
- Simple pricing (unlimited users)
- Good documentation
- Privacy-focused

**Weaknesses:**
- Less mature mobile SDKs
- Fewer mobile-specific features
- No stability scores

**Pricing for Mobile:**
- Free: 5K errors/month
- Small ($39/mo): 150K errors/month

**SDK Size:** Medium (~1MB impact)

**TCO (12 months):**
- Early (10K MAU): $0 (free tier)
- Growth (50K MAU): $468/year (Small)
- Scale (200K MAU): $468/year (Small)

**Integration Effort:** 3 hours (manual SDK setup)

---

## Recommendation

### Top Choice: Bugsnag (95/100)

**Why Bugsnag wins for mobile:**
1. **Mobile-first design** - Built specifically for iOS/Android crash tracking
2. **Stability scores** - Prioritize crashes by user impact (crash-free session rate)
3. **Session tracking** - See errors per session ratio
4. **Automatic symbolication** - Best dSYM/ProGuard handling in market
5. **Cost-effective** - $18/mo for 50K events (cheaper than Sentry)

**When to choose Bugsnag:**
- Pure mobile app (iOS, Android, React Native, Flutter)
- Need crash-free session metrics
- Want simplicity over full observability
- Budget-conscious startup

**Migration Path:**
- Start: Free tier (7,500 events) during beta/TestFlight
- Growth: Lite plan ($18/mo) at public launch
- Scale: Standard plan ($59/mo) at 100K+ MAU

### Runner-Up: Sentry (92/100)

**When to choose Sentry:**
- You have mobile + backend (unified error tracking)
- You need performance monitoring (slow frames, startup time)
- You want advanced debugging (source context, attachments)
- Team already uses Sentry for web/backend

**Trade-offs vs Bugsnag:**
- More expensive ($26/mo vs $18/mo at entry tier)
- Larger SDK size (~1MB vs ~500KB)
- Better integration ecosystem
- Performance monitoring included

### Free Alternative: Firebase Crashlytics (88/100)

**When to choose Firebase Crashlytics:**
- Budget is $0 (free forever)
- You're already using Firebase (Auth, Firestore, Analytics)
- You need basic crash tracking (not advanced features)
- You don't mind Google ecosystem lock-in

**Trade-offs vs Bugsnag:**
- Free (huge advantage)
- Larger SDK size (~2MB)
- Less powerful querying
- No performance monitoring
- Auto symbol upload (easier setup)

---

## Cost Comparison: 12-Month TCO

### Early Stage (10K MAU, 30K sessions/month, 5K crashes/month)
- **Bugsnag**: $0 (free tier)
- **Sentry**: $0 (free tier)
- **Rollbar**: $0 (free tier)
- **Firebase**: $0 (free forever)
- **Datadog**: $540/year (30K sessions)
- **Honeybadger**: $0 (free tier)

**Winner: All free tiers (tie)**

### Growth Stage (50K MAU, 150K sessions/month, 30K crashes/month)
- **Bugsnag**: $216/year (Lite)
- **Sentry**: $312/year (Team)
- **Rollbar**: $290/year (Essentials)
- **Firebase**: $0 (free forever)
- **Datadog**: $2,700/year (150K sessions)
- **Honeybadger**: $468/year (Small)

**Winner: Firebase ($0), but Bugsnag best paid option at $216/year**

### Scale Stage (200K MAU, 600K sessions/month, 150K crashes/month)
- **Bugsnag**: $708/year (Standard)
- **Sentry**: $960/year (Business)
- **Rollbar**: $1,188/year (Advanced)
- **Firebase**: $0 (free forever)
- **Datadog**: $10,800/year (600K sessions)
- **Honeybadger**: $468/year (Small)

**Winner: Firebase ($0), Honeybadger ($468) if need more features, Bugsnag ($708) for mobile-specific features**

---

## Mobile SDK Size Impact

**App size matters for downloads:**

- **Bugsnag**: ~500KB (best for mobile)
- **Honeybadger**: ~1MB
- **Sentry**: ~1MB
- **Rollbar**: ~800KB
- **Firebase**: ~2MB (includes base Firebase SDK)
- **Datadog**: ~2MB+

For mobile apps, SDK size directly impacts download rates. Every 6MB increase = 1% drop in conversions. Bugsnag's 500KB footprint is negligible.

---

## Implementation Guide

### Bugsnag Setup (Recommended for Paid)

**iOS (Swift):**
```swift
// Podfile
pod 'Bugsnag'

// AppDelegate.swift
import Bugsnag

func application(_ application: UIApplication,
                 didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {

    Bugsnag.start(withApiKey: "YOUR_API_KEY")

    // Add user context
    Bugsnag.setUser("12345", withEmail: "user@example.com", andName: "John Doe")

    // Add custom metadata
    Bugsnag.addMetadata(["plan": "premium"], toSection: "user")

    return true
}
```

**Android (Kotlin):**
```kotlin
// build.gradle (app)
dependencies {
    implementation 'com.bugsnag:bugsnag-android:5.+'
}

// Application.kt
import com.bugsnag.android.Bugsnag

class MyApplication : Application() {
    override fun onCreate() {
        super.onCreate()

        Bugsnag.start(this, "YOUR_API_KEY")

        // Set user
        Bugsnag.setUser("12345", "user@example.com", "John Doe")

        // Add metadata
        Bugsnag.addMetadata("user", "plan", "premium")
    }
}
```

**Time to first crash:** 15 minutes
**Time to full setup:** 2 hours (including symbol upload automation)

### Firebase Crashlytics Setup (Recommended for Free)

**iOS:**
```swift
// Podfile
pod 'Firebase/Crashlytics'

// AppDelegate.swift
import Firebase

func application(_ application: UIApplication,
                 didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {

    FirebaseApp.configure()

    // Set user identifier
    Crashlytics.crashlytics().setUserID("12345")

    // Custom keys
    Crashlytics.crashlytics().setCustomValue("premium", forKey: "plan")

    return true
}
```

**Android:**
```kotlin
// build.gradle (app)
plugins {
    id 'com.google.gms.google-services'
    id 'com.google.firebase.crashlytics'
}

dependencies {
    implementation 'com.google.firebase:firebase-crashlytics'
}

// Application.kt
class MyApplication : Application() {
    override fun onCreate() {
        super.onCreate()

        // Set user
        FirebaseCrashlytics.getInstance().setUserId("12345")

        // Custom keys
        FirebaseCrashlytics.getInstance().setCustomKey("plan", "premium")
    }
}
```

**Time to first crash:** 20 minutes (Firebase setup overhead)
**Time to full setup:** 2 hours

---

## Key Takeaways

1. **Bugsnag for serious mobile apps** - Best mobile SDKs, stability scores, $18/mo entry
2. **Firebase Crashlytics for free** - Zero cost, good enough for most apps, Google lock-in
3. **Sentry for full-stack** - Unified if you have mobile + backend errors
4. **Avoid Datadog Mobile unless enterprise** - 10x more expensive than alternatives
5. **SDK size matters** - Bugsnag 500KB vs Firebase 2MB impacts app downloads
6. **Stability scores critical** - Crash-free session rate is key mobile metric
