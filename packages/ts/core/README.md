# @qubrics/core

[![npm version](https://img.shields.io/npm/v/@qubrics%2Fcore)](https://www.npmjs.com/package/@qubrics/core)
[![CI](https://github.com/qubrics/qubrics-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/qubrics/qubrics-sdk/actions/workflows/ci.yml)
[![npm downloads](https://img.shields.io/npm/dm/@qubrics%2Fcore)](https://www.npmjs.com/package/@qubrics/core)
[![Licence](https://img.shields.io/npm/l/@qubrics%2Fcore)](https://github.com/qubrics/qubrics-sdk/blob/main/LICENSE)

Shared runtime helpers and public types for the Qubrics TypeScript SDK packages.

## Documentation

- Qubrics docs: [qubrics.com/docs](https://qubrics.com/docs)
- Source repository: [qubrics/qubrics-sdk](https://github.com/qubrics/qubrics-sdk)

## Requirements

- A JavaScript runtime with the standard Fetch API.
- A surface package such as `@qubrics/sending`, `@qubrics/mailbox`, or `@qubrics/management` for API operations.

## Installation

```sh
npm install @qubrics/core
```

## Usage

Validate a key prefix and prepare request headers before calling a surface package.

```ts
import {
  assertApiKeyKind,
  conditionalHeaders,
  idempotencyHeaders,
} from "@qubrics/core";

assertApiKeyKind(process.env.QUBRICS_MAILBOX_API_KEY!, "mailbox");

const headers = {
  ...idempotencyHeaders("idem_123"),
  ...conditionalHeaders({ ifNoneMatch: 'W/"etag"' }),
};
```

## Helpers

- `assertApiKeyKind` validates `smx_root_*` prefixes for root clients, send-capable `smx_mbx_*` prefixes or owner-approved Sending-resource `smx_agent_*` tokens for Sending clients, and mailbox-compatible `smx_mbx_*` or `smx_agent_*` prefixes for Mailbox clients.
- `paginate` iterates cursor-paginated Qubrics list responses.
- `idempotencyHeaders`, `conditionalHeaders`, and `responseEtag` cover idempotency and conditional requests.
- `createRetryingFetch` retries safe requests and idempotent `POST` requests with replayable bodies. It honours `retryable: false` and server retry delays; when a delay exceeds the configured deadline or runtime limit, it returns the response instead of retrying early.
- `SendmuxApiError`, `mapApiError`, and `createErrorInterceptor` normalise API errors.

## Support

Open an issue in [qubrics/qubrics-sdk](https://github.com/qubrics/qubrics-sdk/issues) with the package name and version.

## Licence

MIT. See the [licence file](https://github.com/qubrics/qubrics-sdk/blob/main/LICENSE).
