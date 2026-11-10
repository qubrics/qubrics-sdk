# qubrics-management

[![PyPI version](https://img.shields.io/pypi/v/qubrics-management)](https://pypi.org/project/qubrics-management/)
[![Python versions](https://img.shields.io/pypi/pyversions/qubrics-management)](https://pypi.org/project/qubrics-management/)
[![PyPI downloads](https://img.shields.io/pypi/dm/qubrics-management)](https://pypi.org/project/qubrics-management/)
[![Licence](https://img.shields.io/pypi/l/qubrics-management)](https://github.com/qubrics/qubrics-sdk/blob/main/LICENSE)

Generated Python client for the Qubrics Management API.

## Documentation

- Management API reference: [qubrics.com/docs/api/introduction](https://qubrics.com/docs/api/introduction)
- Source repository: [qubrics/qubrics-sdk](https://github.com/qubrics/qubrics-sdk)

## Requirements

- Python 3.10 or newer.
- A root Qubrics API key with the `smx_root_*` prefix.

For OAuth, use a REST access token with the scopes and mailbox access required by the operation. See [OAuth for REST APIs](https://qubrics.com/docs/developer-tools/oauth).

## Installation

These commands target the Qubrics release of `qubrics-management`. Until it is published, install `sendmux-management` with its existing import names.

```sh
pip install qubrics-management
```

## OAuth access tokens

Pass either `api_key` or `access_token`. `access_token` accepts a bare token string or a synchronous callable; the callable is evaluated for each authenticated request. Your application owns token storage, expiry checks and refresh coordination.

```python
import os

from qubrics.management import create_management_client

client = create_management_client(
    access_token=lambda: os.environ["QUBRICS_ACCESS_TOKEN"]
)
```

## Usage

```python
import os

from qubrics.management import DomainsApi, create_management_client

client = create_management_client(api_key=os.environ["QUBRICS_MANAGEMENT_API_KEY"])
api = DomainsApi(client)

domains = api.management_list_domains(limit=25)

for domain in domains.data:
    print(domain.id, domain.domain)
```

The package exports every generated Management model and API class plus:

- `create_management_client`
- `configure_management`
- `QubricsManagementApiClient`

## Conditional requests

Generated methods expose ETag parameters directly when the API operation supports them.

```python
import os

from qubrics.management import DomainsApi, create_management_client

client = create_management_client(api_key=os.environ["QUBRICS_MANAGEMENT_API_KEY"])
api = DomainsApi(client)

domain = api.management_get_domain(
    public_id="mdom_123",
    if_none_match='W/"etag"',
)

print(domain.data)
```

## Support

Open an issue in [qubrics/qubrics-sdk](https://github.com/qubrics/qubrics-sdk/issues) with the package name, version, and request ID from any API error.

## Licence

MIT. See the [licence file](https://github.com/qubrics/qubrics-sdk/blob/main/LICENSE).
