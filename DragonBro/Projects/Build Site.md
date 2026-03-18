# Build Site

## Quick Reference
- Live: https://build.drabro.org
- Local: ~/build-kit
- Server: 54.69.14.145 (bitnami), same Lightsail instance as 3d.drabro.org
- GitHub: https://github.com/DragonBroSY/build-kit (private)
- WordPress install: `/opt/bitnami/wordpress-build`
- DB: `bitnami_wordpress_build`
- Status: FULLY LIVE as of 2026-02-22

## Decisions Made
- 2026-02-22: Hosted on same Lightsail instance as 3d.drabro.org to avoid extra cost
- 2026-02-22: Route 53 A record → 54.69.14.145
- SSL via Let's Encrypt (lego) — cert at `/opt/bitnami/apache/conf/build.drabro.org.crt`
- Hardware standard: Simpson Strong-Tie (SDS screws, ZMAX connectors, DTT2Z, LUS hangers)

## How Things Work
- Vhosts: `build-vhost.conf` (HTTP→HTTPS redirect), `build-https-vhost.conf`
- WP-CLI: `sudo /opt/bitnami/wp-cli/bin/wp --path=/opt/bitnami/wordpress-build`

## Pages
| ID | Slug | Title |
|----|------|-------|
| 6 | /build-home/ | Home |
| 7 | /wind-chime-post/ | Wind Chime Post |
| 8 | /deck-build/ | Deck Build |
| 9 | /about-build/ | About |

## Structure
```
build-kit/
├── content/         (4 Elementor pages)
├── plans/           (per-project)
├── assets/simpson/
└── scripts/
```

## Dead Ends / Don't Repeat
-

## Related Sessions
