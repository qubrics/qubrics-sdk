# qubrics/core

[![Packagist version](https://img.shields.io/packagist/v/qubrics/core.svg)](https://packagist.org/packages/qubrics/core)
[![PHP version](https://img.shields.io/packagist/dependency-v/qubrics/core/php.svg)](https://packagist.org/packages/qubrics/core)
[![License](https://img.shields.io/packagist/l/qubrics/core.svg)](https://packagist.org/packages/qubrics/core)

Shared runtime helpers for Qubrics PHP SDK packages.

Read the PHP SDK guide at [qubrics.com/docs/sdks/php](https://qubrics.com/docs/sdks/php).

## Requirements

- PHP 8.2 or newer.
- Composer.

## Installation

Run this command only after
[Packagist lists `qubrics/core` version 3.0.0](https://packagist.org/packages/qubrics/core).
Until then, retain your existing Composer constraint.

```bash
composer require qubrics/core:^3.0
```

Before upgrading from 2.x, read the [PHP 3.0 migration guide](https://github.com/qubrics/qubrics-sdk/blob/main/packages/php/UPGRADING-3.0.md) for Composer package and PHP namespace changes. If you use 1.x, apply the [PHP 2.0 migration guide](https://github.com/qubrics/qubrics-sdk/blob/main/packages/php/UPGRADING.md) first.

If your custom Guzzle client uses `FileCookieJar` or `SessionCookieJar`, back up its state and re-authenticate into a fresh jar when upgrading. Guzzle rejects old records without a boolean `HostOnly`; do not guess that value. Default Qubrics API clients do not enable cookies. See the [upstream migration warning](https://github.com/guzzle/guzzle/security/advisories/GHSA-wm3w-8rrp-j577).

## Usage

Use `qubrics/core` directly when you need the shared helper layer without a generated API client.

```php
<?php

require __DIR__ . '/vendor/autoload.php';

use Qubrics\Core\ApiKeySurface;
use Qubrics\Core\Auth;
use Qubrics\Core\Headers;
use Qubrics\Core\RetryOptions;

$apiKey = getenv('QUBRICS_MAILBOX_API_KEY') ?: getenv('SENDMUX_MAILBOX_API_KEY') ?: '';

Auth::assertApiKeySurface($apiKey, ApiKeySurface::Mailbox);

$headers = array_merge(
    Headers::idempotency('order-123'),
    Headers::conditional(ifMatch: '"mailbox-etag"')
);

$retryOptions = new RetryOptions(maxAttempts: 3);
```

## Features

- `Auth` validates `smx_root_` prefixes for root clients, send-capable `smx_mbx_` prefixes or owner-approved Sending-resource `smx_agent_` tokens for Sending clients, and mailbox-compatible `smx_mbx_` or `smx_agent_` prefixes for Mailbox clients.
- `Headers` builds `Idempotency-Key`, `If-Match`, and `If-None-Match` header arrays.
- `Pagination::iterate()` streams cursor-paginated responses.
- `Auth::accessTokenMiddleware()` validates a bare OAuth token or callable provider and adds the bearer header per attempt.
- `RetryMiddleware` honours `Retry-After`, `X-RateLimit-Reset` and explicit `error.retryable: false`. `maxDelayMilliseconds` caps local backoff only; `RetryOptions(maxElapsedMilliseconds: 5000)` stops retries that would exceed the budget and returns the last response with its retry metadata. The budget does not interrupt an in-flight request; configure transport timeouts separately.
- `ErrorMapper` maps generated exceptions into `QubricsApiError`.

## Package map

| Package | Use it for |
| --- | --- |
| [`qubrics/sending`](https://packagist.org/packages/qubrics/sending) | Sending API client. |
| [`qubrics/mailbox`](https://packagist.org/packages/qubrics/mailbox) | Mailbox API client. |
| [`qubrics/management`](https://packagist.org/packages/qubrics/management) | Management API client. |
| [`qubrics/sdk`](https://packagist.org/packages/qubrics/sdk) | Umbrella package that installs all PHP SDK surfaces. |

## Support

For help, include the package name, version, API surface, and sanitised request details. Do not include API keys, tokens, passwords, webhook secrets, customer data, or private account details.

- SDK docs: [qubrics.com/docs/sdks/php](https://qubrics.com/docs/sdks/php)
- API keys guide: [qubrics.com/docs/guides/api-keys](https://qubrics.com/docs/guides/api-keys)
- Source repository: [github.com/qubrics/qubrics-sdk](https://github.com/qubrics/qubrics-sdk)

## License

MIT. See [LICENSE](LICENSE).
