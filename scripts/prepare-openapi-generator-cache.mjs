import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { createRequire } from "node:module";
import { dirname, join } from "node:path";

const root = process.cwd();
const version = JSON.parse(readFileSync(join(root, "openapitools.json"), "utf8"))["generator-cli"].version;
if (!/^\d+\.\d+\.\d+$/.test(version)) throw new Error("Invalid OpenAPI Generator version");
const command = process.argv[2];
if (command === "version") {
  console.log(version);
} else {
  if (!["seed", "install"].includes(command)) throw new Error("Expected version, seed or install");
  const checksum = readFileSync(join(root, "codegen/openapi-generator.sha1"), "utf8").trim();
  const expected = checksum.match(/^([a-f0-9]{40})  (\d+\.\d+\.\d+)\.jar$/);
  if (!expected || expected[2] !== version) throw new Error("Update codegen/openapi-generator.sha1 from Maven's published .sha1 for this version");
  const directory = join(root, ".tmp/openapi-generator-cache");
  const jar = join(directory, `${version}.jar`);
  if (command === "seed" && !existsSync(jar)) {
    mkdirSync(directory, { recursive: true });
    console.log(`Downloading OpenAPI Generator ${version} once for the shared cache`);
    execFileSync("curl", ["--fail", "--silent", "--show-error", "--location", "--max-time", "120", "--output", jar,
      `https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/${version}/openapi-generator-cli-${version}.jar`], { stdio: "inherit" });
  }
  if (!existsSync(jar)) throw new Error(`Missing OpenAPI Generator ${version} cache; the seed job must finish first`);
  const actual = createHash("sha1").update(readFileSync(jar)).digest("hex");
  if (actual !== expected[1]) throw new Error(`OpenAPI Generator ${version} SHA1 mismatch: expected ${expected[1]}, got ${actual}`);
  console.log(`Verified cached OpenAPI Generator ${version}: ${actual}`);
  if (command === "install") {
    const require = createRequire(join(root, "package.json"));
    const destination = join(dirname(require.resolve("@openapitools/openapi-generator-cli/main.js")), "versions");
    mkdirSync(destination, { recursive: true });
    copyFileSync(jar, join(destination, `${version}.jar`));
    console.log(`Installed verified cached JAR at ${destination}/${version}.jar; no Maven request`);
  }
}
