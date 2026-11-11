# Ruby one-time release overrides (#344)

The intended initial major release PRs now exist. Remove their consumed `release-as` overrides so Release Please can calculate subsequent versions normally, as required by the SDK's local release rules. The change removes exactly five configuration keys; package versions and the release manifest are unchanged. Rollback: revert this cleanup PR.

| Package | Intended version | Existing release PR | Observed head |
| --- | --- | --- | --- |
| qubrics-core | 2.0.0 | #359 | 939db6e00d702ce7decd0ddb225149952449118e |
| qubrics-sending | 2.0.0 | #331 | 04562afd65f46b53cdde8f15f4fa07868578f550 |
| qubrics-mailbox | 3.0.0 | #332 | 55f1ff2a3bc3910d73ffa8104c9dbb1dde2ce266 |
| qubrics-management | 3.0.0 | #333 | 3410b0a62583ebd6e83290cad67017e64b2208fa |
| qubrics-sdk | 3.0.0 | #360 | 8b4ed6f024dfbd053328f28c452325dff9822b15 |

All five PRs carried `autorelease: pending` after the successful, operator-authorised relief rerun of Release Please run 42847017153, attempt 3, job 130284070076. The rerun updated normal bot branches, left main at 61889b3548d984cb8ad50eb1ece3a5651e1d847b and skipped every publication job. This is relief, not an origin fix for the unretained GitHub PATCH error response.

Validation: `git diff --check` exited 0; `pnpm test:release-state` exited 0 with 41 passed, zero failed/skipped/cancelled/todo. Raw log: MAIN `.claude/artifacts/rebrand-qubrics-sdk344/ruby-release-as-native.log`. The existing `.githooks/pre-commit` requires `pnpm drift:check` when creating this commit; its command log is `ruby-release-as-commit.log` in that same artifact directory. No hook is bypassed. No new test is needed for deleting these static one-time values.

`git diff --stat a326bc923fff448470d908bb527afaaa35f6d739 HEAD -- python/ packages/python/` is empty at the source base. This cleanup changes neither Python path. Fresh release heads still require their own normal default-guard qualification. This source PR neither publishes packages nor qualifies the refreshed release artifacts; #344 remains open until the operator publishes the exact approved artifacts and public readbacks pass.
