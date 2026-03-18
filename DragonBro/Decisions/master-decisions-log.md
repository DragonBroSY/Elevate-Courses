# Master Decisions Log

Chronological record of major cross-project decisions.

## Infrastructure
- All drabro.org sites share one Lightsail instance (`WordPress-drabro.org`, us-west-2, $5/mo)
- Route 53 for DNS — A records → 54.69.14.145
- SSL via Let's Encrypt (lego) per domain
- All sites use Elementor + WordPress
- WP-CLI for all programmatic WP operations

## Branding Standards (every new site)
- Site title: project name (never leave WordPress default)
- Header logo: Dragon logo (source on 3d site server)
- Favicon: Harry on the horse (`~/Downloads/harry.jpg`)
- Tagline: always cleared
- Default content (Hello World! post, Sample Page): always deleted

## Git / GitHub
- Account: DragonBroSY
- Every project gets a private GitHub repo
- Git identity: Hans Kreuk / admin@drabro.org
- Commit page JSON before and after every deploy

## 2026-02-21
- Stood up fly.drabro.org (Flight Training) — [[Projects/Flight Training]]

## 2026-02-22
- Stood up build.drabro.org (Build Site) — [[Projects/Build Site]]
