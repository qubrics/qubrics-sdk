# frozen_string_literal: true

require 'json'
require 'minitest/autorun'
require 'qubrics/core'
require 'qubrics/mailbox'
require 'qubrics/management'
require 'qubrics/sdk'
require 'qubrics/sending'
require 'stringio'

class QubricsRubyCoreTest < Minitest::Test
  class GeneratedError < StandardError
    attr_reader :code, :response_headers, :response_body

    def initialize
      super('unprocessable')
      @code = 422
      @response_headers = { 'X-Request-Id' => 'req_header' }
      @response_body = {
        ok: false,
        error: {
          code: 'validation_error',
          message: 'Invalid request',
          param: 'email',
          retryable: false,
          errors: [{ field: 'email', message: 'is invalid' }]
        },
        meta: { request_id: 'req_body' }
      }.to_json
    end
  end

  RequestOptions = Struct.new(:params_encoder, :timeout, :on_data)

  class CaptureRequest
    attr_accessor :headers, :body, :params
    attr_reader :options, :url_value

    def initialize
      @options = RequestOptions.new
    end

    def url(value)
      @url_value = value
    end
  end

  def test_key_surface_validation
    assert_equal Qubrics::Core::ApiKeySurface::ROOT,
                 Qubrics::Core::Auth.assert_api_key_surface('smx_root_test', Qubrics::Core::ApiKeySurface::ROOT)
    assert_equal Qubrics::Core::ApiKeySurface::MAILBOX,
                 Qubrics::Core::Auth.assert_api_key_surface('smx_agent_test', Qubrics::Core::ApiKeySurface::MAILBOX)
    assert_equal Qubrics::Core::ApiKeySurface::MAILBOX,
                 Qubrics::Core::Auth.assert_api_key_surface('smx_mbx_test', Qubrics::Core::ApiKeySurface::SENDING)
    assert_equal Qubrics::Core::ApiKeySurface::MAILBOX,
                 Qubrics::Core::Auth.assert_api_key_surface('smx_agent_test', Qubrics::Core::ApiKeySurface::SENDING)
  end

  def test_root_key_is_rejected_for_sending_surface
    assert_raises(ArgumentError) do
      Qubrics::Core::Auth.assert_api_key_surface('smx_root_test', Qubrics::Core::ApiKeySurface::SENDING)
    end
  end

  def test_agent_token_is_rejected_for_root_surface
    assert_raises(ArgumentError) do
      Qubrics::Core::Auth.assert_api_key_surface('smx_agent_test', Qubrics::Core::ApiKeySurface::ROOT)
    end
  end

  def test_error_mapping_preserves_envelope_details
    mapped = Qubrics::Core::ErrorMapper.map(GeneratedError.new)

    assert_instance_of Qubrics::Core::ApiError, mapped
    assert_equal 422, mapped.status
    assert_equal 'validation_error', mapped.code
    assert_equal 'Invalid request', mapped.message
    assert_equal 'email', mapped.param
    assert_equal false, mapped.retryable
    assert_equal 'req_body', mapped.request_id
    assert_equal [{ 'field' => 'email', 'message' => 'is invalid' }], mapped.errors
  end

  def test_header_helpers_return_generated_option_keys
    assert_equal({ idempotency_key: 'idem_1' }, Qubrics::Core::Headers.idempotency_key('idem_1'))
    assert_equal({ if_match: 'W/"etag"' }, Qubrics::Core::Headers.if_match('W/"etag"'))
    assert_equal({ if_none_match: 'W/"etag"' }, Qubrics::Core::Headers.if_none_match('W/"etag"'))
    assert_equal({ if_match: 'a', if_none_match: 'b' }, Qubrics::Core::Headers.conditional(if_match: 'a',
                                                                                           if_none_match: 'b'))
  end

  def test_cursor_pager_streams_until_cursor_is_empty
    pages = [
      { data: [1, 2], meta: { pagination: { has_more: true, next_cursor: 'next' } } },
      { data: [3], meta: { pagination: { has_more: false } } }
    ]
    cursors = []
    pager = Qubrics::Core.each_cursor(lambda do |opts|
      cursors << opts[:cursor]
      pages.shift
    end)

    assert_equal [1, 2, 3], pager.to_a
    assert_equal [nil, 'next'], cursors
  end

  def test_retry_request_classification
    assert Qubrics::Core::Retry.retryable_request?({ method: :get, request_headers: {}, body: nil })
    assert Qubrics::Core::Retry.retryable_request?(
      { method: :post, request_headers: { 'Idempotency-Key' => 'idem' }, body: StringIO.new('body') }
    )
    refute Qubrics::Core::Retry.retryable_request?({ method: :post, request_headers: {}, body: 'body' })
  end

  def test_surface_clients_configure_auth_and_generated_apis
    sending = Qubrics::Sending::Client.new(api_key: 'smx_mbx_test')
    management = Qubrics::Management::Client.new(api_key: 'smx_root_test')
    mailbox = Qubrics::Mailbox::Client.new(api_key: 'smx_agent_test')

    assert_equal 'smx_mbx_test', sending.configuration.access_token
    assert_instance_of Qubrics::Sending::Generated::EmailsApi, sending.emails
    assert_equal 'smx_root_test', management.configuration.access_token
    assert_equal 'smx_agent_test', mailbox.configuration.access_token
  end

  def test_sending_generated_client_stringifies_content_length_header_before_transport
    request = CaptureRequest.new
    client = Qubrics::Sending::Generated::ApiClient.new(Qubrics::Sending::Generated::Configuration.new)

    client.build_request(:POST, '/emails/attachments', request,
                         header_params: { 'Content-Length': 99 },
                         auth_names: [],
                         body: 'abc')

    assert_equal '99', request.headers[:'Content-Length']
  end

  def test_all_generated_clients_stringify_non_string_headers_before_transport
    clients = [
      Qubrics::Sending::Generated::ApiClient.new(Qubrics::Sending::Generated::Configuration.new),
      Qubrics::Mailbox::Generated::ApiClient.new(Qubrics::Mailbox::Generated::Configuration.new),
      Qubrics::Management::Generated::ApiClient.new(Qubrics::Management::Generated::Configuration.new)
    ]

    clients.each do |client|
      request = CaptureRequest.new
      client.build_request(:POST, '/test', request,
                           header_params: { 'X-Numeric-Header': 3, 'X-Boolean-Header': true },
                           auth_names: [],
                           body: 'abc')

      assert_equal '3', request.headers[:'X-Numeric-Header']
      assert_equal 'true', request.headers[:'X-Boolean-Header']
    end
  end

  def test_umbrella_factories_validate_profile_surfaces
    assert_instance_of Qubrics::Sending::Client, Qubrics::SDK.sending(api_key: 'smx_mbx_test')
    assert_instance_of Qubrics::Mailbox::Client, Qubrics::SDK.mailbox(api_key: 'smx_agent_test')
    assert_raises(ArgumentError) { Qubrics::SDK.management(api_key: 'smx_agent_test') }
  end
end
