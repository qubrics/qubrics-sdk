<?php

declare(strict_types=1);

use Composer\InstalledVersions;
use GuzzleHttp\Handler\MockHandler;
use GuzzleHttp\Middleware;
use GuzzleHttp\Psr7\Response;
use Qubrics\Sending\ClientFactory;
use Qubrics\Sending\Configuration;
use Qubrics\Sending\Model\Connection;
use Qubrics\Sending\Model\ConnectionCredential;
use Qubrics\Sending\Model\ConnectionResponse;
use Qubrics\Sending\ObjectSerializer;

require dirname(__DIR__) . '/vendor/autoload.php';

$expect = static function (bool $condition, string $message): void {
    if (!$condition) {
        throw new RuntimeException($message);
    }
};

$configuration = new Configuration();
$expect($configuration->getHost() === 'https://smtp.qubrics.com/api/v1', 'Sending defaults to the Qubrics host');
$expect(
    $configuration->getHostSettings()[0]['url'] === 'https://smtp.qubrics.com/api/v1',
    'Server settings use the Qubrics host'
);
$expect($configuration->getUserAgent() === 'OpenAPI-Generator/3.0.0/PHP', 'User agent identifies version 3.0.0');
$expect(InstalledVersions::getRootPackage()['name'] === 'qubrics/sending', 'Composer exposes qubrics/sending');
$expect(InstalledVersions::isInstalled('qubrics/core'), 'Composer installs Qubrics core');

$api = ClientFactory::createMetaApi('smx_mbx_fixture');
$request = $api->sendingGetConnectionRequest();
$expect(
    (string) $request->getUri() === 'https://smtp.qubrics.com/api/v1/me',
    'Connection request uses the Qubrics URL'
);
$expect(
    $request->getHeaderLine('Authorization') === 'Bearer smx_mbx_fixture',
    'Existing mailbox credentials authenticate'
);
$expect(
    $request->getHeaderLine('User-Agent') === 'OpenAPI-Generator/3.0.0/PHP',
    'Generated requests carry the package version'
);
$override = ClientFactory::createMetaApi('smx_mbx_fixture', 'https://custom.fixture.test/api/v1');
$expect(
    (string) $override->sendingGetConnectionRequest()->getUri() === 'https://custom.fixture.test/api/v1/me',
    'Explicit hosts remain supported'
);

$body = new SplTempFileObject();
$body->fwrite('test');
$body->rewind();
$upload = ClientFactory::createAttachmentsApi('smx_mbx_fixture')->sendingCompleteAttachmentUploadRequest(
    x_sendmux_upload_token: 'upload.fixture',
    content_length: 4,
    upload_id: 'upl_abcdefghijklmnopqrstuvwx',
    body: $body
);
$expect(
    $upload->getHeaderLine('X-Sendmux-Upload-Token') === 'upload.fixture',
    'Existing upload token header and named argument remain supported'
);

$oauth = ClientFactory::createMetaApiWithAccessToken('oauth.fixture');
$expect(
    $oauth->getConfig()->getHost() === 'https://smtp.qubrics.com/api/v1',
    'OAuth factories use the Qubrics default'
);
$oauthOverride = ClientFactory::createMetaApiWithAccessToken('oauth.fixture', 'https://custom.fixture.test/api/v1');
$expect(
    $oauthOverride->getConfig()->getHost() === 'https://custom.fixture.test/api/v1',
    'OAuth factories preserve explicit hosts'
);
$http = ClientFactory::httpClient(accessToken: static fn (): string => 'oauth.fixture');
$history = [];
$stack = $http->getConfig('handler');
$stack->setHandler(new MockHandler([new Response(204)]));
$stack->push(Middleware::history($history));
$http->send($oauth->sendingGetConnectionRequest());
$expect(
    $history[0]['request']->getHeaderLine('Authorization') === 'Bearer oauth.fixture',
    'OAuth middleware authenticates generated requests'
);
$expect($http->getConfig('allow_redirects') === false, 'OAuth clients keep redirects disabled');

$response = ObjectSerializer::deserialize(json_decode('{
    "meta": {}, "ok": true, "data": {
        "credential": {"id": "credential_fixture", "name": "Fixture", "type": "api_key"},
        "label": "Fixture", "mailboxes": [], "permissions": [],
        "team": {"id": "team_fixture", "name": "Fixture"}
    }
}', false, 512, JSON_THROW_ON_ERROR), ConnectionResponse::class);
$expect($response instanceof ConnectionResponse, 'Connection response loads through Composer');
$expect($response->getData() instanceof Connection, 'Nested connection type loads in the Qubrics namespace');
$expect(
    $response->getData()->getCredential() instanceof ConnectionCredential,
    'Nested credential type loads in the Qubrics namespace'
);
$expect(
    $response->getData()->getCredential()->getName() === 'Fixture',
    'Nested response data survives deserialisation'
);

fwrite(STDOUT, "Sending public contract passed\n");
