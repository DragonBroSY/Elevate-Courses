---
publish: false
title: "DragonBro Vault Home"
date: 2026-02-25
topics: "navigation, markdown reference, vault, obsidian"
---

# DragonBro Vault

## Navigation
- [[master-decisions-log|Decisions Log]]
- [[Projects/ATP|ATP]]
- [[Projects/Flight Training|Flight Training]]
- [[Projects/3D Tours|3D Tours]]
- [[Projects/Build Site|Build Site]]

---

## Markdown Quick Reference

### Text Formatting
| Syntax | Result |
|--------|--------|
| `**bold**` | **bold** |
| `*italic*` | *italic* |
| `~~strikethrough~~` | ~~strikethrough~~ |
| `==highlight==` | ==highlight== |
| `> blockquote` | indented quote block |
| `---` | horizontal rule |

### Headings
```
# H1
## H2
### H3
```

### Lists
```
- unordered item
  - nested item

1. ordered item
2. second item

- [ ] task unchecked
- [x] task checked
```

### Links & Embeds
```
[label](url)                  ← external link
[[Note Name]]                 ← internal wikilink
[[Note Name|display text]]    ← aliased wikilink
![[Note Name]]                ← embed note
![[image.png]]                ← embed image
```

### Code
````
`inline code`

```language
code block
```
````

### Tables
```
| Col A | Col B |
|-------|-------|
| val 1 | val 2 |
```

### Obsidian Callouts
```
> [!note]
> [!tip]
> [!warning]
> [!danger]
> [!info]
> [!example]
> [!quote]
```

### Tags & Frontmatter
```yaml
---
tags: [tag1, tag2]
date: 2026-03-18
---
```
Inline tag: `#tagname`

### Footnotes
```
Here is a claim.[^1]

[^1]: Source or explanation.
```
