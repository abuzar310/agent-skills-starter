# File Uploads

An upload endpoint accepts attacker-controlled bytes and attacker-controlled filenames, then stores both on your infrastructure. Treat every uploaded file as hostile.

## Three Validations

**1. File type** — check the extension against an allowlist *and* verify the magic bytes match. Never rely on the `Content-Type` header; the client sets it.

**2. Content** — read the magic bytes. For images, actually decode with an image library, which rejects malformed and polyglot files. For documents, watch for macros and embedded objects.

**3. Size** — enforce server-side, and at the proxy or web server too. Per-type limits where they differ.

## Magic Bytes

| Type | Hex signature |
|---|---|
| JPEG | `FF D8 FF` |
| PNG | `89 50 4E 47 0D 0A 1A 0A` |
| GIF | `47 49 46 38` |
| PDF | `25 50 44 46` |
| ZIP | `50 4B 03 04` |
| DOCX / XLSX / PPTX | `50 4B 03 04` (ZIP-based) |

Office formats are ZIP archives, so the signature alone can't distinguish a DOCX from a ZIP bomb or a malicious spreadsheet. Validate the internal structure for those.

## Bypasses to Block

| Attack | Example | Prevention |
|---|---|---|
| Extension bypass | `shell.php.jpg` | Allowlist on the full final extension |
| Double extension | `shell.jpg.php` | Permit exactly one extension |
| Null byte | `shell.php%00.jpg` | Strip null bytes, reject filenames containing them |
| MIME spoofing | `Content-Type: image/jpeg` on a script | Validate magic bytes, ignore the header |
| Magic byte prefix | Valid header prepended to a payload | Parse the whole file as its claimed type |
| Polyglot | Valid as both JPEG and JavaScript | Decode strictly; reject on any parse warning |
| SVG with script | `<svg onload="alert(1)">` | Sanitize SVG, or disallow the format |
| XXE via document | Malicious DOCX/XLSX (XML inside) | Disable external entities — see `injection.md` |
| Zip Slip | `../../../etc/cron.d/x` inside an archive | Validate every extracted path stays in the target dir |
| ImageMagick exploit | Crafted image triggering a delegate | Patch, restrict `policy.xml` |
| Filename injection | `; rm -rf /` or `$(cmd)` in the name | Discard the original name entirely |
| MIME sniffing | Browser guesses executable content | `X-Content-Type-Options: nosniff` |

SVG deserves emphasis: it is XML that executes JavaScript when rendered inline. If users upload avatars and you serve SVG from your own origin, that is stored XSS. Either sanitize with DOMPurify in SVG mode, convert to raster on upload, or reject the format.

## Secure Handling

1. **Rename every file.** Generate a UUID, discard the user's filename completely. Store the original as a display-only database field if you need it.
2. **Store outside the webroot** — object storage (S3, R2, GCS) or a directory the web server won't execute from.
3. **Serve from a separate domain.** An upload origin distinct from your app origin means stored XSS can't touch your session cookies. This is the single highest-value control here.
4. **Set headers on delivery:**
   - `Content-Disposition: attachment` for anything not meant to render inline
   - `X-Content-Type-Options: nosniff`
   - `Content-Type` matching the verified type, never the claimed one
5. **Non-executable permissions** on stored files.
6. **Scope the storage path to the owner** so one user can't overwrite another's file. See the Supabase storage policy in `database-security.md`.

## Direct-to-Storage Uploads

Presigned URLs are common and shift the risk: the client uploads straight to S3, so your server never sees the bytes and can't validate them.

- Constrain the presigned URL — content-length range, content-type, key prefix scoped to the user's ID
- Validate after upload with an event trigger, before the file becomes reachable
- Never let the client choose the object key freely

## Verification Goals

- Uploads validated by magic bytes, not by extension or `Content-Type`
- Every stored file renamed to a UUID
- Files stored outside the webroot, ideally on a separate domain
- `X-Content-Type-Options: nosniff` set on file responses
- Server-side size limits enforced
- SVG sanitized, rasterized, or rejected
- Archive extraction validates paths stay within the target directory
- Storage paths scoped to the uploading user
