# Profile README redesign — premium-minimal terminal hero

**Date:** 2026-08-12
**Repo:** Rolazo/Rolazo (GitHub profile README)
**Audience:** Recruiters / hiring managers for SRE / DevOps roles
**Register:** Premium minimal — reads senior, no gimmicks

## Context

All substantive work (foralium-*, org-config, compound, automation) lives in the
private baena-labs org; only the profile repo, `devops-ci-challenge`, and
`giv-token-contracts` are public. The profile must therefore *tell* the story
rather than pin it. Optimize for a ~10-second recruiter skim: seniority,
employers, stack, then the AI/founder layer as "what I'm building now".

## Design

### 1. Hero — terminal-styled SVG banner

- `assets/hero-dark.svg` and `assets/hero-light.svg`, committed to the repo,
  swapped via `<picture>` with `prefers-color-scheme` media queries.
- Terminal window styling: thin rounded border, `nicolas@baena-labs` title bar,
  `$ whoami` prompt, name + title line, one credibility line
  (10+ yrs · AWS · K8s · Terraform), blinking block cursor.
- Cursor blink is an SVG SMIL animation — the only motion on the page. SMIL
  renders in GitHub READMEs (served via camo as `<img>`).
- Monospace type; one accent color: `#58a6ff` family on dark, a matching
  accessible blue on light.

### 2. Body — plain markdown (searchable, accessible)

SVG text is not indexed; every fact in the hero also appears as real text:

- **Value prop** — two lines: SRE/DevOps, 10+ years, core strengths.
- **Experience strip** — `Maersk · Amadeus · UnitedHealth Group · The Home
  Depot` with years, bold plain text, no logos.
- **Stack** — existing flat-square shields.io badges regrouped into labeled
  rows: Cloud / IaC & CI-CD / Runtime / AI tooling.
- **Building now** — 3 bullets describing baena-labs, Foralium, and the
  automation layer, linking to https://github.com/baena-labs.
- **Contact** — keep LinkedIn / Email / GitHub badge row.

### 3. Removed

- `streak-stats.demolab.com` widget and `github-readme-stats` top-langs card:
  third-party-hosted (slow/dead risk), palette-clashing, streak counters read
  junior. v1 has no external dependencies beyond shields.io badges.

### 4. Repo hygiene

- Add `.gitignore` with `*.pdf` — the SRE/DevOps CV PDF sits untracked in the
  working tree and must never land in a public repo (personal data).
- All work on a feature branch (`feat/profile-redesign`); Conventional Commits.

## Error handling / risks

- If SMIL animation is ever stripped by camo, the cursor renders as a static
  block — degrades gracefully.
- Light-mode users on clients ignoring `<picture>` sources fall back to the
  dark SVG (the `<img>` fallback) — acceptable.

## Verification

- Push branch; view rendered README on github.com in both dark and light
  themes; confirm hero swaps, cursor blinks, badges group correctly.
- Confirm `git status` never shows the PDF as tracked.

## Out of scope (possible v2)

- lowlighter/metrics nightly Action with palette-matched activity card.
