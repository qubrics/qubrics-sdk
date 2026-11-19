// Filter only the Management generator input; the live API remains unchanged.
export const retainedManagementSchemaRefs = ["#/components/schemas/WebhookEventPayload"];

export function withholdManagementCalendar(document) {
  const payload = document.components.schemas.WebhookEventPayload;
  payload.oneOf = payload.oneOf.filter(({ $ref }) => $ref !== "#/components/schemas/CalendarWebhookEventPayload");
  delete payload.discriminator.mapping["calendar.changed"];
  document.components.schemas.WebhookDeliveryPayload.properties.payload = { type: "object", additionalProperties: true };

  // Existing subscription/delivery labels remain readable without calendar bindings.
  for (const name of ["WebhookSubscription", "WebhookSubscriptionWithSecret", "WebhookDeliveryAttempt", "WebhookDeliveryPayload"]) {
    const properties = document.components.schemas[name].properties;
    delete (properties.event_type ?? properties.event_types.items).enum;
  }

  function removeCalendarEvent(value) {
    if (!value || typeof value !== "object") return;
    if (Array.isArray(value.enum)) {
      value.enum = value.enum.filter((event) => event !== "calendar.changed");
    }
    for (const child of Object.values(value)) removeCalendarEvent(child);
  }
  removeCalendarEvent(document);
}
