import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, rmSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import {
  checkPythonLangchainDependencyFloors,
  checkPythonMcpDependencyFloors,
  checkPythonSdkDependencyFloors,
  checkPythonSurfaceDependencyFloors,
  readChangedPythonPackages,
} from "./python-release-guardrails.mjs";

const root = mkdtempSync(join(tmpdir(), "sendmux-python-release-"));

try {
  assert.deepEqual(
    [...readChangedPythonPackages({ env: { PYTHON_PATHS_RELEASED: '["packages/python/langchain"]' } })],
    ["langchain"],
  );
  assert.deepEqual(
    [...readChangedPythonPackages({ env: { PYTHON_CHANGED_PACKAGES: "langchain" } })],
    ["langchain"],
  );

  writeFixture({
    manifest: {
      "packages/python/core": "1.2.0",
      "packages/python/mailbox": "1.0.4",
      "packages/python/management": "1.0.4",
      "packages/python/sending": "1.2.0",
    },
    sdkDependencies: [
      '"qubrics-core>=1.2.0,<2.0.0"',
      '"qubrics-mailbox>=1.0.4,<2.0.0"',
      '"qubrics-management>=1.0.4,<2.0.0"',
      '"qubrics-sending>=1.1.0,<2.0.0"',
    ],
    mcpDependencies: ['"qubrics-core>=1.1.0,<2.0.0"'],
  });

  assert.doesNotThrow(() =>
    checkPythonSdkDependencyFloors({ root, changedPackages: new Set(["sending"]) }),
  );
  assert.throws(
    () => checkPythonSdkDependencyFloors({ root, changedPackages: new Set(["sdk"]) }),
    /qubrics-sending >= 1\.2\.0,<2\.0\.0; found >= 1\.1\.0,<2\.0\.0/,
  );
  assert.doesNotThrow(() => checkPythonMcpDependencyFloors({ root, changedPackages: new Set(["core"]) }));
  assert.throws(
    () => checkPythonMcpDependencyFloors({ root, changedPackages: new Set(["mcp"]) }),
    /qubrics-core >= 1\.2\.0,<2\.0\.0; found >= 1\.1\.0,<2\.0\.0/,
  );

  writeFixture({
    manifest: {
      "packages/python/core": "1.2.0",
      "packages/python/mailbox": "1.1.0",
      "packages/python/management": "1.0.4",
      "packages/python/sending": "1.2.0",
    },
    sdkDependencies: [
      '"qubrics-core>=1.2.0,<2.0.0"',
      '"qubrics-mailbox>=1.1.0,<2.0.0"',
      '"qubrics-management>=1.0.4,<2.0.0"',
      '"qubrics-sending>=1.3.0,<2.0.0"',
    ],
    mcpDependencies: ['"qubrics-core>=1.2.0,<2.0.0"'],
  });

  assert.throws(
    () => checkPythonSdkDependencyFloors({ root, changedPackages: new Set(["sdk"]) }),
    /qubrics-sending >= 1\.2\.0,<2\.0\.0; found >= 1\.3\.0,<2\.0\.0/,
  );

  writeFixture({
    manifest: {
      "packages/python/core": "1.2.0",
      "packages/python/mailbox": "1.1.0",
      "packages/python/management": "1.0.4",
      "packages/python/sending": "1.2.0",
    },
    sdkDependencies: [
      '"qubrics-core>=1.2.0,<2.0.0"',
      '"qubrics-mailbox>=1.1.0,<2.0.0"',
      '"qubrics-management>=1.0.4,<2.0.0"',
      '"qubrics-sending>=1.2.0,<2.0.0"',
    ],
    mcpDependencies: ['"qubrics-core>=1.2.0,<2.0.0"'],
  });

  assert.doesNotThrow(() => checkPythonSdkDependencyFloors({ root, changedPackages: new Set(["sdk"]) }));
  assert.doesNotThrow(() => checkPythonMcpDependencyFloors({ root, changedPackages: new Set(["mcp"]) }));

  writeFixture({
    manifest: {
      "packages/python/core": "1.2.0",
      "packages/python/mailbox": "2.0.0",
      "packages/python/management": "1.0.4",
      "packages/python/sending": "1.2.0",
    },
    sdkDependencies: [
      '"qubrics-core>=1.2.0,<2.0.0"',
      '"qubrics-mailbox>=2.0.0,<3.0.0"',
      '"qubrics-management>=1.0.4,<2.0.0"',
      '"qubrics-sending>=1.2.0,<2.0.0"',
    ],
    mcpDependencies: ['"qubrics-core>=1.2.0,<2.0.0"'],
  });

  assert.doesNotThrow(() => checkPythonSdkDependencyFloors({ root, changedPackages: new Set(["sdk"]) }));

  for (const invalidMailboxRange of [
    '"qubrics-mailbox>=2.0.0"',
    '"qubrics-mailbox>=2.0.0,<4.0.0"',
    '"qubrics-mailbox>=2.0.0,<2.0.0"',
  ]) {
    writeFixture({
      manifest: {
        "packages/python/core": "1.2.0",
        "packages/python/mailbox": "2.0.0",
        "packages/python/management": "1.0.4",
        "packages/python/sending": "1.2.0",
      },
      sdkDependencies: [
        '"qubrics-core>=1.2.0,<2.0.0"',
        invalidMailboxRange,
        '"qubrics-management>=1.0.4,<2.0.0"',
        '"qubrics-sending>=1.2.0,<2.0.0"',
      ],
      mcpDependencies: ['"qubrics-core>=1.2.0,<2.0.0"'],
    });
    assert.throws(
      () => checkPythonSdkDependencyFloors({ root, changedPackages: new Set(["sdk"]) }),
      /qubrics-mailbox with an explicit >= floor and <3\.0\.0 upper bound.*>=2\.0\.0,<3\.0\.0/,
    );
  }

  writeFixture({
    manifest: {
      "packages/python/core": "1.2.0",
      "packages/python/mailbox": "2.0.0",
      "packages/python/management": "1.0.4",
      "packages/python/sending": "1.2.0",
    },
    sdkDependencies: [
      '"qubrics-core>=1.2.0,<2.0.0"',
      '"qubrics-mailbox>=1.1.0,<2.0.0"',
      '"qubrics-management>=1.0.4,<2.0.0"',
      '"qubrics-sending>=1.2.0,<2.0.0"',
    ],
    mcpDependencies: ['"qubrics-core>=1.2.0,<2.0.0"'],
  });

  assert.doesNotThrow(() => checkPythonSdkDependencyFloors({ root, changedPackages: new Set(["mailbox"]) }));
  assert.throws(
    () => checkPythonSdkDependencyFloors({ root, changedPackages: new Set(["sdk"]) }),
    /qubrics-mailbox >= 2\.0\.0,<3\.0\.0; found >= 1\.1\.0,<2\.0\.0/,
  );

  writeFixture({
    manifest: {
      "packages/python/core": "1.2.0",
      "packages/python/mailbox": "1.1.0",
      "packages/python/management": "1.0.4",
      "packages/python/sending": "1.2.0",
    },
    sdkDependencies: [
      '"qubrics-core>=1.2.0,<2.0.0"',
      '"qubrics-mailbox>=1.1.0"',
      '"qubrics-management>=1.0.4,<2.0.0"',
      '"qubrics-sending>=1.2.0,<2.0.0"',
    ],
    mcpDependencies: ['"qubrics-core>=1.2.0,<2.0.0"'],
  });

  assert.throws(
    () => checkPythonSdkDependencyFloors({ root, changedPackages: new Set(["sending"]) }),
    /qubrics-mailbox with an explicit >= floor and <2\.0\.0 upper bound/,
  );

  assert.deepEqual(
    [...readChangedPythonPackages({ env: { PYTHON_CHANGED_PACKAGES: "sending, sdk" } })].sort(),
    ["sdk", "sending"],
  );
  assert.deepEqual(
    [
      ...readChangedPythonPackages({
        env: { PYTHON_PATHS_RELEASED: '["packages/python/mailbox","packages/ts/cli"]' },
      }),
    ],
    ["mailbox"],
  );
  assert.throws(
    () => readChangedPythonPackages({ root, env: { GITHUB_BASE_REF: "main" } }),
    /Could not determine changed files for Python release guardrails/,
  );

  for (const surface of ["sending", "mailbox", "management"]) {
    const surfaceErrorPattern = new RegExp(
      `${surface}[\\\\/]pyproject\\.toml must require qubrics-core`,
    );
    assert.match(
      `C:\\repo\\packages\\python\\${surface}\\pyproject.toml must require qubrics-core`,
      surfaceErrorPattern,
    );
    writeFixture({
      manifest: {
        "packages/python/core": "1.3.1",
        "packages/python/mailbox": "1.1.0",
        "packages/python/management": "1.0.4",
        "packages/python/sending": "1.5.1",
      },
      surfaceCoreDependencies: {
        sending: '"qubrics-core>=1.3.1,<2.0.0"',
        mailbox: '"qubrics-core>=1.3.1,<2.0.0"',
        management: '"qubrics-core>=1.3.1,<2.0.0"',
        [surface]: '"qubrics-core>=1.3.0,<2.0.0"',
      },
    });
    assert.throws(
      () => checkPythonSurfaceDependencyFloors({ root, changedPackages: new Set([surface]) }),
      new RegExp(`${surfaceErrorPattern.source} >= 1\\.3\\.1,<2\\.0\\.0`),
    );
    assert.doesNotThrow(() =>
      checkPythonSurfaceDependencyFloors({ root, changedPackages: new Set([surface === "sending" ? "mailbox" : "sending"]) }),
    );

    writeFixture({
      manifest: {
        "packages/python/core": "1.3.1",
        "packages/python/mailbox": "1.1.0",
        "packages/python/management": "1.0.4",
        "packages/python/sending": "1.5.1",
      },
      surfaceCoreDependencies: {
        sending: '"qubrics-core>=1.3.1,<2.0.0"',
        mailbox: '"qubrics-core>=1.3.1,<2.0.0"',
        management: '"qubrics-core>=1.3.1,<2.0.0"',
      },
    });
    assert.doesNotThrow(() =>
      checkPythonSurfaceDependencyFloors({ root, changedPackages: new Set([surface]) }),
    );

    for (const invalidRange of ['"qubrics-core>=1.3.1"', '"qubrics-core>=1.3.1,<3.0.0"']) {
      writeFixture({
        manifest: {
          "packages/python/core": "1.3.1",
          "packages/python/mailbox": "1.1.0",
          "packages/python/management": "1.0.4",
          "packages/python/sending": "1.5.1",
        },
        surfaceCoreDependencies: {
          sending: '"qubrics-core>=1.3.1,<2.0.0"',
          mailbox: '"qubrics-core>=1.3.1,<2.0.0"',
          management: '"qubrics-core>=1.3.1,<2.0.0"',
          [surface]: invalidRange,
        },
      });
      assert.throws(
        () => checkPythonSurfaceDependencyFloors({ root, changedPackages: new Set([surface]) }),
        new RegExp(`${surfaceErrorPattern.source} with an explicit >= floor and <2\\.0\\.0 upper bound`),
      );
    }
  }

  writeFixture({
    manifest: {
      "packages/python/sending": "1.5.1",
      "packages/python/mailbox": "2.0.0",
    },
    langchainDependencies: [
      '"qubrics-sending>=1.5.1,<2.0.0"',
      '"qubrics-mailbox>=2.0.0,<3.0.0"',
    ],
  });
  assert.doesNotThrow(() =>
    checkPythonLangchainDependencyFloors({ root, changedPackages: new Set(["langchain"]) }),
  );

  writeFixture({
    manifest: {
      "packages/python/sending": "1.5.1",
      "packages/python/mailbox": "2.0.0",
    },
    langchainDependencies: [
      '"qubrics-sending>=1.5.0,<2.0.0"',
      '"qubrics-mailbox>=2.0.0,<3.0.0"',
    ],
  });
  assert.throws(
    () => checkPythonLangchainDependencyFloors({
      root,
      changedPackages: readChangedPythonPackages({ env: { PYTHON_CHANGED_PACKAGES: "langchain" } }),
    }),
    /qubrics-sending >= 1\.5\.1,<2\.0\.0; found >= 1\.5\.0,<2\.0\.0/,
  );

  writeFixture({
    manifest: {
      "packages/python/sending": "1.5.1",
      "packages/python/mailbox": "2.0.0",
    },
    langchainDependencies: [
      '"qubrics-sending>=1.5.1,<2.0.0"',
      '"qubrics-mailbox>=1.5.0,<2.0.0"',
    ],
  });
  assert.throws(
    () => checkPythonLangchainDependencyFloors({
      root,
      changedPackages: readChangedPythonPackages({
        env: { PYTHON_PATHS_RELEASED: '["packages/python/langchain"]' },
      }),
    }),
    /qubrics-mailbox >= 2\.0\.0,<3\.0\.0; found >= 1\.5\.0,<2\.0\.0/,
  );

  assert.doesNotThrow(() =>
    checkPythonLangchainDependencyFloors({ root, changedPackages: new Set(["mailbox"]) }),
  );

  console.log("Python release guardrail tests passed.");
} finally {
  rmSync(root, { force: true, recursive: true });
}

function writeFixture({ manifest, sdkDependencies = [], mcpDependencies = [], surfaceCoreDependencies = {}, langchainDependencies = [] }) {
  mkdirSync(join(root, "packages", "python", "sdk"), { recursive: true });
  mkdirSync(join(root, "packages", "python", "mcp"), { recursive: true });
  mkdirSync(join(root, "packages", "python", "langchain"), { recursive: true });
  for (const surface of ["sending", "mailbox", "management"]) {
    mkdirSync(join(root, "packages", "python", surface), { recursive: true });
    writeFileSync(
      join(root, "packages", "python", surface, "pyproject.toml"),
      `dependencies = [\n  ${surfaceCoreDependencies[surface] ?? '"qubrics-core>=1.2.0,<2.0.0"'}\n]\n`,
    );
  }
  writeFileSync(join(root, ".release-please-manifest.json"), `${JSON.stringify(manifest)}\n`);
  writeFileSync(
    join(root, "packages", "python", "sdk", "pyproject.toml"),
    `dependencies = [\n  ${sdkDependencies.join(",\n  ")}\n]\n`,
  );
  writeFileSync(
    join(root, "packages", "python", "mcp", "pyproject.toml"),
    `dependencies = [\n  ${mcpDependencies.join(",\n  ")}\n]\n`,
  );
  writeFileSync(
    join(root, "packages", "python", "langchain", "pyproject.toml"),
    `dependencies = [\n  ${langchainDependencies.join(",\n  ")}\n]\n`,
  );
}
