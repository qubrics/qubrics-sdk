import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import test from "node:test";

const exec = promisify(execFile);

for (const [surface, prefix] of [["Mailbox", "smx_mbx_"], ["Management", "smx_root_"], ["Sending", "smx_mbx_"]]) {
  test(`PHP ${surface} environment defaults preserve legacy names and explicit configuration`, async () => {
    const child = exec("php", [], { timeout: 10000 });
    child.child.stdin.end(`<?php
require 'vendor/autoload.php';
putenv('QUBRICS_API_KEY'); putenv('QUBRICS_BASE_URL');
putenv('SENDMUX_API_KEY=${prefix}legacy'); putenv('SENDMUX_BASE_URL=https://legacy.fixture.test/api/v1');
$legacy = Sendmux\\${surface}\\ClientFactory::configuration();
putenv('QUBRICS_API_KEY=${prefix}current'); putenv('QUBRICS_BASE_URL=https://current.fixture.test/api/v1');
$current = Sendmux\\${surface}\\ClientFactory::configuration();
$explicit = Sendmux\\${surface}\\ClientFactory::configuration('${prefix}explicit', 'https://explicit.fixture.test/api/v1');
echo json_encode(array_map(fn($config) => [$config->getAccessToken(), $config->getHost()], [$legacy, $current, $explicit]));
`);
    const { stdout } = await child;
    assert.deepEqual(JSON.parse(stdout), [
      [`${prefix}legacy`, "https://legacy.fixture.test/api/v1"],
      [`${prefix}current`, "https://current.fixture.test/api/v1"],
      [`${prefix}explicit`, "https://explicit.fixture.test/api/v1"],
    ]);
  });
}
