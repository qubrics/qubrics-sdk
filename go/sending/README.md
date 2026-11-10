# Qubrics Go sending client

[![Go Reference](https://pkg.go.dev/badge/qubrics.com/go/v4/sending.svg)](https://pkg.go.dev/qubrics.com/go/v4/sending)

Go client for Qubrics email sending.

## Install

These commands target unpublished v4 source. Use published `sendmux.ai/go/v3@v3.0.0`.

```sh
go get qubrics.com/go/v4@v4.0.0
```

## Import

```go
import "qubrics.com/go/v4/sending"
```

## Authentication

Use a send-capable `smx_mbx_` key or owner-approved Sending-resource `smx_agent_` token. `sending.New` validates the prefix before creating the client.

### OAuth access tokens

Use `sending.NewWithAccessToken` for a bare token string, or `sending.NewWithTokenProvider` for a function with signature `func(context.Context) (string, error)`. The provider runs for each authenticated request and receives that request's context. Your application owns token storage, expiry checks and refresh coordination.

```go
client, err := sending.NewWithTokenProvider(func(ctx context.Context) (string, error) {
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

	"qubrics.com/go/v4/sending"
)

func main() {
	ctx := context.Background()

	client, err := sending.New(os.Getenv("QUBRICS_SENDING_API_KEY"))
	if err != nil {
		panic(err)
	}

	res, err := client.SendingSendEmail(ctx, &sending.EmailSendRequest{
		From: sending.Address{
			Email: "sender@example.com",
			Name:  sending.NewOptString("Sender"),
		},
		To: sending.EmailSendRequestTo{
			Email: "recipient@example.com",
		},
		Subject:  "Hello from Qubrics",
		HTMLBody: "<p>Hello.</p>",
		TextBody: sending.NewOptString("Hello."),
	}, sending.SendingSendEmailParams{
		IdempotencyKey: sending.IdempotencyKey("email_123"),
	})
	if err != nil {
		panic(err)
	}

	success, ok := res.(*sending.SendSuccessResponse)
	if !ok {
		panic(fmt.Sprintf("send failed: %T", res))
	}

	data := success.GetData()
	fmt.Println(data.GetMessageID())
}
```

## Client options

- `WithBaseURL` overrides the API base URL.
- `WithHTTPClient` supplies the base HTTP client.
- `WithRetryOptions` configures retry and rate-limit backoff behaviour.
- `IdempotencyKey` sets the `Idempotency-Key` header for send requests.
- `APIErrorFromResponse` maps generated error responses into `core.APIError`.

## Documentation

- Sending guide: <https://qubrics.com/docs/guides/sending-via-http>
- Sending API: <https://qubrics.com/docs/sending-api/introduction>
- Go reference: <https://pkg.go.dev/qubrics.com/go/v4/sending>
