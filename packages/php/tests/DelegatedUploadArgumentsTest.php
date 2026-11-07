<?php

declare(strict_types=1);

namespace Qubrics\Tests;

use GuzzleHttp\Client;
use GuzzleHttp\Handler\MockHandler;
use GuzzleHttp\HandlerStack;
use GuzzleHttp\Middleware;
use GuzzleHttp\Promise\PromiseInterface;
use GuzzleHttp\Psr7\Response;
use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\TestCase;
use Psr\Http\Message\RequestInterface;
use Qubrics\Sending\Api\AttachmentsApi;
use Qubrics\Sending\ApiException;
use Qubrics\Sending\Configuration;

final class DelegatedUploadArgumentsTest extends TestCase
{
    /** @return iterable<string, array{string, string}> */
    public static function uploadMethods(): iterable
    {
        $forms = [
            'legacy', 'legacy-content-type', 'numeric-token', 'current', 'coercible-length',
            'named-sendmux', 'named-qubrics', 'named-both',
            'configured-sendmux', 'configured-qubrics',
        ];
        foreach (['', 'WithHttpInfo', 'Async', 'AsyncWithHttpInfo', 'Request'] as $suffix) {
            foreach ($forms as $form) {
                yield $form . $suffix => ['sendingCompleteAttachmentUpload' . $suffix, $form];
            }
        }
    }

    #[DataProvider('uploadMethods')]
    public function testPublishedUploadArgumentsReachRequest(string $method, string $form): void
    {
        $history = [];
        $handler = HandlerStack::create(new MockHandler([new Response(401)]));
        $handler->push(Middleware::history($history));
        $api = new AttachmentsApi(new Client(['handler' => $handler]), new Configuration());
        if (str_starts_with($form, 'configured-')) {
            $header = $form === 'configured-sendmux' ? 'X-Sendmux-Upload-Token' : 'X-Qubrics-Upload-Token';
            $api->getConfig()->setApiKey($header, 'upload-token');
        }
        $file = new \SplTempFileObject();
        $file->fwrite('test');
        $file->rewind();
        $uploadId = 'upl_aaaaaaaaaaaaaaaaaaaaaaaa';
        $token = $form === 'numeric-token' ? '1234' : 'upload-token';
        $contentType = $form === 'legacy-content-type' ? 'application/x-upload-test' : 'application/octet-stream';
        $arguments = match ($form) {
            'legacy', 'numeric-token' => [$token, 4, $uploadId, $file],
            'legacy-content-type' => [$token, 4, $uploadId, $file, $contentType],
            'current' => [4, $uploadId, $file, $token],
            'coercible-length' => ['4', $uploadId, $file, $token],
            'configured-sendmux', 'configured-qubrics' => [4, $uploadId, $file],
            default => [
                'content_length' => 4,
                'upload_id' => $uploadId,
                'body' => $file,
                'contentType' => $contentType,
                ...($form !== 'named-sendmux' ? ['x_qubrics_upload_token' => $token] : []),
                ...($form !== 'named-qubrics' ? ['x_sendmux_upload_token' => $token] : []),
            ],
        };
        $result = null;

        try {
            // Reflection preserves PHP's weak-call coercion for the existing numeric-string length.
            $result = $form === 'coercible-length'
                ? (new \ReflectionMethod($api, $method))->invokeArgs($api, $arguments)
                : $api->$method(...$arguments);
            if ($result instanceof PromiseInterface) {
                $result->wait();
            }
        } catch (ApiException $error) {
            self::assertSame(401, $error->getCode());
        }

        if ($result instanceof RequestInterface) {
            $request = $result;
        } else {
            self::assertIsArray($history);
            self::assertCount(1, $history);
            $transaction = $history[0];
            self::assertIsArray($transaction);
            $request = $transaction['request'];
            self::assertInstanceOf(RequestInterface::class, $request);
        }

        self::assertSame('PUT', $request->getMethod());
        self::assertSame('/api/v1/emails/attachment-uploads/' . $uploadId, $request->getUri()->getPath());
        self::assertSame('4', $request->getHeaderLine('Content-Length'));
        self::assertSame($contentType, $request->getHeaderLine('Content-Type'));
        self::assertSame('test', $request->getBody()->getContents());
        self::assertSame('', $request->getHeaderLine('Authorization'));
        self::assertSame($token, $request->getHeaderLine('X-Sendmux-Upload-Token'));
        self::assertSame($token, $request->getHeaderLine('X-Qubrics-Upload-Token'));
    }
}
