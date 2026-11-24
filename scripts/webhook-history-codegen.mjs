export const retainedManagementSchemaRefs = ["#/components/schemas/WebhookEventPayload"];

export function preserveWebhookHistory(document, { exposeKnownLabels = false } = {}) {
  const schemas = document.components.schemas;
  schemas.WebhookDeliveryPayload.properties.payload = { type: "object", additionalProperties: true };

  // Stored deliveries and subscriptions can contain labels outside the current write API.
  for (const name of ["WebhookSubscription", "WebhookSubscriptionWithSecret", "WebhookDeliveryAttempt", "WebhookDeliveryPayload"]) {
    const properties = schemas[name].properties;
    const property = properties.event_type ?? properties.event_types;
    if (exposeKnownLabels) {
      property["x-sendmux-open-label"] = true;
    } else {
      delete (property.items ?? property).enum;
    }
  }
}
