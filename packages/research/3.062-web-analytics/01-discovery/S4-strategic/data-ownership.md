# Data Ownership & Export Analysis
## Raw Data Access, API Capabilities, Backup Strategies

**Created:** October 11, 2025
**Focus:** Data control, export capabilities, vendor independence
**Strategic Question:** Can you get your data out when you need it?

---

## Core Principle

**Data ownership = vendor independence.** The ability to export complete, usable data determines:
1. **Migration feasibility** (Can you leave this vendor?)
2. **Analysis depth** (Can you run custom queries?)
3. **Backup reliability** (Can you archive historical data?)
4. **Compliance** (Can you demonstrate data control to auditors?)

---

## Data Ownership Spectrum

### Tier 1: Maximum Ownership (Self-Hosted, Direct Database Access)

**Providers:** Umami, Matomo, PostHog (self-hosted), GoatCounter (self-hosted), Plausible (self-hosted)

**Characteristics:**
- ✅ **Direct Database Access:** PostgreSQL, MySQL, ClickHouse - raw SQL queries anytime
- ✅ **100% Data Control:** Data never leaves your infrastructure (GDPR dream)
- ✅ **Instant Export:** `pg_dump` OR `SELECT * INTO OUTFILE` = complete backup in minutes
- ✅ **Custom Analysis:** Connect Metabase, Redash, Tableau directly to analytics database
- ✅ **No Vendor Gatekeeping:** No API rate limits, no export restrictions, no export fees
- ✅ **Compliance Proof:** Auditors can verify data residency (servers you control)

**Example: Umami (PostgreSQL)**
```sql
-- Export all pageviews for last 30 days
SELECT
  website_id,
  session_id,
  created_at,
  url,
  referrer,
  browser,
  os,
  device,
  country
FROM pageview
WHERE created_at >= NOW() - INTERVAL '30 days'
ORDER BY created_at DESC;

-- Export to CSV
COPY (SELECT * FROM pageview WHERE created_at >= '2025-01-01')
TO '/tmp/pageviews-2025.csv' WITH CSV HEADER;
```

**Time to Export:** 5-30 minutes (depends on data volume, database size)
**Cost:** $0 (direct database access, no vendor fees)

### Tier 2: High Ownership (Managed with Comprehensive API)

**Providers:** Plausible (cloud), PostHog (cloud), Mixpanel, Amplitude, Matomo Cloud

**Characteristics:**
- ✅ **Full API Access:** RESTful API, programmatic export of all data
- ✅ **Bulk Export:** `/api/stats` endpoints return JSON (pageviews, events, sources)
- ⚠️ **API Rate Limits:** 600 requests/hour (Plausible), 20 requests/second (PostHog)
- ⚠️ **Complex Schemas:** Event-based data requires scripts to flatten/transform
- ❌ **No Direct Database:** Can't run raw SQL, must use vendor API abstractions

**Example: Plausible API**
```bash
# Export stats for last 30 days (curl)
curl "https://plausible.io/api/v1/stats/aggregate?site_id=yourdomain.com&period=30d&metrics=visitors,pageviews,bounce_rate&api_key=YOUR_API_KEY"

# Response (JSON):
{
  "results": {
    "visitors": { "value": 12543 },
    "pageviews": { "value": 28901 },
    "bounce_rate": { "value": 42.3 }
  }
}

# Export timeseries data (daily breakdown)
curl "https://plausible.io/api/v1/stats/timeseries?site_id=yourdomain.com&period=30d&metrics=visitors,pageviews"
```

**Time to Export:** 1-4 hours (API scripting, rate limit handling, data transformation)
**Cost:** $0-50 (API access included in Plausible plan, Mixpanel charges for high-volume exports)

### Tier 3: Moderate Ownership (CSV Export via UI)

**Providers:** Fathom, Simple Analytics, Cloudflare Analytics (limited)

**Characteristics:**
- ✅ **CSV Export:** Download button in dashboard
- ✅ **Simple Format:** Pageviews, sources, devices in tabular CSV
- ⚠️ **Manual Process:** No API automation, must click export monthly
- ⚠️ **Limited Granularity:** Daily aggregates, not raw event-level data
- ❌ **Incomplete History:** Export limits (e.g., last 90 days, last 1,000 rows)

**Example: Fathom Export**
- Dashboard → Export → Date Range → Download CSV
- Receives: `pageviews.csv` with columns: Date, Page, Visitors, Pageviews, Bounce Rate
- Missing: Raw event timestamps, session IDs, custom event properties

**Time to Export:** 10-30 minutes (manual download, one file per metric)
**Cost:** $0 (included in subscription)
**Limitation:** No programmatic access, must export manually every month for backups

### Tier 4: Low Ownership (Limited Export)

**Providers:** Google Analytics 4 (free), Cloudflare Analytics, Counter.dev

**Characteristics:**
- ⚠️ **Limited Export:** GA4 UI export = 5,000 row limit
- ⚠️ **BigQuery Required:** GA4 raw data export = paid BigQuery export (GA360 or manual setup)
- ❌ **Incomplete Data:** Cloudflare Web Analytics = no export API (viewing only)
- ❌ **Aggregated Only:** No event-level data, only pre-aggregated metrics

**Example: Google Analytics 4**
- Free tier: UI export = 5,000 rows maximum (inadequate for 100K+ pageviews/month)
- BigQuery export: Setup required, streaming cost ~$5-50/month (depends on volume)
- BigQuery query:
```sql
SELECT
  event_date,
  event_name,
  user_pseudo_id,
  geo.country,
  device.category
FROM `your-project.analytics_XXXXXXXX.events_*`
WHERE _TABLE_SUFFIX BETWEEN '20250101' AND '20250131'
LIMIT 1000000;
```

**Time to Export:** 5-15 hours (BigQuery setup, schema learning, query optimization)
**Cost:** $5-50/month (BigQuery storage + queries)
**Complexity:** HIGH (SQL knowledge, GCP billing, data warehouse management)

### Tier 5: No Ownership (No Export)

**Providers:** (Rare in modern analytics, but some legacy/free tools)

**Characteristics:**
- ❌ **Viewing Only:** Dashboard access, no data export capability
- ❌ **Vendor Lock-In:** Complete dependency, migration impossible

**Example:** None in mainstream web analytics (2025), but beware small/unknown tools

---

## Raw Data Access Comparison

| Provider | Access Method | Data Format | Granularity | Time to Export | Cost | Ownership Score |
|----------|---------------|-------------|-------------|----------------|------|-----------------|
| **Umami (Self-hosted)** | Direct DB (PostgreSQL) | SQL table | Event-level | 5-30 min | $0 | 100/100 |
| **Matomo (Self-hosted)** | Direct DB (MySQL) | SQL table | Event-level | 5-30 min | $0 | 100/100 |
| **PostHog (Self-hosted)** | Direct DB (ClickHouse) | Columnar | Event-level | 10-60 min | $0 | 100/100 |
| **Plausible (Cloud)** | REST API | JSON | Aggregate + events | 1-4 hrs | $0 | 85/100 |
| **PostHog (Cloud)** | REST API + UI export | JSON/CSV | Event-level | 1-4 hrs | $0 | 85/100 |
| **Mixpanel** | Export API + Data Pipelines | JSON | Event-level | 2-8 hrs | $0-500 | 75/100 |
| **Amplitude** | Export API + Data Warehouse Sync | JSON/Snowflake | Event-level | 2-8 hrs | $0-500 | 75/100 |
| **Fathom** | CSV export (UI) | CSV | Daily aggregates | 10-30 min | $0 | 70/100 |
| **Simple Analytics** | CSV/Raw export (UI) | CSV | Event-level (limited) | 10-30 min | $0 | 70/100 |
| **Matomo Cloud** | API + Plugins | JSON/CSV | Aggregate + raw | 1-4 hrs | $0 | 80/100 |
| **GA4 (Free)** | UI export (5K limit) + BigQuery | CSV/SQL | Aggregate/Event | 5-15 hrs (BQ setup) | $5-50/mo (BQ) | 60/100 |
| **Cloudflare Analytics** | None | N/A | N/A | N/A | N/A | 40/100 |
| **GoatCounter (Hosted)** | CSV export (UI) | CSV | Aggregate | 10-30 min | $0 | 70/100 |
| **Counter.dev** | Unknown/Limited | CSV (assumed) | Aggregate | Unknown | $0 | 50/100 |
| **Piwik PRO** | API + Data Warehouse | JSON/SQL | Event-level | 2-6 hrs | $0 | 80/100 |
| **Heap** | Export API | JSON | Event-level | 2-8 hrs | $0-500 | 75/100 |

**Scoring Criteria:**
- 100: Direct database access (self-hosted)
- 80-90: Comprehensive API, event-level export
- 60-75: CSV export OR API with limitations (rate limits, complexity)
- 40-50: Limited export (UI only, row limits, no API)
- 0-30: No export capability

---

## API Capabilities Deep-Dive

### Plausible API (Best Managed API)

**Endpoints:**
- `/api/v1/stats/aggregate` - Visitors, pageviews, bounce rate, visit duration (single metric)
- `/api/v1/stats/timeseries` - Daily/hourly breakdown (trend data)
- `/api/v1/stats/breakdown` - Group by page, source, country, device, browser, OS
- `/api/v1/stats/realtime/visitors` - Current live visitors

**Authentication:** API key (generated in account settings)

**Rate Limit:** 600 requests/hour (10 requests/minute)

**Export Script Example (Python):**
```python
import requests
import csv
from datetime import datetime, timedelta

API_KEY = "YOUR_API_KEY"
SITE_ID = "yourdomain.com"
BASE_URL = "https://plausible.io/api/v1"

# Export last 30 days of page stats
end_date = datetime.now().date()
start_date = end_date - timedelta(days=30)

response = requests.get(
    f"{BASE_URL}/stats/breakdown",
    params={
        "site_id": SITE_ID,
        "period": "custom",
        "date": f"{start_date},{end_date}",
        "property": "event:page",
        "metrics": "visitors,pageviews,bounce_rate,visit_duration"
    },
    headers={"Authorization": f"Bearer {API_KEY}"}
)

data = response.json()

# Write to CSV
with open('plausible-pages.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=['page', 'visitors', 'pageviews', 'bounce_rate', 'visit_duration'])
    writer.writeheader()
    for row in data['results']:
        writer.writerow({
            'page': row['page'],
            'visitors': row['visitors'],
            'pageviews': row['pageviews'],
            'bounce_rate': row['bounce_rate'],
            'visit_duration': row['visit_duration']
        })

print(f"Exported {len(data['results'])} pages to plausible-pages.csv")
```

**Time:** 30-60 minutes (script development, one-time)
**Reusable:** Yes (schedule monthly export via cron)

### PostHog API (Event-Level Export)

**Endpoints:**
- `/api/event` - Raw events export (paginated)
- `/api/insights` - Funnel, trend, retention query results
- `/api/person` - User profile data (if user tracking enabled)

**Authentication:** Personal API key (Settings → API)

**Rate Limit:** 20 requests/second (generous)

**Export Script Example:**
```bash
# Export events for last 7 days (cURL + jq)
curl "https://app.posthog.com/api/event/?limit=100&after=2025-01-04" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  | jq -r '.results[] | [.timestamp, .event, .properties."\$current_url", .properties."\$browser"] | @csv' \
  > posthog-events.csv
```

**Complexity:** Medium (pagination required for large datasets, 100 events/page)

### Mixpanel Export API

**Raw Data Export:**
- Endpoint: `/api/2.0/export`
- Format: Newline-delimited JSON (one event per line)
- Authentication: API secret (Account → Project Settings)

**Example:**
```python
import requests
import json

API_SECRET = "YOUR_API_SECRET"
PROJECT_ID = "1234567"

response = requests.get(
    f"https://data.mixpanel.com/api/2.0/export",
    params={
        "from_date": "2025-01-01",
        "to_date": "2025-01-31",
        "event": ["Signup", "Purchase"]  # Filter specific events
    },
    auth=(API_SECRET, '')
)

# Parse NDJSON (newline-delimited JSON)
events = [json.loads(line) for line in response.text.strip().split('\n')]

# events[0] structure:
# {
#   "event": "Signup",
#   "properties": {
#     "time": 1704326400,
#     "$browser": "Chrome",
#     "$city": "San Francisco",
#     "plan": "pro"
#   }
# }
```

**Complexity:** HIGH (NDJSON parsing, event schema unique per project, nested properties)
**Time:** 2-8 hours (first-time export script development)

---

## Backup Strategy Recommendations

### Automated Backup (Self-Hosted)

**Daily PostgreSQL Dump (Umami, Plausible, Matomo):**
```bash
#!/bin/bash
# Daily backup script (cron: 0 2 * * *)

DATE=$(date +%Y%m%d)
DB_NAME="umami_db"
BACKUP_DIR="/backups/analytics"

# PostgreSQL backup
pg_dump -U postgres $DB_NAME | gzip > "$BACKUP_DIR/umami-$DATE.sql.gz"

# Rotate backups (keep last 30 days)
find $BACKUP_DIR -name "umami-*.sql.gz" -mtime +30 -delete

# Upload to S3 (optional offsite backup)
aws s3 cp "$BACKUP_DIR/umami-$DATE.sql.gz" s3://my-backups/analytics/
```

**Result:** Daily snapshot, 30-day retention, S3 archival for disasters

### Manual Export (Managed Services)

**Monthly Export Ritual (Plausible, Fathom, Simple Analytics):**
1. **First day of month:** Export previous month data
2. **Plausible:** API script (run `python export-plausible.py --month 2025-01`)
3. **Fathom:** Dashboard → Export → Last month → Download CSV
4. **Storage:** Archive to `~/Documents/Analytics-Backups/fathom-2025-01.csv`
5. **Duration:** 15-30 minutes/month

**Automation (Cron + API):**
```bash
# Monthly export (cron: 0 3 1 * *)
#!/bin/bash
python /scripts/export-plausible.py --month $(date -d "last month" +%Y-%m) --output /backups/plausible-$(date +%Y%m).csv
```

### Data Warehouse Integration (Enterprise)

**Sync Analytics → Data Warehouse (Snowflake, BigQuery, Redash):**

**Option A: Airbyte (Open-Source ETL)**
- Connectors: Plausible API → Snowflake, PostHog → BigQuery
- Schedule: Daily incremental sync (new events only)
- Cost: $0 (self-hosted Airbyte) OR $50-200/mo (Airbyte Cloud)

**Option B: Custom ETL Script**
```python
# Daily sync: Plausible API → PostgreSQL data warehouse
import psycopg2
import requests

# Fetch yesterday's stats from Plausible
response = requests.get(
    "https://plausible.io/api/v1/stats/breakdown",
    params={...}
)

# Insert into data warehouse
conn = psycopg2.connect("dbname=datawarehouse ...")
cursor = conn.cursor()
for row in response.json()['results']:
    cursor.execute(
        "INSERT INTO analytics_daily (date, page, visitors, pageviews) VALUES (%s, %s, %s, %s)",
        (yesterday, row['page'], row['visitors'], row['pageviews'])
    )
conn.commit()
```

**Benefit:** Combine analytics with CRM, sales, product data for unified reporting

---

## Compliance & Audit Requirements

### GDPR Data Subject Requests

**Scenario:** User requests "all data you have about me" (GDPR Article 15)

**Self-Hosted (Easy):**
```sql
-- Umami: Find user sessions by IP or custom ID
SELECT * FROM session WHERE session_id IN (
  SELECT DISTINCT session_id FROM pageview
  WHERE created_at >= '2025-01-01'
    AND (user_agent LIKE '%USER_AGENT%' OR country = 'DE')
);

-- Export user data
pg_dump -U postgres -t session -t pageview --data-only \
  | grep "SESSION_ID" > user-data-export.sql
```

**Time:** 30-60 minutes (query development, verification)

**Managed (Harder):**
- Plausible/Fathom: No user-level tracking (anonymous) = "We don't store your personal data"
- PostHog/Mixpanel: API query by user ID, export JSON, send to user
- GA4: Google Takeout (complex, slow)

**Time:** 1-4 hours (API queries, data formatting)

### Data Retention Policies

**Self-Hosted: Custom Retention**
```sql
-- Delete pageviews older than 2 years (GDPR compliance)
DELETE FROM pageview WHERE created_at < NOW() - INTERVAL '2 years';

-- Automated cleanup (cron: 0 4 1 * *)
psql -U postgres -d umami_db -c "DELETE FROM pageview WHERE created_at < NOW() - INTERVAL '730 days';"
```

**Managed: Provider-Controlled**
- Plausible: Unlimited retention (all plans)
- Fathom: Unlimited retention (all plans)
- Mixpanel Free: 90 days retention (upgrade for 5+ years)
- Amplitude Free: 1 year retention (Growth plan = 10 years)

**Risk:** Vendor changes retention policy (Mixpanel reduced free tier retention in 2021)

---

## Migration Scenarios: Data Export Quality

### High Quality Export (Lossless Migration)

**Self-Hosted → Self-Hosted (Umami → Matomo):**
1. Export Umami PostgreSQL: `pg_dump umami_db > umami-backup.sql`
2. Transform schema (Umami columns → Matomo schema):
   - `pageview.url` → `log_visit.visit_entry_url`
   - `pageview.created_at` → `log_visit.visit_first_action_time`
3. Import into Matomo MySQL
4. **Data Loss:** 0% (event-level data preserved)
5. **Time:** 5-15 hours (schema transformation scripting)

### Medium Quality Export (Aggregated Migration)

**Plausible → Fathom:**
1. Export Plausible API (daily stats): Visitors, pageviews, sources, pages
2. Fathom: No import capability (start fresh)
3. **Data Loss:** Historical detail (only aggregates exported, not raw events)
4. **Time:** 2-4 hours (export script, CSV backup)
5. **Workaround:** Keep Plausible CSV archives, reference for historical analysis

### Low Quality Export (Partial Migration)

**Google Analytics 4 → Plausible:**
1. GA4 export: 5,000 row UI limit OR BigQuery (complex)
2. Plausible: No GA4 import (start fresh)
3. **Data Loss:** 95%+ (GA4 historical data stays in GA4, inaccessible in Plausible)
4. **Time:** 10-20 hours (BigQuery export IF needed for archival, not import)
5. **Reality Check:** Most migrations = start fresh with new tool, archive old dashboard access

---

## Data Ownership Checklist

Evaluate providers against these criteria:

**Critical Requirements:**
- ✅ Can I export ALL data (not just last 90 days or 5,000 rows)?
- ✅ Is export format usable (CSV, JSON, SQL) or proprietary?
- ✅ Can I export programmatically (API) or manually (UI)?
- ✅ Do I own the data (self-hosted) or trust vendor (managed)?

**Nice-to-Have:**
- ✅ Event-level granularity (raw logs) vs. aggregates only?
- ✅ Real-time export (streaming) vs. batch (daily)?
- ✅ Direct database access (SQL queries) vs. API abstractions?
- ✅ No export fees (included) vs. pay-per-export ($100+ for large datasets)?

**Red Flags:**
- ❌ No export capability (vendor lock-in)
- ❌ Export limits (5,000 rows, 90 days)
- ❌ Export fees ($500+ for historical data)
- ❌ Proprietary format (can't use elsewhere)

---

## Strategic Recommendations

### Maximum Data Ownership (Compliance, Migration Flexibility)
**Choose:** Self-hosted (Umami, Matomo, PostHog)
**Why:** Direct database access = 100% control, zero vendor dependency
**Trade-off:** Self-hosting maintenance (2 hrs/month)
**Use When:** GDPR data residency required, regulated industry, >1M pageviews

### High Data Ownership (Managed with API)
**Choose:** Plausible, PostHog (cloud), Mixpanel
**Why:** Comprehensive API, event-level export, no vendor gatekeeping
**Trade-off:** API scripting required (1-4 hours setup)
**Use When:** Managed simplicity + data warehouse integration + backup automation

### Acceptable Data Ownership (CSV Export)
**Choose:** Fathom, Simple Analytics
**Why:** Simple CSV export, adequate for backups, manual process acceptable
**Trade-off:** No API automation, manual monthly exports
**Use When:** Solo founder, simple needs, willing to click "Export" monthly

### Avoid (Low Data Ownership)
**Avoid:** Google Analytics 4 free tier (5K row limit), Cloudflare Analytics (no export)
**Why:** Export limitations create vendor lock-in
**Exception:** Acceptable IF data not critical (personal blog, side project)

---

## Recommendation

**Default Choice:** Plausible (cloud with API) OR Umami (self-hosted with direct DB)
- **Plausible:** Best managed API, event-level export, 85/100 ownership score
- **Umami:** Best self-hosted, PostgreSQL access, 100/100 ownership score

**Enterprise:** Matomo (self-hosted) OR PostHog (self-hosted)
- **Matomo:** 18-year track record, MySQL/PostgreSQL, comprehensive data warehouse integrations
- **PostHog:** Modern event schema (ClickHouse), best API, event-level everything

**Avoid:** Fathom IF API automation required (CSV-only = manual burden at scale)

**Strategic Path:** Start with managed API provider (Plausible), self-host at >1M pageviews OR data sovereignty requirement (Umami, Matomo). Never choose tools without export capability (vendor lock-in = strategic risk).
