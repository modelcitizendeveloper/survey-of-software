# Event Management: Category Structure

**Parent Category:** 3.080 Event Management
**Research Date:** October 20, 2025
**Methodology:** spawn-solutions MPSE framework

---

## Category Subdivision Rationale

Event management is a **broad domain** covering multiple distinct use cases with different user personas, workflows, and solution requirements. Attempting to analyze as a single category would conflate:

- Public event organizers (conferences, concerts) vs venue operators (managing space)
- B2C ticketing vs B2B corporate events
- In-person vs virtual/hybrid platforms
- Self-service registration vs high-touch private bookings

**Decision:** Subdivide into 5 distinct subcategories based on use case and user persona.

---

## Subcategory Breakdown

### **3.080.1: Public Event Ticketing & Registration**
**Use Case:** Selling tickets and managing registration for public events
**User Persona:** Event organizers (conferences, concerts, festivals, fundraisers)
**Core Need:** Ticket sales, attendee registration, payment processing, check-in

**Solution Examples:**
- Eventbrite (general events, ticketing marketplace)
- Ticketmaster (large venues, concerts)
- Ticket Tailor (white-label ticketing)
- Humanitix (nonprofit-focused)
- Luma (modern event platform)

**Workflow:**
1. Create event listing
2. Set ticket tiers/pricing
3. Promote event (marketplace exposure)
4. Sell tickets online
5. Check-in attendees at event
6. Post-event analytics

**Key Features:** Ticket sales, payment processing, promotional tools, attendee management, check-in apps

---

### **3.080.2: Venue/Space Booking Management**
**Use Case:** Venues managing their space for private events/bookings
**User Persona:** Venue operators (restaurants, wine bars, event spaces, meeting rooms)
**Core Need:** Booking calendar, availability management, proposals, contracts, payments

**Solution Examples:**
- Tripleseat (restaurant/hospitality events)
- Event Temple (hotels, conference centers)
- Perfect Venue (event space marketplace + management)
- Gather (modern event space software)
- Planning Pod (all-in-one event planning)

**Workflow:**
1. Receive inquiry (web form, email, phone)
2. Check availability (calendar)
3. Send proposal/quote
4. Negotiate details (menu, setup, timing)
5. Contract signing
6. Payment processing (deposits, final)
7. Event execution coordination
8. Post-event follow-up

**Key Features:** Availability calendar, proposal generation, contract management, payment processing, CRM, BEO (Banquet Event Orders)

---

### **3.080.3: Virtual & Hybrid Event Platforms**
**Use Case:** Hosting online or hybrid (in-person + virtual) events
**User Persona:** Event organizers, corporate trainers, associations
**Core Need:** Video streaming, attendee engagement, networking, virtual booths

**Solution Examples:**
- Zoom Events (Zoom-native event platform)
- Hopin (virtual + hybrid events)
- Airmeet (virtual events, networking focus)
- vFairs (virtual trade shows)
- Whova (hybrid event app)

**Workflow:**
1. Create event structure (sessions, tracks, speakers)
2. Set up virtual venue (lobby, stages, networking areas)
3. Registration integration
4. Live streaming during event
5. Attendee networking/engagement
6. Post-event content library

**Key Features:** Live streaming, breakout rooms, virtual booths, networking, chat, polls, analytics

---

### **3.080.4: Corporate Event Management (Enterprise)**
**Use Case:** Managing large-scale corporate events (conferences, trade shows, meetings)
**User Persona:** Corporate event planners, associations, enterprise teams
**Core Need:** End-to-end event lifecycle management, attendee management, budgeting

**Solution Examples:**
- Cvent (enterprise event management)
- Bizzabo (corporate events, branding focus)
- Splash (brand-forward event marketing)
- EventMobi (event apps, engagement)
- Swoogo (modern event marketing platform)

**Workflow:**
1. Event planning & budgeting
2. Website/landing page creation
3. Registration & ticketing
4. Email marketing campaigns
5. Attendee management
6. On-site check-in & badging
7. Mobile event app
8. Post-event surveys & ROI reporting

**Key Features:** Event websites, registration, email marketing, budgeting, attendee tracking, mobile apps, reporting

---

### **3.080.5: Restaurant/Hospitality Reservations**
**Use Case:** Managing restaurant dining reservations (not private events)
**User Persona:** Restaurant operators, wine bars, cafes
**Core Need:** Table management, reservation booking, waitlist, guest communication

**Solution Examples:**
- Resy (premium dining reservations)
- OpenTable (marketplace + reservation system)
- Tock (prepaid reservations, ticketed dining)
- SevenRooms (hospitality CRM + reservations)
- Yelp Reservations (SMB-focused)

**Workflow:**
1. Guest books table online or via phone
2. System manages table assignments
3. Waitlist management
4. Guest communication (confirmations, reminders)
5. Table turnover optimization
6. Guest profile tracking (preferences, visit history)

**Key Features:** Online booking, table management, waitlist, guest profiles, two-way SMS, POS integration

---

## Decision Matrix: Which Subcategory to Research?

| Scenario | Recommended Subcategory |
|----------|------------------------|
| **Selling tickets to public events** | 3.080.1: Public Event Ticketing |
| **Venue managing private event bookings** | 3.080.2: Venue/Space Booking |
| **Hosting virtual/online events** | 3.080.3: Virtual & Hybrid Platforms |
| **Large corporate conference planning** | 3.080.4: Corporate Event Management |
| **Restaurant managing dining reservations** | 3.080.5: Restaurant Reservations |

---

## Research Priority

Based on spawn-solutions research needs and common use cases, recommended priority order:

**High Priority:**
- 3.080.2: Venue/Space Booking Management (broad applicability: restaurants, event spaces, hotels)
- 3.080.5: Restaurant/Hospitality Reservations (high volume use case)

**Medium Priority:**
- 3.080.1: Public Event Ticketing (many existing comparisons available)
- 3.080.4: Corporate Event Management (enterprise-focused, narrower applicability)

**Lower Priority:**
- 3.080.3: Virtual & Hybrid Events (market still evolving, many platforms consolidating)

---

**Category Structure Documented:** October 20, 2025
**Research Methodology:** spawn-solutions MPSE v2.0
**Next:** Generic MPSE research on 3.080.2
