# @qubrics/sending

[![npm version](https://img.shields.io/npm/v/@qubrics%2Fsending)](https://www.npmjs.com/package/@qubrics/sending)
[![CI](https://github.com/qubrics/qubrics-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/qubrics/qubrics-sdk/actions/workflows/ci.yml)
[![npm downloads](https://img.shields.io/npm/dm/@qubrics%2Fsending)](https://www.npmjs.com/package/@qubrics/sending)
[![Licence](https://img.shields.io/npm/l/@qubrics%2Fsending)](https://github.com/qubrics/qubrics-sdk/blob/main/LICENSE)

Generated TypeScript client for the Qubrics Sending API.

## Documentation

- Sending API reference: [qubrics.com/docs/sending-api/introduction](https://qubrics.com/docs/sending-api/introduction)
- Source repository: [qubrics/qubrics-sdk](https://github.com/qubrics/qubrics-sdk)

## Requirements

- A send-capable `smx_mbx_*` key or owner-approved Sending-resource `smx_agent_*` token; alternatively, a REST OAuth grant for this surface.
- A JavaScript runtime with the standard Fetch API.

## Installation

```sh
npm install @qubrics/sending
```

## OAuth access tokens

Pass `accessToken` instead of `apiKey` for a REST OAuth token or synchronous/asynchronous provider.

```ts
import { createSendingClient } from "@qubrics/sending";

const client = createSendingClient({
  accessToken: () => process.env.QUBRICS_ACCESS_TOKEN!,
});
```

The provider runs before each request. Your application owns token storage and refresh; required scopes still apply. See [OAuth setup](https://qubrics.com/docs/developer-tools/oauth).

## Usage

```ts
import {
  createSendingClient,
  sendingSendEmail,
} from "@qubrics/sending";

const client = createSendingClient({
  apiKey: process.env.QUBRICS_SENDING_API_KEY!,
});

const response = await sendingSendEmail({
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

The package exports every generated Sending operation plus:

- `createSendingClient`
- `configureSending`
- `SendingClient`
- Node-only helpers from `@qubrics/sending/node`: `uploadAttachmentFromFile`, `sendEmailWithFiles`, and explicit legacy `attachmentFromFile`

## Attachments

For real files, upload bytes first and send with returned `attachment_id` refs. `sendEmailWithFiles` does that automatically, so file bytes never enter model context or the JSON send body. Inline base64 remains available only when you intentionally call `attachmentFromFile` for tiny generated content.

```ts
import { createSendingClient } from "@qubrics/sending";
import { sendEmailWithFiles } from "@qubrics/sending/node";

const client = createSendingClient({ apiKey: process.env.QUBRICS_SENDING_API_KEY! });

await sendEmailWithFiles({
  client,
  files: ["./report.pdf"],
  headers: { "Idempotency-Key": "report-123" },
  body: {
    from: { email: "sender@example.com" },
    to: { email: "recipient@example.com" },
    subject: "Report",
    html_body: "<p>Attached.</p>",
  },
});
```

To upload first and compose the send yourself:

```ts
import { createSendingClient, sendingSendEmail } from "@qubrics/sending";
import { uploadAttachmentFromFile } from "@qubrics/sending/node";

const client = createSendingClient({ apiKey: process.env.QUBRICS_SENDING_API_KEY! });
const attachment = await uploadAttachmentFromFile({ client, filePath: "./report.pdf" });

await sendingSendEmail({
  client,
  body: {
    from: { email: "sender@example.com" },
    to: { email: "recipient@example.com" },
    subject: "Report",
    html_body: "<p>Attached.</p>",
    attachments: [{ attachment_id: attachment.data.attachment_id }],
  },
});
```

## Request helpers

Use `@qubrics/core` when you need idempotency, conditional request, pagination, retry, or typed-error helpers.

```ts
import { idempotencyHeaders } from "@qubrics/core";
import { createSendingClient, sendingSendEmail } from "@qubrics/sending";

const client = createSendingClient({
  apiKey: process.env.QUBRICS_SENDING_API_KEY!,
});

await sendingSendEmail({
  client,
  body: {
    from: { email: "sender@example.com" },
    to: { email: "recipient@example.com" },
    subject: "Receipt",
    html_body: "<p>Thanks.</p>",
    text_body: "Thanks.",
  },
  headers: idempotencyHeaders("email_123"),
});
```

## Support

Open an issue in [qubrics/qubrics-sdk](https://github.com/qubrics/qubrics-sdk/issues) with the package name, version, and request ID from any API error.

## Licence

MIT. See the [licence file](https://github.com/qubrics/qubrics-sdk/blob/main/LICENSE).
