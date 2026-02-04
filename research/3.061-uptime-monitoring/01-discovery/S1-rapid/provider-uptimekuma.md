# Uptime Kuma
## Self-Hosted Open Source Monitoring Alternative

### Market Position
- Most popular open-source uptime monitoring tool
- 60,000+ GitHub stars (massive community adoption)
- 206+ contributors actively maintaining project
- Self-hosted alternative to commercial SaaS tools
- Created by Louis Lam, MIT License

### GitHub Stats
- Repository: https://github.com/louislam/uptime-kuma
- Stars: 60,000+ (as of 2025)
- Active development and regular updates
- Large community support via GitHub Issues and Discord

### Free Tier Details

**100% Free Forever**
- Open source MIT license
- No SaaS fees or subscription costs
- Self-hosted on your infrastructure
- Unlimited monitors (limited only by server resources)
- All features included (no paid tiers)

**Self-Hosting Requirements:**
- Docker container (easiest deployment)
- Or Node.js installation
- ~256MB RAM minimum
- Minimal CPU requirements
- Can run on $5/month VPS or free tier cloud hosting

**Cost Analysis:**
- Software: $0 (open source)
- Hosting: $0-5/month (DigitalOcean, Linode, AWS free tier)
- Total: Essentially free with existing infrastructure

### Features

**Monitor Types:**
- HTTP(s) uptime monitoring
- HTTP(s) keyword monitoring (check for specific text)
- TCP port monitoring
- Ping monitoring
- DNS record monitoring
- Push monitoring (for cron jobs)
- Docker container monitoring
- Steam game server monitoring
- JSON query monitoring

**Check Intervals:**
- Configurable from seconds to hours
- As low as 20-second intervals (server dependent)
- No artificial limits like SaaS providers
- Limited only by server capacity

**Alerting:**
- 90+ notification integrations
- Telegram, Discord, Slack
- Email (SMTP)
- SMS via Twilio, Nexmo
- PagerDuty, Opsgenie
- Webhooks
- Custom notification services

**Status Pages:**
- Unlimited public status pages
- Self-hosted on your domain
- Customizable branding
- Real-time updates
- No Uptime Kuma branding required

**Team Features:**
- Multi-user support
- User authentication
- Role-based access (if configured)
- Shared dashboard access

**Data Retention:**
- Unlimited historical data
- SQLite database (default)
- PostgreSQL/MySQL support for scalability
- Export capabilities

**UI/UX:**
- Modern, clean interface
- Responsive design (mobile-friendly)
- Dark mode support
- Intuitive dashboard

### Technology Stack
- Backend: Node.js
- Frontend: Vue.js
- Languages: TypeScript, JavaScript
- Modern web technologies

### Deployment Options
- Docker (recommended, one-command setup)
- Docker Compose
- Kubernetes
- Bare metal Node.js installation
- Synology NAS, Unraid support
- Free hosting: Railway.app, Fly.io free tiers

### Key Differentiator
Only truly free unlimited uptime monitoring solution with no SaaS fees, offering enterprise-grade features through self-hosting with the largest open-source monitoring community (60K+ stars).

### Best For
- Developers comfortable with self-hosting
- Teams wanting data ownership and privacy
- Projects requiring unlimited monitors without cost
- Companies avoiding SaaS vendor lock-in
- Infrastructure already available for hosting
- Privacy-conscious organizations

### Limitations
- Requires technical skills for setup/maintenance
- Self-managed updates and security patches
- Uptime depends on your hosting reliability
- No managed support (community-based)
- Single point of failure if hosted on single server
- NOT suitable for non-technical users

### MPSE V2 Consideration
Perfect for developers in MPSE framework who:
- Already have a VPS or cloud infrastructure
- Want to avoid recurring SaaS costs
- Need unlimited monitors across multiple projects
- Value data ownership and customization
- Have technical skills for Docker deployment
