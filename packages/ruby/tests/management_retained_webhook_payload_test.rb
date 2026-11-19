# frozen_string_literal: true

require 'minitest/autorun'
require 'qubrics/management'

class QubricsRetainedWebhookPayloadTest < Minitest::Test
  def test_retained_delivery_payload_round_trips_as_opaque_data
    snapshot = File.expand_path('../../python/mcp/qubrics/mcp/openapi/openapi-app.json', __dir__)
    %w[calendar.changed message.received].each do |event|
      payload = JSON.parse(File.read(snapshot)).dig('components', 'schemas', 'WebhookEventPayload', 'example')
      if event == 'calendar.changed'
        payload['type'] = event
        payload['data'] = {
          'mailbox_id' => 'mbx_test', 'resource' => 'event', 'created' => [], 'updated' => ['event_test'],
          'destroyed' => [], 'old_state' => 'state_old', 'new_state' => 'state_new',
          'has_more' => false, 'sync_required' => false
        }
      end
      body = {
        'id' => 'delivery_test', 'event_id' => payload['id'], 'event_type' => event, 'delivery_attempt' => 1,
        'created_at' => '2026-11-19T00:00:00Z', 'expires_at' => '2026-11-20T00:00:00Z', 'payload' => payload
      }
      decoded = Qubrics::Management::Generated::WebhookDeliveryPayload.build_from_hash(body)
      assert_equal payload, decoded.payload
      assert_equal body, JSON.parse(decoded.to_hash.to_json)
    end
  end
end
