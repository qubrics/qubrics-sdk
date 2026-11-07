<?php

declare(strict_types=1);

require dirname(__DIR__) . '/vendor/autoload.php';

use Composer\InstalledVersions;
use GuzzleHttp\Client;
use GuzzleHttp\Handler\MockHandler;
use GuzzleHttp\HandlerStack;
use GuzzleHttp\Middleware;
use GuzzleHttp\Psr7\Response;
use Qubrics\Core\ApiKeySurface;
use Qubrics\Core\Auth;
use Qubrics\Core\ErrorMapper;
use Qubrics\Core\Headers;
use Qubrics\Core\QubricsApiError;

/** Fails the public contract when an observable SDK guarantee breaks. */
$expect = static function (bool $condition, string $message): void {
    if (!$condition) {
        throw new RuntimeException($message);
    }
};

$expect(InstalledVersions::isInstalled('qubrics/core'), 'Composer must install qubrics/core');
$expect(
    Auth::assertApiKeySurface('smx_root_example', ApiKeySurface::Root) === ApiKeySurface::Root,
    'Root keys remain compatible'
);
$expect(
    Auth::assertApiKeySurface('smx_mbx_example', ApiKeySurface::Mailbox) === ApiKeySurface::Mailbox,
    'Mailbox keys remain compatible'
);
$expect(
    Auth::assertApiKeySurface('smx_agent_example', ApiKeySurface::Sending) === ApiKeySurface::Mailbox,
    'Agent sending keys remain compatible'
);

$history = [];
$stack = HandlerStack::create(new MockHandler([new Response(200)]));
$stack->push(Auth::accessTokenMiddleware('oauth-token'));
$stack->push(Middleware::history($history));
(new Client(['handler' => $stack]))->get('https://app.qubrics.com/api');
$expect(
    $history[0]['request']->getHeaderLine('Authorization') === 'Bearer oauth-token',
    'OAuth bearer header remains compatible'
);
$expect(
    Headers::idempotency('order-123') === ['Idempotency-Key' => 'order-123'],
    'Idempotency header remains compatible'
);
$expect(
    Headers::conditional('"mailbox-etag"') === ['If-Match' => '"mailbox-etag"'],
    'Conditional header remains compatible'
);

try {
    Auth::assertApiKeySurface('invalid', ApiKeySurface::Root);
    throw new RuntimeException('Invalid API keys must be rejected');
} catch (InvalidArgumentException $error) {
    $expect(
        $error->getMessage() === 'Qubrics API keys must start with smx_root_, smx_mbx_, or smx_agent_',
        'Invalid key message uses Qubrics'
    );
}

$error = ErrorMapper::fromErrorResponse(null, 429, ['X-Request-Id' => ['request-123']]);
$expect($error instanceof QubricsApiError, 'Error mapper returns QubricsApiError');
$expect(
    $error->statusCode === 429 && $error->apiCode === 'request_failed' && $error->retryable,
    'Rate-limit errors keep status and retry semantics'
);
$expect($error->getMessage() === 'Qubrics API request failed', 'Fallback error message uses Qubrics');
$expect($error->requestId === 'request-123', 'Request ID header remains compatible');
$expect(ErrorMapper::fromThrowable($error) === $error, 'Mapped errors retain identity');

echo "Qubrics core public contract passed\n";
