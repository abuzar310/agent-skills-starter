# Deployment & Configuration

Code can be sound and still ship a compromised application. These are the settings that leak source, credentials, and internals.

## Production Configuration

- **Disable debug mode.** Debug pages leak stack traces, environment variables, and internal paths. Django `DEBUG=True` and Flask debug mode in production are full disclosure — Werkzeug's debugger offers a remote console.
- **Disable source maps**, or restrict them to an error-tracking service. A public `.map` file hands over your entire original source.
- **Verify `.git` isn't served.** If `https://yoursite.com/.git/HEAD` returns content, your full source and commit history — including every secret ever committed — is downloadable.
- **Disable directory listing.**
- **Remove version-disclosing headers** (`X-Powered-By`, verbose `Server`).

## Environment Separation

| Environment | Keys |
|---|---|
| Production | Live keys, real data |
| Preview | Test/staging keys only |
| Development | Local/test keys |

Preview deployments are frequently reachable by anyone with the URL and are often unindexed rather than protected. They must never carry production credentials or point at the production database.

## Security Headers

```
Content-Security-Policy: default-src 'self'; script-src 'self'
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

Set them in **one global middleware**, not per-route — per-route means the route someone adds next month has none.

- Express: `helmet`
- Next.js: `headers()` in `next.config.js`

**CSP** is the one worth effort: it's the difference between an XSS being a catastrophe and an inconvenience. Start restrictive, loosen only as needed — never the reverse. Avoid `unsafe-inline` and `unsafe-eval`; if inline scripts are unavoidable, use nonces or hashes. `X-Frame-Options` is superseded by `frame-ancestors` in CSP, but keep both for older browsers.

## CORS

```javascript
// BAD: any origin, with credentials — total bypass of same-origin protection
app.use(cors({ origin: '*', credentials: true }));

// BAD: reflects whatever the attacker sends
app.use(cors({ origin: (o, cb) => cb(null, true), credentials: true }));

// GOOD: explicit allowlist
const allowed = ['https://yourapp.com', 'https://www.yourapp.com'];
app.use(cors({
  origin: (origin, cb) => cb(null, !origin || allowed.includes(origin)),
  credentials: true,
}));
```

Rules: never `*` on authenticated endpoints. Never combine `origin: '*'` with `credentials: true` — browsers reject the pair, and code that "fixes" it by reflecting the request origin has built an open door. Match origins exactly; a `startsWith` check on `https://yourapp.com` passes `https://yourapp.com.evil.com`.

CORS is not an access control. It governs browser behaviour only — curl ignores it entirely. Authorization still happens server-side.

## Error Handling

Never return stack traces, SQL errors, file paths, library names, or version numbers in an API response. Each one hands an attacker a map.

```typescript
// BAD
catch (err) {
  return res.status(500).json({ error: err.message, stack: err.stack });
}

// GOOD — log detail internally, return a reference
catch (err) {
  logger.error({ err, requestId });
  return res.status(500).json({ error: 'Internal server error', requestId });
}
```

Log the detail server-side, return an opaque ID the user can quote to support.

## Logging

- **Never log** passwords, tokens, API keys, full card numbers, or session IDs. Logs get shipped to third parties, indexed, and read by people who shouldn't see credentials.
- Redact `Authorization` headers and cookies before logging requests.
- Do log security-relevant events: auth failures, permission denials, admin actions.

## Dependencies

- Run `npm audit`, `pip-audit`, `cargo audit`, or equivalent in CI, and fail the build on high severity
- Enable Dependabot or Renovate
- Commit lockfiles — unpinned transitive dependencies mean an unreviewed update reaches production
- Watch for typosquatting: verify unfamiliar package names before installing
- Review `postinstall` scripts in new dependencies; they execute arbitrary code at install time

## Pre-Ship Checklist

- `gitleaks detect` clean across full history
- `.env` files gitignored and untracked
- Debug mode and verbose logging off
- Source maps not publicly served
- `/.git/HEAD` returns 404
- Error responses carry no stack traces
- CORS restricted to your domains
- Security headers present on every response
- Dependency audit clean
- TLS enforced, HTTP redirects to HTTPS
- Database backups exist and restore has been tested

## Verification Goals

- `curl -I https://yoursite.com` shows all six security headers
- `curl https://yoursite.com/.git/HEAD` returns 404
- No `.map` files reachable in production
- An error-triggering request returns no stack trace
- No CORS config uses `*` with credentials
- Preview and production use separate credentials
- Dependency audit passes in CI
