# frozen_string_literal: true

require 'json'
require 'minitest/autorun'
require 'sendmux/sdk'
require_relative 'oauth_http_fixture'

class SendmuxRubyDelegatedUploadTest < Minitest::Test
  include SendmuxRubyOAuthHTTPFixture

  UPLOAD_RESPONSE = {
    ok: true, meta: { request_id: 'req_upload' },
    data: { attachment_id: 'att_aaaaaaaaaaaaaaaaaaaaaaaa', filename: 'test.txt', content_type: 'text/plain',
            size_bytes: 4, expires_at: '2026-11-03T00:00:00Z' }
  }.to_json.freeze

  %w[qubrics sendmux].each do |family|
    define_method("test_#{family}_delegated_upload_does_not_read_or_leak_bearer_provider") do
      with_server(response: [201, {}, UPLOAD_RESPONSE]) do |url, requests|
        client = Sendmux::SDK.sending(
          access_token: -> { raise 'Delegated upload must not read the bearer credential' }, base_url: url
        )
        client.attachments.sending_complete_attachment_upload(
          4, 'upl_aaaaaaaaaaaaaaaaaaaaaaaa', 'test', "x_#{family}_upload_token": 'upload-token'
        )
        assert_equal 'upload-token', requests.first[:headers]["x-#{family}-upload-token"]
        refute requests.first[:headers].key?('authorization')
      end
    end
  end

  %i[sending_complete_attachment_upload sending_complete_attachment_upload_with_http_info].each do |method|
    [false, true].each do |with_options|
      define_method("test_#{method}_retains_legacy_arguments_#{with_options ? 'with' : 'without'}_options") do
        with_server(response: [201, {}, UPLOAD_RESPONSE]) do |url, requests|
          client = Sendmux::SDK.sending(
            access_token: -> { raise 'Delegated upload must not read the bearer credential' }, base_url: url
          )
          arguments = ['1234', 4, 'upl_aaaaaaaaaaaaaaaaaaaaaaaa', 'test']
          arguments << { header_params: { 'X-Compat' => 'kept' } } if with_options
          client.attachments.public_send(method, *arguments)
          assert_equal '1234', requests.first[:headers]['x-sendmux-upload-token']
          assert_equal 'test', requests.first[:body]
          assert_equal 'kept', requests.first[:headers]['x-compat'] if with_options
          refute requests.first[:headers].key?('authorization')
        end
      end
    end
  end
end
