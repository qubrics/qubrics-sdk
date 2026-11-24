# Ruby SDK 3.0.0 native qualification

Prepared 2026-11-19 19:23 AEDT on `agent/sdk344-ruby-sdk-recut-20261119` in `/Users/rj/Desktop/GIT-REPOS/sendmux-sdk-sdk344-ruby-sdk-recut-20261119`, based on `a0ef57d431959257ddb2da30cee6b6e941fba9d3`.

Goal: Prepare Ruby SDK 3.0.0 source and a frozen native gem for root integration, without publication.
Tally: One preparation slice fixed locally, zero shipped by this lane. Shared #344 task ledger remains root-owned and read-only here.

## Source and authority

- `packages/ruby/sdk/lib/qubrics/sdk/version.rb:5`: version `3.0.0`.
- `packages/ruby/sdk/README.md:25`: removed the temporary unpublished-install sentence for the eventual artifact. Existing install command, Gemfile constraint, API examples and migration guidance remain unchanged.
- Canonical per `packages/ruby/sdk/qubrics-sdk.gemspec:3,6,19,21-24`: gem version comes from the version file, archive contains `lib/**/*.rb` plus README/changelog/licence, and existing dependency bounds are Core 2, Sending 2, Mailbox 3, Management 3. No runtime helper or gemspec edit was needed.
- Root alone owns `.release-please-manifest.json`, `Gemfile.lock`, all gemspecs and floors. They are unchanged in this lane. Root must align SDK release/lock metadata before source release gates. `Gemfile.lock` at proof: SHA256 `9338026cd03396e10d262dbff4cee78ebcfd31688fee2cefa5aea7e3a3f9c08e`.

## Frozen gem and inputs

Artifact root: `/Users/rj/Desktop/GIT-REPOS/sendmux-sdk/.claude/artifacts/rebrand-qubrics-sdk344/ruby-sdk-recut-20261119/`.

| Role | Exact file | Bytes | SHA256 |
| --- | --- | ---: | --- |
| SDK candidate | `ruby-sdk-recut-20261119/gems/qubrics-sdk-3.0.0.gem` | 9216 | `622b6aeacb5b069a6c2f3fc7bc02763b17a9478b0a2b2e0e6233a65e29e4dd91` |
| Local Sending input | `ruby-sending-b7dad6ca-20261119/gems/qubrics-sending-2.0.0.gem` | 36352 | `8dd5350aebf55dd588cc2c350dc906c3bb635f608b20dc7f71f0774455bee462` |
| Local Mailbox input | `ruby-mailbox-live-20261119/gems/qubrics-mailbox-3.0.0.gem` | 110592 | `7577dd99a64aebaac44c517943ca84bc8fd1058ca8b03ff5e9cd692d6226d602` |
| Fresh public Core input | `inputs/qubrics-core-2.0.0.gem` (download removed after proof) | 10240 | `736fd1ed4c613f8dfe5c2cc4f81741c5e42f18bb19dd44aeffd4163b71971e79` |
| Fresh public Management input | `inputs/qubrics-management-3.0.0.gem` (download removed after proof) | 108544 | `2592ef7db9e878dda6af5a0c6e7478d06ac166f8288b66dbdbfc0b943f655a9c` |

Candidate and local input paths in the table are relative to MAIN `.claude/artifacts/rebrand-qubrics-sdk344/`; public input paths are relative to this artifact root. Public Core and Management were freshly downloaded from RubyGems, matched API/expected SHA256, and were unyanked. See `public-input-proof.log` and retained `inputs/*-public.json`.

Read-only `https://rubygems.org/api/v2/rubygems/qubrics-sdk/versions/3.0.0.json` returned HTTP 404. See `sdk-public-status.log` and `sdk-public-response.txt`. Absence is a measurement, not a reservation or publication permission.

## Native proof

Existing rbenv Ruby `3.4.1` (`arm64-darwin24`) only. Every gem install used isolated `GEM_HOME` and `GEM_PATH` at this artifact root's `consumer/`. No source load-path substitution, machine setup or global install. `minitest 5.27.0` was installed only as an isolated development test dependency, not added to the SDK runtime dependencies.

| Check | Command / scope | Exit and result | Log |
| --- | --- | --- | --- |
| Native build | `RBENV_VERSION=3.4.1 rbenv exec gem build qubrics-sdk.gemspec --output <artifact>/gems/qubrics-sdk-3.0.0.gem` with isolated gem env | 0; actual SDK 3.0.0 gem built | `build.log` |
| Clean install | `gem install --no-document` of fresh public Core/Management and exact local Sending/Mailbox/SDK gem files under isolated env | 0; five Qubrics gems plus six transitive gems | `install.log` |
| Existing native tests | Installed `qubrics/sdk` plus `ruby -Ipackages/ruby/tests` loading `test_core.rb`, `test_environment.rb`, `test_oauth_retry.rb` | 0; 30 runs, 213 assertions, 0 failures, 0 errors, 0 skips | `native-tests.log` |
| Installed/source runtime bytes | Every installed Qubrics `.rb` runtime file compared byte-for-byte with matching source | 0; Core 9, Sending 41, Mailbox 163, Management 156, SDK 2; total 371 | `runtime-proof.log` |
| Defaults and SDK alias | Instantiate all three SDK clients using fixture keys, inspect `/openapi.json` request URL and `Qubrics::Sdk` alias | 0; Sending `https://smtp.qubrics.com/api/v1/openapi.json`, Mailbox/Management `https://app.qubrics.com/api/v1/openapi.json`; alias exact | `runtime-proof.log` |
| Resolved versions and bounds | Installed SDK runtime dependency bounds and gem versions plus all five `Qubrics::*::VERSION` constants | 0; SDK 3.0.0, Core/Sending 2.0.0, Mailbox/Management 3.0.0; exact existing floor/next-major ceiling matches | `runtime-proof.log`, `version-constants.log` |
| Archive/source equality | Read built gem's `data.tar.gz`, compare complete member set and bytes with source | 0; all five archive members equal source, including README/changelog/version | `archive-source-equality.log` |
| Existing floor gate | `pnpm exec node --input-type=module` invoking exported `checkRubyDependencyFloors({changedPackages:new Set(["sdk"])})` | 0; existing floor/ceiling gate passes | `dependency-floor-gate.log` |
| Syntax and diff | `RBENV_VERSION=3.4.1 rbenv exec ruby -c packages/ruby/sdk/lib/qubrics/sdk/version.rb`; `git diff --check` | 0; `Syntax OK`, no whitespace errors | `syntax.log`; command exit |

All native proof applies to this uncommitted three-file source diff at the base commit and lock hash above. Runtime test imports were checked to resolve from isolated installed gem paths. Installed gem cache SHA256 values also matched all five exact input files. No tests were added, changed, removed or skipped; no new harness was created.

## Documentation pass

## Handoff and limits

Root integration aligns the shared manifest and native SDK version at
3.0.0. Official `RBENV_VERSION=3.4.1 rbenv exec bundle lock --local` changes
only the SDK's resolved version from 2.0.0 to 3.0.0; all existing dependency
floors, other versions and Ruby 3.4.12 lock requirement remain unchanged.
Neither the lock nor manifest is packaged, so the exact frozen archive
and its source-byte proof remain unchanged. Source undo is normal revert.
Fresh exact-head CI/default acceptance still remain required; no release
approval follows from source preparation.

Initial preparation status: local and unpublished; that isolated proof made no external writes, commit, push, PR, CI dispatch, merge, tag, queue, environment approval or upload. Root integration below owns the remaining source and release gates.

Default Skills v2.0.5 is missing 15 producer contract reviews, already routed by root to skills34. No default retry, pin or fallback was attempted. Default acceptance and exact-head CI remain pending. Native Ruby 3.4.1 proof is not CI Ruby 3.4.12 proof. Full polyglot/release checks were outside this isolated authorised slice.

Consumer/transitive caches and duplicate public gem downloads are removed after proof, with absence verified before `cleanup.log` records the retained gem hash. The first forced-remove command was rejected by the command guard; its named safer non-forced removal succeeded. No source check failed or source correction occurred. Frozen SDK gem, logs and public JSON metadata remain. Exact source write leases are released at handoff. No source/worktree cleanup or root-owned state mutation.

## Default acceptance and cache-enabled source refresh

Root integration committed SDK version 3.0.0, matching shared manifest and
official native lock, at `e8456759d4e99f5a039de5fcc5cc08ffc7d49d51`.
Independent Spec and Standards reviews reported zero findings each.
The unchanged default selector downloaded latest Skills v2.0.6 at
`9e2659c9dba3efd943190f2541016d0548db7201`, verified the actual released
receipt and accepted all 22 results on that exact SDK head, including live
OpenAPI equality. Candidate digest:
`df4ce32a2055e42e63405f8b36367a0eb2b73b45afa8ffde2ae182f47b6e19bf`.
Raw MAIN artifacts: `default-v206-sdk/receipts/` and
`default-v206-b25a7cbc/sdk-guard.log`. No workflow pin or fallback.

## Public dependencies and README refresh, 19 November 2026

The root README now lists the publicly available Sending and Mailbox names,
install commands and publication status. It keeps the umbrella SDK on the
published legacy name until a separate SDK publication. Package source and
the frozen 9,216-byte SDK archive remain unchanged from `a9078236`.
Fresh exact-head CI/default acceptance and source merge/main gates remain
required after this documentation update. No tag, queue, environment or
publication action is authorised by this evidence.

## 20 November source refresh
