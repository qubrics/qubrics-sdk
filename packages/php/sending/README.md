# qubrics/sending

[![Packagist version](https://img.shields.io/packagist/v/qubrics/sending.svg)](https://packagist.org/packages/qubrics/sending)
[![PHP version](https://img.shields.io/packagist/dependency-v/qubrics/sending/php.svg)](https://packagist.org/packages/qubrics/sending)
[![License](https://img.shields.io/packagist/l/qubrics/sending.svg)](https://packagist.org/packages/qubrics/sending)

Qubrics Sending API client for PHP.

Read the PHP SDK guide at [qubrics.com/docs/sdks/php](https://qubrics.com/docs/sdks/php).

## Requirements

- PHP 8.2 or newer.
- Composer.
- A send-capable `smx_mbx_` key or owner-approved Sending-resource `smx_agent_` token. Alternatively, use a REST OAuth access token with the required scopes.

## Installation

Run this command only after
[Packagist lists `qubrics/sending` version 3.0.0](https://packagist.org/packages/qubrics/sending).
Until then, retain your existing Composer constraint.

```bash
composer require qubrics/sending:^3.0
```

Upgrading from 1.x? Read the [PHP 2.0 migration guide](https://github.com/qubrics/qubrics-sdk/blob/main/packages/php/UPGRADING.md) before changing your Composer constraint.

If your custom Guzzle client uses `FileCookieJar` or `SessionCookieJar`, back up its state and re-authenticate into a fresh jar when upgrading. Guzzle rejects old records without a boolean `HostOnly`; do not guess that value. Default Qubrics API clients do not enable cookies. See the [upstream migration warning](https://github.com/guzzle/guzzle/security/advisories/GHSA-wm3w-8rrp-j577).

## Usage

Create the API group client with a send-capable key.

```php
<?php

require __DIR__ . '/vendor/autoload.php';

use Qubrics\Sending\ClientFactory;

$emails = ClientFactory::createEmailsApi(
    getenv('QUBRICS_MAILBOX_API_KEY') ?: ''
);

$meta = ClientFactory::createMetaApi(
    getenv('QUBRICS_MAILBOX_API_KEY') ?: ''
);
```

The generated `EmailsApi` exposes `sendingSendEmail()` and `sendingSendEmailBatch()`. The generated `MetaApi` exposes `sendingGetConnection()` to test credentials without sending email, and `sendingGetOpenApiSpec()`.

## OAuth access tokens

`ClientFactory::createMetaApiWithAccessToken($accessToken)` accepts a bare token or a callable returning one. Every API group factory has the same `WithAccessToken` variant. Providers run on each request and retry; your application owns token storage and refresh coordination. OAuth clients do not follow redirects.

```php
$client = ClientFactory::createMetaApiWithAccessToken(
    static fn (): string => getenv('QUBRICS_ACCESS_TOKEN') ?: ''
);
```

See [OAuth setup and lifecycle](https://qubrics.com/docs/developer-tools/oauth).

For API-key authentication, omit `apiKey` to read `QUBRICS_API_KEY`.
Omit `baseUrl` to read `QUBRICS_BASE_URL`.
Nonempty Qubrics values take precedence over `SENDMUX_API_KEY` and
`SENDMUX_BASE_URL`. Explicit arguments take precedence over environment values.

## Features

- Validates `smx_mbx_` keys or owner-approved Sending-resource `smx_agent_` tokens before configuring the client.
- Uses `https://smtp.qubrics.com/api/v1` by default.
- Adds retry and rate-limit backoff behaviour through `qubrics/core`.
- Maps generated API responses into the shared Qubrics envelope and error model.
- Includes generated models for single-send and batch-send requests and responses.

## Related packages

| Package | Use it for |
| --- | --- |
| [`qubrics/core`](https://packagist.org/packages/qubrics/core) | Shared helpers for auth, headers, retries, pagination, and errors. |
| [`qubrics/mailbox`](https://packagist.org/packages/qubrics/mailbox) | Mailbox API client. |
| [`qubrics/management`](https://packagist.org/packages/qubrics/management) | Management API client. |
| [`qubrics/sdk`](https://packagist.org/packages/qubrics/sdk) | Umbrella package that installs all PHP SDK surfaces. |

## Support

For help, include the package name, version, API surface, and sanitised request details. Do not include API keys, tokens, passwords, webhook secrets, customer data, or private account details.

- PHP SDK guide: [qubrics.com/docs/sdks/php](https://qubrics.com/docs/sdks/php)
- Sending API reference: [qubrics.com/docs/sending-api/introduction](https://qubrics.com/docs/sending-api/introduction)
- API keys guide: [qubrics.com/docs/guides/api-keys](https://qubrics.com/docs/guides/api-keys)
- Source repository: [github.com/qubrics/qubrics-sdk](https://github.com/qubrics/qubrics-sdk)

## License

MIT. See [LICENSE](LICENSE).
