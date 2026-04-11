---
publish: false
title: "Flight Training — fly.drabro.org"
date: 2026-02-21
topics: "WordPress, Lightsail, AWS Polly, R22, POH, ACS, web project, fly.drabro.org"
---

# Flight Training

## Quick Reference
- Live: https://fly.drabro.org
- Local: ~/flight-training-kit
- Server: 54.69.14.145 (bitnami), same Lightsail instance
- GitHub: https://github.com/DragonBroSY/flight-training-kit (private)
- WordPress install: default (`/opt/bitnami/wordpress`)
- Status: FULLY LIVE as of 2026-02-21

## Decisions Made
- 2026-02-21: Route 53 A record → 54.69.14.145
- SSL via Let's Encrypt (lego) — vhost: `/opt/bitnami/apache/conf/vhosts/fly-https-vhost.conf`
- Polly voice: Joanna (neural) — 68 MP3s pre-generated
- Audio excluded from git (large files, already on Lightsail)
- Source PDFs: `R22_POH.pdf` (Section 3 extracted), `comm_acs.pdf` (FAA-S-ACS-16, Nov 2023)

## How Things Work
- Audio base URL: `https://fly.drabro.org/wp-content/uploads/flight-audio`
- WP-CLI: `sudo /opt/bitnami/wp-cli/bin/wp`
- SSH: `ssh -i ~/Downloads/LightsailDefaultKey-us-west-2.pem bitnami@54.69.14.145`

## Pages
| ID | Slug | Title |
|----|------|-------|
| 156 | /fly-home/ | Home |
| 157 | /r22-emergency-procedures/ | R22 Emergency Procedures |
| 158 | /commercial-acs-standards/ | ACS Standards |
| 159 | /about-fly/ | About |

## Audio
- `audio/poh/` — 12 MP3s (R22 POH Section 3)
- `audio/acs/` — 56 MP3s (Commercial ACS)

## Structure
```
flight-training-kit/
├── content/
├── audio/poh/      (excluded from git)
├── audio/acs/      (excluded from git)
├── clean-text/
└── aws-setup/
```

## Dead Ends / Don't Repeat
-

## Related Sessions

## PDK
###[[ATP]]