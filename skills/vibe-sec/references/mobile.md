# Mobile Security (React Native / Expo)

## Nothing in the Bundle Is Secret

Every string in the JavaScript bundle is extractable — Hermes bytecode included. The bundle is a file on a device the attacker owns; they can decompile and grep it at leisure.

Not secret, despite appearances:

- `react-native-config` values — baked in at build time
- `EXPO_PUBLIC_` variables — baked in at build time
- Anything injected via `eas.json` or `app.config.js` that lands in the JS bundle
- Constants in native code — harder to reach, still reachable

The only correct pattern for third-party APIs requiring a secret: **a backend proxy.**

```typescript
// BAD: the key ships to every device
const response = await fetch('https://api.openai.com/v1/chat/completions', {
  headers: { 'Authorization': `Bearer ${OPENAI_API_KEY}` }
});

// GOOD: call your own backend, which holds the key
const response = await fetch('https://your-api.com/ai/chat', {
  headers: { 'Authorization': `Bearer ${userSessionToken}` },
  body: JSON.stringify({ message: userInput }),
});
```

## Secure Token Storage

- **Expo:** `expo-secure-store`
- **Bare React Native:** `react-native-keychain`
- **Never `AsyncStorage`** — unencrypted plaintext on disk, trivially readable on a rooted or jailbroken device, and often swept up in device backups.

```typescript
// BAD
await AsyncStorage.setItem('authToken', token);

// GOOD — encrypted, hardware-backed where available
await SecureStore.setItemAsync('authToken', token);
```

Redux Persist and similar state libraries default to AsyncStorage. If auth state lives in the store, it's on disk in plaintext.

## Deep Links

Deep links (`myapp://path?param=value`) can be triggered by any app or any web page. They are an unauthenticated entry point into your app.

- Validate and sanitize every parameter
- Never put tokens, passwords, or access-granting IDs in a deep link URL
- Never perform a destructive or state-changing action straight from deep link parameters without confirmation
- Use **App Links** (Android) and **Universal Links** (iOS) with domain verification — custom schemes can be registered by any other app on the device, enabling hijack

## Certificate Pinning

Standard TLS is defeated by a user-installed root CA, which is how traffic-interception tools work. Pinning raises the effort:

- Pin the certificate or public key for your API domain
- Plan rotation before you ship — a pin outliving its certificate bricks the app
- Treat it as friction against casual inspection, not an absolute barrier; a determined attacker on a jailbroken device can patch the check out

## Biometric Authentication

A boolean return from a biometric prompt (`isAuthenticated = true`) can be hooked with Frida on a jailbroken device. Real biometric auth is cryptographic:

1. Server sends a random challenge
2. App signs it with a hardware-backed key (Secure Enclave / StrongBox), released only on biometric success
3. Server verifies the signature

Bypassing the biometric check then gains nothing — the attacker still can't produce the signature.

## Client-Side Checks Are Advisory

Jailbreak detection, root detection, debugger detection, and tamper checks all run on hardware the attacker controls. They add friction and nothing more. Never make a security decision that only the client enforces — every authorization check must also exist on the server.

## Verification Goals

- No third-party API secret in the JS bundle or in `EXPO_PUBLIC_` variables
- All secret-bearing API calls proxied through a backend
- Auth tokens in `expo-secure-store` or `react-native-keychain`, never `AsyncStorage`
- No persisted state library writing tokens to AsyncStorage
- Deep link parameters validated; no tokens carried in deep links
- App Links / Universal Links used with domain verification
- Biometric auth backed by cryptographic challenge-response, not a boolean
- Every client-side authorization check duplicated server-side
