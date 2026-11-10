# qubrics-sdk

[![Gem Version](https://badge.fury.io/rb/qubrics-sdk.svg)](https://rubygems.org/gems/qubrics-sdk)
[![CI](https://github.com/qubrics/qubrics-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/qubrics/qubrics-sdk/actions/workflows/ci.yml)
[![Licence: MIT](https://img.shields.io/badge/licence-MIT-blue.svg)](https://github.com/qubrics/qubrics-sdk/blob/main/LICENSE)

Umbrella Ruby SDK package for Qubrics.

## Documentation

- Ruby SDK guide: https://qubrics.com/docs/sdks/ruby
- Source: https://github.com/qubrics/qubrics-sdk/tree/main/packages/ruby/sdk
- Changelog: https://github.com/qubrics/qubrics-sdk/blob/main/packages/ruby/sdk/CHANGELOG.md

## Requirements

- Ruby 3.1 or newer.
- A send-capable `smx_mbx_` key or owner-approved Sending-resource `smx_agent_` token for sending clients.
- A mailbox-scoped key beginning with `smx_mbx_` or scoped token beginning with `smx_agent_` for mailbox clients.
- A root key beginning with `smx_root_` for management clients.

For OAuth, use a REST access token with the scopes and mailbox access required by the operation. See [OAuth for REST APIs](https://qubrics.com/docs/developer-tools/oauth).

## Installation

These commands target the Qubrics release of `qubrics-sdk`. Until it is published, install `sendmux-sdk` with its existing require paths and `Sendmux` module.

```sh
gem install qubrics-sdk
```

Or add it to your Gemfile:

```ruby
gem "qubrics-sdk", "~> 3.0"
```

## Result model migration

The `qubrics-management` and `qubrics-mailbox` clients use the result classes
shown below. The umbrella helpers return the same clients, so results from
`Qubrics::SDK.management(...)` and `Qubrics::SDK.mailbox(...)` follow
[the Management migration steps](../management/README.md#provider-model-migration)
and [the Mailbox migration steps](../mailbox/README.md#thread-message-model-migration).
If you check sending-account or thread-message result classes, read `variables`
from sending-account list entries, or build thread-message fixtures by hand,
update that code to use the models below. Code that only reads other result
fields keeps working.

1. `management_list_providers` returns `ProviderListItem` entries instead of
   `ProviderItem`. List entries don't expose `variables`; detail results remain
   `ProviderItem` and require a variables hash, which is empty when none are
   set. Update list-specific class checks to use the class loaded by the
   umbrella entry point, and fetch the detail when you need an account's
   variables:

   ```ruby
   require "qubrics/sdk"

   def provider_list_item?(item)
     # Before: item.is_a?(Qubrics::Management::Generated::ProviderItem)
     item.is_a?(Qubrics::Management::Generated::ProviderListItem)
   end

   def provider_variables(management, public_id)
     detail = management.sending_accounts.management_get_provider(public_id).data
     detail.variables
   end
   ```

   Pass the client returned by `Qubrics::SDK.management(...)` as `management`
   and the account's `id` as `public_id`. Don't convert a list entry into
   `ProviderItem` or substitute an empty variables hash for the account's actual
   variables. Update hand-built detail fixtures to include `variables: {}` when
   no variables are set.

2. `mailbox_list_thread_messages` returns
   `MailboxThreadMessageSummaryCursorListResponse` instead of
   `MailboxMessageSummaryCursorListResponse`: its `meta` is
   `MailboxThreadMessagesMeta`, whose `thread_id` is required and whose
   `sync_state` is an optional string. Update thread-message class checks and
   add the thread identity to every thread-message result you construct:

   ```ruby
   def thread_message_list?(response)
     # Before: response.is_a?(Qubrics::Mailbox::Generated::MailboxMessageSummaryCursorListResponse)
     response.is_a?(Qubrics::Mailbox::Generated::MailboxThreadMessageSummaryCursorListResponse)
   end

   def thread_message_fixture(thread_id)
     # Before: meta: { request_id: "req_fixture" }
     Qubrics::Mailbox::Generated::MailboxThreadMessageSummaryCursorListResponse.build_from_hash(
       ok: true,
       meta: { request_id: "req_fixture", thread_id: thread_id },
       data: [],
       pagination: { has_more: false }
     )
   end
   ```

   Ordinary `mailbox_list_messages` results remain
   `MailboxMessageSummaryCursorListResponse` and have no thread identity. The
   other Mailbox list families replace the generic `ResponseMeta` with typed
   metadata whose `request_id` is unchanged and whose new fields are optional.

3. Run your application's tests with the updated bundle. Verify that list
   handling accepts `ProviderListItem` and only detail handling reads
   `variables`. A constructed thread-message result without `meta.thread_id`
   fails with `ArgumentError: thread_id cannot be nil`.

Update `qubrics-sdk`, `qubrics-mailbox`, `qubrics-management`, the bundle lock,
and affected call sites or fixtures together. To roll back, restore those gem
requirements, lock, and call-site changes together.

## OAuth access tokens

Pass either `api_key:` or `access_token:`. `access_token:` accepts a bare token string or a callable; the callable is evaluated once per authenticated request. Your application owns token storage, expiry checks and refresh coordination.

```ruby
require "qubrics/sdk"

client = Qubrics::SDK.management(
  access_token: -> { ENV.fetch("QUBRICS_ACCESS_TOKEN") }
)
```

## Usage

Use the umbrella gem when you want all Ruby SDK surfaces in one install.

```ruby
require "qubrics/sdk"

sending = Qubrics::SDK.sending(
  api_key: ENV.fetch("QUBRICS_MAILBOX_KEY")
)

mailbox = Qubrics::SDK.mailbox(
  api_key: ENV.fetch("QUBRICS_MAILBOX_KEY")
)

management = Qubrics::SDK.management(
  api_key: ENV.fetch("QUBRICS_ROOT_KEY")
)

puts sending.emails.class
puts mailbox.mailbox_api.class
puts management.mailboxes.class
```

`Qubrics::Sdk` is available as an alias for `Qubrics::SDK`.

### Surface clients

The umbrella package installs and re-exports:

- `qubrics-core`
- `qubrics-sending`
- `qubrics-mailbox`
- `qubrics-management`

The helper methods return the same clients exposed by the surface gems:

- `Qubrics::SDK.sending(...)` returns `Qubrics::Sending::Client`.
- `Qubrics::SDK.mailbox(...)` returns `Qubrics::Mailbox::Client`.
- `Qubrics::SDK.management(...)` returns `Qubrics::Management::Client`.

### Retries, pagination, and errors

Pass `Qubrics::Core::RetryOptions` through any umbrella helper. Use `Qubrics::Core.each_cursor` and `Qubrics::Core::Headers` with the generated operation methods exactly as you would with the surface gems.

```ruby
retry_options = Qubrics::Core::RetryOptions.new(max_attempts: 4)

management = Qubrics::SDK.management(
  api_key: ENV.fetch("QUBRICS_ROOT_KEY"),
  retry_options: retry_options
)

pager = Qubrics::Core.each_cursor(lambda do |opts|
  management.mailboxes.management_list_mailboxes(opts.merge(limit: 50))
end)

pager.each { |mailbox| puts mailbox.id }
```

Generated API errors are mapped to `Qubrics::Core::ApiError`.

## Support

- Documentation: https://qubrics.com/docs
- Contact: contact@qubrics.com

## Licence

MIT licence. See https://github.com/qubrics/qubrics-sdk/blob/main/LICENSE.
