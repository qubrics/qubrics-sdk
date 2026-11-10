# Qubrics Go SDK anchor

[![Go Reference](https://pkg.go.dev/badge/qubrics.com/go/v4/sdk.svg)](https://pkg.go.dev/qubrics.com/go/v4/sdk)

Package `sdk` anchors the Qubrics Go module. It does not re-export the surface clients.

## Install

These commands target unpublished v4 source. Use published `sendmux.ai/go/v3@v3.0.0`.

```sh
go get qubrics.com/go/v4@v4.0.0
```

## Use the surface packages

Most applications should import the package for the API surface they need:

```go
import (
	"qubrics.com/go/v4/mailbox"
	"qubrics.com/go/v4/management"
	"qubrics.com/go/v4/sending"
)
```

| Surface | Import path | API key |
| --- | --- | --- |
| Sending | `qubrics.com/go/v4/sending` | `smx_mbx_*` or owner-approved `smx_agent_*` |
| Mailbox | `qubrics.com/go/v4/mailbox` | `smx_mbx_*` or `smx_agent_*` |
| Management | `qubrics.com/go/v4/management` | `smx_root_*` |
| Core helpers | `qubrics.com/go/v4/core` | n/a |

All three surface packages also provide `NewWithAccessToken` and `NewWithTokenProvider` for [REST OAuth](https://qubrics.com/docs/developer-tools/oauth).

## Documentation

- Guides: <https://qubrics.com/docs>
- Go reference: <https://pkg.go.dev/qubrics.com/go/v4/sdk>

For existing installations, see the [version 4 migration](../README.md#version-4-migration).
