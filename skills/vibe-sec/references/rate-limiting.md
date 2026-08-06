# Rate Limiting & Abuse Prevention

Missing rate limits rarely leak data directly — they enable brute force, drain budgets, and let one user deny service to everyone else. AI assistants almost never add them unasked.

## Where Limits Are Required

- **Auth endpoints** — login, register, password reset, OTP, magic link. Without limits, passwords get brute-forced and accounts enumerated.
- **AI API calls** — one user can consume your entire monthly budget in minutes. See `ai-integration.md`.
- **Email / SMS sending** — otherwise your app becomes a spam relay and your domain reputation dies.
- **File processing** — upload, resize, transcode. CPU-heavy work without limits is a DoS button.
- **Search and report generation** — expensive queries are an amplification vector.
- **Any endpoint accepting external input at scale** — webhooks, public APIs.

## Counters Must Be Tamper-Proof

If rate limit state lives somewhere the user can write, they reset it themselves. A counter in a Supabase public table is editable through the REST API by the very user being limited.

Use:

- **Upstash Redis** — serverless, with rate limiting primitives built in
- **A private schema table** not exposed via PostgREST
- **Edge or API gateway limiting** — Cloudflare, Vercel, your load balancer
- **In-memory** — acceptable for a single server; breaks across replicas, since each holds its own count

## Combine Per-IP and Per-User

- IP-only is defeated by rotating IPs — trivial with a VPN or a botnet
- User-only is defeated by registering new accounts
- Use both, plus a global cap on expensive operations

Be careful with `X-Forwarded-For`: it's client-supplied and spoofable unless you're behind a trusted proxy that overwrites it. Limiting on a forged header means the attacker picks their own bucket, and can also lock out other users by claiming their IP.

## Implementation

```typescript
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '1 m'),
});

export async function POST(request: Request) {
  const ip = request.headers.get('x-forwarded-for') ?? '127.0.0.1';
  const { success } = await ratelimit.limit(ip);
  if (!success) {
    return new Response('Too many requests', { status: 429 });
  }
  // ... handle request
}
```

Return **429** with a `Retry-After` header. Sliding window beats fixed window, which allows a double burst across the boundary.

## Auth-Specific Measures

- Progressive delay or lockout after repeated failures, keyed on the account as well as the IP
- **Constant-time responses** for login regardless of whether the user exists — timing differences enumerate accounts just as effectively as different error messages
- Identical error text for "no such user" and "wrong password"
- CAPTCHA after a failure threshold, not on the first attempt
- Rate limit password reset requests per email address, or it becomes an email-bombing tool

## Billing Protection

- Billing alerts on every provider — AWS, GCP, Vercel, OpenAI, Anthropic
- **Hard spending caps** where offered, not just alerts
- Per-user quotas with enforcement, not soft warnings
- Monitor for spikes and off-hours traffic

Alerts tell you after the money is gone. Caps stop it.

## Verification Goals

- Login, registration, and password reset are rate limited
- AI and other expensive endpoints are rate limited
- Counters live in storage the user cannot modify
- Both per-IP and per-user limits applied
- `X-Forwarded-For` trusted only behind a verified proxy
- 429 returned with `Retry-After`
- Login responses are identical for unknown user and wrong password
- Provider spending caps configured, not only alerts
