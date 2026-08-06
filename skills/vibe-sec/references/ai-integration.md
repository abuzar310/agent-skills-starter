# AI / LLM Integration Security

## API Keys Are Server-Side Only

An LLM API key in client code allows unlimited usage at your expense. Leaked keys get scraped from public bundles within hours and can burn thousands of dollars overnight.

- No `NEXT_PUBLIC_OPENAI_API_KEY`
- No keys in React Native or Expo bundles
- No keys in any client-side JavaScript

Every AI call goes through your backend: the client sends the message to your server, your server calls the provider.

## Spending Caps

Provider-side, set hard limits — OpenAI usage limits, Anthropic spending limits, Google Cloud budget alerts. These lag, so don't rely on them alone.

Application-side, enforce your own:

- Track token usage per user in your database
- Daily and monthly caps per user or per tier
- Return a clear error at the limit rather than silently failing
- Alert on anomalous spikes

Without per-user caps, one account can consume your entire budget. Rate limiting is complementary but not the same thing — ten requests a minute of 100k-token prompts is still ruinous. See `rate-limiting.md`.

## Prompt Injection

User input reaching a prompt can override your instructions. Structural separation is the baseline:

```typescript
// BAD: user text can rewrite the system instruction
const prompt = `You are a helpful assistant. User says: ${userInput}`;

// BETTER: separate roles
const messages = [
  { role: 'system', content: 'You are a helpful assistant.' },
  { role: 'user', content: userInput },
];
```

Be clear-eyed: **role separation reduces but does not eliminate prompt injection.** There is no complete fix today. Design so a successful injection isn't catastrophic:

- Limit what the model can do — no tool access for open user-facing chat
- Validate output before acting on it
- Require human confirmation for consequential actions
- Never let the model's output alone authorize anything

**Indirect injection** is the underrated variant: the model reads a web page, a PDF, an email, or a database row containing instructions. Any content the model ingests is untrusted input, not just what the user typed.

## LLM Output Is Untrusted

Treat responses exactly like user input:

- **Sanitize before rendering as HTML** — model output can contain `<script>` or event handlers, and users can induce that deliberately. See the XSS section in `injection.md`.
- **Never execute output as code** without a sandbox.
- **Never pass output into a shell, SQL query, or filesystem path.**
- **Validate function-call parameters** against a schema and an allowlist before executing.

Markdown rendering deserves care: a model can emit `[click](javascript:...)` or an image URL that exfiltrates data through the query string.

## Tool / Function Calling

When the model can invoke tools:

- Restrict to an explicit allowlist of operations
- Validate every parameter against a schema — the model can hallucinate or be steered into malformed arguments
- Least privilege: read-only where possible, scoped to the requesting user's data
- Never let the model construct raw SQL or shell commands
- Log every invocation for audit
- Confirm destructive actions with the user

The authorization rule: tools execute with the **user's** permissions, never the application's. A model that can query any row on behalf of a user who should see only their own has become an IDOR with extra steps.

## Verification Goals

- No AI provider key in any client bundle or `NEXT_PUBLIC_`/`EXPO_PUBLIC_` variable
- All AI calls proxied through the backend
- Per-user usage caps enforced in the application, not just at the provider
- Provider-side spending limits configured
- System and user content passed as separate messages
- Model output sanitized before HTML rendering
- Tool parameters schema-validated before execution
- Tools scoped to the requesting user's permissions
- Destructive tool actions require confirmation
