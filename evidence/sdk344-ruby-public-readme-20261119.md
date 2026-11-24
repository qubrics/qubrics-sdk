# Ruby public package facts

The root README now lists the published Ruby Core and Management packages,
their install commands and their `Qubrics` require paths. Sending, Mailbox
and SDK install commands retain their published `sendmux-*` names.
The source targets are labelled separately from published packages.

## Public sources

The #344 owner verified the exact version APIs, downloaded archives and
fresh public-registry installs on 19 November 2026. Each API reports the
listed version and an unyanked archive.

| RubyGems package | Version | Bytes | SHA256 |
| --- | --- | ---: | --- |
| [qubrics-core](https://rubygems.org/api/v2/rubygems/qubrics-core/versions/2.0.0.json) | 2.0.0 | 10,240 | `736fd1ed4c613f8dfe5c2cc4f81741c5e42f18bb19dd44aeffd4163b71971e79` |
| [sendmux-core](https://rubygems.org/api/v2/rubygems/sendmux-core/versions/2.0.0.json) | 2.0.0 | 4,096 | `640bf5767f7d8c69d908e04af968d74f63413880141173ca3a3f4b4ef5205ccb` |
| [qubrics-management](https://rubygems.org/api/v2/rubygems/qubrics-management/versions/3.0.0.json) | 3.0.0 | 108,544 | `2592ef7db9e878dda6af5a0c6e7478d06ac166f8288b66dbdbfc0b943f655a9c` |
| [sendmux-management](https://rubygems.org/api/v2/rubygems/sendmux-management/versions/3.0.0.json) | 3.0.0 | 4,096 | `7ae4a7bb2ab735a2d38745446520df4b2a2aa6169f5d1e144db8b921a5643436` |

Owner receipts: `ruby-core-public-20261119.md`,
`ruby-core-pointer-public-20261119.md`, `ruby-management-public-20261119.md`
and `ruby-management-pointer-public-20261119.md` under the task's local
`.claude/tasks/rebrand-qubrics-sdk344/` directory. Raw downloaded archives,
version API responses and install/smoke logs remain under the matching
`.claude/artifacts/rebrand-qubrics-sdk344/` subdirectories.

Isolated public consumers verified `require 'qubrics/core'` and
`require 'qubrics/management'`, Core 2.0.0 and Management 3.0.0 constants,
native dependency resolution and the Management default URL
`https://app.qubrics.com/api/v1`. Both old-name packages resolve the matching
replacement. Their metadata contains no post-install message.

## Scope and validation

Base: immutable main `e8d46fa2f91ece4ebab28c7e8ca51e6f1d53b5fa`.
Only README facts and this evidence file change. No package source,
workflow, registry, tag, queue or environment change is included.
The Ruby Sending, Mailbox and SDK targets remain unpublished.
No move announcement or deprecation message was added.

Validation: `git diff --check` exits 0. Ruby Sending, Mailbox and SDK package
rows and install commands are unchanged. Public package identifiers,
versions and require paths match the owner receipts. Documentation-only
scope requires no package build or runtime test rerun.

Polish: fresh-reader critique's applicable rubric lines pass after one
ambiguous sentence was split and clarified. One humanize pass and the
protected-token check passed. Local receipt:
`.claude/artifacts/rebrand-qubrics-sdk344/ruby-readme-polish-20261119.md`.

Status: documentation candidate only, not merged. Public proof is
12/24 original PyPI/RubyGems identities and Ruby 4/10, not completion of #344.
All publication, queue and tag holds remain in force.
