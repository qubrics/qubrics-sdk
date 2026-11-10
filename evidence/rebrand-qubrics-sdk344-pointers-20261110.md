# SDK #344: final old-name pointer metadata

Status: source candidate, unmerged and unpublished. No public installation or #344 acceptance box is claimed. Registry ownership inspection remains on Ops' sign-in HOLD. Every PyPI/RubyGems and old-name pointer publication requires a separate operator-only exact-artifact/version ASK.

A18 requires each final old-name distribution to depend on its replacement, with a Python Inactive classifier or Ruby post-install deprecation message. Ops settled each final pointer at the SAME next-major version as its replacement, per [SemVer 2.0.0 item 8](https://semver.org/spec/v2.0.0.html#spec-item-8) and A10/A18. This avoids silently moving ~= / ~> pinned users across a breaking replacement.

| Registry | Final old-name release | Replacement dependency |
| --- | --- | --- |
| PyPI | sendmux-core 2.0.0 | qubrics-core >=2.0.0,<3.0.0 |
| PyPI | sendmux-sdk 4.0.0 | qubrics-sdk >=4.0.0,<5.0.0 |
| PyPI | sendmux-mailbox 3.0.0 | qubrics-mailbox >=3.0.0,<4.0.0 |
| PyPI | sendmux-management 3.0.0 | qubrics-management >=3.0.0,<4.0.0 |
| PyPI | sendmux-sending 2.0.0 | qubrics-sending >=2.0.0,<3.0.0 |
| PyPI | sendmux-mcp 3.0.0 | qubrics-mcp >=3.0.0,<4.0.0 |
| PyPI | langchain-sendmux 1.0.0 | langchain-qubrics >=1.0.0,<2.0.0 |
| RubyGems | sendmux-core 2.0.0 | qubrics-core >=2.0.0,<3.0 |
| RubyGems | sendmux-sdk 3.0.0 | qubrics-sdk >=3.0.0,<4.0 |
| RubyGems | sendmux-mailbox 3.0.0 | qubrics-mailbox >=3.0.0,<4.0 |
| RubyGems | sendmux-management 3.0.0 | qubrics-management >=3.0.0,<4.0 |
| RubyGems | sendmux-sending 2.0.0 | qubrics-sending >=2.0.0,<3.0 |

The final pointers contain metadata only. A18 specifies the new `qubrics` import namespace and `Qubrics` module; it does not require legacy import bridges. Historical releases remain immutable and retain their existing import surfaces. A17 wire/environment compatibility stays in the replacement packages. No extra distribution named `qubrics` is needed for a native namespace.

Canonical package configuration follows existing Hatchling and RubyGems conventions. [Hatch wheel options](https://hatch.pypa.io/latest/plugins/builder/wheel/) document `bypass-selection` for empty metadata-only wheels. Python uses the official [Inactive classifier](https://pypi.org/classifiers/). Ruby uses the native [add_dependency and post_install_message fields](https://guides.rubygems.org/specification-reference/). No new build harness, publisher, alias source, generator or CI job was added.

Native `python -m build` produced seven sdists and seven wheels. The first Twine check rejected Hatch's default core metadata 2.5 because the existing Twine 6.1.0 did not support it; explicit metadata 2.4 on both targets, matching existing packages, removed the cause. Rebuilt Python artifacts passed `python -m twine check` 14/14, exit 0. Native `gem build` produced all five gems, exit 0; its `no files specified` warning reflects the intentional metadata-only payload. Native archive and gem metadata inspection confirmed versions, replacement bounds, classifier/message and empty runtime payloads. Metadata copy received the required fresh-reader critique, one humanize pass and protected-token check.

Commands used the existing Python environment and Ruby 3.4.1 through `pnpm exec`; exact commands, tool output and canonical citations are in MAIN `.claude/artifacts/rebrand-qubrics-sdk344/pointers/receipt.md`. Raw receipts there: `python-build.log`, `ruby-build.log`, `twine-check-red.log`, `twine-check.log`, `python-wheel-metadata.log`, `python-sdist-metadata.log`, `ruby-metadata.log`. Build scratch and pip caches were removed and absence verified; artifacts needed for the open publication item remain in its `pypi/` and `rubygems/` directories.

Full dependency-resolution installs and Ruby post-install output proof are BLOCKED until replacement target-version artifacts are available. No fake replacements or ignored-dependency installs were used. Account authority, exact replacement release artifacts, merged-source verification and every public publish/install/smoke remain outstanding. Published PyPI/RubyGems versions cannot be reused; yank only. No publication action is authorised by this evidence.

Independent Spec and Standards reviews of all twelve metadata files found zero documented breaches, zero scoped Spec findings and zero actionable baseline smells. Reviews did not rerun green checks. Receipts: MAIN `.claude/artifacts/rebrand-qubrics-sdk344/pointers/spec-review.md` and `standards-review.md`.

Go source PR367 merged at `8dbf3bff`; its Release Please run `42812439562` passed and refreshed existing PR329 to `go 4.0.0` at `76308e8d`, still open with auto-merge off. All publication/recovery jobs skipped. Existing release rules require removing one-time `release-as` immediately after the intended initial release PR exists; this change removes only that Go override. The original `feat(go)!` source commit `8de0a05c` retains the major-release intent. No release PR was merged and no tag or registry publish was run.
