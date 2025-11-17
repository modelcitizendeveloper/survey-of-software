# Google Cloud Firestore

**Category:** Document Database (Serverless)
**Provider:** Google Cloud Platform
**Type:** Level 3 (Cloud Provider Managed)
**Data Model:** Document (JSON) with real-time sync

---

## Overview

Firestore is Google's serverless document database for mobile, web, and server applications. Successor to Firebase Realtime Database, designed for real-time synchronization and offline support. Part of the Firebase platform.

---

## Pricing

### Free Tier (Spark Plan - Firebase)
- **1 GB storage**
- **50,000 reads/day**
- **20,000 writes/day**
- **20,000 deletes/day**
- **10 GB/month network egress**
- **No credit card required**

### Pay-As-You-Go (Blaze Plan)
**Firestore Native Mode:**
- **Stored data:** $0.18/GB/month
- **Document reads:** $0.06 per 100,000 documents
- **Document writes:** $0.18 per 100,000 documents
- **Document deletes:** $0.02 per 100,000 documents
- **Network egress:** $0.12/GB (10GB free/month)

**Example costs:**
- 1M reads/month: $0.60
- 100K writes/month: $0.18
- 10GB storage: $1.80
- **Total: ~$2.58/month** for small app

### Firestore in Datastore Mode
- **Alternative mode:** Legacy Datastore API compatibility
- Same pricing as Native mode
- Lacks real-time listeners and offline support

---

## Key Strengths

1. **Real-Time Sync:** Automatic real-time updates to all connected clients
2. **Offline Support:** Local persistence, automatic sync when online
3. **Firebase Integration:** Auth, hosting, functions, analytics in one platform
4. **Generous Free Tier:** 50K reads/day is substantial for small apps
5. **Serverless:** Auto-scales, no capacity planning
6. **Multi-Platform SDKs:** Web, iOS, Android, Flutter native support
7. **Security Rules:** Declarative rules language for access control
8. **Simple Pricing:** Pay per operation, very predictable

---

## Key Weaknesses

1. **Query Limitations:** No OR queries, limited array queries, composite index required for many queries
2. **GCP Lock-in:** Proprietary API, no compatible alternatives
3. **Cost at Scale:** Per-operation pricing adds up for read-heavy apps
4. **1 MB Document Limit:** Smaller than MongoDB (16MB)
5. **Limited Aggregations:** No built-in COUNT, SUM, AVG (must compute client-side)
6. **Complex Index Management:** Composite indexes required, can be confusing
7. **No Transactions Across Collections:** Transactions limited to 500 documents

---

## Use Cases

**Best For:**
- Mobile applications (offline-first, real-time sync)
- Chat applications (real-time messaging)
- Collaborative tools (live updates)
- Gaming leaderboards (real-time scores)
- Social feeds (real-time posts)
- Firebase ecosystem apps (integrated platform)
- Serverless web apps (Firebase Hosting + Functions)

**Not Ideal For:**
- Complex queries (use MongoDB or SQL)
- Analytics (use BigQuery)
- High-volume batch processing (use Bigtable)
- Relational data (use Cloud SQL)
- Full-text search (need Algolia/Meilisearch)

---

## Lock-in Assessment

**API:** Proprietary Google/Firebase API
- **Migration Path:** Difficult (unique real-time API)
- **Compatibility:** None
- **Migration Cost:** High (client SDK rewrite + server logic)
- **Egress Costs:** $0.12/GB after 10GB free

**Export Options:**
- Firestore export to Cloud Storage (JSON format)
- Firestore Dataflow templates (BigQuery, Bigtable)
- Manual export via client SDK

**Mitigation:**
- Abstract database layer (harder with real-time features)
- Use Firebase emulator for local development
- Export regularly to Cloud Storage

---

## Ecosystem

- **Client SDKs:** Web, iOS, Android, Flutter, Unity, C++
- **Server SDKs:** Node.js, Python, Java, Go, PHP, Ruby
- **Firebase Platform:**
  - Authentication
  - Cloud Functions
  - Hosting
  - Storage
  - Analytics
  - Crashlytics
- **Community:** Large mobile developer community
- **Documentation:** Excellent

---

## Firestore vs Firebase Realtime Database

| Feature | Firestore | Realtime Database |
|---------|-----------|-------------------|
| Data model | Collections + Documents | JSON tree |
| Querying | Rich queries | Limited |
| Offline | Advanced | Basic |
| Scaling | Automatic, better | Manual sharding |
| Pricing | Per operation | Per GB + connection |
| Status | Recommended | Legacy |

**Recommendation:** Use Firestore for new projects

---

## Decision Factors

**Choose Firestore if:**
- Building mobile app with offline support
- Real-time sync is core feature
- Using Firebase ecosystem (auth, hosting, functions)
- Simple data model, simple queries
- Generous free tier fits your usage
- GCP is your cloud

**Choose alternative if:**
- Complex queries needed (MongoDB)
- Multi-cloud required (MongoDB Atlas)
- High read volume (DynamoDB cheaper at scale)
- Relational data (PostgreSQL)
- Vendor lock-in unacceptable (self-hosted)

---

## Competitive Position

- **vs DynamoDB:** Better real-time sync, easier queries, but GCP-only
- **vs MongoDB:** Better for mobile real-time, worse for complex server-side queries
- **vs PostgreSQL:** Better for mobile offline, worse for relational data
- **vs Supabase:** Firebase is document DB, Supabase is PostgreSQL (relational)
- **vs Realtime Database:** Firestore is more powerful, better scaling

---

## Real-Time Features

**Real-time listeners:**
```javascript
// Client automatically updates on changes
db.collection('posts').onSnapshot(snapshot => {
  snapshot.docChanges().forEach(change => {
    if (change.type === 'added') { /* handle new */ }
    if (change.type === 'modified') { /* handle update */ }
    if (change.type === 'removed') { /* handle delete */ }
  })
})
```

**Offline persistence:**
- Automatic local cache
- Writes queued when offline
- Auto-sync when connection restored

---

## Security Rules

Declarative access control:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Only authenticated users can read/write their own data
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

---

**Recommendation Category:** Best real-time document DB for mobile (Path 1)
**Open Source Alternative:** None with real-time sync (PouchDB/CouchDB closest) (Path 3)
**Standard-Based Alternative:** None (proprietary real-time protocol)
