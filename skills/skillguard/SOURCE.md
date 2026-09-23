# Source

- Upstream: https://github.com/epistemedeus/skillguard
- License: MIT (README; GitHub license field was empty at import)
- Vendored files: `scripts/index.js`, `scripts/mcp.js`, `scripts/package.json` (v1.3.0)
- Added: 2026-09-23 after static review (scanner is read-only; uses `git clone` + file read)

Reviewed: no postinstall, no secret upload, network only for optional git clone of the *target*.
