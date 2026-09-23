# Agent Skills Starter

**A mid-size, battle-tested collection of Agent Skills for Claude Code, Cursor, and other AI coding agents.**

If you've ever stared at a giant skills dump and thought *"which ones do I actually need?"* — this repo is for you.

~**136 skills**, cherry-picked and organized by job-to-be-done. Not 400 random folders. Not 10 toy demos. Enough to ship marketing, SEO, design, video, docs, and real engineering workflows.

Compatible with the [Agent Skills](https://agentskills.io) format (`SKILL.md` + optional scripts/references/assets).

---

## Why this exists

Most people struggle with skills because:

1. **Discovery is broken** — good skills are scattered across repos, Discord threads, and random zips
2. **Too much noise** — mega packs bury the 20 skills you'll use weekly
3. **Install friction** — unclear where files go for Claude vs Cursor

This pack is a **1.5 between "tiny starter" and "full universe"**: curated, categorized, ready to clone.

---

## Quick install

### Option A — Claude Code (project skills)

```bash
git clone https://github.com/abuzar310/agent-skills-starter.git
mkdir -p .claude/skills
cp -R agent-skills-starter/skills/* .claude/skills/
```
Or symlink so you can update with `git pull`:

```bash
git clone https://github.com/abuzar310/agent-skills-starter.git ~/agent-skills-starter
mkdir -p .claude/skills
# copy only the categories you need, e.g.:
cp -R ~/agent-skills-starter/skills/{copywriting,cro,seo,frontend-design,skill-creator} .claude/skills/
```
### Option B — Cursor

Copy skills into your user or project skills folder:

**Windows (PowerShell)**

```powershell
git clone https://github.com/abuzar310/agent-skills-starter.git $env:USERPROFILE\agent-skills-starter
$dest = "$env:USERPROFILE\.claude\skills"   # or your Cursor skills path
New-Item -ItemType Directory -Force -Path $dest | Out-Null
Copy-Item "$env:USERPROFILE\agent-skills-starter\skills\*" $dest -Recurse -Force
```
**macOS / Linux**

```bash
git clone https://github.com/abuzar310/agent-skills-starter.git ~/agent-skills-starter
mkdir -p ~/.claude/skills
cp -R ~/agent-skills-starter/skills/* ~/.claude/skills/
```
### Option C — Install script

From this repo:

```bash
# Unix
./scripts/install.sh ~/.claude/skills

# Windows PowerShell
.\scripts\install.ps1 -Destination $env:USERPROFILE\.claude\skills
```
Pass specific skill names to install a subset:

```bash
./scripts/install.sh ~/.claude/skills copywriting cro seo frontend-design vibe-sec
```
---

## Recommended starter kits

Don't install everything on day one. Start with a kit:

| Kit | Skills | Best for |
|-----|--------|----------|
| **Builder** | `frontend-design`, `ui-ux-pro-max`, `skill-creator`, `systematic-debugging`, `test-driven-development`, `verification-before-completion`, `vibe-sec`, `skillguard`, `stop-slop` | Shipping apps with AI |
| **Marketer** | `product-marketing`, `copywriting`, `cro`, `seo`, `seo-audit`, `ads`, `ad-creative`, `analytics`, `launch` | Growth, landing pages, campaigns |
| **Content / SEO** | `seo`, `seo-content`, `seo-technical`, `ai-seo`, `content-strategy`, `copy-editing`, `schema` | Rankings + AI search |
| **Maker of things** | `pdf`, `pptx`, `docx`, `remotion-create`, `hyperframes`, `canvas-design` | Docs, decks, video |
| **Agent power-user** | `brainstorming`, `planning-with-files`, `writing-plans`, `dispatching-parallel-agents`, `ponytail`, `caveman`, `agent-reach`, `skillguard` | Better agent workflows |

---

## What's inside

### Marketing & Growth (41)

| Skill | What it helps with |
|-------|-------------------|
| [ab-testing](skills/ab-testing/) | When the user wants to plan, design, or implement an A/B test or experiment, or build a growth experimentation program. Also use when the... |
| [ad-creative](skills/ad-creative/) | When the user wants to generate, iterate, or scale ad creative — headlines, descriptions, primary text, or full ad variations — for any p... |
| [ads](skills/ads/) | When the user wants help with paid advertising campaigns on Google Ads, Meta (Facebook/Instagram), LinkedIn, Twitter/X, or other ad platf... |
| [analytics](skills/analytics/) | When the user wants to set up, improve, or audit analytics tracking and measurement. Also use when the user mentions "set up tracking," "... |
| [aso](skills/aso/) | When the user wants to audit or optimize an App Store or Google Play listing. Also use when the user mentions 'ASO audit,' 'app store opt... |
| [churn-prevention](skills/churn-prevention/) | When the user wants to reduce churn, build cancellation flows, set up save offers, recover failed payments, or implement retention strate... |
| [cold-email](skills/cold-email/) | Write B2B cold emails and follow-up sequences that get replies. Use when the user wants to write cold outreach emails, prospecting emails... |
| [co-marketing](skills/co-marketing/) | When the user wants to find co-marketing partners, plan joint campaigns, or brainstorm partnership opportunities. Use when the user says ... |
| [community-marketing](skills/community-marketing/) | Build and leverage online communities to drive product growth and brand loyalty. Use when the user wants to create a community strategy, ... |
| [competitor-profiling](skills/competitor-profiling/) | When the user wants to research, profile, or analyze competitors from their URLs. Also use when the user mentions 'competitor profile,' '... |
| [competitors](skills/competitors/) | When the user wants to create competitor comparison or alternative pages for SEO and sales enablement. Also use when the user mentions 'a... |
| [content-strategy](skills/content-strategy/) | When the user wants to plan a content strategy, decide what content to create, or figure out what topics to cover. Also use when the user... |
| [copy-editing](skills/copy-editing/) | When the user wants to edit, review, or improve existing marketing copy, or refresh outdated content. Also use when the user mentions 'ed... |
| [copywriting](skills/copywriting/) | When the user wants to write, rewrite, or improve marketing copy for any page — including homepage, landing pages, pricing pages, feature... |
| [cro](skills/cro/) | When the user wants to optimize, improve, or increase conversions on any marketing page or form — including homepage, landing pages, pric... |
| [customer-research](skills/customer-research/) | When the user wants to conduct, analyze, or synthesize customer research. Use when the user mentions "customer research," "ICP research,"... |
| [directory-submissions](skills/directory-submissions/) | When the user wants to submit their product to startup, SaaS, AI, agent, MCP, no-code, or review directories for backlinks, domain rating... |
| [emails](skills/emails/) | When the user wants to create or optimize an email sequence, drip campaign, automated email flow, or lifecycle email program. Also use wh... |
| [free-tools](skills/free-tools/) | When the user wants to plan, evaluate, or build a free tool for marketing purposes — lead generation, SEO value, or brand awareness. Also... |
| [image](skills/image/) | When the user wants to create, generate, edit, or optimize images for marketing — blog heroes, social graphics, product mockups, profile ... |
| [launch](skills/launch/) | When the user wants to plan a product launch, feature announcement, or release strategy. Also use when the user mentions 'launch,' 'Produ... |
| [lead-magnets](skills/lead-magnets/) | When the user wants to create, plan, or optimize a lead magnet for email capture or lead generation. Also use when the user mentions "lea... |
| [marketing-council](skills/marketing-council/) | When the user wants multiple expert perspectives on a marketing question — a simulated board of advisors staffed by legendary marketers (... |
| [marketing-ideas](skills/marketing-ideas/) | When the user needs marketing ideas, inspiration, or strategies for their SaaS or software product. Also use when the user asks for 'mark... |
| [marketing-loops](skills/marketing-loops/) | When the user wants to set up a recurring, self-running marketing workflow — a repeatable loop an AI agent runs on a cadence (weekly, dai... |
| [marketing-plan](skills/marketing-plan/) | When the user needs a comprehensive marketing plan for a client, a company they advise, or their own product. Also use when the user ment... |
| [marketing-psychology](skills/marketing-psychology/) | When the user wants to apply psychological principles, mental models, or behavioral science to marketing. Also use when the user mentions... |
| [offers](skills/offers/) | When the user wants to design, construct, or improve an offer — the thing they actually sell — including value framing, bonus stacking, g... |
| [onboarding](skills/onboarding/) | When the user wants to optimize post-signup onboarding, user activation, first-run experience, or time-to-value. Also use when the user m... |
| [paywalls](skills/paywalls/) | When the user wants to create or optimize in-app paywalls, upgrade screens, upsell modals, or feature gates. Also use when the user menti... |
| [popups](skills/popups/) | When the user wants to create or optimize popups, modals, overlays, slide-ins, or banners for conversion purposes. Also use when the user... |
| [pricing](skills/pricing/) | When the user wants help with pricing decisions, packaging, or monetization strategy. Also use when the user mentions 'pricing,' 'pricing... |
| [product-marketing](skills/product-marketing/) | When the user wants to create or update their product marketing context document. Also use when the user mentions 'product context,' 'mar... |
| [prospecting](skills/prospecting/) | When the user wants to find, qualify, and build a list of prospects to reach out to — across B2B SaaS, general B2B, or local small busine... |
| [public-relations](skills/public-relations/) | When the user wants help with public relations, earned media, press coverage, journalist outreach, or media strategy (not pull requests).... |
| [referrals](skills/referrals/) | When the user wants to create, optimize, or analyze a referral program, affiliate program, or word-of-mouth strategy. Also use when the u... |
| [revops](skills/revops/) | When the user wants help with revenue operations, lead lifecycle management, or marketing-to-sales handoff processes. Also use when the u... |
| [sales-enablement](skills/sales-enablement/) | When the user wants to create sales collateral, pitch decks, one-pagers, objection handling docs, or demo scripts. Also use when the user... |
| [signup](skills/signup/) | When the user wants to optimize signup, registration, account creation, or trial activation flows. Also use when the user mentions "signu... |
| [social](skills/social/) | When the user wants help creating, scheduling, or optimizing social media content for LinkedIn, Twitter/X, Instagram, TikTok, Facebook, o... |
| [video](skills/video/) | When the user wants to create, generate, or produce video content using AI tools or programmatic frameworks. Also use when the user menti... |


### SEO (25)

| Skill | What it helps with |
|-------|-------------------|
| [ai-seo](skills/ai-seo/) | When the user wants to optimize content for AI search engines, get cited by LLMs, or appear in AI-generated answers. Also use when the us... |
| [programmatic-seo](skills/programmatic-seo/) | When the user wants to create SEO-driven pages at scale using templates and data. Also use when the user mentions "programmatic SEO," "te... |
| [schema](skills/schema/) | When the user wants to add, fix, or optimize schema markup and structured data on their site. Also use when the user mentions "schema mar... |
| [seo](skills/seo/) | Comprehensive SEO analysis for any website or business type. Full site audits, single-page analysis, technical SEO (crawlability, indexab... |
| [seo-audit](skills/seo-audit/) | When the user wants to audit, review, or diagnose SEO issues on their site. Also use when the user mentions "SEO audit," "technical SEO,"... |
| [seo-backlinks](skills/seo-backlinks/) | Backlink profile analysis: referring domains, anchor text distribution, toxic link detection, competitor gap analysis. Works with free AP... |
| [seo-cluster](skills/seo-cluster/) | SERP-based semantic topic clustering for content architecture planning. Groups |
| [seo-competitor-pages](skills/seo-competitor-pages/) | Generate SEO-optimized competitor comparison and alternatives pages. Covers |
| [seo-content](skills/seo-content/) | Content quality and E-E-A-T analysis with AI citation readiness assessment. |
| [seo-content-brief](skills/seo-content-brief/) | Generate competitive SEO content briefs with per-section word counts, |
| [seo-ecommerce](skills/seo-ecommerce/) | E-commerce SEO analysis: Google Shopping visibility, Amazon marketplace |
| [seo-flow](skills/seo-flow/) | FLOW framework integration — evidence-led SEO using the Find → Leverage → |
| [seo-geo](skills/seo-geo/) | Optimize content for AI Overviews (formerly SGE), ChatGPT web search, |
| [seo-google](skills/seo-google/) | Google SEO APIs: Search Console (Search Analytics, URL Inspection, Sitemaps), |
| [seo-hreflang](skills/seo-hreflang/) | Hreflang and international SEO audit, validation, and generation. Detects |
| [seo-images](skills/seo-images/) | Image optimization analysis for SEO and performance. Checks alt text, file |
| [seo-local](skills/seo-local/) | Local SEO analysis covering Google Business Profile optimization, NAP |
| [seo-page](skills/seo-page/) | Deep single-page SEO analysis covering on-page elements, content quality, |
| [seo-plan](skills/seo-plan/) | Strategic SEO planning for new or existing websites. Industry-specific |
| [seo-programmatic](skills/seo-programmatic/) | Programmatic SEO planning and analysis for pages generated at scale from data |
| [seo-schema](skills/seo-schema/) | Detect, validate, and generate Schema.org structured data. JSON-LD format |
| [seo-sitemap](skills/seo-sitemap/) | Analyze existing XML sitemaps or generate new ones with industry templates. |
| [seo-sxo](skills/seo-sxo/) | Search Experience Optimization: reads Google SERPs backwards to detect page-type |
| [seo-technical](skills/seo-technical/) | Technical SEO audit across 9 categories: crawlability, indexability, security, |
| [site-architecture](skills/site-architecture/) | When the user wants to plan, map, or restructure their website's page hierarchy, navigation, URL structure, or internal linking. Also use... |


### Design & Frontend (21)

| Skill | What it helps with |
|-------|-------------------|
| [apple-design](skills/apple-design/) | Apple's approach to interface design and fluid, physical motion, translated for the web. Use when building or reviewing gesture-driven UI... |
| [banner-design](skills/banner-design/) | Design banners for social media, ads, website heroes, creative assets, and print. Multiple art direction options with AI-generated visual... |
| [brand](skills/brand/) | Brand voice, visual identity, messaging frameworks, asset management, brand consistency. Activate for branded content, tone of voice, mar... |
| [brand-guidelines](skills/brand-guidelines/) | Applies Anthropic's official brand colors and typography to any sort of artifact that may benefit from having Anthropic's look-and-feel. ... |
| [canvas-design](skills/canvas-design/) | Create beautiful visual art in .png and .pdf documents using design philosophy. You should use this skill when the user asks to create a ... |
| [design](skills/design/) | Comprehensive design skill: brand identity, design tokens, UI styling, logo generation (55 styles, Gemini AI), corporate identity program... |
| [design-system](skills/design-system/) | Token architecture, component specifications, and slide generation. Three-layer tokens (primitive→semantic→component), CSS variables, spa... |
| [figma](skills/figma/) | Import Figma content into a HyperFrames composition — rendered assets, brand tokens, components, storyboard sections → reconstructed moti... |
| [frontend-design](skills/frontend-design/) | Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. Helps with aesthetic direction, ty... |
| [gsap-scrolltrigger](skills/gsap-scrolltrigger/) | Comprehensive skill for GSAP (GreenSock Animation Platform) and ScrollTrigger plugin. Use this skill when creating web animations, scroll... |
| [impeccable](skills/impeccable/) | Use when the user wants to design, redesign, shape, critique, audit, polish, clarify, distill, harden, optimize, adapt, animate, colorize... |
| [improve-animations](skills/improve-animations/) | Survey a codebase's animation and motion code as a senior motion advisor, then produce a prioritized audit and self-contained implementat... |
| [lottie-animations](skills/lottie-animations/) | After Effects animation rendering for web and React applications. Use this skill when implementing Lottie animations, JSON vector animati... |
| [modern-web-design](skills/modern-web-design/) | Modern web design trends, principles, and implementation patterns for 2024-2025. Use this skill when designing websites, creating interac... |
| [motion-framer](skills/motion-framer/) | Modern animation library for React and JavaScript. Create smooth, production-ready animations with motion components, variants, gestures ... |
| [react-three-fiber](skills/react-three-fiber/) | Build declarative 3D scenes with React Three Fiber (R3F) - a React renderer for Three.js. Use when building interactive 3D experiences in... |
| [scroll-reveal-libraries](skills/scroll-reveal-libraries/) | Simple scroll-triggered reveal animations using AOS (Animate On Scroll). Use this skill when building marketing pages, landing pages, or ... |
| [theme-factory](skills/theme-factory/) | Toolkit for styling artifacts with a theme. These artifacts can be slides, docs, reportings, HTML landing pages, etc. There are 10 pre-se... |
| [threejs-webgl](skills/threejs-webgl/) | Comprehensive skill for Three.js 3D web development. Use this skill when building interactive 3D scenes, WebGL/WebGPU applications, produ... |
| [ui-ux-pro-max](skills/ui-ux-pro-max/) | UI/UX design intelligence for web and mobile. Searchable local database with 50+ styles, 161 color palettes, 57 font pairings, 161 produc... |
| [web-artifacts-builder](skills/web-artifacts-builder/) | Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind C... |


### Documents & Comms (6)

| Skill | What it helps with |
|-------|-------------------|
| [doc-coauthoring](skills/doc-coauthoring/) | Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technica... |
| [docx](skills/docx/) | Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers include: any mention o... |
| [internal-comms](skills/internal-comms/) | A set of resources to help me write all kinds of internal communications, using the formats that my company likes to use. Claude should u... |
| [pdf](skills/pdf/) | Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combinin... |
| [pptx](skills/pptx/) | Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks... |
| [xlsx](skills/xlsx/) | Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit,... |


### Engineering & Agents (32)

| Skill | What it helps with |
|-------|-------------------|
| [agent-reach](skills/agent-reach/) | MUST USE when user wants to research/search/look up/find anything on the internet — e.g. "research this topic", "do a deep dive on X", "search the... |
| [brainstorming](skills/brainstorming/) | You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explore... |
| [caveman](skills/caveman/) | Ultra-compressed communication mode. Cuts output tokens 65% (measured) by speaking like caveman |
| [caveman-commit](skills/caveman-commit/) | Ultra-compressed commit message generator. Cuts noise from commit messages while preserving |
| [caveman-review](skills/caveman-review/) | Ultra-compressed code review comments. Cuts noise from PR feedback while preserving |
| [claude-api](skills/claude-api/) | /- |
| [dispatching-parallel-agents](skills/dispatching-parallel-agents/) | Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies |
| [do](skills/do/) | Execute a phased implementation plan using subagents. Use when asked to execute, run, or carry out a plan — especially one created by mak... |
| [executing-plans](skills/executing-plans/) | Use when you have a written implementation plan to execute in a separate session with review checkpoints |
| [finishing-a-development-branch](skills/finishing-a-development-branch/) | Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development ... |
| [learn-codebase](skills/learn-codebase/) | Prime a codebase by reading every source file in full. Use when starting work on a new or unfamiliar project, or when the user asks to "l... |
| [mcp-builder](skills/mcp-builder/) | Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-des... |
| [planning-with-files](skills/planning-with-files/) | Manus-style persistent file-based planning for AI coding agents: keeps task_plan.md, findings.md, and progress.md on disk so work survive... |
| [ponytail](skills/ponytail/) | Forces the laziest solution that actually works, simplest, shortest, most |
| [ponytail-audit](skills/ponytail-audit/) | Whole-repo audit for over-engineering. Like ponytail-review, but scans the |
| [ponytail-review](skills/ponytail-review/) | Code review focused exclusively on over-engineering. Finds what to delete: |
| [receiving-code-review](skills/receiving-code-review/) | Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionabl... |
| [requesting-code-review](skills/requesting-code-review/) | Use when completing tasks, implementing major features, or before merging to verify work meets requirements |
| [skill-creator](skills/skill-creator/) | Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch,... |
| [skillguard](skills/skillguard/) | Scan a third-party Agent Skill, Claude Code plugin, or MCP server for malware BEFORE installing it. Use when the user says "is this skill safe?", "scan this... |
| [smart-explore](skills/smart-explore/) | Token-optimized structural code search using tree-sitter AST parsing. Use instead of reading full files when you need to understand code ... |
| [stop-slop](skills/stop-slop/) | Remove AI writing patterns from prose. Use when drafting, editing, or reviewing text to eliminate predictable AI tells. |
| [subagent-driven-development](skills/subagent-driven-development/) | Use when executing implementation plans with independent tasks in the current session |
| [systematic-debugging](skills/systematic-debugging/) | Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes |
| [test-driven-development](skills/test-driven-development/) | Use when implementing any feature or bugfix, before writing implementation code |
| [tikhub](skills/tikhub/) | Fetch live social-platform data via TikHub (posts, profiles, comments, search, trends, analytics, media download URLs) for TikTok, Douyin, Instagram, YouTube,... |
| [using-git-worktrees](skills/using-git-worktrees/) | Use when starting feature work that needs isolation from current workspace or before executing implementation plans - ensures an isolated... |
| [verification-before-completion](skills/verification-before-completion/) | Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands a... |
| [version-bump](skills/version-bump/) | Automated semantic versioning and release workflow for Claude Code plugins. Handles version increments across package.json, marketplace.j... |
| [vibe-sec](skills/vibe-sec/) | Audits codebases for security vulnerabilities, especially those AI coding assistants introduce in rapidly-built apps. Covers exposed API ... |
| [webapp-testing](skills/webapp-testing/) | Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI... |
| [writing-plans](skills/writing-plans/) | Use when you have a spec or requirements for a multi-step task, before touching code |


### Video & Motion (11)

| Skill | What it helps with |
|-------|-------------------|
| [embedded-captions](skills/embedded-captions/) | Add captions to a talking-head video. ONE catalog (CATALOG.md) of 36 visual identities behind two engines: column-flow (captions composit... |
| [general-video](skills/general-video/) | The fallback workflow for authoring or editing any custom HyperFrames composition at any |
| [hyperframes](skills/hyperframes/) | READ THIS FIRST for any request to make, create, edit, animate, or render a |
| [mediabunny](skills/mediabunny/) | Multimedia handling with the Mediabunny library |
| [media-use](skills/media-use/) | Agent Media OS, the single skill for every media need in a HyperFrames project. Resolve BGM, SFX, image, icon, brand logo, voice, color g... |
| [motion-graphics](skills/motion-graphics/) | A short, design-led motion graphic where motion is the message — kinetic |
| [remotion-best-practices](skills/remotion-best-practices/) | Best practices for Remotion |
| [remotion-captions](skills/remotion-captions/) | Dealing with captions in Remotion |
| [remotion-create](skills/remotion-create/) | Creating a new Remotion video |
| [remotion-interactivity](skills/remotion-interactivity/) | Best practices for writing Remotion animations that stay intuitive for agents and editable in Remotion Studio Visual Mode. |
| [remotion-render](skills/remotion-render/) | Best practices for rendering videos |


---

## 2026-09 capability additions

Compared against this pack (source of truth) before adding anything. Existing skills were not modified or deleted.

| Added | Why |
|-------|-----|
| `agent-reach` | Internet research router (X/Reddit/YouTube/GitHub/etc.). Not a UI/design skill. Router skill only — no installer, cookies, or `.env`. |
| `skillguard` | Static scan of third-party skills/MCP **before** install. Complements `vibe-sec` (app code). |
| `tikhub` | Paid TikHub API/MCP for live platform data. One connector skill — not the 19-skill marketplace, and not a duplicate of `social` (copy). |

Skipped: Ghost-Downloader-3 (desktop app, not an agent skill), yizhiyanhua-ai/media-downloader (cookie/`zshrc` installer risk; video skills already cover in-project media), agent-0x/reach (remote command agent; name collision only).

---

## How skills work

Each skill is a folder with a `SKILL.md`:

```
skill-name/
├── SKILL.md          # instructions + when to trigger
├── scripts/          # optional helpers
├── references/       # optional deep docs
└── assets/           # optional templates
```

Your agent reads the skill when the task matches the description — you don't need to memorize filenames. Saying *"audit this landing page for conversion"* should pull in `cro`; *"make this UI less generic"* should pull in `frontend-design` / `ui-ux-pro-max`.

### Tips that actually help

- **Install fewer skills first** — too many similar skills can confuse routing
- **Prefer project skills** for team conventions; user skills for personal defaults
- **Edit descriptions** if a skill never triggers — the YAML `description` is the router
- **Use `skill-creator`** when you want to write your own

---

## Repo layout

```
agent-skills-starter/
├── README.md
├── LICENSE
├── skills/                 # all skills (flat, Agent Skills format)
├── scripts/
│   ├── install.sh
│   └── install.ps1
└── catalogs/
    └── skills-by-category.md
```

---

## Contributing

PRs welcome for:

- Clearer `SKILL.md` descriptions (better trigger accuracy)
- Bug fixes in scripts
- New skills that fill a real gap (not duplicates)

Keep skills self-contained. No API keys, tokens, or private brand assets.

---

## License

MIT — use freely, modify, ship with your projects.

Skills in this collection are curated, adapted, and maintained for practical agent use.

---

## Star if it helped

If this saved you an afternoon of digging through random skill zips, star the repo so other people can find it too.