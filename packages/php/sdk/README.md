# qubrics/sdk

[![Packagist version](https://img.shields.io/packagist/v/qubrics/sdk.svg)](https://packagist.org/packages/qubrics/sdk)
[![PHP version](https://img.shields.io/packagist/dependency-v/qubrics/sdk/php.svg)](https://packagist.org/packages/qubrics/sdk)
[![License](https://img.shields.io/packagist/l/qubrics/sdk.svg)](https://packagist.org/packages/qubrics/sdk)

Umbrella package for Qubrics PHP SDK clients.

Read the PHP SDK guide at [qubrics.com/docs/sdks/php](https://qubrics.com/docs/sdks/php).

## Requirements

- PHP 8.2 or newer.
- Composer.
- A Qubrics API key or REST OAuth grant for each API surface you call.

## Installation

Run this command only after
[Packagist lists `qubrics/sdk` version 3.0.0](https://packagist.org/packages/qubrics/sdk).
Until then, retain your existing Composer constraint.

```bash
composer require qubrics/sdk:^3.0
```

Before upgrading from 2.x, read the [PHP 3.0 migration guide](https://github.com/qubrics/qubrics-sdk/blob/main/packages/php/UPGRADING-3.0.md). SDK 3.0 requires all four Qubrics packages on 3.x. If you use 1.x, apply the [PHP 2.0 migration guide](https://github.com/qubrics/qubrics-sdk/blob/main/packages/php/UPGRADING.md) first.

If your custom Guzzle client uses `FileCookieJar` or `SessionCookieJar`, back up its state and re-authenticate into a fresh jar when upgrading. Guzzle rejects old records without a boolean `HostOnly`; do not guess that value. Default Qubrics API clients do not enable cookies. See the [upstream migration warning](https://github.com/guzzle/guzzle/security/advisories/GHSA-wm3w-8rrp-j577).

## Usage

The umbrella package installs the core, sending, mailbox, and management packages together. Create clients through the surface package factories.

```php
<?php

require __DIR__ . '/vendor/autoload.php';

use Qubrics\Mailbox\ClientFactory as MailboxFactory;
use Qubrics\Management\ClientFactory as ManagementFactory;
use Qubrics\Sending\ClientFactory as SendingFactory;

$sending = SendingFactory::createEmailsApi(
    getenv('QUBRICS_MAILBOX_API_KEY') ?: getenv('SENDMUX_MAILBOX_API_KEY') ?: null
);

$mailbox = MailboxFactory::createMailboxAPIApi(
    getenv('QUBRICS_MAILBOX_API_KEY') ?: getenv('SENDMUX_MAILBOX_API_KEY') ?: null
);

$management = ManagementFactory::createMailboxesApi(
    getenv('QUBRICS_ROOT_API_KEY') ?: getenv('SENDMUX_ROOT_API_KEY') ?: null
);
```

> [!NOTE]
> `qubrics/sdk` installs all PHP SDK surfaces. It does not replace the surface factories.

For OAuth, use each factory's `WithAccessToken` variant, such as `SendingFactory::createMetaApiWithAccessToken($accessToken)`. It accepts a bare token or a callable returning one. See [OAuth setup and lifecycle](https://qubrics.com/docs/developer-tools/oauth).

## Included packages

| Package | Use it for | API key |
| --- | --- | --- |
| [`qubrics/core`](https://packagist.org/packages/qubrics/core) | Shared helpers for auth, headers, retries, pagination, and errors. | Any Qubrics API key. |
| [`qubrics/sending`](https://packagist.org/packages/qubrics/sending) | Sending API client. | `smx_mbx_` or owner-approved `smx_agent_` |
| [`qubrics/mailbox`](https://packagist.org/packages/qubrics/mailbox) | Mailbox API client. | `smx_mbx_` or scoped `smx_agent_` |
| [`qubrics/management`](https://packagist.org/packages/qubrics/management) | Management API client. | `smx_root_` |

The package also exposes `Qubrics\Sdk\Sdk::VERSION` for package-version checks.

## Support

For help, include the package name, version, API surface, and sanitised request details. Do not include API keys, tokens, passwords, webhook secrets, customer data, or private account details.

- PHP SDK guide: [qubrics.com/docs/sdks/php](https://qubrics.com/docs/sdks/php)
- Sending API reference: [qubrics.com/docs/sending-api/introduction](https://qubrics.com/docs/sending-api/introduction)
- Mailbox API reference: [qubrics.com/docs/mailbox-api/introduction](https://qubrics.com/docs/mailbox-api/introduction)
- Management API reference: [qubrics.com/docs/api/introduction](https://qubrics.com/docs/api/introduction)
- API keys guide: [qubrics.com/docs/guides/api-keys](https://qubrics.com/docs/guides/api-keys)
- Source repository: [github.com/qubrics/qubrics-sdk](https://github.com/qubrics/qubrics-sdk)

## License

MIT. See [LICENSE](LICENSE).
