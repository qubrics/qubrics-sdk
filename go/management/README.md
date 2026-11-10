# Qubrics Go management client

[![Go Reference](https://pkg.go.dev/badge/qubrics.com/go/v4/management.svg)](https://pkg.go.dev/qubrics.com/go/v4/management)

Go client for managing domains, mailboxes, sending accounts, billing, logs, and webhooks.

## Install

These commands target unpublished v4 source. Use published `sendmux.ai/go/v3@v3.0.0`.

```sh
go get qubrics.com/go/v4@v4.0.0
```

## Import

```go
import "qubrics.com/go/v4/management"
```

## Authentication

Use a root API key with the `smx_root_` prefix. `management.New` validates the prefix before creating the client.

### OAuth access tokens

Use `management.NewWithAccessToken` for a bare token string, or `management.NewWithTokenProvider` for a function with signature `func(context.Context) (string, error)`. The provider runs for each authenticated request and receives that request's context. Your application owns token storage, expiry checks and refresh coordination.

```go
client, err := management.NewWithTokenProvider(func(ctx context.Context) (string, error) {
    return os.Getenv("QUBRICS_ACCESS_TOKEN"), nil
})
```

Use a REST access token with the operation's required scopes and mailbox access. See [OAuth for REST APIs](https://qubrics.com/docs/developer-tools/oauth).

## Quickstart

```go
package main

import (
	"context"
	"fmt"
	"os"

	"qubrics.com/go/v4/management"
)

func main() {
	ctx := context.Background()

	client, err := management.New(os.Getenv("QUBRICS_API_KEY"))
	if err != nil {
		panic(err)
	}

	res, err := client.ManagementListDomains(ctx, management.ManagementListDomainsParams{
		Limit: management.NewOptInt(25),
	})
	if err != nil {
		panic(err)
	}

	page, ok := res.(*management.DomainItemCursorListResponse)
	if !ok {
		panic(fmt.Sprintf("list domains failed: %T", res))
	}

	for _, domain := range page.GetData() {
		fmt.Println(domain.GetID(), domain.GetDomain())
	}
}
```

## Client options

- `WithBaseURL` overrides the API base URL.
- `WithHTTPClient` supplies the base HTTP client.
- `WithRetryOptions` configures retry and rate-limit backoff behaviour.
- `IdempotencyKey` sets the `Idempotency-Key` header for create and action requests.
- `IfMatch` and `IfNoneMatch` set conditional request headers where supported.
- `APIErrorFromResponse` maps generated error responses into `core.APIError`.

## Documentation

- Management API: <https://qubrics.com/docs/api/introduction>
- Domain guide: <https://qubrics.com/docs/guides/domain-management>
- Go reference: <https://pkg.go.dev/qubrics.com/go/v4/management>
