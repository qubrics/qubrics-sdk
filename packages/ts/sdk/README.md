# @qubrics/sdk

[![npm version](https://img.shields.io/npm/v/@qubrics%2Fsdk)](https://www.npmjs.com/package/@qubrics/sdk)
[![CI](https://github.com/qubrics/qubrics-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/qubrics/qubrics-sdk/actions/workflows/ci.yml)
[![npm downloads](https://img.shields.io/npm/dm/@qubrics%2Fsdk)](https://www.npmjs.com/package/@qubrics/sdk)
[![Licence](https://img.shields.io/npm/l/@qubrics%2Fsdk)](https://github.com/qubrics/qubrics-sdk/blob/main/LICENSE)

Optional umbrella package for the Qubrics TypeScript SDK.

## Documentation

- Qubrics docs: [qubrics.com/docs](https://qubrics.com/docs)
- Management API reference: [qubrics.com/docs/api/introduction](https://qubrics.com/docs/api/introduction)
- Mailbox API reference: [qubrics.com/docs/mailbox-api/introduction](https://qubrics.com/docs/mailbox-api/introduction)
- Sending API reference: [qubrics.com/docs/sending-api/introduction](https://qubrics.com/docs/sending-api/introduction)
- Source repository: [qubrics/qubrics-sdk](https://github.com/qubrics/qubrics-sdk)

## Requirements

- A send-capable `smx_mbx_*` key or owner-approved Sending-resource `smx_agent_*` token for Sending clients.
- A mailbox-scoped `smx_mbx_*` key or scoped `smx_agent_*` token for Mailbox clients.
- A root `smx_root_*` key for Management clients.
- A JavaScript runtime with the standard Fetch API.

## Installation

```sh
npm install @qubrics/sdk
```

<a id="migrate-from-1x-to-20"></a>

## Result-type migration from earlier releases

`@qubrics/sdk` re-exports `@qubrics/management` and `@qubrics/mailbox`,
including their result-type changes from earlier releases.
If you pass sending-account list entries to code that expects a
detail result, or construct thread-message list results (fixtures, mocks, or
wrappers annotated with the operation's result type), update those types before
upgrading from an earlier release. Code that only reads results keeps compiling.

1. `management.managementListProviders` returns `ProviderListItem` entries
   without `variables`; `management.managementGetProvider` returns a
   `ProviderItem` with required `variables`. A list entry no longer satisfies
   the detail type. Derive separate list and detail types from the public
   operations (the namespaces don't export these generated model names
   directly), and give list-only code the list type:

   ```ts
   import { management } from "@qubrics/sdk";

   type ProviderListItem = NonNullable<
     Awaited<ReturnType<typeof management.managementListProviders>>["data"]
   >["data"][number];
   type ProviderItem = NonNullable<
     Awaited<ReturnType<typeof management.managementGetProvider>>["data"]
   >["data"];

   // Before: type ProviderRow = ProviderItem;
   type ProviderRow = ProviderListItem;
   ```

   If you need `variables`, fetch the detail with the account's `id` as
   `path.public_id`. Don't cast a list entry to `ProviderItem` or add an empty
   `variables` object to stand in for the account's actual variables:

   ```ts
   async function loadVariables(
     client: management.ManagementClient,
     account: ProviderListItem,
   ): Promise<ProviderItem["variables"] | undefined> {
     const detail = await management.managementGetProvider({
       client,
       path: { public_id: account.id },
     });
     return detail.data?.data.variables;
   }
   ```

2. `mailbox.mailboxListThreadMessages` returns
   `MailboxThreadMessageSummaryCursorListResponse` instead of
   `MailboxMessageSummaryCursorListResponse`: its `meta.thread_id` is required
   and `meta.sync_state` is an optional string. Add the thread identity to every
   constructed thread-message result:

   ```ts
   import { mailbox } from "@qubrics/sdk";

   type ThreadMessageList = NonNullable<
     Awaited<ReturnType<typeof mailbox.mailboxListThreadMessages>>["data"]
   >;

   // Before: meta: { request_id: "req_fixture" }
   const fixture: ThreadMessageList = {
     ok: true,
     meta: { request_id: "req_fixture", thread_id: "thr_1" },
     data: [],
     pagination: { has_more: false },
   };
   ```

   Ordinary `mailbox.mailboxListMessages` results remain
   `MailboxMessageSummaryCursorListResponse`: they have no thread identity and
   expose an optional typed `meta.sync_state`. Identity, submission, quota, and
   thread list responses likewise expose optional typed state metadata
   (`identity_state`, `query_state`); no new field is required there.

3. Run your application's TypeScript check. List-only code should accept
   `ProviderListItem`, code that reads `variables` must receive a detail result,
   and a constructed thread-message result without `meta.thread_id` fails with
   `Property 'thread_id' is missing in type … but required in type
   'MailboxThreadMessagesMeta'`.

Update `@qubrics/sdk`, any directly installed `@qubrics/management` or
`@qubrics/mailbox`, the lockfile, and affected annotations, fixtures, or call
sites together. To roll back, restore those package, lockfile, and call-site
changes together. The per-surface notes are in the
[`@qubrics/management`](https://github.com/qubrics/qubrics-sdk/blob/main/packages/ts/management/README.md#migrate-from-1x-to-20)
and [`@qubrics/mailbox`](https://github.com/qubrics/qubrics-sdk/blob/main/packages/ts/mailbox/README.md#migrate-from-1x-to-20)
READMEs.

## OAuth access tokens

Each surface client also accepts `accessToken`: a bare token string or a synchronous or asynchronous provider. Pass either `apiKey` or `accessToken`. The provider runs for each authenticated request; your application owns token storage and refresh coordination.

```ts
import { management } from "@qubrics/sdk";

const client = management.createManagementClient({
  accessToken: () => process.env.QUBRICS_ACCESS_TOKEN!,
});
```

Use a REST access token with the operation's required scopes and mailbox access. See [OAuth for REST APIs](https://qubrics.com/docs/developer-tools/oauth).

## Usage

```ts
import { sending } from "@qubrics/sdk";

const client = sending.createSendingClient({
  apiKey: process.env.QUBRICS_SENDING_API_KEY!,
});

const response = await sending.sendingSendEmail({
  client,
  body: {
    from: { email: "sender@example.com" },
    to: { email: "recipient@example.com" },
    subject: "Hello from Qubrics",
    html_body: "<p>Hello.</p>",
    text_body: "Hello.",
  },
});

console.log(response.data?.data.message_id);
```

The umbrella package re-exports:

- `core` from `@qubrics/core`
- `sending` from `@qubrics/sending`
- `mailbox` from `@qubrics/mailbox`
- `management` from `@qubrics/management`

Use the per-surface packages directly when an integration only needs one API surface.

## Support

Open an issue in [qubrics/qubrics-sdk](https://github.com/qubrics/qubrics-sdk/issues) with the package name, version, and request ID from any API error.

## Licence

MIT. See the [licence file](https://github.com/qubrics/qubrics-sdk/blob/main/LICENSE).
