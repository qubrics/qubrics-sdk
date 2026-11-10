# qubrics-mailbox

[![Gem Version](https://badge.fury.io/rb/qubrics-mailbox.svg)](https://rubygems.org/gems/qubrics-mailbox)
[![CI](https://github.com/qubrics/qubrics-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/qubrics/qubrics-sdk/actions/workflows/ci.yml)
[![Licence: MIT](https://img.shields.io/badge/licence-MIT-blue.svg)](https://github.com/qubrics/qubrics-sdk/blob/main/LICENSE)

Ruby SDK package for the Qubrics Mailbox API.

## Documentation

- Ruby SDK guide: https://qubrics.com/docs/sdks/ruby
- Mailbox API reference: https://qubrics.com/docs/mailbox-api
- Source: https://github.com/qubrics/qubrics-sdk/tree/main/packages/ruby/mailbox
- Changelog: https://github.com/qubrics/qubrics-sdk/blob/main/packages/ruby/mailbox/CHANGELOG.md

## Requirements

- Ruby 3.1 or newer.
- A mailbox-scoped `smx_mbx_` key or scoped `smx_agent_` token.

For OAuth, use a REST access token with the scopes and mailbox access required by the operation. See [OAuth for REST APIs](https://qubrics.com/docs/developer-tools/oauth).

## Installation

These commands target the Qubrics release of `qubrics-mailbox`. Until it is published, install `sendmux-mailbox` with its existing require paths and `Sendmux` module.

```sh
gem install qubrics-mailbox
```

Or add it to your Gemfile:

```ruby
gem "qubrics-mailbox", "~> 3.0"
```

## Thread message model migration

If you check thread-message result classes or build thread-message fixtures by hand,
use the thread-specific models below. `mailbox_list_thread_messages` returns
`MailboxThreadMessageSummaryCursorListResponse` instead of
`MailboxMessageSummaryCursorListResponse`: its `meta` is
`MailboxThreadMessagesMeta`, whose `thread_id` is required and whose
`sync_state` is an optional string. Code that only reads thread-message results
keeps working.

1. Update thread-message class checks to use the class loaded by the public
   entry point:

   ```ruby
   require "qubrics/mailbox"

   def thread_message_list?(response)
     # Before: response.is_a?(Qubrics::Mailbox::Generated::MailboxMessageSummaryCursorListResponse)
     response.is_a?(Qubrics::Mailbox::Generated::MailboxThreadMessageSummaryCursorListResponse)
   end
   ```

2. Add the thread identity to every thread-message result you construct. Pass
   the thread's `id` as the `thread_id` argument when you read one from the
   public client:

   ```ruby
   def thread_message_fixture(thread_id)
     # Before: meta: { request_id: "req_fixture" }
     Qubrics::Mailbox::Generated::MailboxThreadMessageSummaryCursorListResponse.build_from_hash(
       ok: true,
       meta: { request_id: "req_fixture", thread_id: thread_id },
       data: [],
       pagination: { has_more: false }
     )
   end

   def thread_sync_state(client, thread_id)
     response = client.mailbox_api.mailbox_list_thread_messages(thread_id, limit: 50)
     [response.meta.thread_id, response.meta.sync_state]
   end
   ```

   Ordinary `mailbox_list_messages` results remain
   `MailboxMessageSummaryCursorListResponse`: they have no thread identity and
   expose an optional typed `meta.sync_state`. Identity, submission, quota, and
   thread list responses likewise replace the generic `ResponseMeta` with
   `MailboxIdentityListMeta` or `MailboxQueryMeta`, which add optional
   `identity_state` or `query_state`; `meta.request_id` is unchanged everywhere
   and no new field is required there.

3. Run your application's tests with the updated bundle. A constructed
   thread-message result without `meta.thread_id` fails with
   `ArgumentError: thread_id cannot be nil`.

Update `qubrics-mailbox`, the bundle lock, and affected call sites or fixtures
together. To roll back, restore those gem requirement, lock, and call-site
changes together.

## OAuth access tokens

Pass either `api_key:` or `access_token:`. `access_token:` accepts a bare token string or a callable; the callable is evaluated once per authenticated request. Your application owns token storage, expiry checks and refresh coordination.

```ruby
require "qubrics/mailbox"

client = Qubrics::Mailbox::Client.new(
  access_token: -> { ENV.fetch("QUBRICS_ACCESS_TOKEN") }
)
```

## Usage

Create a mailbox client with a mailbox key or scoped agent token for the API-key example below.

```ruby
require "qubrics/mailbox"

client = Qubrics::Mailbox::Client.new(
  api_key: ENV.fetch("QUBRICS_MAILBOX_KEY")
)

me = client.mailbox_api.mailbox_get_me
messages = client.mailbox_api.mailbox_list_messages(limit: 25)

puts me.data.email
puts messages.data.length
```

### Client surface

`Qubrics::Mailbox::Client` exposes `client.mailbox_api`, which contains generated mailbox operations such as:

- `mailbox_get_me`
- `mailbox_list_messages`
- `mailbox_get_message`
- `mailbox_send_message`
- `mailbox_list_threads`
- `mailbox_upload_attachment`

When a key grants access to more than one mailbox, pass `mailbox_id:` to operations that accept it.

### Pagination and conditional requests

Use `Qubrics::Core.each_cursor` for list operations that return cursor pagination. Use the ETag helpers for generated operations that accept `:if_match` or `:if_none_match`.

```ruby
pager = Qubrics::Core.each_cursor(lambda do |opts|
  client.mailbox_api.mailbox_list_messages(opts.merge(limit: 50))
end)

pager.each { |message| puts message.id }

client.mailbox_api.mailbox_delete_message(
  "msg_123",
  Qubrics::Core::Headers.if_match('W/"etag"')
)
```

### Attachments and events

Message and event attachment metadata includes `download_url`, a short-lived presigned URL for that single attachment. Fetch it promptly with a plain HTTP client and no `Authorization` header. If it expires, re-fetch the message or attachment metadata to receive a fresh URL.

Use `mailbox_upload_attachment` to upload bytes and pass the returned `blob_id` into `mailbox_send_message` attachments. Inline base64 attachments remain available in the generated send body shape for small payloads.

`mailbox_stream_events` exposes the Mailbox SSE endpoint for clients that want live `message.received` events.

### Errors

Generated API errors are mapped to `Qubrics::Core::ApiError`.

```ruby
begin
  client.mailbox_api.mailbox_get_message("msg_123")
rescue Qubrics::Core::ApiError => error
  warn "#{error.status} #{error.code}: #{error.message}"
end
```

## Support

- Documentation: https://qubrics.com/docs
- Contact: contact@qubrics.com

## Licence

MIT licence. See https://github.com/qubrics/qubrics-sdk/blob/main/LICENSE.
