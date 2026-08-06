# SSRF, Open Redirect & CSRF

Three vulnerabilities that share a theme: the application acts on a URL or a request it shouldn't trust.

---

# Server-Side Request Forgery

Your server fetches a URL the user supplied. The attacker points it at your internal network, and your server — which sits behind the firewall — makes the request for them.

## Where It Hides

- Webhooks where the user provides a callback URL
- Link previews and unfurling
- PDF and screenshot generators that take a URL
- Image or file fetching from a URL
- "Import from URL" features
- RSS and feed readers
- Integrations pointing at a user-supplied endpoint
- Proxy endpoints
- HTML-to-PDF converters

## Protection

**Allowlist is the only robust answer.** If the feature permits it, accept only pre-approved domains. Everything below is mitigation for when you genuinely can't.

**Network segmentation.** Run URL-fetching in an isolated network with no route to internal services or cloud metadata. This survives parser bugs that validation doesn't.

**Validation, if you must:**

1. Scheme is `http` or `https` — nothing else
2. Resolve DNS yourself
3. Verify every resolved IP is public
4. Pin that IP for the request
5. Don't follow redirects, or validate every hop
6. Set a timeout and cap the response size

## Bypasses to Block

Naive string checks for "127.0.0.1" or "localhost" fail against all of these:

| Technique | Example | Why it works |
|---|---|---|
| Decimal IP | `http://2130706433` | 127.0.0.1 in decimal |
| Octal IP | `http://0177.0.0.1` | Octal notation |
| Hex IP | `http://0x7f.0x0.0x0.0x1` | Hexadecimal |
| Short form | `http://127.1` | Expands to 127.0.0.1 |
| IPv6 loopback | `http://[::1]` | IPv6 localhost |
| IPv4-mapped IPv6 | `http://[::ffff:127.0.0.1]` | Mapped address |
| All zeros | `http://[::]` | Resolves to loopback |
| IPv6 scope ID | `http://[fe80::1%25eth0]` | Interface-scoped |
| DNS rebinding | TTL-0 record flips after validation | First resolve external, second internal |
| CNAME to internal | Attacker domain CNAMEs inward | DNS points at an internal host |
| Parser confusion | `http://attacker.com#@internal` | Libraries disagree on the host |
| Redirect chain | External URL 302s to internal | The redirect isn't revalidated |

**Private ranges to block:** `127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.0.0/16`, `0.0.0.0/8`, `::1`, `fc00::/7`, `fe80::/10`.

**Cloud metadata endpoints** — these hand out IAM credentials:
- AWS, Azure, DigitalOcean, GCP: `169.254.169.254`
- GCP also: `metadata.google.internal`, `http://metadata`
- Prefer IMDSv2 on AWS, which requires a token header

**DNS rebinding defense:** resolve, validate the IP, then connect to *that IP* while passing the hostname in the `Host` header. Re-resolving between validation and connection is exactly the window the attack uses.

---

# Open Redirect

An endpoint that redirects to a user-supplied URL. Used for convincing phishing — the link genuinely starts with your domain — and to steal OAuth tokens through a redirect chain.

## Protection

1. **Relative paths only.** Accept `/dashboard`, not a full URL. Require a leading `/` and reject anything starting `//` or `/\`.
2. **Allowlist** of exact hostnames, compared after parsing — never with `startsWith` or a regex on the raw string.
3. **Indirect references.** `?redirect=dashboard` looked up in a server-side map.

## Bypasses to Block

| Technique | Example | Why it works |
|---|---|---|
| `@` as userinfo | `https://legit.com@evil.com` | Everything before `@` is a username |
| Subdomain lookalike | `https://legit.com.evil.com` | Attacker owns that subdomain |
| Protocol-relative | `//evil.com` | Inherits the current scheme |
| Backslash | `https://legit.com\@evil.com` | Some parsers normalize `\` to `/` |
| Double encoding | `%252f%252fevil.com` | Becomes `//evil.com` after two decodes |
| Null byte | `https://legit.com%00.evil.com` | Some parsers truncate at null |
| Tab / newline | `https://legit.com%09.evil.com` | Whitespace splits the host |
| Fragment | `https://legit.com#@evil.com` | Parsers disagree on where the host ends |
| `javascript:` | `javascript:alert(1)` | XSS through the redirect |
| `data:` URL | `data:text/html,<script>…` | Payload executes directly |
| IDN homograph | `https://legіt.com` (Cyrillic і) | Visually identical domain |

**IDN defense:** convert to Punycode before validating, and consider rejecting non-ASCII hostnames outright for redirect targets.

Validate with a real URL parser, then compare the parsed `hostname` against your allowlist. String matching on the raw input loses to at least four rows of that table.

---

# Cross-Site Request Forgery

Another site causes the user's browser to send an authenticated request to yours. The browser attaches cookies automatically, so the request looks legitimate.

## What Needs Protection

**Authenticated state changes:** all POST, PUT, PATCH, DELETE. Any GET that changes state — and fix those to use a proper method. File uploads, settings changes, payment endpoints.

**Pre-authentication endpoints, commonly forgotten:** login (login CSRF logs a victim into the attacker's account), signup, password reset request, password change, email/phone verification, OAuth callbacks.

## Mechanisms

**SameSite cookies** — first line, but not sufficient alone.

```
Set-Cookie: session=abc123; SameSite=Lax; Secure; HttpOnly
```

`Strict` never sends cross-site, which breaks inbound links. `Lax` sends on top-level GET navigation and is the usual balance. Browsers increasingly default to `Lax`, but don't rely on a default you didn't set.

**CSRF tokens** — cryptographically random, tied to the session, validated on every state-changing request, regenerated after login.

**Double-submit cookie** — token in both a cookie and a header, server confirms they match. Useful when you have no server-side session store.

## Common Mistakes

- **Validating only when the token is present.** Missing token must mean rejected, not skipped. This is the single most frequent CSRF bug.
- **Assuming JSON content-type is protection.** It raises the bar but isn't a control. Validate `Origin`/`Referer` *and* use tokens.
- **Permissive CORS undoing SameSite.** An overly broad CORS policy reopens what SameSite closed. See `deployment.md`.
- **Tokens in URLs.** They leak via Referer, browser history, and server logs. Use a custom header — `X-CSRF-Token`.
- **Subdomain scope.** A subdomain takeover becomes a CSRF vector; scope cookies and tokens deliberately.
- **State-changing GETs.** Never. A prefetch or an `<img>` tag triggers them.

---

## Verification Goals

**SSRF**
- Scheme restricted to http/https
- Hostname resolved and the IP checked against private ranges before connecting
- Cloud metadata IPs explicitly blocked
- Redirects disabled, or each hop revalidated
- Request timeout and response size cap in place

**Open redirect**
- Redirect targets are relative paths, or hostnames matched against an allowlist after parsing
- `//`, `\`, `javascript:`, and `data:` all rejected
- Non-ASCII hostnames punycoded before comparison

**CSRF**
- Every state-changing endpoint validates a token
- A missing token is rejected, not bypassed
- Token is random, session-bound, and regenerated on login
- Session cookies set `SameSite`, `Secure`, `HttpOnly`
- No state changes on GET
- No token in a URL
