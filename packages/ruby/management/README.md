# qubrics-management

[![Gem Version](https://badge.fury.io/rb/qubrics-management.svg)](https://rubygems.org/gems/qubrics-management)
[![CI](https://github.com/qubrics/qubrics-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/qubrics/qubrics-sdk/actions/workflows/ci.yml)
[![Licence: MIT](https://img.shields.io/badge/licence-MIT-blue.svg)](https://github.com/qubrics/qubrics-sdk/blob/main/LICENSE)

Ruby SDK package for the Qubrics Management API.

## Documentation

- Ruby SDK guide: https://qubrics.com/docs/sdks/ruby
- Management API reference: https://qubrics.com/docs/api
- Source: https://github.com/qubrics/qubrics-sdk/tree/main/packages/ruby/management
- Changelog: https://github.com/qubrics/qubrics-sdk/blob/main/packages/ruby/management/CHANGELOG.md

## Requirements

- Ruby 3.1 or newer.
- A root Qubrics API key beginning with `smx_root_`.

For OAuth, use a REST access token with the scopes and mailbox access required by the operation. See [OAuth for REST APIs](https://qubrics.com/docs/developer-tools/oauth).

## Installation

These commands target the Qubrics release of `qubrics-management`. Until it is published, install `sendmux-management` with its existing require paths and `Sendmux` module.

```sh
gem install qubrics-management
```

Or add it to your Gemfile:

```ruby
gem "qubrics-management", "~> 3.0"
```

## Provider model migration

If you check sending-account result classes, update those checks to use the current
models. `management_list_providers` returns `ProviderListItem` entries instead of
`ProviderItem`. List entries don't expose `variables`; detail results remain
`ProviderItem` and require a variables hash, which is empty when none are set.

1. Update list-specific class checks to use the class loaded by the public entry
   point:

   ```ruby
   require "qubrics/management"

   def provider_list_item?(item)
     # Before: item.is_a?(Qubrics::Management::Generated::ProviderItem)
     item.is_a?(Qubrics::Management::Generated::ProviderListItem)
   end
   ```

2. If you need an account's variables, fetch its detail using the public client.
   Pass the account's `id` as the `public_id` argument:

   ```ruby
   def provider_variables(client, public_id)
     detail = client.sending_accounts.management_get_provider(public_id).data
     detail.variables
   end
   ```

   Don't convert a list entry into `ProviderItem` or substitute an empty variables
   hash for the account's actual variables. Update hand-built detail fixtures to
   include `variables: {}` when no variables are set.

3. Run your application's tests with the updated bundle. Verify that list
   handling accepts `ProviderListItem` and only detail handling reads variables.

## OAuth access tokens

Pass either `api_key:` or `access_token:`. `access_token:` accepts a bare token string or a callable; the callable is evaluated once per authenticated request. Your application owns token storage, expiry checks and refresh coordination.

```ruby
require "qubrics/management"

client = Qubrics::Management::Client.new(
  access_token: -> { ENV.fetch("QUBRICS_ACCESS_TOKEN") }
)
```

## Usage

Create a management client with a root key for the API-key example below.

```ruby
require "qubrics/management"

client = Qubrics::Management::Client.new(
  api_key: ENV.fetch("QUBRICS_ROOT_KEY")
)

mailboxes = client.mailboxes.management_list_mailboxes(limit: 25)
domains = client.domains.management_list_domains(limit: 25)

puts mailboxes.data.length
puts domains.data.length
```

### Client surface

`Qubrics::Management::Client` exposes generated API groups:

- `client.billing`
- `client.connection`
- `client.domain_filters`
- `client.domains`
- `client.emails`
- `client.inboxes`
- `client.mailbox_filters`
- `client.mailboxes`
- `client.sending_accounts`
- `client.webhooks`

Each group exposes generated operation methods using the `management_` prefix, such as `management_list_mailboxes`, `management_create_mailbox`, `management_list_domains`, and `management_create_webhook`.

### Idempotency and conditional requests

Mutating generated operations accept option hashes. Use the core header helpers for idempotency and ETag preconditions.

```ruby
client.webhooks.management_create_webhook(
  Qubrics::Core::Headers.idempotency_key("create-webhook-001").merge(
    webhook_create_body: Qubrics::Management::Generated::WebhookCreateBody.new(
      url: "https://example.com/webhook",
      event_types: ["sendmux.test"]
    )
  )
)

client.domains.management_update_domain(
  "mdom_123",
  Qubrics::Core::Headers.if_match('W/"etag"')
)
```

### Pagination and errors

Use `Qubrics::Core.each_cursor` for list operations that return cursor pagination. Generated API errors are mapped to `Qubrics::Core::ApiError`.

```ruby
pager = Qubrics::Core.each_cursor(lambda do |opts|
  client.mailboxes.management_list_mailboxes(opts.merge(limit: 50))
end)

pager.each { |mailbox| puts mailbox.id }
```

## Support

- Documentation: https://qubrics.com/docs
- Contact: contact@qubrics.com

## Licence

MIT licence. See https://github.com/qubrics/qubrics-sdk/blob/main/LICENSE.
