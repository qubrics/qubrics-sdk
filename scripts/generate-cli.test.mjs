import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { access, mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { join } from "node:path";
import test from "node:test";
import { transform } from "esbuild";

test("upload-token alternatives keep the CLI capability upload free of API-key authentication", async (t) => {
  const artifactRoot = join(process.cwd(), ".claude/artifacts/rebrand-qubrics-904");
  await mkdir(artifactRoot, { recursive: true });
  const directory = await mkdtemp(join(artifactRoot, "cli-upload-capability-"));
  t.after(() => rm(directory, { recursive: true, force: true }));
  const uploadHeaders = ["X-Qubrics-Upload-Token", "X-Sendmux-Upload-Token"];
  await writeFile(join(directory, "openapi-app.json"), JSON.stringify({
    openapi: "3.1.0", info: { title: "Empty app fixture", version: "1.0.0" }, paths: {},
  }));
  await writeFile(join(directory, "openapi-sending.json"), JSON.stringify({
    openapi: "3.1.0",
    info: { title: "Upload security fixture", version: "1.0.0" },
    components: { securitySchemes: {
      BearerAuth: { type: "http", scheme: "bearer" },
      UploadTokenQubrics: { type: "apiKey", in: "header", name: uploadHeaders[0] },
      UploadTokenSendmux: { type: "apiKey", in: "header", name: uploadHeaders[1] },
    } },
    paths: {
      "/attachments/{attachment_id}/upload": { put: {
        operationId: "sendingCompleteAttachmentUpload",
        security: [{ UploadTokenQubrics: [] }, { UploadTokenSendmux: [] }],
        responses: { "200": { description: "Uploaded" } },
        parameters: [
          { in: "path", name: "attachment_id", required: true, schema: { type: "string" } },
          ...uploadHeaders.map(name => ({ in: "header", name, required: false, schema: { type: "string" } })),
        ],
      } },
      "/emails/send": { post: {
        operationId: "sendingSendEmail",
        security: [{ BearerAuth: [] }],
        responses: { "200": { description: "Sent" } },
      } },
    },
  }));
  const generatedPath = join(directory, "operations.ts");
  const generated = spawnSync(process.execPath, [
    "scripts/generate-cli.mjs", "--input-dir", directory, "--output", generatedPath,
    "--cli-source-dir", join(directory, "src"), "--commands-dir", join(directory, "src/commands"),
  ], { encoding: "utf8", timeout: 10000 });
  assert.equal(generated.status, 0, generated.stderr);
  const { code } = await transform(await readFile(generatedPath, "utf8"), { loader: "ts", format: "esm" });
  const { operations } = await import(`data:text/javascript;base64,${Buffer.from(code).toString("base64")}`);
  assert.equal(operations.sendingCompleteAttachmentUpload.requiredKeyKind, "none");
  assert.equal(operations.sendingSendEmail.requiredKeyKind, "sending");
});

test("mailbox reads and webhook event options come from OpenAPI", async (t) => {
  const artifactRoot = join(process.cwd(), ".claude/artifacts/rebrand-qubrics-sdk344");
  await mkdir(artifactRoot, { recursive: true });
  const directory = await mkdtemp(join(artifactRoot, "cli-mail-"));
  t.after(() => rm(directory, { recursive: true, force: true }));
  const operation = (operationId) => ({ get: { operationId, responses: { "200": { description: "Read" } } } });
  await writeFile(join(directory, "openapi-app.json"), JSON.stringify({
    openapi: "3.1.0", info: { title: "Mailbox fixture", version: "1.0.0" },
    paths: {
      "/mailbox/messages": operation("mailboxListMessages"),
      "/webhook-deliveries": { get: {
        operationId: "managementListWebhookDeliveries",
        parameters: [{ in: "query", name: "event_type", schema: { type: "string", enum: ["message.bounced", "message.received"] } }],
        responses: { "200": { description: "Read" } },
      } },
    },
  }));
  await writeFile(join(directory, "openapi-sending.json"), JSON.stringify({
    openapi: "3.1.0", info: { title: "Empty sending fixture", version: "1.0.0" }, paths: {},
  }));
  const generatedPath = join(directory, "operations.ts");
  const generated = spawnSync(process.execPath, [
    "scripts/generate-cli.mjs", "--input-dir", directory, "--output", generatedPath,
    "--cli-source-dir", join(directory, "src"), "--commands-dir", join(directory, "src/commands"),
  ], { encoding: "utf8", timeout: 10000 });
  assert.equal(generated.status, 0, generated.stderr);
  const { code } = await transform(await readFile(generatedPath, "utf8"), { loader: "ts", format: "esm" });
  const { operations } = await import(`data:text/javascript;base64,${Buffer.from(code).toString("base64")}`);
  assert.deepEqual(Object.keys(operations), ["mailboxListMessages", "managementListWebhookDeliveries"]);
  assert.deepEqual(operations.managementListWebhookDeliveries.queryParams[0].schema.enum, ["message.bounced", "message.received"]);
  await access(join(directory, "src/commands/mailbox/messages/list.ts"));
});
