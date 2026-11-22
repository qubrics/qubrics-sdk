import assert from "node:assert/strict";
import { pathToFileURL } from "node:url";
import { GitHub, Manifest } from "release-please";
import { ManifestPlugin } from "release-please/build/src/plugin.js";
import { Changelog } from "release-please/build/src/updaters/changelog.js";

const pendingVersions = new Map([["packages/python/sdk", "4.0.0"], ["packages/python/langchain", "1.0.0"], ["go", "4.0.0"]]);
const neutralNotes = ({ path, notes }) => path === "go"
  ? notes.replaceAll("rename module and defaults to Qubrics", "update native module imports and API defaults")
    .replaceAll("add compatible Qubrics integration aliases", "add compatible integration aliases")
    .replaceAll("preserve integration contracts with Qubrics aliases", "preserve integration contracts with aliases")
    .replaceAll("retain mail webhook models after calendar filtering", "retain mail webhook models")
    .replaceAll("preserve webhook variants and own calendar lifecycle fixtures", "preserve webhook variants and fixture ownership")
    .replaceAll("regenerate SDKs from current calendar and webhook contracts", "regenerate SDKs from current webhook contracts")
    .replaceAll("preserve mail consumers after calendar filtering", "preserve mail consumers")
    .replaceAll("remove calendar bindings from generated clients", "remove excluded bindings from generated clients")
    .replaceAll("withhold remaining calendar bindings at generation", "exclude remaining bindings outside the selected surfaces")
  : notes.replaceAll("move SDK packages into the Qubrics namespace", "update native package imports");

export class PythonReleaseNotes extends ManifestPlugin {
  async run(candidates) {
    for (const { path, pullRequest } of candidates) {
      if (!pendingVersions.has(path) || pendingVersions.get(path) !== pullRequest.version?.toString()) continue;
      const changelog = pullRequest.updates.find((update) => update.path === `${path}/CHANGELOG.md`);
      assert.ok(changelog?.updater instanceof Changelog, `${path} needs its generated changelog updater`);
      changelog.updater.changelogEntry = neutralNotes({ path, notes: changelog.updater.changelogEntry });
      for (const release of pullRequest.body.releaseData) release.notes = neutralNotes({ path, notes: release.notes });
    }
    return candidates;
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  assert.equal(process.env.GITHUB_ACTIONS, "true", "Bot PR emission runs only in GitHub Actions");
  assert.equal(process.env.GITHUB_EVENT_NAME, "push");
  assert.equal(process.env.GITHUB_REF, "refs/heads/main");
  assert.equal(process.env.GITHUB_REPOSITORY, "qubrics/qubrics-sdk");
  assert.ok(process.env.GITHUB_TOKEN, "GITHUB_TOKEN is required");
  const github = await GitHub.create({ owner: "qubrics", repo: "qubrics-sdk", defaultBranch: "main", token: process.env.GITHUB_TOKEN });
  const manifest = await Manifest.fromManifest(github, "main", "release-please-config.json", ".release-please-manifest.json");
  manifest.plugins.push(new PythonReleaseNotes(github, "main", manifest.repositoryConfig));
  await manifest.createPullRequests();
}
