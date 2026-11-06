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
use Qubrics\Mailbox\ClientFactory as MailboxFactory;
use Qubrics\Management\ClientFactory as ManagementFactory;
use Qubrics\Sdk\Sdk;
use Qubrics\Sending\ClientFactory as SendingFactory;

/** Fails the public contract when an observable SDK guarantee breaks. */
$expect = static function (bool $condition, string $message): void {
    if (!$condition) {
        throw new RuntimeException($message);
    }
};

foreach (['core', 'sdk', 'sending', 'mailbox', 'management'] as $package) {
    $expect(InstalledVersions::isInstalled('qubrics/' . $package), 'Composer must install qubrics/' . $package);
}

$expect(Sdk::VERSION === '3.0.0', 'SDK must expose the next major version');

$sending = SendingFactory::createMetaApi('smx_mbx_example');
$mailbox = MailboxFactory::createMailboxAPIApi('smx_mbx_example');
$management = ManagementFactory::createMailboxesApi('smx_root_example');

$expect($sending->getConfig()->getHost() === 'https://smtp.qubrics.com/api/v1', 'Sending uses the Qubrics host');
$expect($mailbox->getConfig()->getHost() === 'https://app.qubrics.com/api/v1', 'Mailbox uses the Qubrics host');
$expect($management->getConfig()->getHost() === 'https://app.qubrics.com/api/v1', 'Management uses the Qubrics host');
$expect($sending->getConfig()->getAccessToken() === 'smx_mbx_example', 'Sending preserves mailbox authentication');
$expect($management->getConfig()->getAccessToken() === 'smx_root_example', 'Management preserves root authentication');

$oauth = SendingFactory::createMetaApiWithAccessToken('oauth-token');
$expect($oauth->getConfig()->getHost() === 'https://smtp.qubrics.com/api/v1', 'OAuth uses the Qubrics host');

echo "Qubrics SDK public contract passed\n";
