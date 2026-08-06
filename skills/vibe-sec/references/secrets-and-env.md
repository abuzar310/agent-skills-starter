# Secrets & Environment Variables

## Hardcoded Credentials

Never hardcode API keys, tokens, passwords, or credentials in source. This includes:

- Strings that look like API keys in source files
- Connection strings with embedded passwords (`postgresql://user:password@host`)
- Private keys or certificates committed to the repo

**If a secret was ever committed to git, it is compromised.** Deleting the file does not remove it from history. The key must be rotated. Run `gitleaks detect` to scan history.

## Client-Side Environment Variable Prefixes

These prefixes inline env vars into the client bundle at build time. Everything in the bundle is public.

| Framework | Client prefix | What happens |
|-----------|--------------|--------------|
| Next.js | `NEXT_PUBLIC_` | Inlined into browser JS at build time |
| Vite | `VITE_` | Inlined into browser JS at build time |
| Expo / React Native | `EXPO_PUBLIC_` | Baked into the app bundle |
| Create React App | `REACT_APP_` | Inlined into browser JS at build time |

**Safe client-side:**
- Stripe publishable key (`pk_live_*`, `pk_test_*`)
- Supabase anon key
- Firebase client config (apiKey, authDomain, projectId)
- Public analytics IDs

**Never client-side:**
- Supabase `service_role` key — bypasses all RLS
- Stripe secret key (`sk_live_*`, `sk_test_*`)
- Any database connection string
- Any third-party API secret
- JWT signing secrets
- OAuth client secrets

The Firebase `apiKey` genuinely is public — it's an identifier, not a credential. Firebase security comes from Security Rules, not from hiding that key. Don't flag it; check the rules instead.

## .gitignore

`.env`, `.env.local`, `.env.*.local`, and any secret-bearing file must be gitignored **before the first commit**. `.env.example` should contain placeholders only.

## Detection Patterns

When auditing, search for:

- `git ls-files | grep -i env` — env files tracked by git
- Key prefixes: `sk_live_`, `sk_test_`, `AKIA`, `ghp_`, `glpat-`, `xoxb-`, `Bearer `, `-----BEGIN`
- `process.env.NEXT_PUBLIC_` or `import.meta.env.VITE_` referencing anything named secret / private / service / key
- Long alphanumeric literals assigned to variables in frontend code
- URLs containing credentials

## Verification Goals

- `git ls-files .env` returns nothing
- Grep for the secret patterns above across all source returns nothing
- No `NEXT_PUBLIC_` / `VITE_` / `REACT_APP_` / `EXPO_PUBLIC_` var holds a secret key
- `.env.example` exists with placeholder values only
- `gitleaks detect` passes clean
