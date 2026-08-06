# Database Access Control

The #1 source of critical vulnerabilities in AI-generated apps. Assistants routinely produce schemas with no access control, leaving entire tables readable and writable by anyone holding a public key.

## Supabase Row-Level Security

### Enable RLS on Every Table

Tables created via the SQL Editor or migrations have RLS **disabled by default**. A table without RLS is fully readable and writable by anyone with the anon key — which ships in your client bundle.

```sql
DO $$ DECLARE r RECORD;
BEGIN
  FOR r IN SELECT tablename FROM pg_tables WHERE schemaname = 'public'
  LOOP
    EXECUTE format('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY;', r.tablename);
  END LOOP;
END $$;
```

### Dangerous Policies

Never use `USING (true)` or `USING (auth.uid() IS NOT NULL)` on SELECT/UPDATE/DELETE. Both let any authenticated user reach every row.

```sql
-- BAD: any logged-in user reads all rows
CREATE POLICY "Users can view data" ON public.documents
  FOR SELECT TO authenticated USING (true);

-- BAD: same problem, just less obvious
CREATE POLICY "Users can view data" ON public.documents
  FOR SELECT TO authenticated USING (auth.uid() IS NOT NULL);

-- GOOD: scoped to the owner
CREATE POLICY "Users can view own data" ON public.documents
  FOR SELECT TO authenticated USING ((SELECT auth.uid()) = user_id);
```

### Missing WITH CHECK

Always include `WITH CHECK` on INSERT and UPDATE. Without it a user can reassign row ownership or insert rows as someone else.

```sql
-- BAD: user can UPDATE user_id to another person's ID
CREATE POLICY "Users can update tasks" ON public.tasks
  FOR UPDATE TO authenticated USING ((SELECT auth.uid()) = user_id);

-- GOOD
CREATE POLICY "Users can update tasks" ON public.tasks
  FOR UPDATE TO authenticated
  USING ((SELECT auth.uid()) = user_id)
  WITH CHECK ((SELECT auth.uid()) = user_id);
```

### Sensitive Fields on User-Writable Tables

If users can UPDATE their own `profiles` row, they can set `is_admin = true`, `credits = 99999`, or `subscription_tier = 'enterprise'`.

- **Option A** — move sensitive fields to a `private` schema table not exposed via PostgREST; access via `SECURITY DEFINER` functions.
- **Option B** — column-level privileges:
  ```sql
  REVOKE UPDATE ON profiles FROM authenticated;
  GRANT UPDATE (display_name, avatar_url) ON profiles TO authenticated;
  ```

### Forgotten Related Tables

Junction tables, audit logs, and metadata tables routinely lack RLS even when the main table has it. Every table exposed via the REST API needs its own policies. A table with RLS enabled but zero policies blocks all access — safe, but it will look like a mysterious bug.

### SECURITY DEFINER Functions

These bypass RLS entirely, and in the `public` schema they're callable by anyone via REST. Always keep them in a `private` schema, set `SET search_path = ''`, and validate inputs inside the function.

### Storage Buckets

Buckets need their own policies or any authenticated user can read, overwrite, or delete any file.

```sql
CREATE POLICY "Users upload to own folder"
  ON storage.objects FOR INSERT TO authenticated
  WITH CHECK (
    bucket_id = 'avatars'
    AND (storage.foldername(name))[1] = (SELECT auth.uid())::TEXT
  );
```

## Firebase Security Rules

### Never Ship the Defaults

```javascript
// BAD: world readable and writable
allow read, write: if true;

// BAD: any logged-in user reaches everything
allow read, write: if request.auth != null;

// GOOD
allow read, write: if request.auth.uid == userId;
```

### Field-Level Protection

Without restricting modifiable fields, users set `isAdmin: true` on themselves.

```javascript
allow update: if request.auth.uid == userId
  && request.resource.data.diff(resource.data)
     .affectedKeys()
     .hasOnly(['displayName', 'avatarUrl']);
```

### The Subcollection Trap

Subcollections are **not** covered by parent rules. Each needs explicit rules. AI assistants miss this constantly.

### Validation and Roles

```javascript
// Type and size validation
allow create: if request.resource.data.displayName is string
  && request.resource.data.displayName.size() <= 50;

// Server timestamps
allow create: if request.resource.data.createdAt == request.time;
```

Use custom claims (`request.auth.token.role`) for roles rather than reading a users document — claims can't be tampered with and cost no extra read.

Cloud Storage rules must validate `contentType`, `size`, and path ownership, or users upload executables into other users' folders.

## Convex

- Every public `query` and `mutation` must call `ctx.auth.getUserIdentity()` and handle the unauthenticated case.
- Mutations must verify ownership — authentication alone is not enough.
- Internal-only functions must use `internalQuery` / `internalMutation` / `internalAction`. Anything declared `query` or `mutation` is publicly callable.

## Verification Goals

- Every table has RLS enabled
- Every table has explicit policies scoped to `auth.uid()`
- No policy uses `USING (true)` without a further condition
- Every INSERT/UPDATE policy has `WITH CHECK`
- A curl request carrying only the anon key returns empty or 403 for every table
- Storage buckets have ownership-scoped policies
- Firebase: no rule uses `if true` or bare `request.auth != null`
- Every subcollection has its own rules
