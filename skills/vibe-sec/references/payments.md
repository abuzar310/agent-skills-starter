# Payment Security (Stripe)

## Never Trust Client-Submitted Prices

The most common payment bug in AI-generated apps: the amount comes from the request body. An attacker sets it to anything, including $0.

```typescript
// BAD: the client controls what they pay
const session = await stripe.checkout.sessions.create({
  line_items: [{
    price_data: {
      currency: 'usd',
      unit_amount: req.body.price,        // attacker-controlled
      product_data: { name: req.body.name },
    },
    quantity: 1,
  }],
});

// GOOD: look up the price server-side
const product = await db.products.findUnique({ where: { id: req.body.productId } });
if (!product) return new Response('Not found', { status: 404 });

const session = await stripe.checkout.sessions.create({
  line_items: [{ price: product.stripePriceId, quantity: 1 }],
});
```

Prefer Stripe Price IDs created in the dashboard over constructing amounts from your own database — the price then lives in Stripe and can't be altered by a bug on your side either.

Validate quantity too. A negative or absurd quantity can invert or overflow a total.

## Webhook Signature Verification

Without signature verification, anyone who guesses your webhook URL can POST a fake `checkout.session.completed` and unlock paid features for free.

Verification needs the **raw request body**. Parsing JSON first destroys the signature.

```typescript
// Express: raw body middleware BEFORE express.json()
app.post('/webhook', express.raw({ type: 'application/json' }), (req, res) => {
  const sig = req.headers['stripe-signature'];
  const event = stripe.webhooks.constructEvent(req.body, sig, webhookSecret);
  // ...
});

// Next.js App Router: request.text(), NOT request.json()
export async function POST(request: Request) {
  const body = await request.text();
  const sig = request.headers.get('stripe-signature')!;
  const event = stripe.webhooks.constructEvent(body, sig, webhookSecret);
  // ...
}
```

Reject any request with a missing or invalid signature. Never fall back to trusting the payload "just this once" during debugging — that fallback ships.

## Idempotency

Stripe retries webhooks on non-2xx responses, and delivery is at-least-once even on success. A handler that credits an account without deduplication will double-credit.

Store processed event IDs and skip duplicates:

```typescript
const exists = await db.processedEvents.findUnique({ where: { id: event.id } });
if (exists) return new Response('OK', { status: 200 });
await db.processedEvents.create({ data: { id: event.id } });
// ... then handle
```

Return 2xx quickly. Slow handlers cause retries, which cause duplicates.

## Subscription Status

Check status **server-side on every protected request**, against your own database kept in sync by webhooks. Do not rely on:

- A value cached in the session at login
- A client-side flag
- A JWT claim set at token creation and never refreshed

Subscriptions get cancelled, expire, fail payment, and change tier at any moment. A JWT issued this morning says "pro" all day regardless.

Handle the full lifecycle, not just the happy path:

- `checkout.session.completed`
- `payment_intent.succeeded`
- `invoice.payment_failed`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `customer.subscription.past_due`

Missing the failure events means users keep access after their card declines.

## Checkout Metadata

Metadata on a session (user ID, plan) must be set server-side when creating it. If it arrives from the client, an attacker claims a different user or a higher plan.

When the webhook fires, verify the metadata's user ID against your own records rather than trusting it to route the fulfillment.

## Verification Goals

- No price, amount, or currency read from a client request
- Webhook handlers call `constructEvent` with the raw body and reject invalid signatures
- Processed event IDs stored; duplicate deliveries are no-ops
- Subscription status read from the database on each protected request, not from a token claim
- Failure events (`payment_failed`, `subscription.deleted`, `past_due`) all handled
- Checkout metadata set server-side only
- Webhook secret and Stripe secret key are server-side environment variables
