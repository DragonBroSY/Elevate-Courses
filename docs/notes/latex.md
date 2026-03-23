---
layout: note
title: "LaTeX Quick Reference"
---

Write math formulas in Obsidian and on the site using `$...$` (inline) or `$$...$$` (block).

---

## Inline vs Block

| Type | Syntax | Renders as |
|------|--------|------------|
| Inline | `$E = mc^2$` | $E = mc^2$ |
| Block | `$$E = mc^2$$` | $$E = mc^2$$ |

---

## Basic Operations

| Syntax | Renders as |
|--------|------------|
| `$a + b$` | $a + b$ |
| `$a - b$` | $a - b$ |
| `$a \times b$` | $a \times b$ |
| `$a \div b$` | $a \div b$ |
| `$\frac{a}{b}$` | $\frac{a}{b}$ |
| `$a^2$` | $a^2$ |
| `$a^{n+1}$` | $a^{n+1}$ |
| `$\sqrt{x}$` | $\sqrt{x}$ |
| `$\sqrt[n]{x}$` | $\sqrt[n]{x}$ |

---

## Greek Letters

| Syntax | Renders as | Syntax | Renders as |
|--------|------------|--------|------------|
| `$\alpha$` | $\alpha$ | `$\Alpha$` | $A$ |
| `$\beta$` | $\beta$ | `$\Beta$` | $B$ |
| `$\gamma$` | $\gamma$ | `$\Gamma$` | $\Gamma$ |
| `$\delta$` | $\delta$ | `$\Delta$` | $\Delta$ |
| `$\theta$` | $\theta$ | `$\Theta$` | $\Theta$ |
| `$\lambda$` | $\lambda$ | `$\Lambda$` | $\Lambda$ |
| `$\mu$` | $\mu$ | `$\pi$` | $\pi$ |
| `$\rho$` | $\rho$ | `$\sigma$` | $\sigma$ |
| `$\phi$` | $\phi$ | `$\Phi$` | $\Phi$ |
| `$\omega$` | $\omega$ | `$\Omega$` | $\Omega$ |

---

## Subscripts & Superscripts

| Syntax | Renders as |
|--------|------------|
| `$x_1$` | $x_1$ |
| `$x_{12}$` | $x_{12}$ |
| `$x^2$` | $x^2$ |
| `$x^{n+1}$` | $x^{n+1}$ |
| `$x_i^2$` | $x_i^2$ |
| `$V_{ne}$` | $V_{ne}$ |

---

## Fractions & Division

| Syntax | Renders as |
|--------|------------|
| `$\frac{1}{2}$` | $\frac{1}{2}$ |
| `$\frac{a+b}{c+d}$` | $\frac{a+b}{c+d}$ |
| `$\frac{V_1}{T_1} = \frac{V_2}{T_2}$` | $\frac{V_1}{T_1} = \frac{V_2}{T_2}$ |

---

## Equations (Block)

`$$L = \frac{1}{2} \rho v^2 S C_L$$`
$$L = \frac{1}{2} \rho v^2 S C_L$$

`$$\frac{W}{S} = \frac{1}{2} \rho v^2 C_L$$`
$$\frac{W}{S} = \frac{1}{2} \rho v^2 C_L$$

`$$\text{Load Factor} = \frac{1}{\cos\theta}$$`
$$\text{Load Factor} = \frac{1}{\cos\theta}$$

`$$\text{TAS} = \text{IAS} \times \sqrt{\frac{\rho_0}{\rho}}$$`
$$\text{TAS} = \text{IAS} \times \sqrt{\frac{\rho_0}{\rho}}$$

---

## Symbols

| Syntax | Renders as | Syntax | Renders as |
|--------|------------|--------|------------|
| `$\approx$` | $\approx$ | `$\neq$` | $\neq$ |
| `$\leq$` | $\leq$ | `$\geq$` | $\geq$ |
| `$\pm$` | $\pm$ | `$\infty$` | $\infty$ |
| `$\degree$` | $°$ | `$\cdot$` | $\cdot$ |
| `$\rightarrow$` | $\rightarrow$ | `$\Rightarrow$` | $\Rightarrow$ |
| `$\uparrow$` | $\uparrow$ | `$\downarrow$` | $\downarrow$ |

---

## Text Inside Formulas

Use `\text{}` to write plain text inside a formula:

`$\text{Stall speed} = V_S$` → $\text{Stall speed} = V_S$

`$V_{ne} = 163 \text{ kts}$` → $V_{ne} = 163 \text{ kts}$

---

## Aviation Examples

`$$V_A = V_S \times \sqrt{n}$$`
$$V_A = V_S \times \sqrt{n}$$

`$$\text{Density Altitude} = \text{PA} + 120 \times (T - T_{std})$$`
$$\text{Density Altitude} = \text{PA} + 120 \times (T - T_{std})$$

`$$\text{Fuel burn} = \frac{\text{distance}}{\text{TAS}} \times \text{GPH}$$`
$$\text{Fuel burn} = \frac{\text{distance}}{\text{TAS}} \times \text{GPH}$$

`$$\tan(\theta) = \frac{\text{bank angle rate}}{g}$$`
$$\tan(\theta) = \frac{\text{bank angle rate}}{g}$$
