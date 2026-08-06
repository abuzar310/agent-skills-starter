# Injection

Every injection class shares one root cause: untrusted data crossing into an interpreter — SQL, HTML, XML, or the filesystem — without being separated from the instructions.

## SQL Injection

Parameterize. Always.

```typescript
// BAD
const result = await db.query(`SELECT * FROM users WHERE id = '${userId}'`);

// GOOD
const result = await db.query('SELECT * FROM users WHERE id = $1', [userId]);
```

Parameterization handles values, not identifiers. Table and column names can't be parameterized — if they come from user input, validate against a hardcoded allowlist:

```typescript
const SORTABLE = ['created_at', 'name', 'price'];
if (!SORTABLE.includes(sortColumn)) throw new Error('Invalid sort');
const result = await db.query(`SELECT * FROM items ORDER BY ${sortColumn}`);
```

## ORM Misuse

An ORM is not automatic protection.

**Operator injection (Prisma, Mongoose):** passing an unvalidated object as a filter lets the attacker supply operators instead of values.

```typescript
// BAD: attacker sends { "email": { "contains": "" } } and matches every record
const user = await prisma.user.findFirst({ where: req.body });

// GOOD
const schema = z.object({ email: z.string().email() });
const parsed = schema.parse(req.body);
const user = await prisma.user.findFirst({ where: { email: parsed.email } });
```

**Raw escape hatches:** `$queryRawUnsafe` and `$executeRawUnsafe` bypass parameterization completely.

```typescript
// BAD
await prisma.$queryRawUnsafe(`SELECT * FROM users WHERE name = '${name}'`);

// GOOD — tagged template parameterizes automatically
await prisma.$queryRaw`SELECT * FROM users WHERE name = ${name}`;
```

NoSQL injection follows the same shape: `db.users.find({ username: req.body.username })` where the body sends `{"$ne": null}`.

## Cross-Site Scripting

Every user-controllable input must be encoded for the context it lands in.

**Direct inputs:** form fields, search queries, uploaded filenames, rich text editors.

**Indirect inputs, routinely missed:** URL parameters and query strings, URL fragments, HTTP headers you display (Referer, User-Agent), data from third-party APIs, WebSocket messages, `postMessage` from iframes, localStorage values rendered into the page, and LLM output.

### Framework Escape Hatches

React, Vue, Svelte, and Angular escape by default. These opt out:

| Framework | Dangerous API |
|---|---|
| React | `dangerouslySetInnerHTML` |
| Vue | `v-html` |
| Angular | `bypassSecurityTrustHtml` |
| Svelte | `{@html ...}` |
| Vanilla | `innerHTML`, `outerHTML`, `document.write`, `eval` |

If you must render user HTML, sanitize with **DOMPurify** first. Configure an allowlist of tags and attributes — the default config is permissive.

```typescript
import DOMPurify from 'dompurify';
const clean = DOMPurify.sanitize(userHtml, {
  ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br'],
  ALLOWED_ATTR: ['href'],
});
```

### Context Matters

Escaping is context-specific. HTML-escaping a value that lands in a JavaScript string or a URL attribute doesn't protect it.

- **HTML body** — HTML entity encoding
- **HTML attribute** — attribute encoding, always quote the attribute
- **JavaScript** — never interpolate user data into a script block; pass it via `JSON.parse` from a data attribute
- **URL** — `encodeURIComponent`, and validate the scheme (`javascript:` and `data:` are XSS vectors in `href`)
- **CSS** — avoid user input in styles entirely

### Defense in Depth

A Content-Security-Policy limits the damage of an XSS you missed. See `deployment.md`.

## XXE — XML External Entity

XML parsers that resolve external entities let an attacker read local files, reach internal services, or hang the process.

**Where XML shows up unexpectedly:** DOCX/XLSX/PPTX (ZIP-wrapped XML), SVG uploads, SAML assertions, RSS/Atom feeds, SOAP APIs, PDF with XFA forms, and JSON silently converted to XML server-side.

```python
# Python — use defusedxml, or disable resolution explicitly
from lxml import etree
parser = etree.XMLParser(resolve_entities=False, no_network=True)
```

```java
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
dbf.setExpandEntityReferences(false);
```

```csharp
XmlReaderSettings settings = new XmlReaderSettings();
settings.DtdProcessing = DtdProcessing.Prohibit;
settings.XmlResolver = null;
```

```php
libxml_disable_entity_loader(true);
```

Node.js: prefer parsers that disable DTD by default; with libxmljs set `{ noent: false, dtdload: false }`.

Checklist: disable DTD processing entirely if you can, disable external entity resolution, disable external DTD loading, disable XInclude, keep the parser patched, and prefer JSON over XML where the choice is yours.

## Path Traversal

User input controlling a file path lets `../../../etc/passwd` escape the intended directory.

```python
# VULNERABLE
file_path = "/uploads/" + user_input
template = "templates/" + user_provided_template
```

**Best fix — indirect references.** Never let user input touch the path:

```python
FILES = {'report': '/reports/q1.pdf', 'invoice': '/invoices/2024.pdf'}
file_path = FILES.get(user_input)   # None if invalid
```

**If you must build a path**, canonicalize and then verify containment:

```python
import os

def safe_join(base_directory, user_path):
    base = os.path.realpath(base_directory)
    target = os.path.realpath(os.path.join(base, user_path))
    if not target.startswith(base + os.sep):
        raise ValueError("Path traversal attempt")
    return target
```

Resolve **before** checking — `realpath` collapses `..` and follows symlinks. Checking the raw string first misses both. Strip null bytes; some runtimes truncate paths there. Watch encoded variants: `%2e%2e%2f`, `..%252f`, `..\\` on Windows.

The same containment rule applies to archive extraction — a ZIP entry named `../../etc/cron.d/x` is Zip Slip.

## Command Injection

Never build a shell command from user input.

```javascript
// BAD
exec(`convert ${filename} output.png`);

// GOOD — argument array, no shell
execFile('convert', [filename, 'output.png']);
```

Use the array form so there's no shell to inject into. If a shell is unavoidable, validate against a strict allowlist — quoting and escaping are error-prone.

## Insecure Deserialization

Never deserialize untrusted data with a format that can construct arbitrary objects: Python `pickle`, PHP `unserialize`, Java native serialization, Ruby `Marshal`. These grant remote code execution by design.

Use JSON for all network data exchange, and validate the parsed result against a schema.

## Input Validation

Validate all external input at the boundary with a **runtime** schema validator — Zod, Yup, Joi, Pydantic.

TypeScript types provide zero runtime protection. They're erased at compile time; a malformed request bypasses every one of them.

```typescript
// A type checks nothing at runtime
type CreateUserInput = { name: string; email: string };

// A schema actually validates
const CreateUserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
});
```

Boundaries: API route handlers, Server Actions, webhook handlers, form submissions, URL and query parameters, and anything read from a message queue.

## Verification Goals

- No string concatenation into SQL anywhere
- No `$queryRawUnsafe` / `$executeRawUnsafe` with user input
- Request bodies validated by a runtime schema before reaching an ORM filter
- Every `dangerouslySetInnerHTML` / `v-html` / `innerHTML` either takes no user content or is DOMPurify-sanitized
- XML parsers have DTD and external entity resolution disabled
- No user input concatenated into a filesystem path without canonicalize-then-verify
- No `exec` with an interpolated string; `execFile` with an argument array instead
- No `pickle` / `unserialize` / `Marshal` on network data
- Every API boundary validates with a runtime schema
