---
name: skillguard
description: >
  Scan a third-party Agent Skill, Claude Code plugin, or MCP server for malware
  BEFORE installing it. Use when the user says "is this skill safe?", "scan this
  MCP", "vet this plugin", "skillguard", or is about to install a skill from a
  GitHub URL. Static analysis only — never runs the scanned code. Complements
  vibe-sec (which audits application code, not skill/MCP supply chain).
metadata:
  homepage: https://github.com/epistemedeus/skillguard
  version: "1.3.0"
---

# SkillGuard — scan skills and MCP servers before install

Vendored static scanner from [epistemedeus/skillguard](https://github.com/epistemedeus/skillguard).
It clones with `git clone` (hooks disabled) and **reads** files. It never runs
`npm install`, postinstall hooks, or the target code.

## When to use

- Before adding any third-party skill, plugin, or MCP server
- When the user pastes a GitHub URL and asks if it is safe to install
- After `vibe-sec` if the question is supply-chain (skills/MCP), not app vulns

## Run

From this skill folder:

```bash
node <SKILL_DIR>/scripts/index.js https://github.com/owner/repo
node <SKILL_DIR>/scripts/index.js ./path/to/local-skill
```

Or:

```bash
npx github:epistemedeus/skillguard https://github.com/owner/repo
```

Prefer the vendored `scripts/index.js` so the scan does not depend on a live
`npx github:` fetch.

## Verdicts

| Exit | Meaning |
|------|---------|
| 0 | no known-malicious patterns |
| 2 | suspicious — review warnings |
| 3 | dangerous — do not install without reviewing flagged files |

Checks: env/secret exfil to known dump hosts, `curl \| bash` / `eval(atob)`,
prompt-injection in SKILL.md, committed binaries, install hooks, skip-permissions.

Heuristics miss novel attacks. A clean scan is not a guarantee.

## MCP (optional)

`scripts/mcp.js` exposes `scan_skill(target)` over stdio. Do not put secrets
in MCP config.

## Do not

- Execute install scripts from the scanned repo
- Commit `.env`, cookies, or API keys found during a scan
- Treat this as a replacement for reading the code
