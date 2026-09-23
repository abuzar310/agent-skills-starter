---
name: tikhub
description: >
  Fetch live social-platform data via TikHub (posts, profiles, comments, search,
  trends, analytics, media download URLs) for TikTok, Douyin, Instagram, YouTube,
  Twitter/X, Threads, Xiaohongshu, and related APIs. Use when the user wants
  actual platform data or downloads, not social *copy*. For writing posts, see
  `social`. For internet read/search without a TikHub key, see `agent-reach`.
metadata:
  homepage: https://github.com/TikHub/tikhub-plugin
---

# TikHub — platform data access

Official connector docs from [TikHub/tikhub-plugin](https://github.com/TikHub/tikhub-plugin) (MIT).
This pack ships **one** skill so it does not collide with `social` / `video`.
All requests go to TikHub's hosted API/MCP and cost credits. Requires the user's
`TIKHUB_API_KEY`. Never commit or paste the key.

## Setup gate

```bash
if [ -z "${TIKHUB_API_KEY:-}" ]; then
  echo "TIKHUB_API_KEY is not set — get a key at https://user.tikhub.io then export TIKHUB_API_KEY=..."
fi
```

If unset, stop and send the user to <https://user.tikhub.io>. Persist the key in
their own environment — do not write it into this repo or a project `.env`
unless they ask and the file is gitignored.

## Paths

| Path | How |
|------|-----|
| REST | `curl -sS -H "Authorization: Bearer $TIKHUB_API_KEY" https://api.tikhub.io/...` |
| Hosted MCP | `npx -y mcp-remote https://mcp.tikhub.io/<platform>/mcp --header "Authorization: Bearer ${TIKHUB_API_KEY}"` |
| Python SDK | `pip install tikhub` then use the official client |

Platform MCP slugs include: `tiktok`, `douyin`, `instagram`, `youtube`, `twitter`, `threads`, `xiaohongshu`.

## What this is for

- Pull posts, profiles, comments, search, trends
- Creator / hashtag analytics
- Media download URLs (no-watermark where the API offers it)

## What this is not

- Writing or scheduling social copy (`social`)
- Generating Remotion/HyperFrames video (`video`, `media-use`)
- Free public-web reads without an API key (`agent-reach`)

## Safety

- Warn before bulk/paginated pulls (credits)
- Do not log the API key
- Data is subject to TikHub and source-platform terms
- Full 19-skill marketplace lives upstream; do not copy platform-named skills here
