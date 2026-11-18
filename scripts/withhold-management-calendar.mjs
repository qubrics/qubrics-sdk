// Filter only the Management generator input; the live API remains unchanged.
export function withholdManagementCalendar(document) {
  const payload = document.components.schemas.WebhookEventPayload;
  payload.oneOf = payload.oneOf.filter(({ $ref }) => $ref !== "#/components/schemas/CalendarWebhookEventPayload");
  delete payload.discriminator.mapping["calendar.changed"];

  function removeCalendarEvent(value) {
    if (!value || typeof value !== "object") return;
    if (Array.isArray(value.enum)) {
      value.enum = value.enum.filter((event) => event !== "calendar.changed");
    }
    for (const child of Object.values(value)) removeCalendarEvent(child);
  }
  removeCalendarEvent(document);
}
