# Access Control

Authentication proves identity. Authorization decides permission. Code that checks only the first is the most common serious flaw in AI-generated applications: every logged-in user can reach every other user's data.

## The Core Requirement

For every data point and action behind a login:

1. **User-level ownership** — each user reaches only their own rows. Verify at the data layer, not just the route.
2. **Organization scoping** — in multi-tenant apps, check org membership, not just login.
3. **Role validation** — role-gated actions verify the role server-side, on every request.

## IDOR — Insecure Direct Object Reference

The pattern: a route takes a resource ID and fetches it without checking who's asking.

```typescript
// BAD: authenticated, but any user reads any invoice by changing the number
app.get('/api/invoices/:id', requireAuth, async (req, res) => {
  const invoice = await db.invoices.findUnique({ where: { id: req.params.id } });
  res.json(invoice);
});

// GOOD: ownership is part of the query
app.get('/api/invoices/:id', requireAuth, async (req, res) => {
  const invoice = await db.invoices.findFirst({
    where: { id: req.params.id, userId: req.user.id }
  });
  if (!invoice) return res.status(404).json({ error: 'Not found' });
  res.json(invoice);
});
```

Put the ownership condition **inside the query**. A fetch-then-compare works but invites the bug where someone later removes the comparison.

### Return 404, Not 403

Returning 403 for a resource that exists but isn't yours confirms it exists. Attackers enumerate IDs on that signal. Return 404 for both "doesn't exist" and "not yours".

```
function getResource(resourceId, currentUser):
    resource = database.find(resourceId)
    if resource is null:
        return 404
    if resource.ownerId != currentUser.id:
        if not currentUser.hasOrgAccess(resource.orgId):
            return 404          # not 403 — don't confirm existence
    return resource
```

### Check the Parent Too

Accessing a comment means verifying ownership of the post it belongs to. Nested resources need the whole chain checked, not just the leaf.

### Use Non-Guessable IDs

Sequential integer IDs make enumeration trivial — `/invoices/1`, `/invoices/2`. Use UUIDv4 or similar. This is defense in depth, not a substitute for ownership checks: a UUID that isn't checked is still an IDOR, just a slower one to find.

## Privilege Escalation

**Vertical** — a regular user reaching admin functionality. Every admin route verifies the admin role server-side and returns 403 for everyone else. Hiding the button is not access control.

**Horizontal** — user A reaching user B's resources at the same privilege level. This is IDOR above.

Never trust role information from the client — not from the request body, not from a cookie the client can edit, not from a JWT claim set at login and never rechecked. Read the role from the database or from a signed, verified token, on every request.

```typescript
// BAD: client asserts its own role
if (req.body.role === 'admin') { /* ... */ }

// BAD: JWT claim from login, possibly hours stale
if (session.user.role === 'admin') { /* ... */ }

// GOOD: authoritative lookup
const user = await db.users.findUnique({
  where: { id: session.user.id },
  select: { role: true }
});
if (user.role !== 'admin') return res.status(403).json({ error: 'Forbidden' });
```

## Mass Assignment

Spreading a request body into a database write lets an attacker set fields you never exposed.

```typescript
// BAD: attacker sends { name: "x", isAdmin: true, credits: 99999 }
await db.users.update({ where: { id }, data: req.body });

// GOOD: allowlist the fields
const { name, email } = validatedInput;
await db.users.update({ where: { id }, data: { name, email } });
```

Allowlist, never denylist — a denylist misses the field someone adds next month.

This applies to the database layer too: if a Supabase or Firebase policy lets users update their own row without column restrictions, mass assignment happens at the database and never touches your code. See `database-security.md`.

## GraphQL

GraphQL moves authorization into resolvers, and a single query can traverse the whole graph. Field-level checks are mandatory — a nested field reached through an authorized parent is not automatically authorized.

| Issue | Prevention |
|---|---|
| Introspection enabled in production | Disable it — it publishes your entire schema |
| Query depth attack | Depth limit, typically 10 levels |
| Query complexity attack | Cost analysis with an enforced maximum |
| Batching attack | Cap operations per request — batching defeats per-request rate limits |
| Field-level authorization gaps | Check permissions in each resolver, not just at the entry point |

```javascript
const server = new ApolloServer({
  introspection: process.env.NODE_ENV !== 'production',
  validationRules: [
    depthLimit(10),
    costAnalysis({ maximumCost: 1000 })
  ]
});
```

Batching deserves attention: sending 1,000 login mutations in one HTTP request bypasses rate limiting keyed on requests. Limit operations per request and count operations, not requests, when limiting auth attempts.

## Verification Goals

- Every route taking a resource ID verifies the authenticated user owns it
- Ownership checks are separate from, and additional to, authentication
- Unauthorized resource access returns 404, not 403
- Admin routes verify role server-side and return 403
- No role decision made from a client-supplied value
- No request body spread directly into a database write
- Nested resources verify the parent chain
- GraphQL: introspection disabled in production, depth and cost limits set, resolvers check field-level permissions
