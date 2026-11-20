package management

import (
	"encoding/json"
	"reflect"
	"testing"
)

func TestRetainedWebhookPayloadAndLabelsStayOpaque(t *testing.T) {
	wire := []byte(`{"created_at":"2026-11-20T00:00:00Z","delivery_attempt":1,"event_id":"evt_retained","event_type":"calendar.changed","expires_at":"2026-11-21T00:00:00Z","id":"delivery_retained","payload":{"type":"calendar.changed","data":{"opaque":["retained",{"unknown":true}]}}}`)
	var retained WebhookDeliveryPayload
	if err := json.Unmarshal(wire, &retained); err != nil {
		t.Fatal(err)
	}
	if retained.EventType != "calendar.changed" {
		t.Fatalf("retained label changed: %q", retained.EventType)
	}
	encoded, err := json.Marshal(retained)
	if err != nil {
		t.Fatal(err)
	}
	var before, after map[string]any
	if err := json.Unmarshal(wire, &before); err != nil {
		t.Fatal(err)
	}
	if err := json.Unmarshal(encoded, &after); err != nil {
		t.Fatal(err)
	}
	if !reflect.DeepEqual(before["payload"], after["payload"]) {
		t.Fatalf("retained payload changed: %s", encoded)
	}
	subscription := WebhookSubscription{EventTypes: []string{"calendar.changed", "historical.event"}}
	if !reflect.DeepEqual(subscription.GetEventTypes(), []string{"calendar.changed", "historical.event"}) {
		t.Fatal("retained subscription labels changed")
	}
}

func TestMailWebhookModelsKeepEveryMailDiscriminator(t *testing.T) {
	for _, eventType := range []string{"message.bounced", "message.complained", "message.delivered", "message.delivery_delayed", "message.received", "message.received.spam", "message.rejected", "sendmux.test"} {
		t.Run(eventType, func(t *testing.T) {
			mail := MailWebhookEventPayload{
				Data: WebhookEventData{MessageID: NewNilString("message@example.com"), Recipients: []string{"inbox@example.com"}},
				ID:   "evt_fixture", OccurredAt: "2026-11-20T00:00:00Z", TeamPublicID: "team_fixture",
				Type: MailWebhookEventPayloadType(eventType),
			}
			var event WebhookEventPayload
			event.SetMailWebhookEventPayload(WebhookEventPayloadType(eventType), mail)
			wire, err := json.Marshal(event)
			if err != nil {
				t.Fatal(err)
			}
			var decoded WebhookEventPayload
			if err := json.Unmarshal(wire, &decoded); err != nil {
				t.Fatal(err)
			}
			retained, ok := decoded.GetMailWebhookEventPayload()
			if !ok || string(decoded.Type) != eventType || !reflect.DeepEqual(retained, mail) {
				t.Fatalf("mail webhook changed: %s", wire)
			}
		})
	}
}
