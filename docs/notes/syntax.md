---
layout: note
title: "Syntax Reference"
---

Quick reference for Markdown, Obsidian, and LaTeX math syntax.

---

## Markdown

### Text Formatting

| Syntax | Result |
|--------|--------|
| `**bold**` | **bold** |
| `*italic*` | *italic* |
| `~~strikethrough~~` | ~~strikethrough~~ |
| `` `inline code` `` | `inline code` |
| `> blockquote` | blockquote |
| `---` | horizontal rule |

### Headings

```
# H1
## H2
### H3
#### H4
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

### Links & Images

```
[label](https://url.com)          external link
![alt text](image.png)            image
```

### Tables

```
| Col A | Col B |
|-------|-------|
| val 1 | val 2 |
```

### Code Blocks

````
```python
def hello():
    print("hello")
```
````

---

## Obsidian

### Links & Embeds

```
[[Note Name]]                     link to note
[[Note Name|display text]]        link with alias
![[Note Name]]                    embed note
![[image.png]]                    embed image
![[image.png|300]]                embed image at width
```

*Note: wikilinks are auto-converted to standard links when published to the site.*

### Frontmatter

```yaml
---
publish: true
title: "My Note"
date: 2026-03-24
topics: "topic1, topic2"
---
```

### Tags

```
#tagname                          inline tag
```

### Callouts

```
> [!note]
> Content here

> [!tip]
> Content here

> [!warning]
> Content here

> [!danger]
> Content here

> [!info]
> Content here
```

*Note: callouts render in Obsidian but show as blockquotes on the site.*

### Footnotes

```
Here is a claim.[^1]

[^1]: Source or explanation.
```

---

## LaTeX Math

Supported in Obsidian natively and on the site via MathJax.

### Inline vs Block

| Type | Syntax | Renders as |
|------|--------|------------|
| Inline | `$E = mc^2$` | $E = mc^2$ |
| Block | `$$E = mc^2$$` | $$E = mc^2$$ |

### Basic Operations

| Syntax | Renders as |
|--------|------------|
| `$a \times b$` | $a \times b$ |
| `$a \div b$` | $a \div b$ |
| `$\frac{a}{b}$` | $\frac{a}{b}$ |
| `$a^2$` | $a^2$ |
| `$a^{n+1}$` | $a^{n+1}$ |
| `$\sqrt{x}$` | $\sqrt{x}$ |
| `$x_1$` | $x_1$ |
| `$x_{12}$` | $x_{12}$ |

### Greek Letters

| Syntax | Renders as | Syntax | Renders as |
|--------|------------|--------|------------|
| `$\alpha$` | $\alpha$ | `$\gamma$` | $\gamma$ |
| `$\beta$` | $\beta$ | `$\delta$` | $\delta$ |
| `$\theta$` | $\theta$ | `$\Delta$` | $\Delta$ |
| `$\lambda$` | $\lambda$ | `$\mu$` | $\mu$ |
| `$\pi$` | $\pi$ | `$\rho$` | $\rho$ |
| `$\sigma$` | $\sigma$ | `$\phi$` | $\phi$ |
| `$\omega$` | $\omega$ | `$\Omega$` | $\Omega$ |

### Symbols

| Syntax | Renders as | Syntax | Renders as |
|--------|------------|--------|------------|
| `$\approx$` | $\approx$ | `$\neq$` | $\neq$ |
| `$\leq$` | $\leq$ | `$\geq$` | $\geq$ |
| `$\pm$` | $\pm$ | `$\infty$` | $\infty$ |
| `$\rightarrow$` | $\rightarrow$ | `$\Rightarrow$` | $\Rightarrow$ |
| `$\cdot$` | $\cdot$ | `$\times$` | $\times$ |

### Text Inside Formulas

`$V_{ne} = 163 \text{ kts}$` → $V_{ne} = 163 \text{ kts}$

`$\text{Load Factor} = \frac{1}{\cos\theta}$` → $\text{Load Factor} = \frac{1}{\cos\theta}$

### Aviation Examples

```
$$L = \frac{1}{2} \rho v^2 S C_L$$
```
$$L = \frac{1}{2} \rho v^2 S C_L$$

```
$$V_A = V_S \times \sqrt{n}$$
```
$$V_A = V_S \times \sqrt{n}$$

```
$$\text{Density Altitude} = \text{PA} + 120 \times (T - T_{std})$$
```
$$\text{Density Altitude} = \text{PA} + 120 \times (T - T_{std})$$

```
$$\text{TAS} = \text{IAS} \times \sqrt{\frac{\rho_0}{\rho}}$$
```
$$\text{TAS} = \text{IAS} \times \sqrt{\frac{\rho_0}{\rho}}$$

```
$$\text{Fuel burn} = \frac{\text{distance}}{\text{TAS}} \times \text{GPH}$$
```
$$\text{Fuel burn} = \frac{\text{distance}}{\text{TAS}} \times \text{GPH}$$
