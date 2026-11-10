# qubrics-core

[![Gem Version](https://badge.fury.io/rb/qubrics-core.svg)](https://rubygems.org/gems/qubrics-core)
[![CI](https://github.com/qubrics/qubrics-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/qubrics/qubrics-sdk/actions/workflows/ci.yml)
[![Licence: MIT](https://img.shields.io/badge/licence-MIT-blue.svg)](https://github.com/qubrics/qubrics-sdk/blob/main/LICENSE)

Shared authentication, retry, pagination, header, and error helpers for the Qubrics Ruby SDK packages.

## Documentation

- Ruby SDK guide: https://qubrics.com/docs/sdks/ruby
- Source: https://github.com/qubrics/qubrics-sdk/tree/main/packages/ruby/core
- Changelog: https://github.com/qubrics/qubrics-sdk/blob/main/packages/ruby/core/CHANGELOG.md

## Requirements

- Ruby 3.1 or newer.
- A Qubrics API key or REST OAuth access token when using a surface client.

## Installation

These commands target the Qubrics release of `qubrics-core`. Until it is published, install `sendmux-core` with its existing require paths and `Sendmux` module.

```sh
gem install qubrics-core
```

Or add it to your Gemfile:

```ruby
gem "qubrics-core", "~> 2.0"
```

## Usage

The core package is installed automatically by the surface gems, but it can also be used directly when you need shared helpers.

```ruby
require "qubrics/core"

surface = Qubrics::Core::Auth.assert_api_key_surface(
  ENV.fetch("QUBRICS_ROOT_KEY"),
  Qubrics::Core::ApiKeySurface::ROOT
)

puts surface
```

Use `Qubrics::Core::ApiKeySurface::ROOT` for root-key management clients, `Qubrics::Core::ApiKeySurface::SENDING` for send-capable `smx_mbx_` keys or owner-approved Sending-resource `smx_agent_` tokens, and `Qubrics::Core::ApiKeySurface::MAILBOX` for mailbox-compatible credentials. Mailbox-compatible credentials can start with `smx_mbx_` or `smx_agent_`.

Surface clients accept `access_token:` as a bare token or callable instead of `api_key:`. Token providers run before each request; the application owns token storage and refresh.

### Header helpers

Generated Ruby operations accept option hashes. The header helpers return the option keys expected by those generated operations.

```ruby
headers = Qubrics::Core::Headers.idempotency_key("idem_123")
etag = Qubrics::Core::Headers.if_match('W/"etag"')
conditional = Qubrics::Core::Headers.conditional(if_none_match: 'W/"cached"')
```

### Cursor pagination

`Qubrics::Core.each_cursor` wraps any generated list call that accepts a cursor option and returns Qubrics pagination metadata.

```ruby
pager = Qubrics::Core.each_cursor(lambda do |opts|
  mailbox_client.mailbox_api.mailbox_list_messages(opts.merge(limit: 50))
end)

pager.each do |message|
  puts message.id
end
```

### Retries and errors

Surface clients accept `Qubrics::Core::RetryOptions` and map generated errors to `Qubrics::Core::ApiError`.

```ruby
retry_options = Qubrics::Core::RetryOptions.new(max_attempts: 4)

begin
  # Pass retry_options: retry_options to any Qubrics surface client.
  # Call a generated operation here.
  nil
rescue Qubrics::Core::ApiError => error
  warn "#{error.code}: #{error.message} (request #{error.request_id})"
end
```

Retries are enabled for safe requests and for idempotent `POST` requests that use an `Idempotency-Key`.

## Support

- Documentation: https://qubrics.com/docs
- Contact: contact@qubrics.com

## Licence

MIT licence. See https://github.com/qubrics/qubrics-sdk/blob/main/LICENSE.
