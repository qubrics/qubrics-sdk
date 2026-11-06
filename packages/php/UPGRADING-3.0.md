# Migrate the PHP SDK from 2.x to 3.0

Update your dependencies and PHP imports. Version 3.0 replaces the five
`sendmux/*` Composer packages with `qubrics/*`, so change each directly required
package name in `composer.json` and replace `Sendmux\` with `Qubrics\` in your
PHP code. Rename `SendmuxApiError` to `QubricsApiError`.

Keep your existing `smx_*` credentials. Both `X-Sendmux-*` headers and
`sendmux_message_id` remain supported.

For Mailbox and the umbrella SDK, version 3.0 also changes the successful response
models for `mailboxGetChanges()` so both legacy and typed changes retain
their data. It also separates thread-message list responses and replaces
generic list metadata with operation-specific models. Update your Composer
constraint, response type declarations, and manually constructed metadata.

All five Qubrics packages start at 3.0.0 and use `^3.0` sibling dependency
constraints. Their maintained HTTP security constraints remain in place.

## Before you begin

- Use PHP 8.2 or newer and Composer.
- Commit your application, `composer.json`, and `composer.lock` so you can
  restore them together if you need to roll back.
- Before updating Mailbox directly, confirm that Packagist lists
  [`qubrics/mailbox` version 3.0.0](https://packagist.org/packages/qubrics/mailbox)
  and [`qubrics/core` version 3.0.0](https://packagist.org/packages/qubrics/core).
  Before updating the umbrella SDK, confirm that Packagist lists
  [`qubrics/sdk` version 3.0.0](https://packagist.org/packages/qubrics/sdk),
  [`qubrics/mailbox` version 3.0.0](https://packagist.org/packages/qubrics/mailbox),
  and version 3.0.0 of [`qubrics/core`](https://packagist.org/packages/qubrics/core),
  [`qubrics/sending`](https://packagist.org/packages/qubrics/sending), and
  [`qubrics/management`](https://packagist.org/packages/qubrics/management).
  Until Packagist lists every version required for your installation path,
  retain your existing Composer constraints.
- If you use 1.x, apply the [PHP 2.0 migration guide](UPGRADING.md) first.
- If your custom Guzzle client uses `FileCookieJar` or `SessionCookieJar`,
  back up its state and re-authenticate into a fresh jar when upgrading.
  Guzzle rejects old records without a boolean `HostOnly`; do not guess
  that value. Default Qubrics clients do not enable cookies. See the
  [upstream migration warning](https://github.com/guzzle/guzzle/security/advisories/GHSA-wm3w-8rrp-j577).

## Upgrade your application

1. In your application directory, replace directly required `sendmux/*`
   names in `composer.json` with their `qubrics/*` equivalents and `^3.0`
   constraints. Then update the package you install directly.
   For the umbrella SDK, run:

   ```bash
   composer require qubrics/sdk:^3.0 --with-all-dependencies
   ```

   If you install only Mailbox, run this command instead:

   ```bash
   composer require qubrics/mailbox:^3.0 --with-all-dependencies
   ```

   If both packages are direct dependencies, update both in one command:

   ```bash
   composer require qubrics/sdk:^3.0 qubrics/mailbox:^3.0 \
     --with-all-dependencies
   ```

   Composer resolves Mailbox and the umbrella SDK, when installed, to 3.x.
   The umbrella SDK requires all four Qubrics packages on 3.x.

2. Replace assumptions about `MailboxGetChanges200Response` in your imports,
   type declarations, subclasses, and response handling. For example, a
   wrapper that previously expected only the typed data model looked like:

   ```php
   use Qubrics\Mailbox\Model\MailboxGetChanges200Response;
   use Qubrics\Mailbox\Model\MailboxTypedChanges;

   function changesData(
       MailboxGetChanges200Response $response
   ): MailboxTypedChanges {
       return $response->getData();
   }
   ```

   Accept both successful response models and their corresponding data:

   ```php
   use Qubrics\Mailbox\Model\MailboxChanges;
   use Qubrics\Mailbox\Model\MailboxChangesResponse;
   use Qubrics\Mailbox\Model\MailboxTypedChanges;
   use Qubrics\Mailbox\Model\MailboxTypedChangesResponse;

   function changesData(
       MailboxChangesResponse|MailboxTypedChangesResponse $response
   ): MailboxChanges|MailboxTypedChanges {
       return $response->getData();
   }
   ```

   Legacy data provides `getCreated()`, `getUpdated()`, `getDestroyed()`,
   and `getNewState()`. Typed data provides `getTypes()`; for example,
   `getTypes()->getMessages()` returns `MailboxChanges` or null when that
   type is absent. Branch on the model before using model-specific getters.

   Apply the same change to responses from `mailboxGetChangesWithHttpInfo()`
   and resolved asynchronous calls. Method arguments are unchanged.
   With the default client, non-success responses still raise `ApiException`.
   Invalid JSON raises `ApiException`; valid JSON matching neither response
   model raises `UnexpectedValueException`. The declared `ApiError` union
   member remains unchanged; the breaking change concerns successful responses.

3. Replace `MailboxMessageSummaryCursorListResponse` with
   `MailboxThreadMessageSummaryCursorListResponse` wherever you type a
   successful `mailboxListThreadMessages()` result. Both classes remain
   available, but neither extends the other. Ordinary message-list responses
   still use `MailboxMessageSummaryCursorListResponse`.

   Apply the replacement to all four call forms:

   | Method | Successful result location |
   | --- | --- |
   | `mailboxListThreadMessages()` | Return value |
   | `mailboxListThreadMessagesWithHttpInfo()` | First element of `[response, status, headers]` |
   | `mailboxListThreadMessagesAsync()` | Resolved promise value |
   | `mailboxListThreadMessagesAsyncWithHttpInfo()` | First element of the resolved tuple |

   Update imports, typed wrappers, subclass overrides, and promise callbacks.
   For example, replace the old wrapper declaration:

   ```php
   use Qubrics\Mailbox\Model\MailboxMessageSummaryCursorListResponse;

   function threadRequestId(
       MailboxMessageSummaryCursorListResponse $response
   ): string {
       return $response->getMeta()->getRequestId();
   }
   ```

   Use the distinct thread response instead:

   ```php
   use Qubrics\Mailbox\Model\MailboxThreadMessageSummaryCursorListResponse;

   function threadRequestId(
       MailboxThreadMessageSummaryCursorListResponse $response
   ): string {
       return $response->getMeta()->getRequestId();
   }
   ```

   Method arguments, HTTP-info tuple structure, and the declared `ApiError`
   union member are unchanged.

4. Replace `ResponseMeta` in typed metadata consumers and in manually
   constructed response fixtures. For these five existing response classes,
   both `getMeta()` and `setMeta()` change from `ResponseMeta` to the listed
   class in `Qubrics\Mailbox\Model`:

   | Response class | 3.0 metadata class | Optional state field |
   | --- | --- | --- |
   | `MailboxIdentityCursorListResponse` | `MailboxIdentityListMeta` | `identity_state` |
   | `MailboxMessageSummaryCursorListResponse` | `MailboxSyncMeta` | `sync_state` |
   | `MailboxQuotaCursorListResponse` | `MailboxQueryMeta` | `query_state` |
   | `MailboxSubmissionCursorListResponse` | `MailboxQueryMeta` | `query_state` |
   | `MailboxThreadSummaryCursorListResponse` | `MailboxQueryMeta` | `query_state` |

   Each class requires `request_id`; none extends `ResponseMeta`. For example,
   replace `new ResponseMeta(['request_id' => 'request_example'])` with
   `new MailboxSyncMeta(['request_id' => 'request_example'])` when constructing
   an ordinary message-list response or calling its `setMeta()` method.

   The distinct thread-message response uses `MailboxThreadMessagesMeta`,
   which requires both `request_id` and `thread_id`; `sync_state` is optional.
   An empty `data` list does not remove the thread ID requirement. When you
   validate manually constructed responses, validate their metadata explicitly:
   the envelope's `valid()` does not recursively validate nested metadata.

   With your application's Composer autoloader loaded, this fixture needs no
   API call and prints `request_example thread_example`:

   ```php
   use Qubrics\Mailbox\Model\CursorPagination;
   use Qubrics\Mailbox\Model\MailboxThreadMessageSummaryCursorListResponse;
   use Qubrics\Mailbox\Model\MailboxThreadMessagesMeta;

   $meta = new MailboxThreadMessagesMeta([
       'request_id' => 'request_example',
       'thread_id' => 'thread_example',
   ]);
   $response = new MailboxThreadMessageSummaryCursorListResponse();
   $response->setMeta($meta);
   $response->setOk(true);
   $response->setData([]);
   $response->setPagination(new CursorPagination(['has_more' => false]));
   if (!$response->valid() || !$response->getMeta()->valid()) {
       throw new UnexpectedValueException('Invalid thread response or metadata');
   }
   echo $response->getMeta()->getRequestId(), ' ',
       $response->getMeta()->getThreadId(), PHP_EOL;
   ```

5. Replace `MailboxRealtimeMessageAllOfBody` with `MailboxRealtimeMessageBody`
   in imports, type declarations, and manually constructed realtime events.
   `MailboxRealtimeMessage::getBody()` returns the renamed class and
   `setBody()` accepts it; the `text`, `html`, `is_truncated`, and
   `max_bytes` accessors are unchanged. Remove any reference to
   `Qubrics\Mailbox\Model\Mailbox`, which no mailbox operation returned;
   `mailboxGetMe()` still returns `MailboxMeItemResponse` with `MailboxMe` data.

6. Update your Management provider-list wrappers and fixtures to accept
   `ProviderListItem[]` from `ProviderItemCursorListResponse::getData()` and
   pass that type to `setData()`. The response envelope keeps its name.
   List items have no `variables` field or `getVariables()` method.
   Call `managementGetProvider()` to read variables from its detail response:
   `ProviderItemResponse::getData()` returns `ProviderItem`, which exposes
   `getVariables()`.

7. Use concrete webhook payload models when constructing Management events.
   For mail events, use `MailWebhookEventPayload` with `WebhookEventData`.
   Calendar events use `CalendarWebhookEventPayload` with
   `CalendarWebhookEventData`. All four classes are in
   `Qubrics\Management\Model`. The base `WebhookEventPayload::setData()`
   accepts `CalendarWebhookEventData`, so move any mail fixtures using that
   base class to `MailWebhookEventPayload`. Schema-supported mail and
   calendar payloads still deserialise through their concrete models.

8. Replace the two Management model aliases scheduled for removal in 3.0.
   Both are in `Qubrics\Management\Model`:
   `MailboxAppPasswordResultCredential` becomes `MailboxCredential`, and
   `ProviderCreateBodyQuotasPerDayAnyOf` becomes `ProviderQuotaRange`.
   Update imports, type declarations, and constructor calls. The deprecated
   names no longer load.

## Verify the migration

Run this command in your application directory:

```bash
composer show 'qubrics/*'
```

Confirm that every installed Qubrics package is 3.x. Run your application's type checks
and tests for legacy changes, typed changes, thread-message lists, metadata
construction, and failed requests. Successful responses must preserve the
matching data model. Test empty ordinary and thread-message lists with absent
optional state, and explicitly reject thread metadata missing `thread_id`.
Malformed JSON and non-success requests must still follow your `ApiException`
handling; unmatched valid JSON, including `null`, must follow your
`UnexpectedValueException` handling.

For Management consumers, also test provider-list wrappers, provider detail
variables, and manually constructed mail and calendar webhook events. Confirm
that no application code refers to either removed Management model alias.

## Roll back

Restore the application code, `composer.json`, and `composer.lock` from the
same pre-upgrade revision, then run `composer install`. This package change
does not migrate server data. Returning to the previous packages also restores
their previous changes-response behaviour.

For client setup and API methods, see the [Mailbox package guide](mailbox/README.md).
