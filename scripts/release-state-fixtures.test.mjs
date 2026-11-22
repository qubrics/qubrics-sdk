import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { cpSync, existsSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import test from "node:test";
import { PythonReleaseNotes } from "./python-release-notes.mjs";
import { PullRequestBody } from "release-please/build/src/util/pull-request-body.js";
import { Changelog } from "release-please/build/src/updaters/changelog.js";
import { Version } from "release-please/build/src/version.js";

const repository = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const readJson = (path) => JSON.parse(readFileSync(path, "utf8"));
const editJson = (path, edit) => { const value = readJson(path); edit(value); writeFileSync(path, JSON.stringify(value)); };

function fixture(run) {
  const root = mkdtempSync(join(tmpdir(), "sendmux-release-state-"));
  try {
    for (const path of ["packages", "go/go.mod", "rust/Cargo.toml", "rust/ci/floor-consumer/Cargo.lock", "release-please-config.json", ".release-please-manifest.json", ".ruby-version"]) {
      if (!existsSync(join(repository, path))) continue;
      cpSync(join(repository, path), join(root, path), { recursive: true, filter: (source) => !/node_modules|vendor|\.venv|__pycache__|\/dist(?:\/|$)/.test(source) && (!/\.[^/]+$/.test(source) || /(?:package\.json|pyproject\.toml|Cargo\.toml|Cargo\.lock|go\.mod|composer\.json|\.gemspec|version\.rb|__init__\.py|release-please.*\.json|\.ruby-version)$/.test(source)) });
    }
    run(root);
  } finally {
    rmSync(root, { recursive: true, force: true });
    assert.equal(existsSync(root), false);
    console.log(`release fixture ${root} absent`);
  }
}

function check(root) {
  const child = spawnSync(process.execPath, [join(repository, "scripts/release-state.test.mjs"), "--root", root], { encoding: "utf8", timeout: 30_000 });
  assert.ok(child.pid);
  assert.throws(() => process.kill(child.pid, 0), { code: "ESRCH" });
  console.log(`release checker child ${child.pid} ESRCH`);
  for (const line of child.stdout.split("\n")) if (line.startsWith("Ruby metadata child ")) console.log(line);
  assert.equal(child.error, undefined);
  return child;
}

const rustConsumerLockEntry = /^name = "qubrics"\nversion = "([^"]+)"$/m;

function mutateNativeVersion(root, file, pattern) {
  const path = join(root, file);
  const before = readFileSync(path, "utf8");
  const match = before.match(pattern);
  assert.ok(match, `${file} must contain a native version`);
  const version = match[1];
  const changed = before.replace(pattern, (field) => field.replace(version, version === "0.0.0" ? "0.0.1" : "0.0.0"));
  assert.notEqual(changed, before, `${file} version mutation must change native bytes`);
  writeFileSync(path, changed);
}

const mutations = {
  "typescript version": (root) => editJson(join(root, "packages/ts/core/package.json"), (p) => { p.version = "0.0.0"; }),
  "python version": (root) => mutateNativeVersion(root, "packages/python/core/pyproject.toml", /^version = "([^"]+)"$/m),
  "rust version": (root) => mutateNativeVersion(root, "rust/Cargo.toml", /^version = "([^"]+)"$/m),
  "rust floor consumer lock": (root) => mutateNativeVersion(root, "rust/ci/floor-consumer/Cargo.lock", rustConsumerLockEntry),
  "rust floor consumer lock updater": (root) => editJson(join(root, "release-please-config.json"), (c) => { delete c.packages.rust["extra-files"]; }),
  "ruby version": (root) => mutateNativeVersion(root, "packages/ruby/core/lib/qubrics/core/version.rb", /^\s*VERSION = '([^']+)'$/m),
  "ruby identity": (root) => writeFileSync(join(root, "packages/ruby/core/qubrics-core.gemspec"), readFileSync(join(root, "packages/ruby/core/qubrics-core.gemspec"), "utf8").replace("spec.name = 'qubrics-core'", "spec.name = 'wrong-core'")),
  "go identity": (root) => writeFileSync(join(root, "go/go.mod"), readFileSync(join(root, "go/go.mod"), "utf8").replace("module qubrics.com/go", "module wrong.invalid/go")),
  "go tag convention": (root) => editJson(join(root, "release-please-config.json"), (c) => { c.packages.go["tag-separator"] = "-"; }),
  "missing manifest owner": (root) => editJson(join(root, ".release-please-manifest.json"), (m) => { delete m["packages/python/mcp"]; }),
  "extra manifest owner": (root) => editJson(join(root, ".release-please-manifest.json"), (m) => { m["packages/other"] = "1.0.0"; }),
  "missing config owner": (root) => editJson(join(root, "release-please-config.json"), (c) => { delete c.packages["rust"]; }),
  "missing both owners": (root) => { editJson(join(root, "release-please-config.json"), (c) => { delete c.packages["packages/python/mcp"]; }); editJson(join(root, ".release-please-manifest.json"), (m) => { delete m["packages/python/mcp"]; }); },
  "php release ownership": (root) => editJson(join(root, "release-please-config.json"), (c) => { c.packages["packages/php/core"] = { "package-name": "sendmux/core" }; }),
  "php invented version": (root) => editJson(join(root, "packages/php/core/composer.json"), (c) => { c.version = "2.1.0"; }),
  "php identity": (root) => editJson(join(root, "packages/php/core/composer.json"), (c) => { c.name = "wrong/core"; }),
  "php missing umbrella dependency": (root) => editJson(join(root, "packages/php/sdk/composer.json"), (c) => { delete c.require["qubrics/sending"]; }),
};

for (const [name, mutate] of Object.entries(mutations)) {
  test(`native release gate rejects ${name}`, () => fixture((root) => {
    mutate(root);
    const result = check(root);
    assert.notEqual(result.status, 0, `${name} drift was accepted: ${result.stdout}`);
  }));
}

test("native release gate accepts native versions without inventing Go or PHP fields", () => fixture((root) => {
  const result = check(root);
  assert.equal(result.status, 0, result.stderr);
}));

test("Python release preparation updates dependent floors across a major boundary and is idempotent", () => fixture((root) => {
  const owner = "packages/python/core";
  const manifest = readJson(join(root, ".release-please-manifest.json"));
  const current = manifest[owner];
  const future = `${Number(current.split(".")[0]) + 1}.0.0`;
  const path = join(root, owner, "pyproject.toml");
  writeFileSync(path, readFileSync(path, "utf8").replace(current, future));
  editJson(join(root, ".release-please-manifest.json"), (m) => { m[owner] = future; });
  const stale = check(root);
  assert.notEqual(stale.status, 0, "native gate accepted dependencies excluding the new core major");
  assert.match(stale.stderr, /must require qubrics-core/);
  const prepare = () => {
    const child = spawnSync(process.execPath, [join(repository, "scripts/sync-python-dependency-floors.mjs")], { cwd: root, encoding: "utf8", timeout: 10_000 });
    assert.equal(child.status, 0, child.stderr);
  };
  prepare();
  assert.equal(check(root).status, 0, "prepared dependency ranges must match the native release state");
  const metadata = () => Object.keys(manifest).filter((p) => p.startsWith("packages/python/")).map((p) => readFileSync(join(root, p, "pyproject.toml"), "utf8"));
  const prepared = metadata();
  prepare();
  assert.deepEqual(metadata(), prepared, "a second preparation must leave native metadata unchanged");
}));

for (const [language, owner, versionFile, lockFile] of [
  ["python", "packages/python/core", "packages/python/core/pyproject.toml"],
  ["rust", "rust", "rust/Cargo.toml", "rust/ci/floor-consumer/Cargo.lock"],
  ["ruby", "packages/ruby/core", "packages/ruby/core/lib/qubrics/core/version.rb"],
]) {
  test(`native release gate accepts synchronized future ${language} release and rejects its version mutation`, () => fixture((root) => {
    const manifest = readJson(join(root, ".release-please-manifest.json"));
    const current = manifest[owner];
    const future = `${Number(current.split(".")[0]) + 1}.0.0`;
    const path = join(root, versionFile);
    const before = readFileSync(path, "utf8");
    const advanced = before.replace(current, future);
    assert.notEqual(advanced, before, `${language} future fixture must change native bytes`);
    writeFileSync(path, advanced);
    if (lockFile) writeFileSync(join(root, lockFile), readFileSync(join(root, lockFile), "utf8").replace(rustConsumerLockEntry, (entry) => entry.replace(current, future)));
    editJson(join(root, ".release-please-manifest.json"), (m) => { m[owner] = future; });
    if (language === "python") {
      const preparation = spawnSync(process.execPath, [join(repository, "scripts/sync-python-dependency-floors.mjs")], { cwd: root, encoding: "utf8", timeout: 10_000 });
      assert.equal(preparation.status, 0, preparation.stderr);
    }
    const healthy = check(root);
    assert.equal(healthy.status, 0, healthy.stderr);
    mutations[`${language} version`](root);
    const mismatch = check(root);
    assert.notEqual(mismatch.status, 0, `${language} future version drift was accepted: ${mismatch.stdout}`);
    assert.notEqual(readFileSync(path, "utf8"), advanced, `${language} mutation must change native bytes`);
  }));
}
test("Python release-note producer keeps neutral notes across bot refreshes", async () => {
  // Captured constructor output for PR358/36108a03 and PR355/47955f81.
  const entry = "### ⚠ BREAKING CHANGES\n\n* **python:** move SDK packages into the Qubrics namespace\n\n### Features\n\n* **python:** move SDK packages into the Qubrics namespace ([a326bc9](https://github.com/qubrics/qubrics-sdk/commit/a326bc923fff448470d908bb527afaaa35f6d739))\n\n### Bug Fixes\n\n* align changed SDK dependency floors with release manifest ([b1c5548](https://github.com/qubrics/qubrics-sdk/commit/b1c5548c1dde8b441b4fa2605253907971c2f5d2))";
  const neutral = "### ⚠ BREAKING CHANGES\n\n* **python:** update native package imports\n\n### Features\n\n* **python:** update native package imports ([a326bc9](https://github.com/qubrics/qubrics-sdk/commit/a326bc923fff448470d908bb527afaaa35f6d739))\n\n### Bug Fixes\n\n* align changed SDK dependency floors with release manifest ([b1c5548](https://github.com/qubrics/qubrics-sdk/commit/b1c5548c1dde8b441b4fa2605253907971c2f5d2))";
  const candidates = [["packages/python/sdk", "4.0.0"], ["packages/python/langchain", "1.0.0"], ["go", "4.0.0"], ["packages/python/sdk", "4.0.1"]].map(([path, value]) => {
    const version = Version.parse(value);
    const notes = `## [${value}](https://github.com/qubrics/qubrics-sdk/compare/before...after) (2026-11-20)\n\n${entry}`;
    return { path, pullRequest: {
      version,
      body: new PullRequestBody([{ notes, version }], { header: "existing header", footer: "existing footer", extra: "existing extra" }),
      updates: [{ path: `${path}/CHANGELOG.md`, updater: new Changelog({ version, changelogEntry: notes }) }, { path: ".release-please-manifest.json", updater: { version } }],
    } };
  });
  const plugin = new PythonReleaseNotes(undefined, "main", {});
  const before = candidates.map(({ pullRequest }) => ({ body: pullRequest.body.toString(), entry: pullRequest.updates[0].updater.changelogEntry }));
  assert.strictEqual(await plugin.run(candidates), candidates);
  for (const [index, { pullRequest }] of candidates.entries()) {
    const { body, updates, version } = pullRequest;
    const expected = index < 2 ? neutral : entry;
    assert.ok(body.toString().includes(expected), `candidate ${index} body must preserve neutral release notes`);
    assert.ok(updates[0].updater.changelogEntry.endsWith(expected), `candidate ${index} changelog must match its body`);
    assert.strictEqual(body.releaseData[0].version, version);
    assert.strictEqual(updates[1].updater.version, version);
    assert.equal(body.header, "existing header");
    assert.equal(body.footer, "existing footer");
    assert.equal(body.extra, "existing extra");
    assert.equal(updates[0].updater.updateContent("# Changelog\n\n## 0.9.0\n\nhistorical unchanged\n"), `# Changelog\n\n${updates[0].updater.changelogEntry}\n\n## 0.9.0\n\nhistorical unchanged\n`);
    if (index >= 2) assert.deepEqual({ body: body.toString(), entry: updates[0].updater.changelogEntry }, before[index]);
  }
  const after = candidates.map(({ pullRequest }) => pullRequest.body.toString());
  await plugin.run(candidates);
  assert.deepEqual(candidates.map(({ pullRequest }) => pullRequest.body.toString()), after);
});

test("Go release-note producer neutralises captured Go4 notes without changing other releases", async () => {
  // Captured constructor output for PR329/6b44445f.
  const entry = `## [4.0.0](https://github.com/qubrics/qubrics-sdk/compare/go/v3.0.0...go/v4.0.0) (2026-11-22)


### ⚠ BREAKING CHANGES

* **go:** rename module and defaults to Qubrics

### Features

* add compatible Qubrics integration aliases ([dff5cb8](https://github.com/qubrics/qubrics-sdk/commit/dff5cb89bccb5840d55071d23f79ff88c7e58040))
* **go:** rename module and defaults to Qubrics ([8de0a05](https://github.com/qubrics/qubrics-sdk/commit/8de0a05c09088507709af92e3f4fb11729ffea0b))
* **mailbox:** expose durable drafts and agent-email workflows ([bb2f462](https://github.com/qubrics/qubrics-sdk/commit/bb2f462447affd43b3b175b9625068f1a02e3172))
* **mailbox:** expose durable drafts and agent-email workflows ([7e867c5](https://github.com/qubrics/qubrics-sdk/commit/7e867c5bd7b7c85add27c7c04e036997ae57dbc4))
* **mailbox:** expose permitted sender choices to consumers ([#317](https://github.com/qubrics/qubrics-sdk/issues/317)) ([7ac3dc1](https://github.com/qubrics/qubrics-sdk/commit/7ac3dc1c08915ec12477171a49edb87b3d482f39))
* preserve integration contracts with Qubrics aliases ([722fbab](https://github.com/qubrics/qubrics-sdk/commit/722fbab2f98248d17b4878dd5149a35a711d5a18))


### Bug Fixes

* **go:** retain mail webhook models after calendar filtering ([4416e3c](https://github.com/qubrics/qubrics-sdk/commit/4416e3cec4e5cff2440f7aff8cbd6e5cd4b70c5e))
* preserve legacy SDK compatibility with dual aliases ([4910037](https://github.com/qubrics/qubrics-sdk/commit/491003792dd742cb2c83e4a09501abdf4f4458c9))
* preserve webhook variants and own calendar lifecycle fixtures ([49d4604](https://github.com/qubrics/qubrics-sdk/commit/49d4604235528b2fd56ac0bb51d55c244a18f771))
* regenerate SDKs from current calendar and webhook contracts ([276082c](https://github.com/qubrics/qubrics-sdk/commit/276082cb5e525c0a6fb1e521858846cbd21c8714))
* regenerate SDKs from current calendar and webhook contracts ([d728ea8](https://github.com/qubrics/qubrics-sdk/commit/d728ea87ac3f0aeebdb6380ad3bd515bac63d413))
* **sdk:** preserve mail consumers after calendar filtering ([d481266](https://github.com/qubrics/qubrics-sdk/commit/d481266dd8f4c3f3791c4627a05c49d8eee53374))
* **sdk:** preserve timestamps and fixture prerequisites ([894ee58](https://github.com/qubrics/qubrics-sdk/commit/894ee580c8331ac19f80a3778300f265a1a39300))
* **sdk:** remove calendar bindings from generated clients ([128169a](https://github.com/qubrics/qubrics-sdk/commit/128169a811c51f71d9c8440b2386b6c5029ee2af))
* **sdk:** withhold remaining calendar bindings at generation ([27c2cd1](https://github.com/qubrics/qubrics-sdk/commit/27c2cd1be5fcdcc5376be7a06223a0eca1e8a4ae))`;
  const neutral = `## [4.0.0](https://github.com/qubrics/qubrics-sdk/compare/go/v3.0.0...go/v4.0.0) (2026-11-22)


### ⚠ BREAKING CHANGES

* **go:** update native module imports and API defaults

### Features

* add compatible integration aliases ([dff5cb8](https://github.com/qubrics/qubrics-sdk/commit/dff5cb89bccb5840d55071d23f79ff88c7e58040))
* **go:** update native module imports and API defaults ([8de0a05](https://github.com/qubrics/qubrics-sdk/commit/8de0a05c09088507709af92e3f4fb11729ffea0b))
* **mailbox:** expose durable drafts and agent-email workflows ([bb2f462](https://github.com/qubrics/qubrics-sdk/commit/bb2f462447affd43b3b175b9625068f1a02e3172))
* **mailbox:** expose durable drafts and agent-email workflows ([7e867c5](https://github.com/qubrics/qubrics-sdk/commit/7e867c5bd7b7c85add27c7c04e036997ae57dbc4))
* **mailbox:** expose permitted sender choices to consumers ([#317](https://github.com/qubrics/qubrics-sdk/issues/317)) ([7ac3dc1](https://github.com/qubrics/qubrics-sdk/commit/7ac3dc1c08915ec12477171a49edb87b3d482f39))
* preserve integration contracts with aliases ([722fbab](https://github.com/qubrics/qubrics-sdk/commit/722fbab2f98248d17b4878dd5149a35a711d5a18))


### Bug Fixes

* **go:** retain mail webhook models after calendar filtering ([4416e3c](https://github.com/qubrics/qubrics-sdk/commit/4416e3cec4e5cff2440f7aff8cbd6e5cd4b70c5e))
* preserve legacy SDK compatibility with dual aliases ([4910037](https://github.com/qubrics/qubrics-sdk/commit/491003792dd742cb2c83e4a09501abdf4f4458c9))
* preserve webhook variants and own calendar lifecycle fixtures ([49d4604](https://github.com/qubrics/qubrics-sdk/commit/49d4604235528b2fd56ac0bb51d55c244a18f771))
* regenerate SDKs from current calendar and webhook contracts ([276082c](https://github.com/qubrics/qubrics-sdk/commit/276082cb5e525c0a6fb1e521858846cbd21c8714))
* regenerate SDKs from current calendar and webhook contracts ([d728ea8](https://github.com/qubrics/qubrics-sdk/commit/d728ea87ac3f0aeebdb6380ad3bd515bac63d413))
* **sdk:** preserve mail consumers after calendar filtering ([d481266](https://github.com/qubrics/qubrics-sdk/commit/d481266dd8f4c3f3791c4627a05c49d8eee53374))
* **sdk:** preserve timestamps and fixture prerequisites ([894ee58](https://github.com/qubrics/qubrics-sdk/commit/894ee580c8331ac19f80a3778300f265a1a39300))
* **sdk:** remove calendar bindings from generated clients ([128169a](https://github.com/qubrics/qubrics-sdk/commit/128169a811c51f71d9c8440b2386b6c5029ee2af))
* **sdk:** withhold remaining calendar bindings at generation ([27c2cd1](https://github.com/qubrics/qubrics-sdk/commit/27c2cd1be5fcdcc5376be7a06223a0eca1e8a4ae))`;
  const candidates = [["go", "4.0.0"], ["go", "4.0.1"], ["packages/python/sdk", "4.0.0"], ["rust", "4.0.0"]].map(([path, value]) => {
    const version = Version.parse(value);
    return { path, pullRequest: {
      version,
      body: new PullRequestBody([{ notes: entry, version }], { header: "existing header", footer: "existing footer", extra: "existing extra" }),
      updates: [{ path: `${path}/CHANGELOG.md`, updater: new Changelog({ version, changelogEntry: entry }) }, { path: ".release-please-manifest.json", updater: { version } }],
    } };
  });
  const plugin = new PythonReleaseNotes(undefined, "main", {});
  const before = candidates.map(({ pullRequest }) => ({ body: pullRequest.body.toString(), entry: pullRequest.updates[0].updater.changelogEntry }));
  const history = "# Changelog\n\n## 3.0.0\n\nrename module and defaults to Qubrics\n";
  assert.strictEqual(await plugin.run(candidates), candidates);
  for (const [index, { pullRequest }] of candidates.entries()) {
    const { body, updates, version } = pullRequest;
    const expected = index === 0 ? neutral : entry;
    assert.equal(body.releaseData[0].notes, expected, `candidate ${index} body must contain the scoped notes`);
    assert.equal(updates[0].updater.changelogEntry, expected, `candidate ${index} changelog must match its body`);
    assert.strictEqual(body.releaseData[0].version, version);
    assert.strictEqual(updates[1].updater.version, version);
    assert.equal(body.header, "existing header");
    assert.equal(body.footer, "existing footer");
    assert.equal(body.extra, "existing extra");
    assert.equal(updates[0].updater.updateContent(history), `# Changelog\n\n${expected}\n\n## 3.0.0\n\nrename module and defaults to Qubrics\n`);
    if (index > 0) assert.deepEqual({ body: body.toString(), entry: updates[0].updater.changelogEntry }, before[index]);
  }
  const after = candidates.map(({ pullRequest }) => ({ body: pullRequest.body.toString(), entry: pullRequest.updates[0].updater.changelogEntry }));
  await plugin.run(candidates);
  assert.deepEqual(candidates.map(({ pullRequest }) => ({ body: pullRequest.body.toString(), entry: pullRequest.updates[0].updater.changelogEntry })), after);
});
