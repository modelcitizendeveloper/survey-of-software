# S3: Need-Driven - Email Library Selection by Use Case

**Experiment**: 1.034 - Email Libraries
**Methodology**: S3 - Need-Driven (Requirements-first matching)
**Date**: 2025-10-16
**Time Spent**: ~60 minutes

## Overview

This section provides decision frameworks for selecting email libraries based on specific use cases, project constraints, and team requirements. Instead of comparing features abstractly, we match libraries to real-world scenarios.

---

## Use Case Categories

### 1. Transactional Emails (Account, Order, Notification)
### 2. Internal Notifications (Alerts, Reports, Monitoring)
### 3. Marketing Campaigns (Newsletters, Promotions)
### 4. Bulk Email Systems (Mass Communication)
### 5. Developer Tools & Scripts (Automation, Testing)
### 6. Learning & Prototyping (Education, Experimentation)

---

## Use Case 1: Transactional Emails

**Examples**: Password reset, order confirmation, shipping notification, account verification

**Requirements**:
- High deliverability (must reach inbox)
- Fast sending (<500ms)
- Professional templates
- Event tracking (opened, clicked)
- Compliance (CAN-SPAM, GDPR)

### Recommended Path: Managed Email Service (Tier 3.020)

**Why**: Transactional emails require deliverability expertise that DIY SMTP cannot match

**Library choice within managed services**:

**Django projects:**
```python
# Use django-anymail for ESP abstraction
ANYMAIL = {'MAILGUN_API_KEY': '...'}
EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'

from django.core.mail import send_mail
send_mail('Password Reset', body, 'noreply@example.com', [user.email])
```
**Recommendation**: `django-anymail` - Prevents vendor lock-in, supports 15+ ESPs

**Flask projects:**
```python
# Option 1: Use ESP's native SDK
from sendgrid import SendGridAPIClient
sg = SendGridAPIClient(api_key)
sg.send(message)

# Option 2: Flask-Mail configured for ESP's SMTP relay
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
mail.send(msg)
```
**Recommendation**: ESP native SDK > SMTP relay for better features (templates, analytics)

**Non-framework projects:**
```python
# Use ESP's Python SDK directly
import mailgun
mailgun.send(to, subject, html, api_key)
```

### If DIY SMTP Required (Not Recommended)

**Best library**: `yagmail` (simplest) or `redmail` (templates)

**Limitations**:
- Gmail daily limits (500/day free, 2000/day Workspace)
- No deliverability guarantees (may hit spam)
- No analytics (opens, clicks, bounces)
- Manual DKIM/SPF configuration required
- Your IP reputation matters (shared hosting = bad)

**When DIY SMTP is acceptable**:
- Internal company emails (trusted domain)
- Low volume (<50/day)
- Non-critical communications
- Development/testing environments

---

## Use Case 2: Internal Notifications

**Examples**: Server alerts, error notifications, daily reports, monitoring alerts

**Requirements**:
- Simple, fast implementation
- Low cost (potentially high volume)
- Reliable delivery (but not mission-critical)
- No fancy formatting needed

### Recommended Library: yagmail or smtplib

**Why DIY works here**:
- Recipients are internal (deliverability less critical)
- Plain text acceptable
- Speed matters (5-10 lines of code)
- Cost-effective (no per-email charges)

**yagmail approach (recommended):**
```python
import yagmail

class AlertNotifier:
    def __init__(self):
        self.yag = yagmail.SMTP('alerts@company.com', oauth2_file='oauth2.json')

    def send_alert(self, level, service, message):
        subject = f'[{level.upper()}] {service} Alert'
        self.yag.send(
            to='oncall@company.com',
            subject=subject,
            contents=f'{service} reported:\n\n{message}'
        )

# Usage
notifier = AlertNotifier()
notifier.send_alert('critical', 'database', 'Connection pool exhausted')
```

**smtplib approach (zero dependencies):**
```python
import smtplib
from email.mime.text import MIMEText

def send_alert(level, service, message):
    msg = MIMEText(f'{service} reported:\n\n{message}')
    msg['Subject'] = f'[{level.upper()}] {service} Alert'
    msg['From'] = 'alerts@company.com'
    msg['To'] = 'oncall@company.com'

    with smtplib.SMTP('smtp.company.com', 587) as server:
        server.starttls()
        server.login(username, password)
        server.send_message(msg)
```

**Integration with monitoring tools:**
```python
# Prometheus Alertmanager → Email
# Sentry → Email
# Custom monitoring → yagmail

import yagmail
from prometheus_client import Gauge

yag = yagmail.SMTP('alerts@company.com')

def check_disk_space():
    usage = get_disk_usage()
    if usage > 90:
        yag.send(
            to='ops@company.com',
            subject='Disk Space Critical',
            contents=f'Disk usage: {usage}%'
        )
```

**Best practice**: For high-volume alerts, consider:
- Alert aggregation (batch every 15 minutes)
- Rate limiting (max 1 email/5 minutes per alert type)
- Dedicated alerting service (PagerDuty, Opsgenie) for critical alerts

---

## Use Case 3: Marketing Campaigns

**Examples**: Newsletters, product announcements, promotional emails

**Requirements**:
- High deliverability
- Professional templates
- A/B testing
- Unsubscribe management
- Analytics (opens, clicks, conversions)
- CAN-SPAM/GDPR compliance
- List segmentation

### Recommended Path: Dedicated Email Marketing Platform

**DO NOT use DIY SMTP for marketing emails**

**Why**:
- Email marketing platforms optimize for deliverability
- Compliance features (unsubscribe, list management) are complex
- Analytics and A/B testing require specialized infrastructure
- Sending reputation is critical (DIY SMTP will hit spam)

**Platforms to evaluate** (separate from Tier 3.020):
- Mailchimp, SendGrid Marketing, Brevo (Sendinblue), MailerLite, ConvertKit

**If integrating marketing platform with your app:**

**django-anymail for transactional + marketing ESP:**
```python
# Use ESP's marketing features via API
import sendgrid
from sendgrid.helpers.mail import Mail, Email, Personalization

def add_user_to_newsletter(user):
    # Add to marketing list via SendGrid Marketing API
    sg = sendgrid.SendGridAPIClient(api_key)
    sg.client.marketing.contacts.put(request_body={
        'contacts': [{'email': user.email, 'first_name': user.name}]
    })
```

**Never send marketing emails via SMTP**: Use ESP's marketing API or dedicated platform

---

## Use Case 4: Bulk Email Systems

**Examples**: Mass notifications, announcement to all users, broadcast messages

**Requirements**:
- Send to 1000s-100,000s of recipients
- Performance (throughput)
- Rate limiting
- Bounce handling
- Cost-effectiveness

### Recommended Approach: Task Queue + ESP

**Architecture**:
```
Application → Task Queue (Celery/RQ) → Worker Pool → ESP API
                                     ↓
                              Rate Limiter
```

**Implementation (Celery + yagmail):**
```python
from celery import Celery
import yagmail

celery = Celery('tasks', broker='redis://localhost:6379')

@celery.task(rate_limit='30/m')  # 30 emails per minute
def send_email_task(to, subject, body):
    yag = yagmail.SMTP('sender@example.com')
    yag.send(to=to, subject=subject, contents=body)

# Send to 10,000 users
for user in users:  # 10,000 users
    send_email_task.delay(user.email, 'Announcement', body)
    # Returns immediately, Celery handles queuing and rate limiting
```

**Performance comparison**:

| Method | 10,000 emails | Infrastructure | Cost |
|--------|--------------|----------------|------|
| Synchronous SMTP | ~8 hours | 1 process | Free (Gmail limits) |
| Celery (10 workers) | ~30 minutes | 10 workers + Redis | Low |
| ESP API (bulk) | ~5 minutes | API calls | $10-50 |
| ESP Marketing | ~1 minute | Platform | $50-300/month |

**Library choice**:
- **Celery + yagmail**: Good for 1K-10K emails with rate limiting
- **ESP API (SendGrid, Mailgun)**: Better for 10K+ emails, better deliverability
- **django-anymail**: If already using Django

**Rate limiting to avoid bans:**
```python
# Gmail: 500/day (free), 2000/day (Workspace)
# Mailgun: 300/hour (free tier)
# SendGrid: 100/day (free tier)

from celery import Celery
from kombu.utils.limits import TokenBucket

celery = Celery('tasks')

# Rate limit: 100 emails per hour
@celery.task(rate_limit='100/h')
def send_bulk_email(to, subject, body):
    # Implementation
    pass
```

---

## Use Case 5: Developer Tools & Scripts

**Examples**: CI/CD notifications, cron job results, data export emails, automated reports

**Requirements**:
- Minimal setup time
- Simple, readable code
- No production SLA
- Often run from command line or cron

### Recommended Library: yagmail

**Why**:
- Fastest time-to-email (3 lines of code)
- OAuth2 support (no password in scripts)
- Works great for one-off scripts

**Example: Daily report emailer**
```python
#!/usr/bin/env python3
import yagmail
import pandas as pd
from datetime import datetime

# Generate report
df = generate_daily_metrics()
report_html = df.to_html()

# Send email
yag = yagmail.SMTP('reports@company.com')
yag.send(
    to='team@company.com',
    subject=f'Daily Report - {datetime.now().strftime("%Y-%m-%d")}',
    contents=[
        '<h2>Daily Metrics</h2>',
        report_html
    ],
    attachments='metrics.csv'
)
```

**Example: CI/CD notification**
```python
# .github/workflows/notify.yml
# After tests complete, run:

import yagmail
import os

yag = yagmail.SMTP(os.environ['EMAIL_USER'], os.environ['EMAIL_PASS'])
yag.send(
    to='dev@company.com',
    subject=f'Build {os.environ["GITHUB_RUN_NUMBER"]} Status',
    contents=f'Build status: {os.environ["BUILD_STATUS"]}\n'
              f'Branch: {os.environ["GITHUB_REF"]}'
)
```

**Alternative (zero dependencies): smtplib**
```python
import smtplib
from email.mime.text import MIMEText
import os

msg = MIMEText('Build complete')
msg['Subject'] = 'CI/CD Notification'
msg['From'] = 'ci@company.com'
msg['To'] = 'dev@company.com'

with smtplib.SMTP('smtp.gmail.com', 587) as s:
    s.starttls()
    s.login(os.environ['EMAIL_USER'], os.environ['EMAIL_PASS'])
    s.send_message(msg)
```

---

## Use Case 6: Learning & Prototyping

**Examples**: Learning SMTP, testing email features, rapid prototyping, experiments

**Requirements**:
- Educational value
- Clear documentation
- Experimentation-friendly
- Fast iteration

### Recommended Path: smtplib (learning) → yagmail (prototyping)

**Learning phase - Use smtplib:**

**Why**: Understanding smtplib teaches:
- SMTP protocol fundamentals
- MIME message structure
- TLS/SSL negotiation
- Authentication mechanisms
- Error handling

**Example learning progression:**

**Step 1: Plain text email**
```python
import smtplib
from email.mime.text import MIMEText

msg = MIMEText('Hello, World!')
msg['Subject'] = 'My First Email'
msg['From'] = 'me@example.com'
msg['To'] = 'recipient@example.com'

with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.set_debuglevel(1)  # See SMTP conversation!
    server.starttls()
    server.login('me@example.com', 'password')
    server.send_message(msg)
```

**Step 2: HTML with attachments**
```python
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

msg = MIMEMultipart('alternative')
msg.attach(MIMEText('Plain text version', 'plain'))
msg.attach(MIMEText('<h1>HTML version</h1>', 'html'))

# Add attachment
with open('file.pdf', 'rb') as f:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename=file.pdf')
    msg.attach(part)
```

**Prototyping phase - Switch to yagmail:**

Once you understand the fundamentals, use yagmail for rapid prototyping:

```python
import yagmail

yag = yagmail.SMTP('me@example.com')
yag.send(
    to='recipient@example.com',
    subject='Prototype',
    contents=['<h1>HTML content</h1>', 'Plain text'],
    attachments='file.pdf'
)
```

**Testing email functionality:**

**Use Mailtrap/MailHog for development:**
```python
# Point to MailHog (localhost SMTP server)
server = smtplib.SMTP('localhost', 1025)  # No auth needed
server.send_message(msg)
# View emails in web UI at http://localhost:8025
```

---

## Decision Trees

### Tree 1: Framework-Based Decision

```
Are you using a web framework?
├─ No → Go to Tree 2
└─ Yes
   ├─ Django?
   │  ├─ Using/might use transactional email services? → django-anymail
   │  └─ Simple SMTP only? → Django built-in (smtplib wrapper)
   │
   └─ Flask?
      ├─ Need Flask config integration? → Flask-Mail
      └─ Framework-agnostic preferred? → yagmail
```

### Tree 2: Non-Framework Decision

```
What's your primary requirement?
├─ Simplicity (minimal code) → yagmail
├─ Zero dependencies → smtplib + email.mime
├─ Template integration → redmail
├─ Learning SMTP → smtplib + email.mime
├─ Multiple transport options → marrow.mailer
└─ Production transactional email → Use ESP + their SDK (see Tier 3.020)
```

### Tree 3: Volume-Based Decision

```
How many emails per day?
├─ < 10 → Any library works, use yagmail for simplicity
├─ 10-100 → yagmail or smtplib, consider OAuth2
├─ 100-1000 → Task queue + yagmail/smtplib, watch rate limits
├─ 1000-10,000 → Task queue + ESP SMTP relay (django-anymail if Django)
└─ > 10,000 → ESP API (not SMTP), marketing platform for bulk
```

### Tree 4: Use Case Decision

```
What type of emails?
├─ Transactional (password reset, orders) → ESP + django-anymail or SDK
├─ Internal notifications (alerts, reports) → yagmail or smtplib
├─ Marketing (newsletters) → Marketing platform (not DIY)
├─ Bulk announcements → Task queue + ESP API
├─ Developer tools/scripts → yagmail (OAuth2) or smtplib
└─ Learning/prototyping → smtplib (learn) → yagmail (build)
```

---

## Anti-Patterns: When NOT to Use Each Library

### ❌ Don't Use yagmail When:
- You need zero dependencies (embedded systems, Lambda with size limits)
- You're building a library (don't force keyring dependency on users)
- You need fine-grained SMTP control (debugging protocol issues)

### ❌ Don't Use smtplib + email.mime When:
- You want rapid prototyping (too verbose)
- Team lacks SMTP knowledge (high learning curve)
- You need OAuth2 (complex to implement manually)

### ❌ Don't Use Flask-Mail When:
- Not using Flask (obviously)
- Need advanced ESP features (django-anymail better for multi-ESP)
- Building standalone scripts (unnecessary Flask dependency)

### ❌ Don't Use django-anymail When:
- Not using Django (Django dependency required)
- Only doing SMTP (overengineered for simple use)
- Using DIY SMTP servers (designed for ESPs)

### ❌ Don't Use redmail When:
- Don't need templates (yagmail simpler)
- Zero dependency requirement (Jinja2 required)
- Very high volume (overhead from template rendering)

### ❌ Don't Use mailer When:
- Simple use case (overengineered, complex architecture)
- Need strong community support (smaller ecosystem)

### ❌ Don't Use envelopes When:
- ANY use case (better alternatives exist: yagmail, redmail, smtplib)

### ❌ Don't Use DIY SMTP (Any Library) When:
- Sending marketing emails (use marketing platform)
- Need high deliverability (use ESP like SendGrid, Mailgun)
- Compliance critical (CAN-SPAM, GDPR → use managed service)
- Analytics required (opens, clicks → use ESP)
- Volume > 1000/day (use ESP API)

---

## Migration Paths

### Scenario: Outgrowing yagmail

**When**: Your project scales from 100 emails/day to 10,000/day

**Migration path**:
```python
# Before (yagmail)
yag = yagmail.SMTP('sender@example.com')
yag.send(to=user.email, subject='Welcome', contents=body)

# After (django-anymail + Mailgun)
from django.core.mail import send_mail
send_mail('Welcome', body, 'sender@example.com', [user.email])
# Settings: EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
```

**Effort**: 2-4 hours (setup ESP account, configure django-anymail, test)

### Scenario: Moving from Flask-Mail to django-anymail

**When**: Migrating Flask app to Django, or adding multi-ESP support

**Migration**:
```python
# Before (Flask-Mail)
from flask_mail import Mail, Message
msg = Message('Welcome', sender='x@x.com', recipients=[email])
msg.body = body
mail.send(msg)

# After (django-anymail)
from django.core.mail import EmailMessage
msg = EmailMessage('Welcome', body, 'x@x.com', [email])
msg.send()
```

**Effort**: 1-2 hours (Django migration separate, email part is quick)

### Scenario: ESP Switching (Mailgun → SendGrid)

**When**: Cost optimization, deliverability issues, feature requirements

**With django-anymail (2-line change)**:
```python
# settings.py - Change 2 lines
EMAIL_BACKEND = 'anymail.backends.sendgrid.EmailBackend'  # Line 1
ANYMAIL = {'SENDGRID_API_KEY': 'SG...'}  # Line 2

# All application code unchanged!
```

**Effort**: 30 minutes (signup, configure, test)

**Without django-anymail (rewrite all email code)**:
```python
# Before (Mailgun SDK)
import mailgun
mailgun.send(...)

# After (SendGrid SDK)
import sendgrid
sendgrid.send(...)
# Rewrite every email send in codebase
```

**Effort**: 4-20 hours depending on codebase size

---

## Constraint-Based Recommendations

### Constraint: Zero Budget

**Best choice**: smtplib or yagmail with Gmail
- Gmail free tier: 500 emails/day
- Google Workspace: 2000 emails/day ($6/user/month)

**Limitations**: Deliverability, rate limits, no analytics

### Constraint: Zero Dependencies

**Best choice**: smtplib + email.mime (standard library)

**When you might relax this**:
- If OAuth2 required (yagmail worth the dependency)
- If templates needed (redmail + Jinja2 worth it)

### Constraint: Maximum Deliverability

**Best choice**: Managed ESP (SendGrid, Mailgun, Postmark)
**Library**: django-anymail (Django) or ESP's native SDK

**Why DIY fails**: Shared IP reputation, no dedicated IPs, spam filter optimization

### Constraint: Minimal Learning Curve

**Best choice**: yagmail (3 lines to send email)

**Comparison**:
- yagmail: 30 minutes to productive
- Flask-Mail: 1 hour (if familiar with Flask)
- smtplib: 4-8 hours (learning SMTP, MIME, TLS)
- django-anymail: 2 hours (ESP setup + Django config)

### Constraint: Maximum Privacy/Control

**Best choice**: smtplib with self-hosted SMTP server (Postfix, Exim)

**Why**: Full control over email data, no third-party involvement

**Cost**: Server management, deliverability expertise, time investment

### Constraint: Team Has No SMTP Knowledge

**Best choice**: yagmail or Flask-Mail/django-anymail

**Avoid**: smtplib (requires SMTP understanding)

---

## Summary: Library → Use Case Mapping

| Library | Best For | Avoid For |
|---------|----------|-----------|
| **smtplib + email.mime** | Learning, zero dependencies, maximum control | Rapid prototyping, beginners |
| **yagmail** | Scripts, automation, rapid development, OAuth2 | Zero dependency requirement |
| **redmail** | Template-heavy applications, modern API preference | Simple emails without templates |
| **Flask-Mail** | Flask applications | Non-Flask projects |
| **django-anymail** | Django + ESPs, multi-ESP flexibility | Non-Django, DIY SMTP |
| **mailer** | Multiple transports (SES, maildir, sendmail) | Simple SMTP use cases |
| **envelopes** | Nothing (use alternatives) | Everything |
| **ESP SDK** | Transactional emails, high volume, deliverability | Internal notifications, learning |

---

## Key Takeaways

1. **Match tool to use case**: Don't use django-anymail for scripts, don't use smtplib for transactional emails
2. **Volume matters**: <100/day = DIY works, >1000/day = need ESP
3. **Framework integration**: Use framework-native tools when available (Flask-Mail, django-anymail)
4. **Learning vs. production**: smtplib for learning, yagmail for building, ESP for production
5. **Marketing ≠ transactional**: Never DIY marketing emails, use dedicated platforms
6. **Zero dependencies has costs**: smtplib requires more code and SMTP knowledge
7. **Simplicity has limits**: yagmail perfect for 90% of use cases, but lacks fine-grained control
8. **Templates need planning**: If templates are core requirement, use redmail or ESP with template support
9. **Migration planning**: django-anymail = easy ESP switching, direct SDK integration = vendor lock-in
10. **When in doubt**: yagmail for standalone, django-anymail for Django, ESP for transactional

---

## Next Steps for S4: Strategic Selection

1. **Long-term architecture patterns**: How email strategy evolves with company growth
2. **Cost modeling**: DIY vs. ESP cost comparison at different scales
3. **Risk analysis**: Deliverability risks, vendor lock-in, compliance
4. **Team skills mapping**: Matching library complexity to team expertise
5. **Future-proofing**: Building email systems that adapt to changing requirements
