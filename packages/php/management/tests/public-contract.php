<?php

declare(strict_types=1);

require dirname(__DIR__) . '/vendor/autoload.php';

$baseUrls = ['QUBRICS_BASE_URL' => getenv('QUBRICS_BASE_URL'), 'SENDMUX_BASE_URL' => getenv('SENDMUX_BASE_URL')];
register_shutdown_function(static function () use ($baseUrls): void {
    foreach ($baseUrls as $name => $value) {
        putenv($value === false ? $name : "$name=$value");
    }
});
foreach ($baseUrls as $name => $_) {
    putenv($name);
}

use Composer\InstalledVersions;
use Qubrics\Management\ClientFactory;
use Qubrics\Management\Configuration;
use Qubrics\Management\Model\Connection;
use Qubrics\Management\Model\ConnectionResponse;
use Qubrics\Management\Model\ProviderUpdateBody;
use Qubrics\Management\Model\WebhookEventData;
use Qubrics\Management\ObjectSerializer;

$expect = static function (bool $condition, string $message): void {
    if (!$condition) {
        throw new RuntimeException($message);
    }
};

$expect(InstalledVersions::isInstalled('qubrics/management'), 'Composer must install qubrics/management');
$api = ClientFactory::createConnectionApi('smx_root_example');
$request = $api->managementGetConnectionRequest();
$expect(
    (string) $request->getUri() === 'https://app.qubrics.com/api/v1/me',
    'Connection request uses the Qubrics host'
);
$expect(
    $request->getHeaderLine('Authorization') === 'Bearer smx_root_example',
    'Root key authentication remains compatible'
);
$expect(
    $request->getHeaderLine('User-Agent') === 'OpenAPI-Generator/3.0.0/PHP',
    'User agent identifies the package version'
);
$expect(
    (new Configuration())->getHostSettings()[0]['url'] === 'https://app.qubrics.com/api/v1',
    'Server defaults use the Qubrics host'
);

$custom = ClientFactory::createConnectionApi('smx_root_example', 'https://api.example.test/api/v1');
$expect(
    $custom->managementGetConnectionRequest()->getUri()->getHost() === 'api.example.test',
    'Explicit hosts remain supported'
);
$oauth = ClientFactory::createConnectionApiWithAccessToken('oauth-token');
$expect($oauth->getConfig()->getHost() === 'https://app.qubrics.com/api/v1', 'OAuth factories use the Qubrics host');

try {
    ClientFactory::createConnectionApi('smx_mbx_example');
    throw new RuntimeException('Mailbox keys must not create Management clients');
} catch (InvalidArgumentException $error) {
    $expect(str_contains($error->getMessage(), 'root'), 'Wrong-surface keys are rejected');
}

$response = ObjectSerializer::deserialize((object) ['data' => (object) []], ConnectionResponse::class);
$expect(
    $response instanceof ConnectionResponse && $response->getData() instanceof Connection,
    'Nested generated model names autoload'
);

$event = ObjectSerializer::deserialize(
    (object) ['sendmux_message_id' => 'message-123', 'recipients' => []],
    WebhookEventData::class
);
$expect($event->getSendmuxMessageId() === 'message-123', 'Legacy message-ID accessor remains available');
$event->setSendmuxMessageId('message-456');
$expect(
    ObjectSerializer::sanitizeForSerialization($event)->sendmux_message_id === 'message-456',
    'Legacy message-ID setter preserves its wire key'
);

$start = new DateTime('2026-11-01T00:00:00+00:00');
$end = new DateTime('2026-11-02T00:00:00+00:00');
$usage = ClientFactory::createMailboxesApi('smx_root_example')->managementGetMailboxCostUsageRequest(
    'mailbox_fixture',
    $start,
    $end,
    'revision.fixture'
);
parse_str($usage->getUri()->getQuery(), $query);
$expect($query === [
    'start' => '2026-11-01T00:00:00+00:00',
    'end' => '2026-11-02T00:00:00+00:00',
], 'Cost usage dates encode as RFC3339 query strings');
$expect($usage->getHeaderLine('If-None-Match') === 'revision.fixture', 'Conditional query requests retain headers');

foreach ([[], ['project' => 'fixture']] as $variables) {
    $provider = new ProviderUpdateBody(['variables' => $variables]);
    $wire = json_decode(json_encode(ObjectSerializer::sanitizeForSerialization($provider), JSON_THROW_ON_ERROR));
    $expect($wire->variables instanceof stdClass, 'Provider variables encode as a JSON object, including empty maps');
    $expect((array) $wire->variables === $variables, 'Provider variables retain their values');
}
$omitted = ObjectSerializer::sanitizeForSerialization(new ProviderUpdateBody());
$expect(!property_exists($omitted, 'variables'), 'Omitted provider variables remain omitted');

echo "Qubrics Management public contract passed\n";
