# Security Rules

Drop this file into a project root so these constraints apply to all generated code. They are non-negotiable.

## Secrets

- NEVER put API keys, database credentials, or tokens in frontend code (anything under `src/`, `app/`, `pages/`, `components/`, `public/`)
- NEVER put secret keys in env vars prefixed `NEXT_PUBLIC_`, `VITE_`, `REACT_APP_`, or `EXPO_PUBLIC_` — these are bundled into the client
- NEVER hardcode credentials in source. Use environment variables loaded server-side only
- `.env` MUST be in `.gitignore` before the first commit. Verify this before creating any `.env` file
- `.env.example` holds placeholder values only, never real credentials
- A secret that reached git history is compromised. Rotate it — deleting the file is not enough

## Database

- Enable Row Level Security on EVERY Supabase table before deployment. Default deny; write explicit policies scoped to `auth.uid()`
- NEVER write an RLS policy using `USING (true)` or `USING (auth.uid() IS NOT NULL)` for SELECT/UPDATE/DELETE
- ALWAYS include `WITH CHECK` on INSERT and UPDATE policies, or users can reassign row ownership
- Firebase rules MUST require `request.auth != null` AND scope to `request.auth.uid`. Bare `request.auth != null` is not access control
- Firebase subcollections are NOT covered by parent rules — each needs its own
- Supabase storage buckets need policies scoped to the owner's UID folder
- Convex: every public `query`/`mutation` calls `ctx.auth.getUserIdentity()`; internal-only functions use `internalQuery`/`internalMutation`

## Authentication and Authorization

- EVERY API route returning or modifying user data MUST have auth middleware running BEFORE the handler, not inside it
- Unauthenticated requests to protected endpoints MUST return 401
- EVERY route taking a resource ID MUST verify the authenticated user owns it: `current_user.id == resource.owner_id`. This is a SEPARATE check from authentication
- Put the ownership condition INSIDE the database query, not in a comparison afterwards
- Return 404, not 403, for resources the user doesn't own — 403 confirms existence and enables enumeration
- Admin endpoints MUST verify the admin role server-side and return 403 otherwise
- NEVER decide a role from a client-supplied value or a stale JWT claim. Read it from the database
- Session cookies MUST set `httpOnly: true`, `secure: true`, `sameSite: 'lax'`
- NEVER store auth tokens in localStorage
- Use `jwt.verify()`, never `jwt.decode()`, and pin the algorithm
- Next.js middleware is NOT sufficient alone (CVE-2025-29927). Re-verify in Server Actions, route handlers, and data access
- Every Server Action starts with: input validation, authentication, authorization
- Hash passwords with Argon2id, bcrypt, or scrypt. Never MD5, SHA1, or plain SHA256

## Input and Output

- NEVER concatenate user input into SQL. ALWAYS use parameterized queries or ORM methods
- NEVER pass an unvalidated request body as an ORM filter — validate with Zod first, or an attacker sends operators instead of values
- NEVER use `$queryRawUnsafe` or `$executeRawUnsafe` with user input
- NEVER use `dangerouslySetInnerHTML`, `v-html`, `{@html}`, or `innerHTML` with user content unless sanitized with DOMPurify
- ALL user input MUST be validated server-side with a runtime schema. TypeScript types do not exist at runtime
- NEVER spread a request body into a database write — allowlist the fields
- NEVER build a shell command by string interpolation. Use `execFile` with an argument array
- NEVER use `pickle`, `unserialize`, `Marshal`, or Java native deserialization on network data. Use JSON
- XML parsers MUST disable DTD processing and external entity resolution
- File paths from user input MUST be canonicalized and verified to stay inside the base directory

## File Uploads

- Validate file type by reading magic bytes, NOT the extension or `Content-Type` header
- Rename every upload to a UUID server-side; discard the original filename
- Store uploads on a separate domain (S3, R2, GCS), never the app origin
- Enforce size limits server-side
- SVG uploads must be sanitized, rasterized, or rejected — SVG executes JavaScript
- Validate extracted archive paths stay within the target directory (Zip Slip)

## URL Fetching (SSRF)

If the app fetches user-supplied URLs — link previews, image proxies, webhooks, PDF generation — it MUST:

- Allow only `http` and `https` schemes
- Resolve the hostname and check the IP BEFORE connecting
- Block private ranges: `127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.0.0/16`, `::1`, `fc00::/7`, `fe80::/10`
- Block cloud metadata: `169.254.169.254`, `metadata.google.internal`
- Disable redirect following, or revalidate every hop
- Set a timeout and a response size cap

Prefer an allowlist of permitted domains over blocklist validation.

## Redirects

- Accept relative paths only, or match hostnames against an allowlist AFTER parsing with a real URL parser
- Reject `//`, `\`, `javascript:`, and `data:` targets
- Never validate redirect targets with `startsWith` on the raw string

## Security Headers

Set on ALL responses via one global middleware:

```
Content-Security-Policy: default-src 'self'
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
```

Express: use `helmet`. Next.js: set them in `next.config.js`.

## CORS

- NEVER set CORS origin to `*` on authenticated endpoints
- NEVER combine `origin: '*'` with `credentials: true`
- NEVER reflect the request origin back as the allowed origin
- Match allowed origins exactly — `startsWith` passes `yourapp.com.evil.com`

## Rate Limiting

- Login, registration, and password reset MUST be rate limited
- AI/LLM endpoints MUST be rate limited AND have per-user usage caps
- Rate limit counters MUST live in storage the user cannot modify — not a public Supabase table
- Do NOT trust `X-Forwarded-For` unless behind a trusted reverse proxy
- Login responses must be identical for "unknown user" and "wrong password"

## Payments

- NEVER take a price, amount, or currency from a client request. Look it up server-side
- Stripe webhooks MUST verify the signature with the RAW body on every request. Reject missing or invalid signatures
- Webhook handlers MUST deduplicate by event ID — delivery is at-least-once
- Handle the full lifecycle: `payment_intent.succeeded`, `invoice.payment_failed`, `customer.subscription.deleted`, `customer.subscription.past_due`
- Check subscription status against the database on every protected request, never from a JWT claim

## AI / LLM

- AI provider keys are server-side only. All calls proxied through the backend
- Per-user usage caps enforced in the application, plus hard spending caps at the provider
- Pass system and user content as separate messages; never interpolate user input into the system prompt
- Treat model output as untrusted input: sanitize before rendering, never execute, never pass to a shell or SQL
- Validate tool-call parameters against a schema; scope tools to the requesting user's permissions

## Mobile

- Nothing in the JS bundle is secret, including `EXPO_PUBLIC_` values and Hermes bytecode
- Use a backend proxy for any API requiring a secret key
- Store tokens in `expo-secure-store` or `react-native-keychain`. NEVER `AsyncStorage`
- Validate deep link parameters; never carry tokens in deep links
- Client-side jailbreak/root/tamper checks are friction, not security. Every check must also exist server-side

## Error Handling and Logging

- NEVER expose stack traces, SQL errors, file paths, or library names in API responses
- Log detail server-side, return an opaque request ID
- NEVER log passwords, tokens, API keys, or session IDs. Redact `Authorization` headers

## Deployment

- Disable debug mode and public source maps in production
- `/.git/` must not be reachable
- Preview deployments never use production credentials
- Run dependency audits in CI and fail on high severity
- Commit lockfiles
