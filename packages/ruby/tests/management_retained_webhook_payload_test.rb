# frozen_string_literal: true

require 'minitest/autorun'
require 'qubrics/management'

class QubricsRetainedWebhookPayloadTest < Minitest::Test
  def test_retained_delivery_payload_round_trips_as_opaque_data
    snapshot = File.expand_path('../../python/mcp/qubrics/mcp/openapi/openapi-app.json', __dir__)
    %w[historical.event message.received].each do |event|
      payload = JSON.parse(File.read(snapshot)).dig('components', 'schemas', 'WebhookEventPayload', 'example')
      if event == 'historical.event'
        payload['type'] = event
        payload['data'] = { 'opaque' => ['retained', { 'unknown' => true }] }
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
