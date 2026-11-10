# qubrics-sending

[![Gem Version](https://badge.fury.io/rb/qubrics-sending.svg)](https://rubygems.org/gems/qubrics-sending)
[![CI](https://github.com/qubrics/qubrics-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/qubrics/qubrics-sdk/actions/workflows/ci.yml)
[![Licence: MIT](https://img.shields.io/badge/licence-MIT-blue.svg)](https://github.com/qubrics/qubrics-sdk/blob/main/LICENSE)

Ruby SDK package for the Qubrics Sending API.

## Documentation

- Ruby SDK guide: https://qubrics.com/docs/sdks/ruby
- Sending API reference: https://qubrics.com/docs/sending-api
- Source: https://github.com/qubrics/qubrics-sdk/tree/main/packages/ruby/sending
- Changelog: https://github.com/qubrics/qubrics-sdk/blob/main/packages/ruby/sending/CHANGELOG.md

## Requirements

- Ruby 3.1 or newer.
- A send-capable `smx_mbx_` key or owner-approved Sending-resource `smx_agent_` token.

For OAuth, use a REST access token with the scopes and mailbox access required by the operation. See [OAuth for REST APIs](https://qubrics.com/docs/developer-tools/oauth).

## Installation

These commands target the Qubrics release of `qubrics-sending`. Until it is published, install `sendmux-sending` with its existing require paths and `Sendmux` module.

```sh
gem install qubrics-sending
```

Or add it to your Gemfile:

```ruby
gem "qubrics-sending", "~> 2.0"
```

## OAuth access tokens

Pass either `api_key:` or `access_token:`. `access_token:` accepts a bare token string or a callable; the callable is evaluated once per authenticated request. Your application owns token storage, expiry checks and refresh coordination.

```ruby
require "qubrics/sending"

client = Qubrics::Sending::Client.new(
  access_token: -> { ENV.fetch("QUBRICS_ACCESS_TOKEN") }
)
```

## Usage

Create a sending client with a send-capable key for the API-key example below.

```ruby
require "qubrics/sending"

client = Qubrics::Sending::Client.new(
  api_key: ENV.fetch("QUBRICS_MAILBOX_KEY")
)

request = Qubrics::Sending::Generated::EmailSendRequest.new(
  from: Qubrics::Sending::Generated::Address.new(email: "sender@example.com"),
  to: Qubrics::Sending::Generated::Address.new(email: "recipient@example.com"),
  subject: "Hello from Qubrics",
  text_body: "This message was sent with the Qubrics Ruby SDK."
)

response = client.emails.sending_send_email(
  request,
  Qubrics::Core::Headers.idempotency_key("send-email-001")
)

puts response.data.message_id
```

### Client surface

`Qubrics::Sending::Client` exposes:

- `client.emails` for `sending_send_email` and `sending_send_email_batch`.
- `client.meta` for `sending_get_open_api_spec`.

Pass `base_url:` only when you are targeting an explicitly provided Qubrics endpoint for a controlled environment.

### Idempotency and retries

Mutating sending operations accept the `:idempotency_key` option. Use `Qubrics::Core::Headers.idempotency_key` so retries are safe when a request is replayable.

```ruby
client.emails.sending_send_email(
  request,
  Qubrics::Core::Headers.idempotency_key("send-email-002")
)
```

### Errors

Generated API errors are mapped to `Qubrics::Core::ApiError`.

```ruby
begin
  client.emails.sending_send_email(request)
rescue Qubrics::Core::ApiError => error
  warn "#{error.status} #{error.code}: #{error.message}"
end
```

## Support

- Documentation: https://qubrics.com/docs
- Contact: contact@qubrics.com

## Licence

MIT licence. See https://github.com/qubrics/qubrics-sdk/blob/main/LICENSE.
