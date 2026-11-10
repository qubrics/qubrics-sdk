import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, rmSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { checkRubyDependencyFloors } from "./check-ruby.mjs";

const root = mkdtempSync(join(tmpdir(), "qubrics-ruby-release-"));

try {
  for (const name of ["sending", "sdk"]) mkdirSync(join(root, "packages/ruby", name), { recursive: true });
  writeFileSync(join(root, ".release-please-manifest.json"), JSON.stringify({
    "packages/ruby/core": "1.3.0",
    "packages/ruby/mailbox": "1.4.0",
    "packages/ruby/management": "2.0.0",
    "packages/ruby/sending": "1.4.0",
  }));
  writeFileSync(join(root, "packages/ruby/sending/qubrics-sending.gemspec"), "spec.add_dependency 'qubrics-core', '>= 1.3.0', '< 2.0'\n");

  writeSdk(">= 2.0.0', '< 3.0");
  assert.doesNotThrow(() => checkRubyDependencyFloors({ root, changedPackages: new Set(["sdk"]) }));
  console.log("PASS: declared Management 2 floor accepts next-major 3 ceiling");

  for (const ceiling of ["2.0", "4.0"]) {
    writeSdk(`>= 2.0.0', '< ${ceiling}`);
    assert.throws(() => checkRubyDependencyFloors({ root, changedPackages: new Set(["sdk"]) }), /qubrics-management.*< 3\.0/);
  }
  writeSdk(">= 2.0.0");
  assert.throws(() => checkRubyDependencyFloors({ root, changedPackages: new Set() }), /explicit >= floor/);
  console.log("PASS: wrong and missing ceilings rejected");

  writeSdk(">= 1.3.0', '< 2.0");
  assert.doesNotThrow(() => checkRubyDependencyFloors({ root, changedPackages: new Set(["management"]) }));
  assert.throws(() => checkRubyDependencyFloors({ root, changedPackages: new Set(["sdk"]) }), /qubrics-management >= 2\.0\.0; found >= 1\.3\.0/);
  console.log("PASS: unchanged-package allowance and changed-package manifest floor retained");
} finally {
  rmSync(root, { recursive: true, force: true });
  console.log(JSON.stringify({ removed_fixture: root }));
}

function writeSdk(managementRange) {
  writeFileSync(join(root, "packages/ruby/sdk/qubrics-sdk.gemspec"), [
    "spec.add_dependency 'qubrics-core', '>= 1.3.0', '< 2.0'",
    "spec.add_dependency 'qubrics-mailbox', '>= 1.4.0', '< 2.0'",
    `spec.add_dependency 'qubrics-management', '${managementRange}'`,
    "spec.add_dependency 'qubrics-sending', '>= 1.4.0', '< 2.0'",
  ].join("\n"));
}
