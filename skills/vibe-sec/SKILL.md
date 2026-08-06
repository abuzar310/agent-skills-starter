---
name: vibe-sec
description: Audits codebases for security vulnerabilities, especially those AI coding assistants introduce in rapidly-built apps. Covers exposed API keys and secrets, broken database access control (Supabase RLS, Firebase rules, Convex), missing auth and ownership checks, IDOR, injection (SQL, XSS, XXE, path traversal), SSRF, CSRF, open redirect, insecure file uploads, payment manipulation, LLM/AI integration risks, mobile token storage, rate limiting, and deployment misconfiguration. Use whenever the user asks about security, wants a code review, mentions "vibe coding", or when writing or reviewing code that touches authentication, payments, database access, file uploads, URL fetching, API keys, secrets, or user data — even if security is not explicitly mentioned. Also trigger on "is this safe?", "check my code", "audit this", "review for vulnerabilities", "can someone hack this?", or "am I going to get pwned?".
license: MIT
metadata:
  version: "1.0"
  merged_from:
    - "BehiSecc/VibeSec-Skill (Apache-2.0) — vulnerability depth"
    - "raroque/vibe-security-skill (MIT, Chris Raroque) — skill architecture, modern stack"
    - "benavlabs/vibe-check (MIT, Benav Labs) — audit process, verification goals"
---

Audit code for security vulnerabilities, with emphasis on the mistakes AI code generation makes repeatedly. These issues are widespread in rapidly-built apps where security fundamentals get skipped, and they lead to real breaches: stolen keys, drained billing accounts, leaked user databases.

Approach code from a **bug hunter's perspective**. Assume an attacker has your source, your bundle, and unlimited time.


## The Core Principle

**Never trust the client.** Every price, user ID, role, subscription status, feature flag, and rate limit counter must be validated or enforced server-side. If it exists only in the browser, the mobile bundle, or the request body, an attacker controls it.

Four supporting rules:

- **Defense in depth** — never rely on a single control. Middleware plus handler plus database policy.
- **Fail closed** — when a check errors or a value is missing, deny.
- **Least privilege** — grant the minimum permission that works.
- **Authentication ≠ authorization** — "is this user logged in?" and "does this user own this row?" are two separate checks. Missing the second is the most common bug in this entire skill.


## Two Modes

This skill runs in one of two modes. Pick based on what the user asked for.

### Mode 1 — Quick Audit (default)

For "check my code", "is this safe?", or a review of specific files. Work through the audit map below, load only the references your stack needs, and report findings in the output format. Do not create files unless asked.

### Mode 2 — Full Audit

For "full security audit", "audit the whole project", or an explicit request for reports and fixes. Work **one category at a time, start to finish** — do not batch. For each category:

1. **Investigate** — search every file that could relate. Configs, routes, middleware, schemas, env files, frontend code, package manifests, CI config. Do not skim, do not assume.
2. **Report** — write `security/reports/{CATEGORY}_REPORT.md`: what's vulnerable, what's already safe, what's missing entirely, and severity.
3. **Plan** — write `security/plans/{CATEGORY}_PLAN.md`: the specific changes, plus **verification goals stated as commands or observable outcomes**, not vibes.
4. **Implement** the fixes.
5. **Verify** against every goal. Update the report with the result.

Create `security/reports/` and `security/plans/` if absent. Finish with a summary across all categories.

A verification goal must be checkable. `git ls-files .env` returns nothing — good. "Ensure secrets are handled safely" — useless, rewrite it.


## Audit Map

Skip any row whose technology the codebase doesn't use. Load a reference only when that row is in scope.

| # | Area | Look for | Reference |
|---|---|---|---|
| 1 | **Secrets & env** | Hardcoded keys, `NEXT_PUBLIC_`/`VITE_`/`EXPO_PUBLIC_` leaks, `.env` tracked by git | `secrets-and-env.md` |
| 2 | **Database access** | Supabase RLS, Firebase rules, Convex guards. **#1 source of critical bugs** | `database-security.md` |
| 3 | **Auth** | JWT verification, middleware ordering, Server Actions, session cookies | `authentication.md` |
| 4 | **Access control** | IDOR, ownership checks, privilege escalation, mass assignment, GraphQL | `access-control.md` |
| 5 | **Injection** | SQLi, ORM operator injection, XSS, XXE, path traversal | `injection.md` |
| 6 | **SSRF & redirects** | User-supplied URLs fetched server-side, open redirect, CSRF | `ssrf-and-redirects.md` |
| 7 | **File uploads** | Magic-byte validation, storage location, filename handling | `file-uploads.md` |
| 8 | **Payments** | Client-set prices, webhook signatures, subscription status | `payments.md` |
| 9 | **AI / LLM** | Exposed keys, spend caps, prompt injection, unsafe output rendering | `ai-integration.md` |
| 10 | **Mobile** | Token storage, API keys in bundle, deep links, biometrics | `mobile.md` |
| 11 | **Rate limiting** | Auth endpoints, AI calls, tamper-proof counters | `rate-limiting.md` |
| 12 | **Deployment** | Security headers, CORS, source maps, error leakage, dependencies | `deployment.md` |

**Where to start:** if you only have time for three, do 1, 2, and 4. Exposed secrets, missing RLS, and missing ownership checks account for the overwhelming majority of real-world compromises in this class of app.


## Core Instructions

- Report only genuine security issues. Do not nitpick style or non-security concerns.
- Prioritize by exploitability and real-world impact, not by category order.
- If the codebase doesn't use a technology, skip that section entirely — don't pad the report.
- Flag critical findings (exposed secrets, disabled RLS, auth bypass) **at the top**, immediately. Never bury them mid-list.
- Distinguish confirmed from suspected. If you can't verify a path is reachable, say so rather than inflating severity.
- If a secret was ever committed to git, it is compromised. Deleting the file does not remove it from history — the key must be rotated. Say this explicitly.


## Output Format

Organize by severity: **Critical** → **High** → **Medium** → **Low**.

For each issue:
1. File and line(s).
2. Name of the vulnerability.
3. What an attacker could actually do — concrete impact, not abstract risk.
4. Before/after code fix.

Skip clean areas. End with a prioritized summary.

### Example

#### Critical

**`lib/supabase.ts:3` — Supabase `service_role` key exposed in client bundle**

The `service_role` key bypasses all Row-Level Security. Anyone can extract it from the browser bundle and read, modify, or delete every row in your database.

```typescript
// Before
const supabase = createClient(url, process.env.NEXT_PUBLIC_SUPABASE_SERVICE_KEY!)

// After — anon key client-side; service_role only in server-side code
const supabase = createClient(url, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!)
```

Rotate the key now — it is in your deployed bundle and in git history.

#### High

**`app/api/checkout/route.ts:15` — Price taken from client request body**

An attacker can set any price, including $0.01, by modifying the request.

```typescript
// Before
const session = await stripe.checkout.sessions.create({
  line_items: [{ price_data: { unit_amount: req.body.price } }]
})

// After — look up the price server-side
const product = await db.products.findUnique({ where: { id: req.body.productId } })
const session = await stripe.checkout.sessions.create({
  line_items: [{ price: product.stripePriceId }]
})
```

### Summary

1. **Service role key exposed (Critical)** — full database compromise. Rotate immediately, move server-side.
2. **Client-controlled pricing (High)** — purchases at arbitrary prices. Use server-side lookup.


## When Generating Code

These rules apply proactively, not just to audits. Before writing code that touches auth, payments, database access, file uploads, URL fetching, API keys, or user data, consult the relevant reference and avoid introducing the vulnerability in the first place. Prevention beats detection.

`AGENTS.md` in this skill folder is a condensed rules file you can drop into a project root so these constraints apply to all generated code there.


## What This Skill Won't Catch

Be honest about limits. Static review does not cover:

- **Business logic flaws** — a workflow that's individually secure at each step but exploitable in sequence.
- **Race conditions** — TOCTOU bugs, double-spend on concurrent requests.
- **Runtime and infra config** — actual deployed headers, WAF rules, network segmentation, IAM policies.
- **Dependency CVEs** — run `npm audit`, `pip-audit`, or Dependabot; this skill reads your code, not the advisory database.
- **Anything requiring execution** — auth bypass proven only by sending real requests.

Recommend a real penetration test before handling payments, health data, or anything regulated.


## References

- `references/secrets-and-env.md` — API keys, client-side env prefixes, `.gitignore`, detection patterns.
- `references/database-security.md` — Supabase RLS, Firebase Security Rules, Convex auth.
- `references/authentication.md` — JWT, middleware, Server Actions, sessions, password storage.
- `references/access-control.md` — IDOR, ownership verification, privilege escalation, mass assignment, GraphQL.
- `references/injection.md` — SQL injection, ORM misuse, XSS, XXE, path traversal, input validation.
- `references/ssrf-and-redirects.md` — SSRF with bypass tables, open redirect, CSRF.
- `references/file-uploads.md` — magic bytes, upload bypasses, secure storage and serving.
- `references/payments.md` — Stripe price validation, webhook signatures, subscription state.
- `references/ai-integration.md` — LLM key protection, spend caps, prompt injection, tool calling.
- `references/mobile.md` — React Native / Expo secure storage, backend proxy, deep links, biometrics.
- `references/rate-limiting.md` — where limits are required, tamper-proof counters, billing protection.
- `references/deployment.md` — headers, CORS, production config, environment separation, dependencies.


## Credits

Merged from three open-source projects, each contributing its strongest part:

- **[VibeSec-Skill](https://github.com/BehiSecc/VibeSec-Skill)** (Apache-2.0) — depth on SSRF, XXE, open redirect, file uploads, CSRF, path traversal, and the bypass tables.
- **[vibe-security-skill](https://github.com/raroque/vibe-security-skill)** (MIT, Chris Raroque) — skill architecture, progressive reference loading, and the AI/LLM, mobile, Supabase RLS, and payments material.
- **[vibe-check](https://github.com/benavlabs/vibe-check)** (MIT, Benav Labs) — the investigate → report → plan → implement → verify process, machine-checkable verification goals, and the `AGENTS.md` rules format.
