---
publish: false
title: "3D Tours — 3d.drabro.org"
date: 2026-02-21
topics: "Matterport, WordPress, Elementor, Lightsail, web project, 3d.drabro.org"
---

# 3D Tours (Matterport)

## Quick Reference
- Live: https://3d.drabro.org
- Local: ~/matterport-tours-kit
- Server: 54.69.14.145 (bitnami), us-west-2 Lightsail
- GitHub: https://github.com/DragonBroSY/dragon-3d-tours
- WP post ID for home page: 110

## Decisions Made
- Chose Lightsail (WordPress-drabro.org instance) as shared host for all drabro.org projects
- Elementor used for all page editing
- Dragon logo used site-wide (copied from 3d site as the source of truth for branding)

## How Things Work
- Deploy page: `scripts/deploy.sh <json> <post_id>`
- Pull page: `scripts/pull.sh <post_id> <json>`
- Page JSON lives in `pages/` — commit before and after every deploy
- WP-CLI path: `/opt/bitnami/wp-cli/bin/wp` (run with sudo)
- SSH: `ssh -i ~/Downloads/LightsailDefaultKey-us-west-2.pem bitnami@54.69.14.145`

## Structure
```
matterport-tours-kit/
├── content/
├── manifest.json
├── site-settings.json
└── README.md
```

## Dead Ends / Don't Repeat
-

## Related Sessions
