import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import test from "node:test";

const exec = promisify(execFile);

for (const [surface, prefix, api] of [["Mailbox", "smx_mbx_", "MailboxAPIApi"], ["Management", "smx_root_", "ConnectionApi"], ["Sending", "smx_mbx_", "MetaApi"]]) {
  test(`PHP ${surface} environment defaults preserve legacy names and explicit configuration`, async () => {
    const child = exec("php", [], { timeout: 10000 });
    child.child.stdin.end(`<?php
require 'vendor/autoload.php';
putenv('QUBRICS_API_KEY'); putenv('QUBRICS_BASE_URL');
putenv('SENDMUX_API_KEY=${prefix}legacy'); putenv('SENDMUX_BASE_URL=https://legacy.fixture.test/api/v1');
$legacy = Qubrics\\${surface}\\ClientFactory::configuration();
putenv('QUBRICS_API_KEY=${prefix}current'); putenv('QUBRICS_BASE_URL=https://current.fixture.test/api/v1');
$current = Qubrics\\${surface}\\ClientFactory::configuration();
$explicit = Qubrics\\${surface}\\ClientFactory::configuration('${prefix}explicit', 'https://explicit.fixture.test/api/v1');
echo json_encode(array_map(fn($config) => [$config->getAccessToken(), $config->getHost()], [$legacy, $current, $explicit]));
`);
    const { stdout } = await child;
    assert.deepEqual(JSON.parse(stdout), [
      [`${prefix}legacy`, "https://legacy.fixture.test/api/v1"],
      [`${prefix}current`, "https://current.fixture.test/api/v1"],
      [`${prefix}explicit`, "https://explicit.fixture.test/api/v1"],
    ]);
  });

  test(`PHP ${surface} preserves nonempty zero-valued Qubrics settings`, async () => {
    const child = exec("php", [], { timeout: 10000 });
    child.child.stdin.end(`<?php
require 'vendor/autoload.php';
putenv('SENDMUX_API_KEY=${prefix}legacy'); putenv('SENDMUX_BASE_URL=https://legacy.fixture.test/api/v1');
putenv('QUBRICS_API_KEY=0'); putenv('QUBRICS_BASE_URL=');
try { Qubrics\\${surface}\\ClientFactory::configuration(); $zeroKey = 'accepted'; }
catch (InvalidArgumentException $error) { $zeroKey = 'rejected'; }
putenv('QUBRICS_API_KEY='); putenv('QUBRICS_BASE_URL=0');
$zeroUrl = Qubrics\\${surface}\\ClientFactory::configuration()->getHost();
$zeroOAuthUrl = Qubrics\\${surface}\\ClientFactory::create${api}WithAccessToken('test.token')->getConfig()->getHost();
putenv('QUBRICS_BASE_URL=');
$fallback = Qubrics\\${surface}\\ClientFactory::configuration();
putenv('SENDMUX_BASE_URL=0');
$legacyFalsyUrl = Qubrics\\${surface}\\ClientFactory::configuration()->getHost();
$explicit = Qubrics\\${surface}\\ClientFactory::configuration('${prefix}explicit', 'https://explicit.fixture.test/api/v1');
echo json_encode([$zeroKey, $zeroUrl, $zeroOAuthUrl, $fallback->getAccessToken(), $fallback->getHost(), $legacyFalsyUrl, $explicit->getAccessToken(), $explicit->getHost()]);
`);
    const { stdout } = await child;
    assert.deepEqual(JSON.parse(stdout), [
      "rejected", "0", "0", `${prefix}legacy`, "https://legacy.fixture.test/api/v1",
      surface === "Sending" ? "https://smtp.qubrics.com/api/v1" : "https://app.qubrics.com/api/v1",
      `${prefix}explicit`, "https://explicit.fixture.test/api/v1",
    ]);
  });
}
