<?php

declare(strict_types=1);

namespace Qubrics\Sending;

use Qubrics\Sending\Api\AttachmentsApi;
use Qubrics\Sending\Api\EmailsApi;
use Qubrics\Sending\Api\MetaApi;
use GuzzleHttp\Client;
use GuzzleHttp\ClientInterface;
use GuzzleHttp\HandlerStack;
use Qubrics\Core\ApiKeySurface;
use Qubrics\Core\Auth;
use Qubrics\Core\RetryMiddleware;
use Qubrics\Core\RetryOptions;

final class ClientFactory
{
    public static function configuration(?string $apiKey = null, ?string $baseUrl = null): Configuration
    {
        $qubricsApiKey = getenv('QUBRICS_API_KEY');
        $apiKey ??= $qubricsApiKey !== false && $qubricsApiKey !== ''
            ? $qubricsApiKey : (getenv('SENDMUX_API_KEY') ?: '');
        $qubricsBaseUrl = getenv('QUBRICS_BASE_URL');
        $baseUrl ??= $qubricsBaseUrl !== false && $qubricsBaseUrl !== ''
            ? $qubricsBaseUrl : (getenv('SENDMUX_BASE_URL') ?: null);
        $configuration = new Configuration();
        if ($baseUrl !== null && $baseUrl !== '') {
            $configuration->setHost($baseUrl);
        }

        /** @var Configuration $configured */
        $configured = Auth::configureBearer($configuration, $apiKey, ApiKeySurface::Sending);
        return $configured;
    }

    /** @param string|callable(): string|null $accessToken */
    public static function httpClient(
        ?RetryOptions $retryOptions = null,
        string|callable|null $accessToken = null
    ): ClientInterface {
        $stack = HandlerStack::create();
        $stack->push(RetryMiddleware::create($retryOptions), 'sendmux_retry');
        if ($accessToken !== null) {
            $stack->push(Auth::accessTokenMiddleware($accessToken), 'sendmux_oauth');
        }

        return new Client(['handler' => $stack, 'allow_redirects' => $accessToken === null]);
    }

    public static function createAttachmentsApi(
        ?string $apiKey = null,
        ?string $baseUrl = null,
        ?RetryOptions $retryOptions = null
    ): AttachmentsApi {
        return new AttachmentsApi(
            self::httpClient($retryOptions),
            self::configuration($apiKey, $baseUrl)
        );
    }

    /** @param string|callable(): string $accessToken */
    public static function createAttachmentsApiWithAccessToken(
        string|callable $accessToken,
        ?string $baseUrl = null,
        ?RetryOptions $retryOptions = null
    ): AttachmentsApi {
        $qubricsBaseUrl = getenv('QUBRICS_BASE_URL');
        $baseUrl ??= $qubricsBaseUrl !== false && $qubricsBaseUrl !== ''
            ? $qubricsBaseUrl : (getenv('SENDMUX_BASE_URL') ?: null);
        $configuration = new Configuration();
        if ($baseUrl !== null && $baseUrl !== '') {
            $configuration->setHost($baseUrl);
        }

        return new AttachmentsApi(
            self::httpClient($retryOptions, $accessToken),
            $configuration
        );
    }

    public static function createEmailsApi(
        ?string $apiKey = null,
        ?string $baseUrl = null,
        ?RetryOptions $retryOptions = null
    ): EmailsApi {
        return new EmailsApi(
            self::httpClient($retryOptions),
            self::configuration($apiKey, $baseUrl)
        );
    }

    /** @param string|callable(): string $accessToken */
    public static function createEmailsApiWithAccessToken(
        string|callable $accessToken,
        ?string $baseUrl = null,
        ?RetryOptions $retryOptions = null
    ): EmailsApi {
        $qubricsBaseUrl = getenv('QUBRICS_BASE_URL');
        $baseUrl ??= $qubricsBaseUrl !== false && $qubricsBaseUrl !== ''
            ? $qubricsBaseUrl : (getenv('SENDMUX_BASE_URL') ?: null);
        $configuration = new Configuration();
        if ($baseUrl !== null && $baseUrl !== '') {
            $configuration->setHost($baseUrl);
        }

        return new EmailsApi(
            self::httpClient($retryOptions, $accessToken),
            $configuration
        );
    }

    public static function createMetaApi(
        ?string $apiKey = null,
        ?string $baseUrl = null,
        ?RetryOptions $retryOptions = null
    ): MetaApi {
        return new MetaApi(
            self::httpClient($retryOptions),
            self::configuration($apiKey, $baseUrl)
        );
    }

    /** @param string|callable(): string $accessToken */
    public static function createMetaApiWithAccessToken(
        string|callable $accessToken,
        ?string $baseUrl = null,
        ?RetryOptions $retryOptions = null
    ): MetaApi {
        $qubricsBaseUrl = getenv('QUBRICS_BASE_URL');
        $baseUrl ??= $qubricsBaseUrl !== false && $qubricsBaseUrl !== ''
            ? $qubricsBaseUrl : (getenv('SENDMUX_BASE_URL') ?: null);
        $configuration = new Configuration();
        if ($baseUrl !== null && $baseUrl !== '') {
            $configuration->setHost($baseUrl);
        }

        return new MetaApi(
            self::httpClient($retryOptions, $accessToken),
            $configuration
        );
    }
}
