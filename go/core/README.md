# Qubrics Go core helpers

[![Go Reference](https://pkg.go.dev/badge/qubrics.com/go/v4/core.svg)](https://pkg.go.dev/qubrics.com/go/v4/core)

Shared runtime helpers used by the Qubrics Go surface packages.

## Install

These commands target unpublished v4 source. Use published `sendmux.ai/go/v3@v3.0.0`.

```sh
go get qubrics.com/go/v4@v4.0.0
```

## Import

```go
import "qubrics.com/go/v4/core"
```

## What it provides

- API-key prefix validation with `ValidateAPIKey` and `KeySurface`.
- Bare access-token validation with `ValidateAccessToken`.
- Shared `APIError`, `ErrorIssue`, `SuccessEnvelope`, and `Pagination` types.
- Retry-aware HTTP clients through `NewHTTPClient`, `NewRetryingTransport`, and `RetryOptions`.
- Cursor iteration through `IterateCursor` for code that adapts a response type to the `core.Page` interface.

## Example

```go
package main

import (
	"net/http"
	"os"
	"time"

	"qubrics.com/go/v4/core"
)

func newHTTPClient() *http.Client {
	if err := core.ValidateAPIKey(os.Getenv("QUBRICS_API_KEY"), core.KeySurfaceRoot); err != nil {
		panic(err)
	}

	return core.NewHTTPClient(nil, core.RetryOptions{
		MaxAttempts: 4,
		BaseDelay:   250 * time.Millisecond,
		MaxDelay:    5 * time.Second,
	})
}
```

Use `KeySurfaceSending` for send-capable `smx_mbx_` keys or owner-approved Sending-resource `smx_agent_` tokens, `KeySurfaceMailbox` for `smx_mbx_` keys or scoped `smx_agent_` tokens, and `KeySurfaceRoot` for `smx_root_` keys.

Most applications should import `qubrics.com/go/v4/sending`, `qubrics.com/go/v4/mailbox`, or `qubrics.com/go/v4/management` directly. Those packages apply the core helpers for you.

## Documentation

- Guides: <https://qubrics.com/docs>
- Go reference: <https://pkg.go.dev/qubrics.com/go/v4/core>
