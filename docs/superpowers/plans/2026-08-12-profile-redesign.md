# Profile README Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the Rolazo/Rolazo profile README as a premium-minimal, recruiter-facing page with a terminal-styled adaptive SVG hero.

**Architecture:** Two hand-written SVGs (dark/light) committed under `assets/`, swapped by a `<picture>` element in `README.md`; all hero facts duplicated as plain markdown below for searchability. No GitHub Actions, no third-party embeds except shields.io badges.

**Tech Stack:** Hand-written SVG (SMIL animation), GitHub-flavored markdown, shields.io flat-square badges.

## Global Constraints

- Branch: all work on `feat/profile-redesign`; Conventional Commits, imperative, ≤72-char subject.
- The CV PDF (`- SRE DevOps Specialist CV Nicolas Baena.pdf`) must NEVER be tracked by git.
- Accent colors: `#58a6ff` (dark theme), `#0969da` (light theme). Dark bg `#0d1117`, dark border `#30363d`; light bg `#ffffff`, light border `#d0d7de`.
- Only motion on the page: the hero's blinking cursor (SVG SMIL).
- Do not invent per-employer dates or metrics — the only verified claim is "10+ years" total across Maersk, Amadeus, UnitedHealth Group, The Home Depot.
- No visual/render checks can run locally beyond XML validity; final verification happens on github.com (Task 4).

---

### Task 1: Repo hygiene — keep the CV out of the public repo

**Files:**
- Create: `.gitignore`

**Interfaces:**
- Consumes: nothing
- Produces: nothing later tasks depend on; standalone safety task

- [ ] **Step 1: Write `.gitignore`**

```gitignore
*.pdf
.DS_Store
```

- [ ] **Step 2: Verify the PDF is ignored and untracked**

Run: `git status --porcelain && git check-ignore -v "./- SRE DevOps Specialist CV Nicolas Baena.pdf"`
Expected: status shows only `.gitignore` as new (`?? .gitignore` or `A .gitignore`), no PDF line; check-ignore prints the `.gitignore:1:*.pdf` rule match.

- [ ] **Step 3: Commit**

```bash
git add .gitignore
git commit -m "chore: ignore pdf and macos artifacts"
```

---

### Task 2: Terminal hero SVGs (dark + light)

**Files:**
- Create: `assets/hero-dark.svg`
- Create: `assets/hero-light.svg`

**Interfaces:**
- Consumes: nothing
- Produces: the exact paths `assets/hero-dark.svg` and `assets/hero-light.svg` referenced by the `<picture>` element in Task 3. Both SVGs are 800×230 viewBox, so Task 3 embeds them at `width="100%"` with no size attributes needed on the sources.

- [ ] **Step 1: Write `assets/hero-dark.svg`**

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 230" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" role="img" aria-label="Terminal: Nicolas Baena, SRE / DevOps Engineer">
  <!-- window -->
  <rect x="1" y="1" width="798" height="228" rx="10" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>
  <!-- title bar -->
  <line x1="1" y1="40" x2="799" y2="40" stroke="#30363d" stroke-width="1"/>
  <circle cx="26" cy="20.5" r="6" fill="#30363d"/>
  <circle cx="46" cy="20.5" r="6" fill="#30363d"/>
  <circle cx="66" cy="20.5" r="6" fill="#30363d"/>
  <text x="400" y="25" text-anchor="middle" font-size="13" fill="#8b949e">nicolas@baena-labs: ~</text>
  <!-- prompt -->
  <text x="32" y="78" font-size="15">
    <tspan fill="#58a6ff">$</tspan>
    <tspan fill="#8b949e" dx="8">whoami</tspan>
  </text>
  <!-- identity -->
  <text x="32" y="118" font-size="26" font-weight="600" fill="#e6edf3">Nicolas Baena</text>
  <text x="32" y="148" font-size="16" fill="#58a6ff">SRE / DevOps Engineer</text>
  <!-- credibility -->
  <text x="32" y="180" font-size="14" fill="#8b949e">10+ yrs · AWS · Kubernetes · Terraform · CI/CD at global scale</text>
  <text x="32" y="204" font-size="14" fill="#8b949e">Maersk · Amadeus · UnitedHealth Group · The Home Depot</text>
  <!-- blinking cursor -->
  <rect x="240" y="163" width="9" height="18" fill="#58a6ff">
    <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.2s" repeatCount="indefinite"/>
  </rect>
</svg>
```

Note: the cursor rect sits at the end of the first credibility line's visual block; exact x is not critical, but keep it clear of text. If line lengths change, re-check overlap by opening the file in a browser.

- [ ] **Step 2: Write `assets/hero-light.svg`**

Same geometry, light palette:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 230" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" role="img" aria-label="Terminal: Nicolas Baena, SRE / DevOps Engineer">
  <!-- window -->
  <rect x="1" y="1" width="798" height="228" rx="10" fill="#ffffff" stroke="#d0d7de" stroke-width="1.5"/>
  <!-- title bar -->
  <line x1="1" y1="40" x2="799" y2="40" stroke="#d0d7de" stroke-width="1"/>
  <circle cx="26" cy="20.5" r="6" fill="#d0d7de"/>
  <circle cx="46" cy="20.5" r="6" fill="#d0d7de"/>
  <circle cx="66" cy="20.5" r="6" fill="#d0d7de"/>
  <text x="400" y="25" text-anchor="middle" font-size="13" fill="#57606a">nicolas@baena-labs: ~</text>
  <!-- prompt -->
  <text x="32" y="78" font-size="15">
    <tspan fill="#0969da">$</tspan>
    <tspan fill="#57606a" dx="8">whoami</tspan>
  </text>
  <!-- identity -->
  <text x="32" y="118" font-size="26" font-weight="600" fill="#1f2328">Nicolas Baena</text>
  <text x="32" y="148" font-size="16" fill="#0969da">SRE / DevOps Engineer</text>
  <!-- credibility -->
  <text x="32" y="180" font-size="14" fill="#57606a">10+ yrs · AWS · Kubernetes · Terraform · CI/CD at global scale</text>
  <text x="32" y="204" font-size="14" fill="#57606a">Maersk · Amadeus · UnitedHealth Group · The Home Depot</text>
  <!-- blinking cursor -->
  <rect x="240" y="163" width="9" height="18" fill="#0969da">
    <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.2s" repeatCount="indefinite"/>
  </rect>
</svg>
```

- [ ] **Step 3: Validate both SVGs are well-formed XML**

Run: `xmllint --noout assets/hero-dark.svg assets/hero-light.svg && echo VALID`
Expected: `VALID` (no output before it). If `xmllint` is missing, use `python3 -c "import xml.dom.minidom,sys; [xml.dom.minidom.parse(f) for f in sys.argv[1:]]; print('VALID')" assets/hero-dark.svg assets/hero-light.svg`.

- [ ] **Step 4: Visual spot-check locally**

Run: `open -a "Google Chrome" assets/hero-dark.svg assets/hero-light.svg`
Expected: both render as terminal windows, cursor blinks, no text overlaps the cursor rect or overflows the 800-wide frame.

- [ ] **Step 5: Commit**

```bash
git add assets/
git commit -m "feat: add adaptive terminal hero svgs"
```

---

### Task 3: Rewrite README.md

**Files:**
- Modify: `README.md` (full replacement)

**Interfaces:**
- Consumes: `assets/hero-dark.svg`, `assets/hero-light.svg` from Task 2 (relative paths — GitHub resolves them against the repo root on the profile page).
- Produces: final README; nothing downstream.

- [ ] **Step 1: Replace `README.md` with the following content, verbatim**

````markdown
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/hero-light.svg">
  <img alt="Nicolas Baena — SRE / DevOps Engineer. 10+ years: Maersk, Amadeus, UnitedHealth Group, The Home Depot." src="assets/hero-dark.svg" width="100%">
</picture>

Site reliability and DevOps engineer with **10+ years** shipping cloud infrastructure at global scale — CI/CD, Kubernetes, and Terraform as products, not chores.

**Maersk** · **Amadeus** · **UnitedHealth Group** · **The Home Depot**

---

## Stack

**Cloud & runtime**
&nbsp;![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazonaws&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)

**IaC & CI/CD**
&nbsp;![Terraform](https://img.shields.io/badge/Terraform-623CE4?style=flat-square&logo=terraform&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)

**Languages**
&nbsp;![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=nodedotjs&logoColor=white)

**AI tooling**
&nbsp;![Claude Code](https://img.shields.io/badge/Claude_Code-000000?style=flat-square&logo=anthropic&logoColor=white)

---

## Building now

- An **event-driven AI automation layer** on AWS — Lambda, ECS, Terraform, triggered by GitHub webhooks — so org-wide CI/CD and agent operations run without human intervention
- **[baena-labs](https://github.com/baena-labs)** — governance-as-code for Claude Code: agents, skills, hooks, and rules synced across every repo in an org automatically
- A **repo-split framework** — AI that decides when a domain needs one repo vs a family (`{domain}`, `{domain}-infra`, `{domain}-web`)

---

## Connect

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/nicolas-baena-3b2a9b17b/)
[![Email](https://img.shields.io/badge/Email-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:nicobaena96@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/Rolazo)
````

- [ ] **Step 2: Sanity-check the markdown structure**

Run: `grep -c "streak-stats\|github-readme-stats" README.md; grep -c "hero-dark.svg" README.md`
Expected: `0` (old third-party embeds gone) then `2` (source + img fallback).

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "feat: redesign profile with terminal hero, drop third-party stats"
```

---

### Task 4: Push, verify rendered output, merge

**Files:**
- None (verification + integration)

**Interfaces:**
- Consumes: all prior commits on `feat/profile-redesign`
- Produces: merged `main`; live profile at https://github.com/Rolazo

- [ ] **Step 1: Push the branch**

```bash
git push -u origin feat/profile-redesign
```

- [ ] **Step 2: Verify rendered README on the branch**

Open `https://github.com/Rolazo/Rolazo/blob/feat/profile-redesign/README.md` in a browser. Check:
- Hero renders as a terminal window; cursor blinks.
- Toggle GitHub theme (Settings → Appearance, or emulate `prefers-color-scheme` in devtools): dark shows `hero-dark.svg`, light shows `hero-light.svg`.
- Badges group into four labeled rows; no dead images.

Expected: all three checks pass. If the SVG shows raw XML or a broken-image icon, the file has an XML error — re-run Task 2 Step 3.

- [ ] **Step 3: Open PR and merge**

```bash
gh pr create --title "feat: redesign profile with terminal hero" --body "Premium-minimal recruiter-facing redesign per docs/superpowers/specs/2026-08-12-profile-redesign-design.md

- Adaptive dark/light terminal SVG hero (SMIL cursor blink)
- Plain-markdown credibility strip + grouped stack badges
- Drops third-party streak/stats embeds
- Ignores *.pdf so the CV never lands in the public repo

🤖 Generated with [Claude Code](https://claude.com/claude-code)"
gh pr merge --squash --delete-branch
```

Expected: PR merges clean (no conflicts — nothing else touches these files). Profile at https://github.com/Rolazo updates within a minute.

- [ ] **Step 4: Final live check**

Open `https://github.com/Rolazo`. Expected: new hero + sections render on the profile page; `git status` locally still shows the PDF as untracked-and-ignored.
