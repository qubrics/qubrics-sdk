# Qubrics Rust SDK

Official async Rust SDK for the Qubrics Sending, Mailbox, and Management APIs.

Use the `qubrics` clients for email sending, mailbox automation and account
management. Sending includes typed request and response models. For Mailbox
and Management, typed surface clients expose raw JSON helpers. Not every
OpenAPI operation has a named Rust method:

- `qubrics::sending` for Sending API requests with send-capable `smx_mbx_*` keys or owner-approved Sending-resource `smx_agent_*` tokens.
- `qubrics::mailbox` for Mailbox API requests with `smx_mbx_*` keys or scoped `smx_agent_*` tokens.
- `qubrics::management` for Management API requests with `smx_root_*` keys.

Version 1.0.0 excludes calendar-specific client bindings. Generic raw JSON helpers remain available.

## Install

```sh
cargo add qubrics@1
```

## Quick Start

```rust,no_run
use qubrics::sending::{Address, EmailSendRequest, SendingClient};

#[tokio::main]
async fn main() -> qubrics::Result<()> {
    let client = SendingClient::new(std::env::var("QUBRICS_MAILBOX_API_KEY").unwrap())?;

    let response = client
        .send_email(&EmailSendRequest::new(
            Address::new("sender@example.com").with_name("Example App"),
            Address::new("user@example.com"),
            "Welcome to Qubrics",
            "<p>Hello from Rust.</p>",
        ))
        .await?;

    println!("queued {} via {}", response.data.message_id, response.request_id());
    Ok(())
}
```

## Connection Checks

Each surface exposes `get_connection()` to validate its current credential and retrieve the team, label, permissions and authorised mailboxes. It does not require a mailbox selector or send an email. Sending credentials must include `email.send`.

```rust,no_run
#[tokio::main]
async fn main() -> qubrics::Result<()> {
    let client = qubrics::management(std::env::var("QUBRICS_API_KEY").unwrap())?;
    let connection = client.get_connection().await?;
    println!("{}", connection.data.label);
    Ok(())
}
```

## Sending API

Use a send-capable `smx_mbx_` key or owner-approved Sending-resource `smx_agent_` token.

```rust,no_run
use qubrics::core::RequestOptions;
use qubrics::sending::{Address, BatchSendRequest, EmailSendRequest, SendingClient};

#[tokio::main]
async fn main() -> qubrics::Result<()> {
    let client = SendingClient::new(std::env::var("QUBRICS_MAILBOX_API_KEY").unwrap())?;

    let message = EmailSendRequest::new(
        Address::new("sender@example.com"),
        Address::new("user@example.com"),
        "Receipt",
        "<p>Your receipt is ready.</p>",
    )
    .text_body("Your receipt is ready.");

    let response = client
        .send_email_with_options(
            &message,
            &RequestOptions::new().idempotency_key("receipt-123"),
        )
        .await?;

    println!("{:?}", response.data.status);

    let batch = BatchSendRequest::new(vec![message]);
    let batch_response = client.send_email_batch(&batch).await?;
    println!("queued {}", batch_response.data.summary.queued);

    Ok(())
}
```

## Mailbox API

Use a mailbox-scoped `smx_mbx_` key or scoped `smx_agent_` token.

```rust,no_run
#[tokio::main]
async fn main() -> qubrics::Result<()> {
    let client = qubrics::mailbox(std::env::var("QUBRICS_MAILBOX_API_KEY").unwrap())?;

    let me = client.get_me().await?;
    println!("mailbox request id: {}", me.request_id());

    let messages = client.list_messages().await?;
    println!("{}", messages.data);

    Ok(())
}
```

## Management API

Use a root API key beginning with `smx_root_`.

```rust,no_run
#[tokio::main]
async fn main() -> qubrics::Result<()> {
    let client = qubrics::management(std::env::var("QUBRICS_ROOT_API_KEY").unwrap())?;

    let domains = client.list_domains().await?;
    println!("domains response: {}", domains.data);

    let balance = client.billing_balance().await?;
    println!("billing response: {}", balance.data);

    Ok(())
}
```

## OAuth Access Tokens

Each surface client provides `new_with_access_token` for a bare token string and `new_with_token_provider` for an asynchronous provider. The provider runs for each request, including requests from cloned clients. Your application owns token storage, expiry checks and refresh coordination.

```rust,no_run
#[tokio::main]
async fn main() -> qubrics::Result<()> {
    let client = qubrics::management::ManagementClient::new_with_token_provider(|| async {
        Ok(std::env::var("QUBRICS_ACCESS_TOKEN").expect("access token is configured"))
    })?;
    let connection = client.get_connection().await?;
    println!("{}", connection.data.label);
    Ok(())
}
```

Use a REST access token with the operation's required scopes and mailbox access. The API-key constructors retain their prefix checks. See [OAuth for REST APIs](https://qubrics.com/docs/developer-tools/oauth).

## API Keys

Do not hard-code API keys or commit them to source control.

- Sending clients accept send-capable keys with the `smx_mbx_` prefix or owner-approved Sending-resource `smx_agent_` tokens.
- Mailbox clients accept `smx_mbx_` keys or scoped `smx_agent_` tokens.
- Management clients require root keys with the `smx_root_` prefix.
- Store keys in your secret manager and pass them through environment variables
  or your runtime secret injection mechanism.

An empty constructor credential reads `QUBRICS_API_KEY` or
`QUBRICS_ACCESS_TOKEN`, then the matching `SENDMUX_*` variable.
`QUBRICS_BASE_URL` takes precedence over `SENDMUX_BASE_URL`.

## Errors and Request IDs

SDK methods return `qubrics::Result<Response<T>>`. API failures are mapped to
`qubrics::Error::Api`, including status code, machine-readable code, retryable
flag, raw response body, and the Qubrics request ID when available.

```rust,no_run
#[tokio::main]
async fn main() -> qubrics::Result<()> {
    if let Err(qubrics::Error::Api(error)) =
        qubrics::sending("smx_mbx_example")?.openapi().await
    {
        eprintln!("{} {:?}", error.message, error.request_id);
    }

    Ok(())
}
```

## OpenAPI Source

The source checkout's `rust/operation-decisions.json` and
`docs/surface-coverage.md` account for all 128 snapshot operations and 20 named
operation IDs. Conditional GET/304/ETag handling, optional list filters and
selectors, automatic retries, and missing named operations aren't implied by
raw JSON access. `ApiError.retryable` reports the server/fallback classification;
the Rust transport doesn't retry or wait on `Retry-After` automatically.

### 0.5.0 Rust contract changes

`0.5.0` is an incompatible upgrade from `0.4.x`:

- Raw Mailbox and Management paths must be relative to the configured API base.
  Absolute URLs, authority paths, and backslash paths return
  `Error::InvalidRequestPath` before credentials are resolved or HTTP starts.
- `Response<T>` adds `pagination: Option<CursorPagination>`. The six list methods
  have additive `*_with_cursor(Option<&str>)` variants. Pass the previous
  response's `pagination.next_cursor.as_deref()` to advance; stop when
  `has_more` is false. The original no-argument list methods still request the
  first page.
- `Attachment` changes from a struct to `Inline(InlineAttachment)` or
  `Uploaded(UploadedAttachmentRef)`. Use `Attachment::base64(filename, content)`
  for inline bytes or `Attachment::uploaded(attachment_id)` for an existing
  Sending reference. `with_content_type` applies only to inline attachments;
  it leaves uploaded references unchanged. Both forms work in single and batch
  send requests. This doesn't add an attachment upload method.

Code that constructs `Response` or `Attachment` with struct literals, or accesses
old attachment fields directly, must migrate before adopting `0.5.0`.
Replace attachment literals with the constructors or match the enum variants;
include `pagination: None` when constructing response fixtures without cursor
metadata. Rebuild and run your application's tests before deploying the upgrade.
To roll back, restore your previous `Cargo.toml`, `Cargo.lock`, and corresponding
call-site changes together.

This crate is aligned to the committed Qubrics OpenAPI snapshots in the
`qubrics-sdk` repository:

- Sending: `packages/python/mcp/qubrics/mcp/openapi/openapi-sending.json`
- Mailbox and Management: `packages/python/mcp/qubrics/mcp/openapi/openapi-app.json`

Generated/provenance metadata lives under `qubrics::generated`; hand-written
client helpers live under `qubrics::core`, `qubrics::sending`,
`qubrics::mailbox`, and `qubrics::management`.

## Links

- Product docs: <https://qubrics.com/docs>
- Sending API: <https://qubrics.com/docs/sending-api/introduction>
- Mailbox API: <https://qubrics.com/docs/mailbox-api/introduction>
- Management API: <https://qubrics.com/docs/api/introduction>
- GitHub: <https://github.com/qubrics/qubrics-sdk>
- Support: <https://github.com/qubrics/qubrics-sdk/issues>

## Publishing Safety

Publishing to crates.io is permanent for a version: published versions cannot be
overwritten, and code cannot be deleted. Run `cargo publish --dry-run` and
inspect `target/package` before any real publish.
