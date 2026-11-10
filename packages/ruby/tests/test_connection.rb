# frozen_string_literal: true

require 'minitest/autorun'
require 'qubrics/sdk'

class QubricsRubyConnectionTest < Minitest::Test
  def test_base_url_preserves_ipv6_port_and_normalises_default_https_port
    %i[management mailbox sending].each do |surface|
      key = surface == :management ? 'smx_root_test' : 'smx_mbx_test'
      custom = Qubrics::SDK.public_send(surface, api_key: key, base_url: 'http://[::1]:45678/api/v1')
      assert_equal 'http://[::1]:45678/api/v1', custom.configuration.base_url
      default = Qubrics::SDK.public_send(surface, api_key: key, base_url: 'https://example.com:443/api/v1')
      assert_equal 'https://example.com/api/v1', default.configuration.base_url
    end
  end
end
