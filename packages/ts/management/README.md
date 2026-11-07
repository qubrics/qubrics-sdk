# @qubrics/management

[![npm version](https://img.shields.io/npm/v/@qubrics%2Fmanagement)](https://www.npmjs.com/package/@qubrics/management)
[![CI](https://github.com/qubrics/qubrics-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/qubrics/qubrics-sdk/actions/workflows/ci.yml)
[![npm downloads](https://img.shields.io/npm/dm/@qubrics%2Fmanagement)](https://www.npmjs.com/package/@qubrics/management)
[![Licence](https://img.shields.io/npm/l/@qubrics%2Fmanagement)](https://github.com/qubrics/qubrics-sdk/blob/main/LICENSE)

Generated TypeScript client for the Qubrics Management API.

## Documentation

- Management API reference: [qubrics.com/docs/api/introduction](https://qubrics.com/docs/api/introduction)
- Source repository: [qubrics/qubrics-sdk](https://github.com/qubrics/qubrics-sdk)

## Requirements

- A root Qubrics API key with the `smx_root_*` prefix; alternatively, a REST OAuth grant for this surface.
- A JavaScript runtime with the standard Fetch API.

## Installation

```sh
npm install @qubrics/management
```

<a id="migrate-from-1x-to-20"></a>

## Result-type migration from earlier releases

If you pass sending-account list entries to code that expects a detail result,
update those types when upgrading from an earlier release. `managementListProviders` returns
`ProviderListItem` entries without `variables`; `managementGetProvider` returns
a `ProviderItem` with required `variables`. A list entry no longer satisfies the
detail type.

1. Derive separate list and detail types from the public operations. The package
   doesn't export these generated model names directly:

   ```ts
   import {
     managementGetProvider,
     managementListProviders,
   } from "@qubrics/management";

   type ProviderListItem = NonNullable<
     Awaited<ReturnType<typeof managementListProviders>>["data"]
   >["data"][number];
   type ProviderItem = NonNullable<
     Awaited<ReturnType<typeof managementGetProvider>>["data"]
   >["data"];
   ```

2. For code that only needs list fields, replace the detail annotation with the
   list type:

   ```ts
   // Before: type ProviderRow = ProviderItem;
   type ProviderRow = ProviderListItem;
   ```

   If you need `variables`, fetch the detail with `managementGetProvider` using
   the account's `id` as `path.public_id`. Don't cast a list entry to `ProviderItem` or add
   an empty `variables` object to stand in for the account's actual variables.

3. Run your application's TypeScript check. List-only code should accept
   `ProviderListItem`; code that reads `variables` must receive a detail result.

## OAuth access tokens

Pass `accessToken` instead of `apiKey` for a REST OAuth token or synchronous/asynchronous provider.

```ts
import { createManagementClient } from "@qubrics/management";

const client = createManagementClient({
  accessToken: () => process.env.QUBRICS_ACCESS_TOKEN!,
});
```

The provider runs before each request. Your application owns token storage and refresh; required scopes still apply. See [OAuth setup](https://qubrics.com/docs/developer-tools/oauth).

## Usage

```ts
import {
  createManagementClient,
  managementListDomains,
} from "@qubrics/management";

const client = createManagementClient({
  apiKey: process.env.QUBRICS_API_KEY!,
});

const domains = await managementListDomains({ client });

console.log(domains.data);
```

The package exports every generated Management operation plus:

- `createManagementClient`
- `configureManagement`
- `ManagementClient`

## Conditional requests

Use `conditionalHeaders` from `@qubrics/core` for operations that accept `If-Match` or `If-None-Match`.

```ts
import { conditionalHeaders } from "@qubrics/core";
import {
  createManagementClient,
  managementGetDomain,
} from "@qubrics/management";

const client = createManagementClient({
  apiKey: process.env.QUBRICS_API_KEY!,
});

const domain = await managementGetDomain({
  client,
  path: { public_id: "mdom_123" },
  headers: { ...conditionalHeaders({ ifNoneMatch: 'W/"etag"' }) },
});

console.log(domain.data);
```

## Support

Open an issue in [qubrics/qubrics-sdk](https://github.com/qubrics/qubrics-sdk/issues) with the package name, version, and request ID from any API error.

## Licence

MIT. See the [licence file](https://github.com/qubrics/qubrics-sdk/blob/main/LICENSE).
