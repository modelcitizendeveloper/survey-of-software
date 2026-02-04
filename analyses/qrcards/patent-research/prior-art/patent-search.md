# Comprehensive Patent Search Results
## Google Patents Search for Audience Orchestration Prior Art

**Search Date:** December 2, 2025
**Database:** Google Patents (https://patents.google.com/)
**Geographic Scope:** Worldwide (emphasis on US patents for FTO analysis)
**Time Range:** 1990-2025 (focus on active/recently expired patents)

---

## Search Strategy

### Keywords Searched

**Primary Searches:**
1. "device synchronization" + "live events"
2. "audience response system" + "QR code"
3. "time code synchronization" + "broadcast"
4. "second screen synchronization"
5. "crowd synchronization" + "mobile devices"
6. "LED wristband synchronization"
7. "WebSocket synchronization" + "real-time"
8. "smartphone crowd" + "coordinated display"

**Secondary Searches:**
9. "PixMob" + "infrared" + "LED"
10. "Xyloband" + "radio controlled"
11. "HbbTV" + "companion screen"
12. "ultrasonic" + "data transmission" + "mobile"
13. "audience participation" + "broadcast"
14. "crowd control" + "multiplayer"
15. "classroom response system" + "synchronization"

---

## Patents Found and Analyzed

### HIGH RELEVANCE - Multi-Device Crowd Synchronization

---

#### 1. US9148510B2 - Smart Phone Crowd Enhancement

**Title:** Smart phone crowd enhancement

**Assignee:** Mea Mobile

**Filed:** June 23, 2010
**Granted:** September 29, 2015
**Expiration:** September 17, 2030
**Current Status:** **EXPIRED** (maintenance fees not paid; expired November 2019)

**Claims Summary:**

**Independent Claim 1:**
A computer-implemented method of facilitating coordinated displays of crowd visual patterns using mobile computing devices, comprising:
- Defining a crowd boundary of a gathered crowd
- Dynamically identifying a plurality of mobile computing devices located within said crowd boundary
- At a control device identified from one of said plurality of mobile computing devices, identifying a crowd visual pattern
- At said control device and based on respective physical attributes of said plurality of mobile computing devices, dynamically converting said crowd visual pattern into respective display information to be displayed on display devices

**Key Dependent Claims:**
- Claim 5: Identifying crowd visual pattern responsive to user input
- Claim 6: Voting on candidate crowd visual patterns via user input from plurality of devices
- Claim 9: Predetermined motion pattern detection triggering predetermined display/audio
- Claim 12: Operating across different operating systems using mobile ad hoc network

**Technology Approach:**
- Uses wireless signal strength (Bluetooth/TCP-IP) to determine device positioning
- "Root device" coordinates pattern distribution
- Segments single image across multiple screens to form aggregate larger picture
- Handles moving displays (predictive algorithms for crowd movement)
- Self-healing mesh networking

**Overlap with Our Approach:**
- **Similarity:** Coordinating smartphone displays across crowds, visual pattern synchronization
- **Differences:**
  - Positioning-based (relative device location) vs. uniform broadcast triggers
  - Peer-to-peer mesh network vs. client-server WebSocket architecture
  - Visual pattern segmentation (jigsaw puzzle model) vs. uniform content display
  - Ad-hoc network discovery vs. QR code registration

**Blocking Risk:** **NONE (EXPIRED)**

**Even If Still Active, Infringement Risk:** LOW
- Different technical architecture (mesh networking vs. centralized server)
- Different use case (position-based image segmentation vs. time-code-triggered content)
- Different registration method (wireless discovery vs. QR code)

**Expiration Date:** Technically 2030, but **expired due to non-payment of maintenance fees in 2019**

**Design-Around (if patent were active):**
- Use centralized server architecture (not peer-to-peer mesh)
- Trigger uniform content (not position-segmented images)
- QR code registration (not wireless proximity detection)

---

#### 2. US9129640B2 - CrowdFlik Synchronized Video Platform

**Title:** Collaborative digital video platform that enables synchronized capture, curation and editing of multiple user-generated videos

**Assignee:** Crowdflik Inc

**Filed:** December 11, 2013 (originally filed March 6, 2014 per some sources)
**Granted:** September 8, 2015
**Expiration:** December 11, 2033

**Claims Summary:**

**Independent Claim 1:**
A method for enabling synchronized multi-angle video capture and editing, comprising:
- Capturing video at event from multiple mobile devices
- Cutting/tagging videos at synchronized Y-second intervals using master clock
- Associating location/time metadata with each segment
- Enabling user selection of preferred segments from each time slot
- Creating custom edits by combining segments from different devices
- Crowd voting to determine "best-of" selections

**Key Technical Elements:**
- Atomic clock reference (US Naval Observatory) for master timing
- Time-delta adjustments across devices to compensate for clock drift
- Geofencing (GPS/triangulation) for event detection
- Uniform temporal segmentation (Y-second cuts)
- Post-event curation platform

**Technology Approach:**
- **Synchronization Mechanism:** Atomic clock-based timestamp tagging
- **Event Detection:** GPS geofencing, not QR code registration
- **Content Model:** Video segments cut at uniform intervals
- **Editing:** Post-capture on centralized platform (not real-time)
- **Precision:** 1/1000 second (1ms) timestamp accuracy claimed

**Overlap with Our Approach:**
- **Similarity:**
  - Multi-device coordination at events
  - Precise time synchronization (though different mechanisms)
  - Crowd-sourced content concept
- **Differences:**
  - Video capture/editing vs. content display/triggering
  - Atomic clock sync vs. WebSocket-delivered time codes
  - Post-event curation vs. real-time synchronization
  - Geofencing detection vs. QR code registration
  - One-way upload model vs. bidirectional communication

**Blocking Risk:** **LOW**

**Infringement Analysis:**
- Different application: Video capture/editing vs. display synchronization
- Different timing mechanism: Pre-tagging with atomic clock vs. real-time trigger delivery
- Different content flow: Device→server (upload) vs. server→device (trigger)
- Different event detection: GPS geofencing vs. QR code enrollment

**Expiration Date:** December 11, 2033

**Design-Around:**
- Use real-time WebSocket trigger delivery (not pre-tagging with atomic clock)
- QR code registration (not GPS geofencing)
- Focus on display synchronization (not video capture/editing)
- Pre-loaded content + triggers (not video upload + post-curation)

**Additional Patents:**
CrowdFlik announced second US Patent (#10,347,288) and 12 worldwide patents (Japan, China, South Korea, Canada, Germany, Italy, Great Britain, Sweden, Finland, France). Specific claims not analyzed but likely cover similar video synchronization technology.

---

### MEDIUM RELEVANCE - Second Screen / Broadcast Synchronization

---

#### 3. US9854298B2 - Samsung N-Screen Service in Broadcast System

**Title:** Apparatus and method for providing N-screen service in broadcast system

**Assignee:** Samsung Electronics Co., Ltd.

**Filed:** July 30, 2013
**Granted:** December 26, 2017
**Expiration:** July 30, 2033
**European Equivalent:** EP2880868B1

**Claims Summary:**

**Independent Claim 1 (Apparatus):**
A main N-screen device configured to:
- Receive Application Information Table (AIT) including `screen_type` parameter
- Execute one of three actions based on device type:
  a) Run broadcast service application if screen_type matches device
  b) Perform operations considering sub-device relationships
  c) Discard AIT if incompatible

**Independent Claim (Method):**
A method for N-screen device to:
- Receive AIT with screen_type indicator ("Main", "Sub", or "Sub_Alternative")
- Determine appropriate action based on parameter
- Execute broadcast service application or coordinate with other devices

**Key Technical Elements:**
- Application Information Table (AIT) metadata in HbbTV broadcast signal
- Screen_type classification system (Main/Sub/Sub_Alternative)
- "Application bound" mechanism linking related apps across devices
- Automatic app termination when dependent app stops

**Technology Approach:**
- **HbbTV-Specific:** Designed for Hybrid Broadcast Broadband TV standard
- **Metadata-Driven:** Broadcast signal contains device-type indicators
- **Application Routing:** Which app runs on which device determined by AIT
- **Use Case:** Complementary apps on multiple screens (e.g., shopping on TV, checkout on mobile)

**Overlap with Our Approach:**
- **Similarity:**
  - Multi-device coordination concept
  - Different content on different device types
  - Synchronized experiences across screens
- **Differences:**
  - Broadcast signal metadata (AIT) vs. WebSocket-delivered time codes
  - HbbTV standard-specific vs. web-based proprietary protocol
  - Application routing vs. content triggering
  - TV broadcast domain vs. live event domain
  - Local network (household) vs. internet/cellular (venue)

**Blocking Risk:** **LOW to MEDIUM**

**Infringement Analysis:**
- **Different Technology Stack:** HbbTV broadcast standard vs. WebSocket internet protocol
- **Different Domain:** TV viewing in home vs. live event participation in venue
- **Different Scale:** 1-5 devices per household vs. 1000+ devices in venue
- **Different Trigger Mechanism:** Broadcast AIT metadata vs. server-sent time codes

**Why MEDIUM (Not LOW):**
- Broad language in claims about "multi-device coordination"
- Could argue our time-code distribution across devices conceptually similar
- Samsung has resources to enforce broadly

**Expiration Date:** July 30, 2033

**Design-Around:**
- Emphasize non-broadcast application (live events, not TV)
- WebSocket vs. HbbTV AIT metadata
- Mass-scale venue (not household)
- QR code registration (not local network discovery)
- Pre-loaded content + triggers (not app routing via metadata)

---

#### 4. US9609395B2 - Second Screen Subtitles Function

**Title:** Second screen subtitles function

**Assignee:** Nagravision S.A. (Switzerland - digital TV security/conditional access company)

**Filed:** July 25, 2013
**Granted:** March 28, 2017
**Expiration:** July 25, 2033

**Claims Summary:**

**Independent Claim 1:**
A system for displaying video information comprising:
- Primary screen device displaying video
- Second screen device obtaining current play position data from primary device
- Second screen device displaying information synchronized with contemporaneously played video
- Information displayed on second screen corresponds to obtained current play position

**Key Technical Elements:**
- Second screen queries primary screen for current video timestamp
- Fetches corresponding subtitle/caption data for that timestamp
- Renders synchronized text on companion device
- Continuous timeline synchronization (polling or push-based)

**Technology Approach:**
- **Timeline Synchronization:** Continuous sync to video playback position
- **Content Type:** Subtitles, captions, supplementary text
- **Query Model:** Secondary device requests timestamp from primary device
- **Use Case:** Accessibility (alternative subtitle display)

**Overlap with Our Approach:**
- **Similarity:**
  - Time-based synchronization of content on secondary devices
  - Displaying information synchronized to specific moments
- **Differences:**
  - Continuous timeline polling vs. discrete time-code triggers
  - Primary device as timing source vs. server as timing source
  - Subtitle display vs. interactive media content
  - Two devices (primary + secondary) vs. many devices (server + thousands)

**Blocking Risk:** **LOW**

**Infringement Analysis:**
- Different synchronization model: Continuous timeline tracking vs. discrete event triggers
- Different timing source: Primary viewing device vs. centralized server
- Different content type: Text subtitles vs. multimedia interactive content
- Different architecture: Peer-to-peer (2 devices) vs. client-server (many devices)

**Expiration Date:** July 25, 2033

**Design-Around:**
- Centralized server timing (not primary device as timing source)
- Discrete time-code triggers (not continuous timeline polling)
- Pre-loaded multimedia content (not fetched subtitle text)
- Mass-scale synchronization (not paired device model)

---

#### 5. US10979477B2 - Amazon Time Sync for Live Video & Metadata

**Title:** Time synchronization between live video streaming and live metadata

**Assignee:** Amazon Technologies, Inc.

**Filed:** Date not specified in search results (estimated 2018-2019 based on grant date)
**Granted:** April 13, 2021
**Expiration:** ~2038-2039 (20 years from filing, estimated)

**Inventors:** Jeremy Matthew Cabrido, Vinay Raj, Yongjun Wu

**Claims Summary:**

**Problem Addressed:**
Video of live event and separately generated metadata must synchronize to avoid "spoiler effect" (metadata appearing before video event).

**Technical Solution:**
- Determine timing delay for encoding/packaging pipeline at each origin
- Provide synchronization offset in client manifest
- Client requests metadata and synchronizes with content segments using timing information and offset

**Key Technical Elements:**
- Separate pipelines for video encoding and metadata generation
- Synchronization offset communicated in manifest file
- Timing information associated with each content segment
- Client-side synchronization logic

**Technology Approach:**
- **Broadcast Infrastructure:** Focused on live streaming platforms (Amazon Prime Video, Twitch)
- **Manifest-Based Sync:** Offset values in HLS/DASH manifests
- **Use Case:** Sports broadcasts with live stats, esports with game data overlays

**Overlap with Our Approach:**
- **Similarity:**
  - Live event synchronization
  - Time-based coordination of content display
  - Multiple clients receiving synchronized experience
- **Differences:**
  - Broadcast video streaming vs. live event participation
  - Manifest-based sync offsets vs. WebSocket time-code delivery
  - Video + metadata vs. pre-loaded content + triggers
  - Streaming platform infrastructure vs. event orchestration platform

**Blocking Risk:** **LOW**

**Infringement Analysis:**
- Different domain: Broadcast streaming infrastructure vs. in-venue live events
- Different mechanism: Manifest sync offsets vs. WebSocket triggers
- Different content model: Streaming video + metadata vs. pre-loaded content + triggers
- Amazon patent focuses on encoding pipeline timing, not multi-device coordination

**Expiration Date:** Estimated 2038-2039 (20 years from filing date, not yet disclosed)

**Design-Around:**
- Not a streaming video platform (pre-loaded content)
- WebSocket time-code delivery (not manifest-based sync)
- Live event focus (not broadcast infrastructure)

---

#### 6. US20110202687A1 - Synchronizing Audience Feedback (Live & Time-Shifted)

**Title:** Synchronizing audience feedback from live and time-shifted broadcast views

**Assignee:** Not specified in search results
**Filed:** Estimated 2010-2011
**Status:** Application (grant status unclear)

**Claims Summary:**

**Technical Approach:**
- Uses audio channel to provide synchronization across various platforms
- Pre-processes media into non-unique hashes to yield accurate time offsets
- Handles both live viewers and time-shifted viewers (DVR, on-demand)
- Synchronizes audience feedback (social media, voting) to specific content moments

**Key Technical Elements:**
- Audio fingerprinting for content identification
- Hash-based timeline synchronization
- Handles variable latency (live broadcast, time-shifted playback)
- Social media integration for audience feedback collection

**Overlap with Our Approach:**
- **Similarity:**
  - Synchronizing audience experience to specific moments
  - Handles variable latency across participants
- **Differences:**
  - Audio fingerprinting vs. explicit time-code delivery
  - Feedback collection (input) vs. content triggering (output)
  - Broadcast viewing vs. live event attendance
  - Time-shifted playback support (DVR) vs. real-time live event

**Blocking Risk:** **LOW**
- Application status unclear (may not have been granted)
- Different synchronization mechanism (audio fingerprinting vs. time codes)
- Different direction (collecting feedback FROM audience vs. triggering TO audience)

---

### LOW RELEVANCE - Different Technology/Domain

---

#### 7. US20150039694A1 - Synchronized Web-Browsing (WebSocket)

**Title:** Synchronized web-browsing

**Assignee:** Been Inc

**Filed:** July 31, 2014
**Status:** **ABANDONED** (application published but never granted)

**Claims Summary:**

**Technical Approach:**
- WebSocket-based synchronization of web browsing across multiple devices
- "Session leader" navigates, URLs pushed to participant devices
- Designed for "thousands of concurrent users"
- Browser extension or mobile app implementation

**Why WebSocket:**
> "WebSockets represents the preferred technology for implementing surfing together because it is full-duplex and bi-directional"

**Overlap with Our Approach:**
- **Similarity:**
  - WebSocket for multi-device synchronization
  - Mass-scale (thousands of users)
  - Real-time bidirectional communication
- **Differences:**
  - Web browsing synchronization vs. event content triggering
  - URL sharing vs. time-code delivery
  - Collaborative browsing use case vs. live event participation

**Blocking Risk:** **NONE (ABANDONED)**

**Infringement Analysis:**
- Patent never granted, no legal enforceability
- Even if granted, narrow application to synchronized web browsing
- Our use case (live events) distinct from collaborative browsing

**Why Abandoned:**
- Likely prior art in screen sharing/collaborative browsing
- Novelty questionable (WebSocket is standard technology)
- Commercial viability uncertain

---

#### 8. US20100235854A1 - Audience Response System (UT Austin)

**Title:** Audience Response System

**Assignee:** Board of Regents of the University of Texas System

**Filed:** March 11, 2010
**Status:** **ABANDONED** (never granted)

**Claims Summary:**

**Technical Approach:**
- Receiving "free responses" (open-ended text) from multiple devices
- Automatic classification using NLP, spell-check, semantic similarity
- Breaking answers into "discrete concepts" for partial credit
- Sorting responses by frequency
- "Revealing all answers at the same time" for group discussion

**Technology Approach:**
- Network-based response collection
- Server-side natural language processing
- Team-based learning applications

**Overlap with Our Approach:**
- **Similarity:**
  - Multi-device network coordination
  - "Revealing all answers at same time" = synchronization concept
  - Group collaboration
- **Differences:**
  - Input collection (text responses) vs. output triggering (display content)
  - NLP/classification vs. time-code synchronization
  - Educational assessment vs. live event participation

**Blocking Risk:** **NONE (ABANDONED)**

**Why Abandoned:**
- Prior art in audience response systems and NLP
- Novelty likely insufficient for patent grant
- University may have determined low commercial value

---

#### 9. US5226177A - Real-Time Wireless Audience Response System

**Title:** Real-time wireless audience response system

**Filed:** 1992
**Granted:** 1993
**Expired:** 2013

**Claims Summary:**
- Central processor receiving response data from audience via wireless communication
- Radio, optical, or acoustic communication links
- Real-time tabulation and display of aggregate results

**Current Status:** **EXPIRED** - No legal enforceability

**Historical Significance:**
- Early RF clicker technology
- Predates modern web-based systems

**Blocking Risk:** **NONE (EXPIRED)**

---

#### 10. EP2804387A1 / US20150326952A1 - Multi-Device Digital TV Sync

**Title:** System for synchronizing content transmitted to a digital TV receiver with multiple portable devices with or without internet access

**Assignee:** Multiple individual inventors (Brazil)

**Filed:** May 22, 2013 (EP), November 13, 2015 (US)
**Status:** Application published (grant status unclear)

**Claims Summary:**
- Continuously maintains synchronization between broadcaster content and portable devices
- Works with or without internet connectivity on mobile devices
- TV receiver acts as hub for synchronizing companion devices

**Overlap with Our Approach:**
- **Similarity:** Multi-device synchronization concept
- **Differences:**
  - Broadcast TV-centric vs. live event-centric
  - TV as hub vs. server as hub
  - Local network vs. internet/cellular

**Blocking Risk:** **LOW**
- Different architecture (TV-centric vs. server-centric)
- Unclear if patent was granted
- Different application domain

---

### RELATED BUT NOT BLOCKING - General Technologies

---

#### 11. WO2014207305A1 - Mobile Device Management Using WebSocket

**Title:** Mobile device management using websocket

**Filed:** ~2014 (WIPO publication)
**Status:** International application

**Claims Summary:**
- WebSocket protocol for bi-directional, full-duplex communications over single TCP socket
- Mobile device management applications
- Persistent connection that disconnects only after session completion

**Overlap with Our Approach:**
- **Similarity:** WebSocket usage for mobile device coordination
- **Differences:**
  - Device management (MDM) vs. event participation
  - Enterprise IT use case vs. consumer live events

**Blocking Risk:** **NONE**
- Completely different application domain (MDM)
- WebSocket is standard protocol (not patentable in itself)

---

#### 12. US8711737B2 - Crowd Formation Based on Wireless Context

**Title:** Crowd formation based on wireless context information

**Assignee:** Not specified
**Filed/Granted:** Dates not found in search
**Status:** Granted

**Claims Summary:**
- MAP server synchronizes wireless context discovery
- Simultaneously requests mobile devices at location detect and report wireless contexts
- Crowd detection and coordination

**Overlap with Our Approach:**
- **Similarity:** Crowd coordination using mobile devices
- **Differences:**
  - Wireless context detection (WiFi, Bluetooth scanning) vs. explicit registration
  - Context reporting vs. content triggering

**Blocking Risk:** **LOW**
- Different use case (context detection vs. content synchronization)
- Limited information available on specific claims

---

## Patents NOT Found (Searched But No Results)

### PixMob LED Wristband Technology
**Search Terms:** "PixMob", "PixMob synchronization", "PixMob infrared", "LED wristband infrared synchronization"
**Results:** No patents assigned to PixMob Inc. found in Google Patents
**Conclusion:** Company likely protects technology via trade secrets, not published patents

### Xyloband Radio-Controlled Wristbands
**Search Terms:** "Xyloband", "Jason Regler", "Xyloband patent", "radio controlled LED wristband Coldplay"
**Results:** No patents found despite Wikipedia mention of "patent rights co-owned by Regler and Coldplay"
**Conclusion:** Either patent not published in searchable databases, or protected via trade secret

### CUE Audio Ultrasonic Synchronization
**Search Terms:** "CUE Audio", "ultrasonic synchronization", "data over audio", "ultrasonic live events"
**Results:** No patents assigned to CUE Audio LLC found
**Conclusion:** Open-source foundation (GitHub repo) with proprietary enhancements kept as trade secrets

### Kahoot, Mentimeter, Slido
**Search Terms:** "Kahoot AS", "Mentimeter AB", "Slido"
**Results:** No patents found for any of these classroom/presentation response platforms
**Conclusion:** Software platforms relying on trade secrets, copyright, and first-mover advantage (not patents)

---

## Summary by Risk Level

### NO RISK (Patent Expired or Abandoned)
1. **US9148510B2** - Smart phone crowd enhancement (EXPIRED 2019)
2. **US20150039694A1** - Synchronized web-browsing (ABANDONED)
3. **US20100235854A1** - Audience response system (ABANDONED)
4. **US5226177A** - Real-time wireless audience response (EXPIRED 2013)

### LOW RISK (Different Technology or Domain)
5. **US9129640B2** - CrowdFlik video sync (different application: video editing vs. display sync)
6. **US9609395B2** - Second screen subtitles (different architecture: peer-to-peer vs. client-server)
7. **US10979477B2** - Amazon time sync (different domain: broadcast streaming infrastructure)
8. **US20110202687A1** - Audience feedback sync (different direction: input collection vs. output triggering)
9. **EP2804387A1 / US20150326952A1** - Multi-device TV sync (different architecture: TV-centric vs. server-centric)

### MEDIUM RISK (Design-Around Recommended)
10. **US9854298B2** - Samsung N-screen service (broad multi-device coordination claims, but HbbTV-specific)

### NO PATENTS FOUND (Trade Secrets)
- PixMob infrared/RF wristbands
- Xyloband radio-controlled wristbands
- CUE Audio ultrasonic sync
- Kahoot/Mentimeter/Slido response systems

---

## Patent Landscape Conclusion

**Total Relevant Patents Analyzed:** 12
**Blocking Patents:** 0
**Expired/Abandoned:** 4
**Low Risk:** 5
**Medium Risk:** 1
**Active Patents Requiring Design-Around:** 1 (Samsung HbbTV)

**Freedom to Operate:** YES - No blocking patents prevent us from building and commercializing our Audience Orchestration system.

**Recommendation:** Proceed with provisional patent filing, emphasizing unique combination of QR registration + WebSocket sync + pre-loaded content + time-code triggers for live events.
