<?php

declare(strict_types=1);

namespace Qubrics\Management;

use Qubrics\Management\Api\BillingApi;
use Qubrics\Management\Api\ConnectionApi;
use Qubrics\Management\Api\DomainFiltersApi;
use Qubrics\Management\Api\DomainsApi;
use Qubrics\Management\Api\EmailsApi;
use Qubrics\Management\Api\InboxesApi;
use Qubrics\Management\Api\MailboxFiltersApi;
use Qubrics\Management\Api\MailboxesApi;
use Qubrics\Management\Api\SendingAccountsApi;
use Qubrics\Management\Api\WebhooksApi;
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
        $configured = Auth::configureBearer($configuration, $apiKey, ApiKeySurface::Root);
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

    public static function createBillingApi(
        ?string $apiKey = null,
        ?string $baseUrl = null,
        ?RetryOptions $retryOptions = null
    ): BillingApi {
        return new BillingApi(
            self::httpClient($retryOptions),
            self::configuration($apiKey, $baseUrl)
        );
    }

    /** @param string|callable(): string $accessToken */
    public static function createBillingApiWithAccessToken(
        string|callable $accessToken,
        ?string $baseUrl = null,
        ?RetryOptions $retryOptions = null
    ): BillingApi {
        $qubricsBaseUrl = getenv('QUBRICS_BASE_URL');
        $baseUrl ??= $qubricsBaseUrl !== false && $qubricsBaseUrl !== ''
            ? $qubricsBaseUrl : (getenv('SENDMUX_BASE_URL') ?: null);
        $configuration = new Configuration();
        if ($baseUrl !== null && $baseUrl !== '') {
            $configuration->setHost($baseUrl);
        }

        return new BillingApi(
            self::httpClient($retryOptions, $accessToken),
            $configuration
        );
    }

    public static function createConnectionApi(
        ?string $apiKey = null,
        ?string $baseUrl = null,
        ?RetryOptions $retryOptions = null
    ): ConnectionApi {
        return new ConnectionApi(
            self::httpClient($retryOptions),
            self::configuration($apiKey, $baseUrl)
        );
    }

    /** @param string|callable(): string $accessToken */
    public static function createConnectionApiWithAccessToken(
        string|callable $accessToken,
        ?string $baseUrl = null,
        ?RetryOptions $retryOptions = null
    ): ConnectionApi {
        $qubricsBaseUrl = getenv('QUBRICS_BASE_URL');
        $baseUrl ??= $qubricsBaseUrl !== false && $qubricsBaseUrl !== ''
            ? $qubricsBaseUrl : (getenv('SENDMUX_BASE_URL') ?: null);
        $configuration = new Configuration();
        if ($baseUrl !== null && $baseUrl !== '') {
            $configuration->setHost($baseUrl);
        }

        return new ConnectionApi(
            self::httpClient($retryOptions, $accessToken),
            $configuration
        );
    }

    public static function createDomainFiltersApi(
        ?string $apiKey = null,
        ?string $baseUrl = null,
        ?RetryOptions $retryOptions = null
    ): DomainFiltersApi {
        return new DomainFiltersApi(
            self::httpClient($retryOptions),
            self::configuration($apiKey, $baseUrl)
        );
    }

    /** @param string|callable(): string $accessToken */
    public static function createDomainFiltersApiWithAccessToken(
        string|callable $accessToken,
        ?string $baseUrl = null,
        ?RetryOptions $retryOptions = null
    ): DomainFiltersApi {
        $qubricsBaseUrl = getenv('QUBRICS_BASE_URL');
        $baseUrl ??= $qubricsBaseUrl !== false && $qubricsBaseUrl !== ''
            ? $qubricsBaseUrl : (getenv('SENDMUX_BASE_URL') ?: null);
        $configuration = new Configuration();
        if ($baseUrl !== null && $baseUrl !== '') {
            $configuration->setHost($baseUrl);
        }

        return new DomainFiltersApi(
            self::httpClient($retryOptions, $accessToken),
            $configuration
        );
    }

    public static function createDomainsApi(
        ?string $apiKey = null,
        ?string $baseUrl = null,
        ?RetryOptions $retryOptions = null
    ): DomainsApi {
        return new DomainsApi(
            self::httpClient($retryOptions),
            self::configuration($apiKey, $baseUrl)
        );
    }

    /** @param string|callable(): string $accessToken */
    public static function createDomainsApiWithAccessToken(
        string|callable $accessToken,
        ?string $baseUrl = null,
        ?RetryOptions $retryOptions = null
    ): DomainsApi {
        $qubricsBaseUrl = getenv('QUBRICS_BASE_URL');
        $baseUrl ??= $qubricsBaseUrl !== false && $qubricsBaseUrl !== ''
            ? $qubricsBaseUrl : (getenv('SENDMUX_BASE_URL') ?: null);
        $configuration = new Configuration();
        if ($baseUrl !== null && $baseUrl !== '') {
            $configuration->setHost($baseUrl);
        }

        return new DomainsApi(
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

    public static function createInboxesApi(
        ?string $apiKey = null,
        ?string $baseUrl = null,
        ?RetryOptions $retryOptions = null
    ): InboxesApi {
        return new InboxesApi(
            self::httpClient($retryOptions),
            self::configuration($apiKey, $baseUrl)
        );
    }

    /** @param string|callable(): string $accessToken */
    public static function createInboxesApiWithAccessToken(
        string|callable $accessToken,
        ?string $baseUrl = null,
        ?RetryOptions $retryOptions = null
    ): InboxesApi {
        $qubricsBaseUrl = getenv('QUBRICS_BASE_URL');
        $baseUrl ??= $qubricsBaseUrl !== false && $qubricsBaseUrl !== ''
            ? $qubricsBaseUrl : (getenv('SENDMUX_BASE_URL') ?: null);
        $configuration = new Configuration();
        if ($baseUrl !== null && $baseUrl !== '') {
            $configuration->setHost($baseUrl);
        }

        return new InboxesApi(
            self::httpClient($retryOptions, $accessToken),
            $configuration
        );
    }

    public static function createMailboxFiltersApi(
        ?string $apiKey = null,
        ?string $baseUrl = null,
        ?RetryOptions $retryOptions = null
    ): MailboxFiltersApi {
        return new MailboxFiltersApi(
            self::httpClient($retryOptions),
            self::configuration($apiKey, $baseUrl)
        );
    }

    /** @param string|callable(): string $accessToken */
    public static function createMailboxFiltersApiWithAccessToken(
        string|callable $accessToken,
        ?string $baseUrl = null,
        ?RetryOptions $retryOptions = null
    ): MailboxFiltersApi {
        $qubricsBaseUrl = getenv('QUBRICS_BASE_URL');
        $baseUrl ??= $qubricsBaseUrl !== false && $qubricsBaseUrl !== ''
            ? $qubricsBaseUrl : (getenv('SENDMUX_BASE_URL') ?: null);
        $configuration = new Configuration();
        if ($baseUrl !== null && $baseUrl !== '') {
            $configuration->setHost($baseUrl);
        }

        return new MailboxFiltersApi(
            self::httpClient($retryOptions, $accessToken),
            $configuration
        );
    }

    public static function createMailboxesApi(
        ?string $apiKey = null,
        ?string $baseUrl = null,
        ?RetryOptions $retryOptions = null
    ): MailboxesApi {
        return new MailboxesApi(
            self::httpClient($retryOptions),
            self::configuration($apiKey, $baseUrl)
        );
    }

    /** @param string|callable(): string $accessToken */
    public static function createMailboxesApiWithAccessToken(
        string|callable $accessToken,
        ?string $baseUrl = null,
        ?RetryOptions $retryOptions = null
    ): MailboxesApi {
        $qubricsBaseUrl = getenv('QUBRICS_BASE_URL');
        $baseUrl ??= $qubricsBaseUrl !== false && $qubricsBaseUrl !== ''
            ? $qubricsBaseUrl : (getenv('SENDMUX_BASE_URL') ?: null);
        $configuration = new Configuration();
        if ($baseUrl !== null && $baseUrl !== '') {
            $configuration->setHost($baseUrl);
        }

        return new MailboxesApi(
            self::httpClient($retryOptions, $accessToken),
            $configuration
        );
    }

    public static function createSendingAccountsApi(
        ?string $apiKey = null,
        ?string $baseUrl = null,
        ?RetryOptions $retryOptions = null
    ): SendingAccountsApi {
        return new SendingAccountsApi(
            self::httpClient($retryOptions),
            self::configuration($apiKey, $baseUrl)
        );
    }

    /** @param string|callable(): string $accessToken */
    public static function createSendingAccountsApiWithAccessToken(
        string|callable $accessToken,
        ?string $baseUrl = null,
        ?RetryOptions $retryOptions = null
    ): SendingAccountsApi {
        $qubricsBaseUrl = getenv('QUBRICS_BASE_URL');
        $baseUrl ??= $qubricsBaseUrl !== false && $qubricsBaseUrl !== ''
            ? $qubricsBaseUrl : (getenv('SENDMUX_BASE_URL') ?: null);
        $configuration = new Configuration();
        if ($baseUrl !== null && $baseUrl !== '') {
            $configuration->setHost($baseUrl);
        }

        return new SendingAccountsApi(
            self::httpClient($retryOptions, $accessToken),
            $configuration
        );
    }

    public static function createWebhooksApi(
        ?string $apiKey = null,
        ?string $baseUrl = null,
        ?RetryOptions $retryOptions = null
    ): WebhooksApi {
        return new WebhooksApi(
            self::httpClient($retryOptions),
            self::configuration($apiKey, $baseUrl)
        );
    }

    /** @param string|callable(): string $accessToken */
    public static function createWebhooksApiWithAccessToken(
        string|callable $accessToken,
        ?string $baseUrl = null,
        ?RetryOptions $retryOptions = null
    ): WebhooksApi {
        $qubricsBaseUrl = getenv('QUBRICS_BASE_URL');
        $baseUrl ??= $qubricsBaseUrl !== false && $qubricsBaseUrl !== ''
            ? $qubricsBaseUrl : (getenv('SENDMUX_BASE_URL') ?: null);
        $configuration = new Configuration();
        if ($baseUrl !== null && $baseUrl !== '') {
            $configuration->setHost($baseUrl);
        }

        return new WebhooksApi(
            self::httpClient($retryOptions, $accessToken),
            $configuration
        );
    }
}
