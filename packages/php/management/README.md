# qubrics/management

[![Packagist version](https://img.shields.io/packagist/v/qubrics/management.svg)](https://packagist.org/packages/qubrics/management)
[![PHP version](https://img.shields.io/packagist/dependency-v/qubrics/management/php.svg)](https://packagist.org/packages/qubrics/management)
[![License](https://img.shields.io/packagist/l/qubrics/management.svg)](https://packagist.org/packages/qubrics/management)

Qubrics Management API client for PHP.

Read the PHP SDK guide at [qubrics.com/docs/sdks/php](https://qubrics.com/docs/sdks/php).

## Requirements

- PHP 8.2 or newer.
- Composer.
- A team-scoped API key with the `smx_root_` prefix. Alternatively, use a REST OAuth access token with the required scopes.

## Installation

Run this command only after
[Packagist lists `qubrics/management` version 3.0.0](https://packagist.org/packages/qubrics/management).
Until then, retain your existing Composer constraint.

```bash
composer require qubrics/management:^3.0
```

Upgrading from 1.x? Read the [PHP 2.0 migration guide](https://github.com/qubrics/qubrics-sdk/blob/main/packages/php/UPGRADING.md) before changing your Composer constraint.

If your custom Guzzle client uses `FileCookieJar` or `SessionCookieJar`, back up its state and re-authenticate into a fresh jar when upgrading. Guzzle rejects old records without a boolean `HostOnly`; do not guess that value. Default Qubrics API clients do not enable cookies. See the [upstream migration warning](https://github.com/guzzle/guzzle/security/advisories/GHSA-wm3w-8rrp-j577).

## Usage

Create the generated API group you need with a team-scoped key.

```php
<?php

require __DIR__ . '/vendor/autoload.php';

use Qubrics\Management\ClientFactory;

$connection = ClientFactory::createConnectionApi(
    getenv('QUBRICS_ROOT_API_KEY') ?: ''
);

$mailboxes = ClientFactory::createMailboxesApi(
    getenv('QUBRICS_ROOT_API_KEY') ?: ''
);

$domains = ClientFactory::createDomainsApi(
    getenv('QUBRICS_ROOT_API_KEY') ?: ''
);

$webhooks = ClientFactory::createWebhooksApi(
    getenv('QUBRICS_ROOT_API_KEY') ?: ''
);
```

Use `$connection->managementGetConnection()` to test credentials and retrieve team and credential details.

The factory also exposes clients for billing, domain filters, emails, inboxes, mailbox filters, sending accounts, and webhooks.

## OAuth access tokens

`ClientFactory::createConnectionApiWithAccessToken($accessToken)` accepts a bare token or a callable returning one. Every API group factory has the same `WithAccessToken` variant. Providers run on each request and retry; your application owns token storage and refresh coordination. OAuth clients do not follow redirects.

```php
$client = ClientFactory::createConnectionApiWithAccessToken(
    static fn (): string => getenv('QUBRICS_ACCESS_TOKEN') ?: ''
);
```

See [OAuth setup and lifecycle](https://qubrics.com/docs/developer-tools/oauth).

For API-key authentication, omit `apiKey` to read `QUBRICS_API_KEY`.
Omit `baseUrl` to read `QUBRICS_BASE_URL`.
Nonempty Qubrics values take precedence over `SENDMUX_API_KEY` and
`SENDMUX_BASE_URL`. Explicit arguments take precedence over environment values.

## Features

- Validates `smx_root_` API keys before configuring the client.
- Uses `https://app.qubrics.com/api/v1` by default.
- Adds retry and rate-limit backoff behaviour through `qubrics/core`.
- Covers domains, sending accounts, mailboxes, filters, webhooks, logs, metrics, and billing data.
- Includes generated models for Management API requests and responses.

## Related packages

| Package | Use it for |
| --- | --- |
| [`qubrics/core`](https://packagist.org/packages/qubrics/core) | Shared helpers for auth, headers, retries, pagination, and errors. |
| [`qubrics/sending`](https://packagist.org/packages/qubrics/sending) | Sending API client. |
| [`qubrics/mailbox`](https://packagist.org/packages/qubrics/mailbox) | Mailbox API client. |
| [`qubrics/sdk`](https://packagist.org/packages/qubrics/sdk) | Umbrella package that installs all PHP SDK surfaces. |

## Support

For help, include the package name, version, API surface, and sanitised request details. Do not include API keys, tokens, passwords, webhook secrets, customer data, or private account details.

- PHP SDK guide: [qubrics.com/docs/sdks/php](https://qubrics.com/docs/sdks/php)
- Management API reference: [qubrics.com/docs/api/introduction](https://qubrics.com/docs/api/introduction)
- API keys guide: [qubrics.com/docs/guides/api-keys](https://qubrics.com/docs/guides/api-keys)
- Source repository: [github.com/qubrics/qubrics-sdk](https://github.com/qubrics/qubrics-sdk)

## License

MIT. See [LICENSE](LICENSE).
