# Elevate Courses — GitHub Setup Reference

## Prerequisites
- Git installed
- A GitHub account

---

## Step 1: Configure Git Identity

```bash
git config --global user.name "your-github-username"
git config --global user.email "your@email.com"
```

---

## Step 2: Generate SSH Key

```bash
ssh-keygen -t ed25519 -C "your@email.com" -f ~/.ssh/id_ed25519 -N ""
```

---

## Step 3: Start SSH Agent & Add Key

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

---

## Step 4: Copy Public Key

```bash
cat ~/.ssh/id_ed25519.pub
```

Go to **github.com/settings/ssh/new**, paste the output, title it (e.g. `Windows Home`), click **Add SSH key**.

---

## Step 5: Add GitHub to Known Hosts & Test Connection

```bash
ssh-keyscan github.com >> ~/.ssh/known_hosts
ssh -T git@github.com
```

Expected output: `Hi username! You've successfully authenticated...`

---

## Step 6: Create Repo on GitHub

Go to **github.com/new**:
- Name your repo
- Set to Public
- **Do NOT** initialize with README
- Click **Create repository**

---

## Step 7: Initialize Local Repo & Push

```bash
cd ~/Documents/Obsidian\ Vault
git init
git remote add origin git@github.com:YOUR-USERNAME/YOUR-REPO.git
git add .
git commit -m "Initial commit"
git branch -M main
git push -u origin main
```

---

## Daily Push Workflow

After making changes to your notes:

```bash
cd ~/Documents/Obsidian\ Vault
git add .
git commit -m "your message here"
git push
```

---

## Pulling on Another Machine

First-time setup on a new machine: repeat Steps 1–5, then:

```bash
git clone git@github.com:YOUR-USERNAME/YOUR-REPO.git
```

For subsequent syncs on that machine:

```bash
cd ~/Documents/Obsidian\ Vault
git pull
```

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
