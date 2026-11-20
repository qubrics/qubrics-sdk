# Exact-byte sendmux 1.0.0 publication preparation

Prepared under the operator's 20 November overnight reversible-only
instruction. No workflow dispatch, publication, tag, merge or registry
configuration change is authorised tonight.

## Cause and route

Canonical qubrics 1.0.0 was initially published via the registry API
using a regular token, not a trusted-publishing workflow. Its retained
HTTP 200 response reports creation at 07:37:11Z and trustpub_only=false;
public version metadata names roshanjonah and has trustpub_data=null.
By contrast, the single attempted sendmux 1.0.0 upload returned 403 with
the explicit Trusted Publishing-only policy error. No sendmux 1.0.0
index row exists. Do not infer that its saved publisher binding is absent.

The public publisher-list read also returns 403. The vendor's documented
endpoint checks authentication, TrustedPublishing scope and crate
ownership; the binding is not a publicly readable setting:
https://github.com/rust-lang/crates.io/blob/main/src/controllers/trustpub/github_configs/list.rs .
Vendor setup fields and the initial-token requirement are documented at
https://crates.io/docs/trusted-publishing .

Existing main 12d4901d release-please.yml:216–269 uses OIDC but is gated
on release/tag state, then runs cargo publish from rust/. It cannot
consume the retained pointer archive and must not be used as a substitute.

This separate workflow preserves those existing controls. PRs run only
offline validation. The publish job requires explicit workflow_dispatch,
main, the approved hash and the existing release environment's required
roshanjonah approval. It reuses the default Skills action and guards
the exact approved source 12d4901d before exchanging an OIDC credential.
No API token secret, fallback selector or rebuild is used.

## Exact archive and transport

File: release-pointers/cratesio/sendmux/sendmux-1.0.0.crate.
Bytes: 11,593. SHA-256:
0382c47cd5ae1b8afa20ecd59cf8e5218424f80786429603535a73b1d8dad802.
It is copied byte-for-byte from the approved archive, never regenerated.
Calendar client code: NO, by the previously qualified immutable contents.

The standard registry API envelope encodes metadata and the unchanged
archive using little-endian u32 lengths. Canonical transport:
https://doc.rust-lang.org/cargo/reference/registry-web-api.html .
The helper defaults to offline checking. Only --publish reads the public
index and submits one PUT, with bounded timeouts and zero retries. An
existing 1.0.0 row stops before upload. Ambiguous responses require public
readback before any further operator decision; no automatic repeat.

## Verification

Focused red: the new test failed because the uploader was absent
(FileNotFoundError). Green: one test checks the real approved archive's
encoded name/version/dependency and byte-exact embedded payload, and
proves both same-size byte mutation and truncation are refused. Default
CLI check succeeds without a token or network access. It prints the
approved 11,593-byte identity. A second test first failed on the absent
response validator, then proved HTTP-200 error envelopes and malformed
JSON are rejected; optional warnings remain optional per the vendor API.
Both tests pass. No authenticated publication test was run.

Independent spec and standards reviews found the initial guard-checkout
mismatch and missing HTTP-200 response validation. Both were corrected:
the guard uses a separate approved-source checkout through its existing
--repo interface, while the uploader retains the current fixed archive;
the new response test covers the second finding. No guard/workflow
fallback was added, and rejected or ambiguous responses never retry.

Raw receipts: SDK MAIN .claude/artifacts/rebrand-qubrics-sdk344/
rust-pointer-20261120/ (dispatch-test-red.log, retained canonical/upload
responses, vendor docs and public-config responses). Normal PR CI and
review results are recorded in the owner task receipt, not assumed here.

## Morning operator configuration

After return, inspect https://crates.io/crates/sendmux/settings as a
sendmux crate owner. Settings → Trusted Publishing: reuse an exact
matching GitHub publisher if present; otherwise Add → GitHub with:

- Repository owner: qubrics
- Repository name: qubrics-sdk
- Workflow filename: publish-sendmux-crate.yml
- Environment: release

Keep Trusted Publishing-only enabled and preserve existing publishers.
Do not configure or dispatch anything overnight. Source PR merge and
this binding must be complete before a separately authorised manual run.
Morning dispatch must enter the full approved SHA-256 above and the
operator must approve the protected release environment. Agent then
requires public 1.0.0 index/API checksum equality, public archive equality
and clean registry consumer proof; it must not repeat an upload blindly.

Preparation rollback: revert this PR. Public-version rollback: yank only
on a new named approval; the same version can never be reused. The exact
qubrics=1.0.0 dependency follow-up remains parked, unchanged.
