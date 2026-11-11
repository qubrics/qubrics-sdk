# Python core 2.0.0 release-head preparation (#344)

Current bot head: 02fd476f46ac7489368a027acb95b544aa1f0404, based on main 75acd6a64feafe14404aec10d591f73349181156. Ops authorised refreshing PR356 after sdk343's origin PR375 merged; main CI42961464785 passed34/34 and natural Release Please42961464736 succeeded with every publisher skipped. No merge, tag, registry change or publication is authorised until Ops relays GO. Source rollback: normal revert.

## Origin and refresh

The previous prepared56f6768e passed exact CI42957784360,34/34. Natural Release Please42958705212 subsequently rebuilt the bot branch from main, dropping six dependent-metadata changes (`rp-42958705212-natural-refresh.log:2477-2484`). A local successor03573ec4 restored the generated metadata and passed native41/41, mandatory drift and fresh default Skills acceptance. It was kept local while PR375 settled.

True comparison db66820b..02fd476f changes only four Windows-origin files. Python source and metadata are identical. Comparing bot db66820b with prepared03573ec4 shows the same six metadata lines plus tracked evidence. Current bot02fd already contains main75acd6a6; this preparation is its normal fast-forward successor. The earlier56f and035 branches remain reachable, with no force-push or rewritten remote history.

The existing native gate previously reproduced the actual obsolete range at `scripts/python-release-guardrails.mjs:120`: `sending/pyproject.toml must require qubrics-core >= 2.0.0,<3.0.0; found >= 1.3.1,<2.0.0` (`python-core-refresh-native-red.log:10`). Mailbox, management, sdk and mcp share that range. Current unprepared bot02fd has identical Python bytes, so the same diagnosed failure applies.

Canonical per local SDK AGENTS.md: prepare language-native dependency metadata on the actual release-PR state. Existing `pnpm generate:python`, then `pnpm generate:mcp`, updates five requirements to `>=2.0.0,<3.0.0` and regenerates MCP's pyproject provenance hash. No generated output is hand-edited. Core manifest/native version/changelog remain2.0.0 as selected by the bot; no other package version changes. No workflow, updater, pin, fork, assertion or release selection changes.

## Qualification and boundaries

Receipts live in MAIN `.claude/artifacts/rebrand-qubrics-sdk344/`; exact commit/check results live in task `python-core-release-qualification.md`.

- Prepared `python/` and `packages/python/` are byte-identical to green03573ec4 and56f6768e. Versus a326bc92: `python/` empty; `packages/python/` eight files,+25/-7. Python source/metadata changed from a326, so normal fresh SHA-bound Skills acceptance remains required.
- Run current native release checks, mandatory commit drift hook, live OpenAPI canary, native distributions/Twine, exact core publication selection and default released Skills guard against this refresh. Normal PR CI must pass at the exact pushed successor; final review sweep must settle before merge ASK.
- The earlier source206/206, installed309/309, six clean dependency cohorts and real core-pointer resolution receipts remain supporting evidence for identical Python inputs. Fresh current checks are recorded separately; no unchanged result is represented as newly run.
- PR356 changes core manifest/version/changelog to2.0.0 plus these six dependent metadata lines and this evidence file. Its eventual merge can trigger Release Please's `python-core-v2.0.0` release/tag and the protected core PyPI publication job; these remain separate approval gates.

Every PyPI/RubyGems publish and old-name pointer is operator-approved and operator-executed with exact versions/artifacts. Published versions cannot be reused; withdrawal is yank only, with no full rollback. RubyGems confirmation stays step1 of its future publication ASK. Go3294.0.0 remains held for #901/#902. #344 is not complete until public installation/smoke and all acceptance boxes are measured.
