#!/usr/bin/env node

import { execFileSync } from "node:child_process";
import { pythonPackages } from "./python-release-guardrails.mjs";

const generatedPackageDirs = [
  ...pythonPackages.map((name) => `packages/python/${name}/pyproject.toml`),
  "go/mailbox",
  "go/management",
  "go/sending",
  "packages/php/mailbox/src",
  "packages/php/management/src",
  "packages/php/sending/src",
  "packages/python/mailbox/qubrics/mailbox",
  "packages/python/management/qubrics/management",
  "packages/python/mcp/qubrics/mcp/openapi",
  "packages/python/mcp/qubrics/mcp/mcp-contract.json",
  "packages/python/sending/qubrics/sending",
  "packages/ruby/mailbox/lib/sendmux_mailbox_generated",
  "packages/ruby/mailbox/lib/sendmux_mailbox_generated.rb",
  "packages/ruby/management/lib/sendmux_management_generated",
  "packages/ruby/management/lib/sendmux_management_generated.rb",
  "packages/ruby/sending/lib/sendmux_sending_generated",
  "packages/ruby/sending/lib/sendmux_sending_generated.rb",
  "packages/ts/mailbox/src/generated",
  "packages/ts/management/src/generated",
  "packages/ts/sending/src/generated",
  "packages/ts/cli/src/generated",
  "rust/operation-decisions.json",
  "rust/src/generated/mod.rs",
];

const unstagedDiff = execFileSync("git", ["diff", "--name-status", "--", ...generatedPackageDirs], {
  encoding: "utf8",
});
const untracked = execFileSync("git", ["ls-files", "--others", "--exclude-standard", "--", ...generatedPackageDirs], {
  encoding: "utf8",
});

const drift = [unstagedDiff.trim(), untracked.trim()].filter(Boolean).join("\n");

if (drift) {
  throw new Error(
    [
      "Generated SDK package directories are stale.",
      drift,
      "Regenerate the SDKs from the current snapshots and stage or commit the resulting package changes.",
    ].join("\n"),
  );
}

console.log("Generated SDK package directories have no uncommitted drift.");
