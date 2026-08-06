# Authentication

Authentication answers "who is this?" Authorization answers "may they do this?" This file covers the first. See `access-control.md` for the second — and note that having one without the other is the single most common vulnerability in AI-generated code.

## JWT Handling

- **Use `jwt.verify()`, never `jwt.decode()` alone.** `decode` reads the payload without checking the signature — an attacker forges any claim they like.
- **Explicitly reject `"alg": "none"`.** Some libraries accept unsigned tokens when the header says so.
- **Validate issuer, audience, and expiration**, not just the signature.
- **Don't put secrets in the payload.** JWTs are base64, not encrypted — anyone can read the contents.

```typescript
// BAD: reads the token without verifying anything
const payload = jwt.decode(token);

// GOOD
const payload = jwt.verify(token, secret, {
  algorithms: ['HS256'],   // pin the algorithm; don't accept whatever the token claims
  issuer: 'your-app',
  audience: 'your-api',
});
```

Revocation: JWTs are valid until they expire. Logout does not invalidate them. Use short-lived access tokens with refresh tokens, or maintain a revocation list. When a user is removed from an org or an account is deleted, existing tokens keep working unless you handle this explicitly.

## Middleware Is Not Enough

Next.js middleware runs at the edge and is convenient, but it is **not a sufficient sole auth layer**. CVE-2025-29927 showed it could be bypassed entirely with a spoofed `x-middleware-subrequest` header.

Verify auth again in:
- Server Actions
- Route Handlers (`app/api/`)
- Data access functions

Middleware is a convenience layer, not the only wall between an attacker and your data.

Ordering matters everywhere: auth middleware must run **before** the handler, not as the first line inside it. A handler that checks auth internally will leak whatever runs before the check.

## Server Actions Are Public Endpoints

Server Actions compile to public POST endpoints. Anyone can call them with curl. AI assistants generate them as if only the UI can.

```typescript
// BAD: no auth, no validation — anyone deletes anything
'use server';
export async function deleteItem(id: string) {
  await db.items.delete({ where: { id } });
}

// GOOD
'use server';
export async function deleteItem(input: unknown) {
  const parsed = schema.safeParse(input);
  if (!parsed.success) return { error: 'Invalid input' };

  const session = await auth();
  if (!session?.user) redirect('/login');

  // Authorize, not just authenticate — scope the delete to the owner
  await db.items.deleteMany({
    where: { id: parsed.data.id, userId: session.user.id }
  });
}
```

Every Server Action needs three things at the top: **input validation**, **authentication**, **authorization**. Same applies to every `app/api/` route handler.

## Session & Token Storage

- Store tokens in `HttpOnly + Secure + SameSite=Lax` cookies, **not localStorage**.
- localStorage is readable by any JavaScript on the page — one XSS exposes every token.
- `HttpOnly` cookies are invisible to JavaScript and sent automatically.

```typescript
cookies().set('session', token, {
  httpOnly: true,
  secure: true,
  sameSite: 'lax',
  path: '/',
  maxAge: 60 * 60 * 24 * 7,
});
```

Regenerate the session identifier on login to prevent session fixation.

## Data Leakage to Client Components

Never pass whole database objects to Client Components — they carry hashed passwords, internal IDs, and admin flags.

```typescript
// BAD: every field crosses to the client
const user = await db.users.findUnique({ where: { id } });
return <UserProfile user={user} />;

// GOOD
const user = await db.users.findUnique({
  where: { id },
  select: { name: true, avatarUrl: true }
});
```

Put `import 'server-only'` at the top of data access modules so they can't be pulled into a Client Component by accident.

## Password Storage

- Use **Argon2id**, **bcrypt**, or **scrypt**. Never MD5, SHA1, or plain SHA256 — they're built for speed, which is exactly wrong here.
- Minimum 8 characters, 12+ recommended. No maximum below ~128. Allow every character including spaces and unicode.
- Don't mandate character classes — length beats complexity rules, and rules push users toward `Password1!`.
- Check candidate passwords against a breach corpus (Have I Been Pwned's k-anonymity API) rather than inventing composition rules.
- Password reset tokens: single-use, short-lived, cryptographically random, invalidated after use.

## Account Lifecycle

- Removing a user from an organization must revoke their tokens and sessions immediately.
- Deleting or deactivating an account must invalidate all sessions and API keys.
- Any privilege change should force re-validation — a demoted admin holding a valid token is still an admin until it expires.

## Verification Goals

- No call to `jwt.decode()` on an untrusted token anywhere in the codebase
- Every protected route has auth middleware running before the handler
- Unauthenticated requests to protected routes return 401
- Every Server Action validates input and checks a session
- Session cookies set `httpOnly`, `secure`, and `sameSite`
- No tokens in localStorage
- Passwords hashed with Argon2id, bcrypt, or scrypt
- Session ID regenerates on login
