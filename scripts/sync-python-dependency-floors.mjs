import { readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const root = process.cwd();
const manifest = JSON.parse(readFileSync(join(root, ".release-please-manifest.json"), "utf8"));
const config = JSON.parse(readFileSync(join(root, "release-please-config.json"), "utf8"));
const packages = Object.entries(config.packages).filter(([path]) => path.startsWith("packages/python/"));
const ranges = new Map(packages.map(([path, owner]) => {
  const version = manifest[path];
  const match = version?.match(/^(\d+)\.\d+\.\d+$/);
  if (!match) throw new Error(`Unsupported Python dependency version: ${version}`);
  return [owner["package-name"], `${owner["package-name"]}>=${version},<${Number(match[1]) + 1}.0.0`];
}));

for (const [path] of packages) {
  const file = join(root, path, "pyproject.toml");
  const source = readFileSync(file, "utf8");
  const updated = source.replace(/"([^"\n]+)>=[^,"\n]+,<[^"\n]+"/g, (range, name) =>
    ranges.has(name) ? `"${ranges.get(name)}"` : range,
  );
  if (updated !== source) writeFileSync(file, updated);
}

console.log("Python internal dependency floors match the release manifest.");
