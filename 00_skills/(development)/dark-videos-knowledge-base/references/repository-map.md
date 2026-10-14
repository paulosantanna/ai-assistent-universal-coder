# Dark Videos Knowledge Base

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Overview

This skill provides a complete Alpha mapping of the `D:\Git\dark-videos` repository. It documents the full directory structure, module organization, file inventory, and architectural patterns of the dark-videos video pipeline platform.

**Purpose:** Serves as a reference for understanding the codebase structure, onboarding new developers, and navigating the modular pipeline architecture.

**Scope:** Complete repository mapping covering backend, frontend, documentation, and AEOS framework artifacts.

## Repository Structure

The `dark-videos` repository is a comprehensive video pipeline platform with the following high-level structure:

### Root Level (47 directories, 187+ files)

| Directory | Purpose |
|-----------|---------|
| `.aeos/` | AEOS framework artifacts (bug-solver, evidence, moldura-preview, reports, sandbox) |
| `.cursor/` | Cursor editor rules |
| `.github/` | GitHub workflows and CI/CD |
| `.idea/` | IntelliJ IDEA configuration |
| `.postgres/` | PostgreSQL data and configurations |
| `.pytest_cache/` | pytest cache directories |
| `.redis/` | Redis data and configurations |
| `.ruff_cache/` | Python Ruff linter cache |
| `.specs/` | Project specifications and EARS requirements |
| `backend/` | Python FastAPI backend application |
| `docs/` | Architecture and security documentation |
| `frontend/` | Next.js/React frontend application |
| `scripts/` | Helper scripts (merge-gate.sh) |
| `social-media-mcp/` | Social media MCP services |

### Backend Structure (`backend/`)

The backend is a Python modular monolith built with FastAPI, organized into feature-based modules:

#### Core Application (`backend/app/`)

- `api/` - API endpoints for accounts, auth, mining, pipeline, settings
- `core/` - Core business logic: AI, audit, clock, config, HTTP, logging, middleware, ratelimit, redaction
- `modules/` - Feature modules (mining, publishing, analytics, creative, learning)
- `contracts/` - API contracts and schema definitions
- `security/` - Authentication, vault, secrets, field_seal
- `pipeline/` - Pipeline orchestrator, registry, service, stage
- `data/` - Data storage configurations (postgresql, redis)
- `db/` - Database models and session management

#### Modules Detail

##### `backend/app/modules/mining/`

Video mining and acquisition module:

| File | Description |
|------|-------------|
| `acquire.py` | Video acquisition logic |
| `api.py` | Mining API endpoints |
| `dedup.py` | Deduplication using fingerprints |
| `fingerprints.py` | Content fingerprinting (simhash, audio/video) |
| `gates.py` | Mining stage gates and filters |
| `history.py` | Mining history and state tracking |
| `models.py` | Data models for mined content |
| `net.py` | Network operations and API clients |
| `persistence.py` | Persistence layer for mining state |
| `pool.py` | Mining pool management |
| `ranking.py` | Video ranking and velocity scoring |
| `service.py` | Mining service orchestration |
| `settings.py` | Mining configuration |
| `stages.py` | Mining pipeline stages |
| `template_gate.py` | Template validation gate |
| `thumbnails.py` | Thumbnail generation |
| `connectors/` - External platform connectors |
| `account_feed.py` | Account feed connector |
| `base.py` | Connector base class |
| `dailymotion.py` | Dailymotion connector |
| `instagram_hashtag.py` | Instagram hashtag search |
| `provider.py` | Provider base/abstract |
| `youtube.py` | YouTube Data API connector |
| `youtube_shorts.py` | YouTube Shorts connector |
| `ytdlp_feed.py` | yt-dlp feed extraction |
| `ytdlp_search.py` | yt-dlp search extraction |

##### `backend/app/modules/publishing/`

Video publishing and dispatch module:

| File | Description |
|------|-------------|
| `api.py` | Publishing API endpoints |
| `browser_post.py` | Browser-based posting automation |
| `dispatch.py` | Central dispatch orchestration |
| `download.py` | Media download and processing |
| `errors.py` | Error handling and classifications |
| `fakes.py` | Fake/test data generation |
| `gates.py` | Publishing stage gates |
| `media.py` | Media processing and transformation |
| `models.py` | Publishing data models |
| `outlive.py` | Outlive/evergreen content logic |
| `prime.py` | Prime-time scheduling |
| `release.py` | Release management |
| `settings.py` | Publishing configuration |
| `signing.py` | Content signing and verification |
| `slots.py` | Slot/time slot management |
| `stages.py` | Publishing pipeline stages |
| `stories.py` | Story/Reels management |
| `tasks.py` | Background tasks |
| `publishers/` - Platform-specific publishers |
| `base.py` | Publisher base class |
| `http.py` | HTTP publisher |
| `instagram.py` | Instagram publisher |
| `tiktok.py` | TikTok publisher |
| `youtube.py` | YouTube publisher |

##### `backend/app/modules/analytics/`

Analytics and insights module:

| File | Description |
|------|-------------|
| `account_insights.py` | Account-level analytics |
| `api.py` | Analytics API endpoints |
| `cadence.py` | Cadence and timing analysis |
| `collection.py` | Data collection logic |
| `collectors.py` | Data collectors for social platforms |
| `fakes.py` | Fake analytics data |
| `instagram_browser.py` | Instagram browser automation |
| `milestones.py` | Milestone tracking |
| `models.py` | Analytics models |
| `service.py` | Analytics service |
| `settings.py` | Analytics configuration |
| `tasks.py` | Analytics tasks |

##### `backend/app/modules/creative/`

Creative content generation module:

| File | Description |
|------|-------------|
| `api.py` | Creative API endpoints |
| `assembly.py` | Content assembly logic |
| `fakes.py` | Fake creative data |
| `gates.py` | Creative stage gates |
| `generators.py` | Content generators (text, video) |
| `models.py` | Creative data models |
| `persistence.py` | Creative persistence |
| `schemas.py` | JSON schemas |
| `service.py` | Creative service |
| `settings.py` | Creative configuration |
| `stages.py` | Creative pipeline stages |
| `tasks.py` | Creative tasks |
| `templates.py` | Content templates |
| `text_policy.py` | Text policy and compliance |
| `trending.py` | Trending analysis |

##### `backend/app/modules/learning/`

Learning and AI/ML module with JeV integration:

| File | Description |
|------|-------------|
| `analysis.py` | Learning analysis |
| `api.py` | Learning API endpoints |
| `calibration.py` | Model calibration |
| `diagnosis.py` | Diagnosis and troubleshooting |
| `fakes.py` | Fake learning data |
| `history.py` | Learning history |
| `jev_decision_engine.py` | JeV decision engine |
| `judgments.py` | Judgment and evaluation |
| `laya_finetuning.py` | LAYA fine-tuning |
| `laya_jev_client.py` | LAYA JeV client |
| `models.py` | Learning models |
| `predict.py` | Prediction logic |
| `providers.py` | Learning providers |
| `ranking.py` | Ranking algorithms |
| `retrieval.py` | Retrieval mechanisms |
| `service.py` | Learning service |
| `settings.py` | Learning configuration |
| `stages.py` | Learning stages |
| `tasks.py` | Learning tasks |
| `content_gate/` - Content admission gate |
| `admit.py` | Admission logic |
| `audio.py` | Audio processing |
| `category.py` | Category definitions |
| `decide.py` | Decision logic |
| `locale.py` | Localization |
| `speech.py` | Speech processing |
| `stage.py` | Stage definitions |
| `types.py` | Type definitions |
| `jev/` - JeV module |
| `client.py` | JeV client |
| `content_policy.py` | Content policy |
| `ev.py` | Evaluation |
| `types.py` | Types |

##### Other Backend Directories

- `backend/app/contracts/` - Contract definitions (common, creative, learning, mining, pipeline, tokens)
- `backend/app/db/` - Database layer (base, connect, session, revision_repair)
- `backend/app/data/` - Data storage (postgresql, redis)

### Frontend Structure (`frontend/`)

Next.js/React application with TypeScript.

#### `frontend/src/`

- `app/` - App directory (Next.js 13+)
- `components/` - React components:
  - `accounts/` - PlatformCard.tsx
  - `auth/` - AuthProvider, authentication flow
  - `pipeline/` - RunTimeline.tsx, RunTimeline.test.tsx
  - `shell/` - AppShell, nav.ts, ScheduleNotice
  - `ui/` - icons.tsx, LiveIndicator.tsx, ModuleNotice.tsx, primitives.tsx
- `lib/` - Libraries and utilities:
  - `api/` - API clients (analytics, client, core, creative, publishing, internal-url, learning, mining, observability, publishing)
  - `hooks/` - usePolling.ts, usePolling.test.tsx
  - `format.ts` - Formatting utilities
  - `oauth.ts` - OAuth implementation
- `test/` - Test helpers (fetch.ts, setup.ts)

#### Configuration Files

- `package.json` - Dependencies (Next.js, React, Vitest, etc.)
- `next.config.ts` - Next.js configuration
- `tsconfig.json`/`.tsbuildinfo` - TypeScript configuration
- `eslint.config.mjs` - ESLint config
- `vitest.config.mts` - Vitest config

### Documentation (`docs/`)

- `ARCHITECTURE.md` - 23KB architecture document
- `SECURITY.md` - 10KB security documentation

### AEOS Framework (`.aeos/`)

- `bug-solver/` - Bug solving infrastructure
- `evidence/` - Evidence caching and integrity
- `moldura-preview/` - Preview moldura generation
- `reports/` - Report generation
- `sandbox/` - Execution sandbox

### Scripts and MCP

- `scripts/merge-gate.sh` - Merge gate shell script
- `social-media-mcp/` - Social Media MCP (node_modules)

## Module Organization Pattern

The repository follows a **modular-by-aggregate** pattern:

1. **Domain-driven**: Each module represents a business domain (mining, publishing, analytics, etc.)
2. **Feature-focused**: Files are organized by feature, not layer
3. **Self-contained modules**: Each module has its own models, services, gates, and settings
4. **Clear boundaries**: Contracts define API boundaries between modules
5. **Hierarchical stages**: Pipeline stages gate progress at each step

## Key Architectural Patterns

### 1. Connector Pattern (Mining)

- External platforms (YouTube, Instagram, TikTok, Dailymotion) implemented as connectors
- Base class (`provider.py`, `base.py`) defines the interface
- yt-dlp used for fallback/search when API keys are unavailable
- Synthetic samples for dry-run simulation

### 2. Dispatch Pattern (Publishing)

- Single dispatch publisher (`publishing.dispatch`) is the only authorized publisher
- Browser-based posting for Instagram/TikTok
- YouTube publishing through API
- File cleanup after real posts

### 3. JeV/Decision Engine (Learning)

- JeV (Jev evaluation system) for confidence-aware decisions
- LAYA fine-tuning for heat scoring
- Decision engine with ranking based on velocity + LAYA signal
- Heat score: `0.65 * baseline velocity + 0.35 * LAYA signal`
- Heat >= 9.5 badge maintains top 20 position

### 4. Content Gate (Learning)

- Admission gate (`content_gate/admit.py`) filters content before learning
- Multi-stage decision process (audio, category, locale, speech)
- Judgment and evaluation pipeline

### 5. Security & Vault

- Vault (`security/vault.py`) for secret management
- Field seal (`security/field_seal.py`) for data sealing
- Authentication flows (desktop_login, local_login)
- Password hashing and session management

### 6. Contracts & Schemas

- API contracts in `backend/app/contracts/`
- JSON schemas for request/validation
- Token management (`contracts/tokens.py`)
- Common patterns across modules

## Environment Variables

| Variable | Purpose | Optimized Default |
|----------|---------|-------------------|
| `MINING_YOUTUBE_API_KEY` | YouTube Data API key for mining | Required for real runs |
| `MINING_PROVIDER_BASE_URL` | Optional Instagram/TikTok provider base URL | Off by default |
| `MINING_PROVIDER_API_KEY` | Instagram/TikTok API key | Off by default |
| `DARKVIDEOS_DESKTOP=1` | Forces dry_run=false for real execution | Use for actual posts |
| `DARKVIDEOS_API_BASE` | Local API base URL | `http://127.0.0.1:8000` |
| `PUBLISHING_MEDIA_TMP_DIR` | Temporary media directory | `~/.local/share/dark-videos/media` |

## Reference Files Structure

The `references/` directory in this skill contains:

- `mining.md` - Connectors, synthetic samples, lookback widening
- `frame.md` - Framing and copy generation (one frame per video)
- `heat.md` - Heat scoring and top 20 ranking
- `publish.md` - Publishing dispatch and accounts
- `usage-and-verification.md` - Example usage and failure handling
- `provenance.md` - Provenance and source freshness
- `INDEX.md` - Skill INDEX and routing

## Performance Optimizations

- Cache TTL: status 5s, mining 10s, enqueue 3s
- Cache mining results for 10s to avoid redundant API calls
- yt-dlp fallback when YouTube API keys unavailable
- Lookback widening: 7 → 14 → 30 → 90 days
- Synthetic sample isolation (`.invalid` URLs, no real posts)

## Do Not Activate For

- New poster without proper connector configuration
- Scrapers that bypass YouTube Data API
- Instagram hashtag search (stays off by default)
- Any path that publishes outside dispatch
- Filling connector gaps with synthetic samples in real runs

## Token Discipline

- Read only the references notes needed for the current mission
- Cache TTL: status 5s, mining 10s, enqueue 3s
- Never expose credentials in logs or tool outputs
- Open only the mining, frame, heat, or publish note that the mission needs

## Example Use Cases

1. **Onboarding new developer**: Review this mapping to understand the codebase structure
2. **Debugging pipeline issues**: Identify which module/stage handles the problematic step
3. **Adding new platform connector**: Follow the pattern in `connectors/` directory
4. **Extending learning/JeV**: Review `learning/` module and `jev/` submodule
5. **Security review**: Examine `security/` module and vault implementation

## Provenance

- Original repository: `D:\Git\dark-videos`
- Mapped: Mon Oct 12 2026
- Mapping version: 3.0.0 (Full Alpha)
- Categories: development, architecture, pipeline, learning, security

---