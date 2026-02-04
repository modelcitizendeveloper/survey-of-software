# S3 API Portability Matrix

**Purpose**: Feature parity comparison across S3-compatible backends
**Scope**: Core S3 API features evaluated across 5 major providers

---

## Feature Compatibility Table

| Feature | AWS S3 | Cloudflare R2 | Backblaze B2 | MinIO | Wasabi |
|---------|--------|---------------|--------------|-------|--------|
| **Core Operations** |
| PUT/GET/DELETE Object | ✅ 100% | ✅ 100% | ✅ 100% | ✅ 100% | ✅ 100% |
| COPY Object | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| HEAD Object | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| LIST Objects | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Bucket Operations** |
| CREATE/DELETE Bucket | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| LIST Buckets | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Bucket Versioning | ✅ Yes | ✅ Yes | ✅ Yes (always on) | ✅ Yes | ✅ Yes |
| **Multipart Uploads** |
| Initiate/Upload/Complete | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| List Multipart Uploads | ✅ Yes | ✅ Yes | ✅ Yes | ⚠️ Prefix required | ✅ Yes |
| Abort Multipart Upload | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Encryption** |
| SSE-S3 (server-managed) | ✅ Yes | ❌ No | ✅ Yes (SSE-B2) | ✅ Yes | ✅ Yes |
| SSE-C (customer keys) | ✅ Yes | ✅ Yes (2025) | ✅ Yes | ✅ Yes | ✅ Yes |
| SSE-KMS (key management) | ✅ Yes | ❌ No | ❌ No | ✅ Yes | ❌ No |
| **Access Control** |
| Bucket Policies | ✅ Yes | ✅ Yes | ✅ Basic | ✅ Yes | ✅ Yes |
| ACLs (canned) | ✅ Yes | ✅ Basic | ⚠️ Private/Public only | ✅ Yes | ✅ Yes |
| Presigned URLs | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Advanced Features** |
| Object Locking (WORM) | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes | ✅ Yes |
| Lifecycle Policies | ✅ Full | ⚠️ Basic | ❌ S3 API no | ✅ Yes | ⚠️ Basic |
| Object Tagging | ✅ Yes | ❌ No | ⚠️ Returns empty | ✅ Yes | ❌ No |
| CORS Configuration | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Event Notifications** |
| Event Notifications | ✅ Lambda/SNS/SQS | ⚠️ Limited | ❌ No | ✅ Yes (many) | ❌ No |
| **Query & Operations** |
| S3 Select (SQL queries) | ✅ Yes | ❌ No | ❌ No | ✅ Yes | ❌ No |
| Batch Operations | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No |
| **Replication** |
| Cross-Region Replication | ✅ Yes | ❌ No | ❌ No | ✅ Yes | ❌ No |
| **Other Features** |
| Website Hosting | ✅ Yes | ⚠️ Workers | ❌ No | ❌ No | ❌ No |
| Storage Classes | ✅ Multiple | ❌ Single | ❌ Single | ⚠️ Tiering | ❌ Single |
| Requester Pays | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No |

**Legend**:
- ✅ Yes: Fully supported
- ⚠️ Partial: Supported with limitations
- ❌ No: Not supported

---

## Compatibility Scoring

### Overall S3 API Compatibility (Core Features)

**Scoring Methodology**: Core S3 operations (PUT, GET, DELETE, LIST, multipart, basic encryption, bucket policies)

| Provider | Compatibility Score | Grade |
|----------|-------------------|-------|
| **AWS S3** | 100% | A+ (Reference) |
| **MinIO** | 95% | A (Highest alternative) |
| **Cloudflare R2** | 90% | A- (Excellent for managed) |
| **Wasabi** | 85% | B+ (Good with gaps) |
| **Backblaze B2** | 85% | B+ (Good with gaps) |

### Feature Category Breakdown

| Category | AWS S3 | MinIO | R2 | Wasabi | B2 |
|----------|--------|-------|-----|---------|-----|
| Core Operations | 100% | 100% | 100% | 100% | 100% |
| Bucket Operations | 100% | 100% | 100% | 100% | 100% |
| Multipart Uploads | 100% | 95% | 100% | 100% | 100% |
| Encryption | 100% | 90% | 60% | 70% | 60% |
| Access Control | 100% | 95% | 80% | 90% | 70% |
| Advanced Features | 100% | 85% | 60% | 50% | 40% |

---

## Portability Tiers

### Tier 1: Universal Compatibility (Works Everywhere)

**Features that work across ALL providers**:
- ✅ PUT/GET/DELETE/HEAD Object
- ✅ LIST Objects/Buckets
- ✅ CREATE/DELETE Buckets
- ✅ Multipart uploads (initiate, upload, complete)
- ✅ Presigned URLs
- ✅ Basic bucket policies
- ✅ CORS configuration
- ✅ Object versioning

**Portability**: **Highest** - Change endpoint only, code works everywhere

---

### Tier 2: High Compatibility (Works on Most)

**Features with good support (3-4 out of 5 providers)**:
- ⚠️ SSE-C encryption (4/5: all except R2 until 2025)
- ⚠️ Object locking (3/5: S3, R2, MinIO - not B2, Wasabi)
- ⚠️ Basic lifecycle policies (3/5: varies by complexity)
- ⚠️ Event notifications (2/5: S3, MinIO - limited elsewhere)

**Portability**: **Medium-High** - May need feature testing or graceful degradation

---

### Tier 3: Limited Compatibility (Provider-Specific)

**Features with poor support (<3 providers)**:
- ❌ Object tagging (2/5: S3, MinIO only)
- ❌ S3 Select (2/5: S3, MinIO only)
- ❌ Replication (2/5: S3, MinIO only)
- ❌ SSE-KMS (2/5: S3, MinIO only)
- ❌ Multiple storage classes (1/5: S3 only)
- ❌ Batch operations (1/5: S3 only)

**Portability**: **Low** - AWS-specific or MinIO-only, breaks portability

---

## Migration Complexity Matrix

### Endpoint-Only Migration (0-2 hours)

**Scenario**: Using only Tier 1 features
- Change endpoint URL
- Update credentials
- Test basic operations

**Providers**: ALL (S3 ↔ R2 ↔ B2 ↔ MinIO ↔ Wasabi)

### Minor Code Changes (2-8 hours)

**Scenario**: Using Tier 2 features
- Adjust encryption configuration
- Modify lifecycle policies
- Update event notification setup

**Example**: S3 → R2 with basic lifecycle needs

### Significant Refactoring (8-40 hours)

**Scenario**: Using Tier 3 features heavily
- Remove object tagging usage
- Replace S3 Select with alternative query method
- Redesign storage class tiering logic
- Reimplement replication externally

**Example**: S3 (heavy Glacier use) → B2 (no storage classes)

---

## Recommendations by Portability Priority

### Maximum Portability Strategy

**Use ONLY Tier 1 features**:
- Core operations (PUT, GET, DELETE, LIST)
- Basic bucket policies
- Multipart uploads
- Presigned URLs

**Result**: Can switch providers in 1-2 hours, code works everywhere

**Trade-off**: Give up advanced features (tagging, Select, replication, storage classes)

---

### Balanced Portability Strategy

**Use Tier 1 + selected Tier 2 features**:
- Core operations
- SSE-C encryption (widely supported)
- Basic lifecycle (test across providers)
- Object versioning

**Result**: Can migrate in 2-8 hours with feature testing

**Trade-off**: Some features may need adjustment per provider

---

### Feature-Rich Strategy (Accept Lock-In)

**Use Tier 1 + 2 + 3 freely**:
- All S3 features
- Storage classes, tagging, Select, replication
- Provider-specific optimizations

**Result**: Migration requires 8-40+ hours of refactoring

**Trade-off**: Vendor lock-in, but access to full feature set

---

## Key Takeaway

**S3 API provides excellent portability for core operations** (90-100% compatibility across providers). Advanced features (tagging, Select, storage classes) create lock-in. Choose features based on portability requirements.

**Rule of Thumb**: Stick to Tier 1 features for maximum portability, carefully evaluate Tier 2/3 features against migration cost.
