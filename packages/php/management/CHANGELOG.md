# Changelog

## Unreleased

### Qubrics rename

- Publish as `qubrics/management` at 3.0.0 with `Qubrics\` namespaces and Qubrics service defaults.
- Keep existing credential prefixes, OAuth/custom URL configuration and compatibility wire names.

### Features

- Add provider variable management fields and delivery-group fields to delivery logs.

### Breaking changes

- Return `ProviderListItem[]` from `ProviderItemCursorListResponse::getData()` for `managementListProviders()`. Read variables from the `ProviderItem` detail model returned by `managementGetProvider()`.
- Use `MailWebhookEventPayload` for mail fixtures and `CalendarWebhookEventPayload` for calendar fixtures. The base `WebhookEventPayload::setData()` accepts `CalendarWebhookEventData`.
- Remove the deprecated `MailboxAppPasswordResultCredential` alias in 3.0. Use `MailboxCredential` instead.
- Remove the deprecated `ProviderCreateBodyQuotasPerDayAnyOf` alias in 3.0. Use `ProviderQuotaRange` instead.
- Follow the [PHP 3.0 migration guide](https://github.com/qubrics/qubrics-sdk/blob/main/packages/php/UPGRADING-3.0.md) when updating typed wrappers and manually constructed models.

## 2.1.1 (2026-09-16)

### Security

- Require Guzzle `^7.15.5`, PSR7 `^2.13.1`, and core `^2.1.1` for HTTP security fixes. If you use a custom persistent cookie jar, follow the [upgrade warning](README.md#installation) before updating.

## 2.1.0 (2026-09-11)

- Add `WithAccessToken` factories for REST OAuth tokens and callable providers.
- Require core 2.1 for OAuth authentication and retry handling.

## 2.0.0 (2026-09-08)

- Add `managementGetConnection()` and the connection client factory.
- Update generated Management API models and require core 2.0.
- Reject malformed JSON consistently in synchronous and asynchronous responses.
- Validate missing required fields without passing null to string or pattern constraints.
- Breaking: delivery-log detail data uses `DeliveryLogDetail`, and mailbox update scopes use `UpdateMailboxBodySendScope`; see the [migration guide](https://github.com/Sendmux/sendmux-sdk/blob/main/packages/php/UPGRADING.md).
