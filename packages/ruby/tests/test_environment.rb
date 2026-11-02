# frozen_string_literal: true

require 'minitest/autorun'
require 'sendmux/sdk'

class SendmuxEnvironmentTest < Minitest::Test
  def test_legacy_then_qubrics_then_explicit_configuration
    names = %w[SENDMUX_API_KEY SENDMUX_BASE_URL QUBRICS_API_KEY QUBRICS_BASE_URL]
    previous = names.to_h { |name| [name, ENV.fetch(name, nil)] }
    %i[mailbox management sending].each do |surface|
      prefix = surface == :management ? 'smx_root_' : 'smx_mbx_'
      ENV.delete('QUBRICS_API_KEY')
      ENV.delete('QUBRICS_BASE_URL')
      ENV['SENDMUX_API_KEY'] = "#{prefix}legacy"
      ENV['SENDMUX_BASE_URL'] = 'https://legacy.fixture.test/api/v1'
      legacy = Sendmux::SDK.public_send(surface)
      assert_configuration(legacy, "#{prefix}legacy", 'https://legacy.fixture.test/api/v1')
      ENV['QUBRICS_API_KEY'] = "#{prefix}current"
      ENV['QUBRICS_BASE_URL'] = 'https://current.fixture.test/api/v1'
      current = Sendmux::SDK.public_send(surface)
      assert_configuration(current, "#{prefix}current", 'https://current.fixture.test/api/v1')
      explicit = Sendmux::SDK.public_send(surface, api_key: "#{prefix}explicit", base_url: 'https://explicit.fixture.test/api/v1')
      assert_configuration(explicit, "#{prefix}explicit", 'https://explicit.fixture.test/api/v1')
    end
  ensure
    previous.each { |name, value| value.nil? ? ENV.delete(name) : ENV[name] = value }
  end

  private

  def assert_configuration(client, api_key, base_url)
    assert_equal api_key, client.configuration.access_token
    assert_equal base_url, client.configuration.base_url
  end
end
