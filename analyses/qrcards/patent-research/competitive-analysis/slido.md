# Slido Competitive Analysis
## Platform Overview

**Owner**: Cisco (acquired)
**Market Position**: Market leader in corporate/conference audience engagement
**Primary Use Cases**: Corporate meetings, conferences, webinars, all-hands meetings
**Tagline**: "Audience Interaction Made Easy"

## Registration Method

### QR Code Support
- **Available**: Yes, in all plans, enabled by default
- **Method**: Participants scan QR code from Slido Present mode or Webex devices
- **Speed**: "Immediate access" (exact timing not documented, estimated 10-20 seconds)
- **No download required**: Users go to slido.com or scan QR, enter event code
- **Unique codes**: Each QR code is unique to each slido created

### Join Process
1. Scan QR code OR visit slido.com
2. Enter event code (if not using QR)
3. Join session (no account required)
4. Access current polls/Q&A

**Estimated join time**: 10-20 seconds from QR scan to active participation

## Real-Time Sync Capabilities

### What Gets Synchronized
- **Poll results**: Updated in real-time as people vote
- **Q&A questions**: Submitted questions appear instantly
- **Live quiz answers**: Results shown in real-time

### What DOESN'T Get Synchronized
- **Presentation content itself**: No evidence of slide content sync
- **Pre-loaded slides**: Content appears to be pushed live, not pre-loaded
- **Time-code triggers**: No automated slide progression features documented

### Technical Specs
- **Uptime**: 99.95% documented
- **Latency**: No specific millisecond metrics published
- **Internet requirements**: 5-10 Mbits/s per 100 participants recommended
- **Data usage**: ~5 MB/day per participant, ~15 MB/day per host
- **Recommended setup**: LAN line for Present view for best performance

## Content Delivery

### Architecture Type
- **Live push model**: Content delivered during presentation
- **Browser-based**: Web application, no installation required
- **PowerPoint integration**: Polls embedded directly in slides, but not pre-loaded

### Pre-Loading Capabilities
- **No evidence found**: All documentation suggests live interaction model
- **Requires persistent internet**: Stable connection required throughout event
- **No offline mode**: No documented offline functionality

## Audience Segmentation

### Capabilities
- **No advanced segmentation documented**
- **Single broadcast model**: Same polls shown to all participants
- **No dynamic grouping**: No evidence of real-time behavioral segmentation
- **Basic reporting**: Can filter results by demographics if collected

### Missing Features
- Cannot show different content to different audience segments
- No real-time audience grouping based on responses
- One-size-fits-all poll/Q&A delivery

## Latency Characteristics

### Documented Performance
- **User feedback**: "Speed of answers appearing on screen live" mentioned as positive
- **99.95% uptime**: Reliable but not ultra-low latency
- **Connection quality dependent**: Stable internet required; "login loops can be connected to internet connection not being stable"

### Estimated Latency
- **Poll results**: Likely 200-500ms based on web architecture (not documented)
- **No sub-50ms claims**: No documentation of ultra-low latency synchronization
- **Best-effort delivery**: Standard web app performance

## Use Cases

### Primary Applications
- Corporate all-hands meetings
- Large conferences and summits
- Webinars and virtual events
- Team meetings and workshops
- Hybrid events (Webex integration)

### Event Scale
- Free plan: Limited participants
- Paid plans: Scales to thousands of participants
- Enterprise: Custom solutions for large events

## Pricing Model

### Structure
- **Free tier**: Limited features (3 polls per event, basic Q&A)
- **Engage plan**: ~$10/month (billed annually)
- **Professional plan**: ~$40/month (billed annually)
- **Enterprise**: Custom pricing

### Pricing Complaints
- "Costs can add up quickly with per-event pricing"
- Free version has many limitations
- Time-limited events (cannot extend beyond scheduled duration)

## User Complaints & Pain Points

### Top Complaints from Reviews

1. **Limited free version**
   - "Free version has many limitations, including restricted customization"
   - Cannot export results in free tier
   - Restricted poll numbers

2. **Integration limitations**
   - "Want more integration options beyond Webex, PowerPoint, Google Slides"
   - Difficult to duplicate questions (creates new QR codes)

3. **Performance issues**
   - "Can be slow and laggy at times"
   - Connection quality affects experience
   - Some delay in results displaying

4. **Time constraints**
   - "Events scheduled only for limited time"
   - "Wish survey time limit could be extended to two weeks"

5. **Scope limitations**
   - "Mainly focuses on live meeting interactions"
   - "Doesn't offer much for ongoing employee feedback"

### Feature Requests (from reviews)
- More customization options for branding
- Better offline/asynchronous capabilities
- Longer event durations
- More flexible pricing options

## Patent Differentiation Analysis

### What Slido DOES Have (Not Differentiating)
- QR code registration (industry standard)
- Real-time poll/Q&A results (industry standard)
- PowerPoint integration (common feature)
- Live interaction during presentations (core use case)

### What Slido DOESN'T Have (Our Opportunities)
1. **Pre-loaded content architecture**
   - No evidence of presentation content pre-loading
   - Appears to use live push model

2. **Time-code triggered content**
   - No automated slide progression features
   - Presenter manually controls all content

3. **Content synchronization**
   - Syncs RESULTS, not presentation CONTENT itself
   - No slide-by-slide device synchronization

4. **Sub-50ms latency**
   - No documented ultra-low latency claims
   - Standard web app performance (~200-500ms likely)

5. **Offline-first operation**
   - Requires persistent internet connection
   - No documented offline capabilities

6. **Dynamic audience segmentation**
   - No real-time behavioral grouping
   - Single broadcast model for all participants

## Prior Art Risk Assessment

**Risk Level: LOW**

Slido focuses on poll/Q&A interaction, not content orchestration. Key differentiators:
- They synchronize INTERACTION RESULTS (votes, questions)
- We synchronize PRESENTATION CONTENT (slides, media)
- They require live internet connection throughout
- We pre-load content for offline-first operation
- They use manual presenter control
- We use automated time-code triggers

## Recommendations

**Slido does NOT invalidate our core patent claims:**
- Pre-loaded content + time-code triggers: No competing implementation
- Sub-50ms content sync: No documented capability
- Offline-first architecture: Not supported
- Dynamic content segmentation: Not supported

**Proceed with confidence** - Slido is in adjacent but non-competing technical space (interaction tools vs. content orchestration).
