# qubrics-sdk

[![PyPI version](https://img.shields.io/pypi/v/qubrics-sdk)](https://pypi.org/project/qubrics-sdk/)
[![Python versions](https://img.shields.io/pypi/pyversions/qubrics-sdk)](https://pypi.org/project/qubrics-sdk/)
[![PyPI downloads](https://img.shields.io/pypi/dm/qubrics-sdk)](https://pypi.org/project/qubrics-sdk/)
[![Licence](https://img.shields.io/pypi/l/qubrics-sdk)](https://github.com/qubrics/qubrics-sdk/blob/main/LICENSE)

Optional umbrella package for the Qubrics Python SDK.

## Documentation

- Qubrics docs: [qubrics.com/docs](https://qubrics.com/docs)
- Management API reference: [qubrics.com/docs/api/introduction](https://qubrics.com/docs/api/introduction)
- Mailbox API reference: [qubrics.com/docs/mailbox-api/introduction](https://qubrics.com/docs/mailbox-api/introduction)
- Sending API reference: [qubrics.com/docs/sending-api/introduction](https://qubrics.com/docs/sending-api/introduction)
- Source repository: [qubrics/qubrics-sdk](https://github.com/qubrics/qubrics-sdk)

## Requirements

- Python 3.10 or newer.
- A send-capable `smx_mbx_*` key or owner-approved Sending-resource `smx_agent_*` token for Sending clients.
- A mailbox-scoped `smx_mbx_*` key or scoped `smx_agent_*` token for Mailbox clients.
- A root `smx_root_*` key for Management clients.

For OAuth, use a REST access token with the scopes and mailbox access required by the operation. See [OAuth for REST APIs](https://qubrics.com/docs/developer-tools/oauth).

## Installation

These commands target the Qubrics release of `qubrics-sdk`. Until it is published, install `sendmux-sdk` with its existing import names.

```sh
pip install qubrics-sdk
```

## Connection checks

Check a Management credential without creating resources:

```python
import os

from qubrics.sdk import management

with management.create_management_client(
    api_key=os.environ["QUBRICS_MANAGEMENT_API_KEY"]
) as client:
    connection = management.ConnectionApi(client).management_get_connection()
    print(connection.data.label, connection.data.team.id)
```

Use `data.label` for the connection name and `data.team.id` for its stable team
identifier. Each API surface has its own connection operation:

| Surface | API class | Method |
| --- | --- | --- |
| Management | `management.ConnectionApi` | `management_get_connection()` |
| Mailbox | `mailbox.MailboxAPIApi` | `mailbox_get_connection()` |
| Sending | `sending.MetaApi` | `sending_get_connection()` |

Create each client with the credential for that surface.

## OAuth access tokens

Pass either `api_key` or `access_token`. `access_token` accepts a bare token string or a synchronous callable; the callable is evaluated for each authenticated request. Your application owns token storage, expiry checks and refresh coordination.

```python
import os

from qubrics.sdk import management

client = management.create_management_client(
    access_token=lambda: os.environ["QUBRICS_ACCESS_TOKEN"]
)
```

## Usage

```python
import os

from qubrics.sdk import sending

client = sending.create_sending_client(api_key=os.environ["QUBRICS_SENDING_API_KEY"])
api = sending.EmailsApi(client)

response = api.sending_send_email(
    sending.EmailSendRequest(
        var_from=sending.Address(email="sender@example.com"),
        to=sending.Address(email="recipient@example.com"),
        subject="Hello from Qubrics",
        html_body="<p>Hello.</p>",
        text_body="Hello.",
    ),
    idempotency_key="email_123",
)

print(response.data.message_id)
```

The umbrella package lazy-loads:

- `core` from `qubrics.core`
- `sending` from `qubrics.sending`
- `mailbox` from `qubrics.mailbox`
- `management` from `qubrics.management`

Use the per-surface packages directly when an integration only needs one API surface.

## Provider model migration

The `management` module's provider-list responses contain `ProviderListItem` objects instead of `ProviderItem` objects. Detail responses retain `ProviderItem` and require the `variables` map; list items omit that map.

To update provider-list callers:

1. Update your requirements to `qubrics-sdk` and regenerate your lockfile. If you pin components directly, update `qubrics-core`, `qubrics-mailbox`, `qubrics-management`, and `qubrics-sending` together.
2. Change provider-list annotations and type checks from `management.ProviderItem` to `management.ProviderListItem`. Keep `management.ProviderItem` for detail responses, and include `variables` in detail fixtures (`{}` when none are set).
3. Run `python -m pip check` and your provider-list, provider-detail, and sending tests. Confirm list items use `ProviderListItem`, detail fixtures retain their variables, and delivery-group requests serialize the selected group.

To roll back, restore the previous SDK and component requirements, lockfile, and affected call sites together.

## Thread message model migration

The umbrella's `mailbox` module adopts the thread-specific list response: thread-message results require `meta.thread_id` and expose optional typed `meta.sync_state`, while ordinary message-list results remain thread-independent. Other Mailbox list families expose typed state metadata where applicable.

Update `qubrics-sdk`, `qubrics-mailbox`, the lockfile, and affected annotations or fixtures together. To roll back, restore the previous package requirements, lockfile, and call sites together.

## Support

Open an issue in [qubrics/qubrics-sdk](https://github.com/qubrics/qubrics-sdk/issues) with the package name, version, and request ID from any API error.

## Licence

MIT. See the [licence file](https://github.com/qubrics/qubrics-sdk/blob/main/LICENSE).
