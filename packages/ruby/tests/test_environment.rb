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

  def test_empty_qubrics_api_key_uses_legacy_value
    names = %w[SENDMUX_API_KEY SENDMUX_ACCESS_TOKEN QUBRICS_API_KEY QUBRICS_ACCESS_TOKEN]
    previous = names.to_h { |name| [name, ENV.fetch(name, nil)] }
    names.each { |name| ENV.delete(name) }
    ENV['QUBRICS_API_KEY'] = ''
    %i[mailbox management sending].each do |surface|
      prefix = surface == :management ? 'smx_root_' : 'smx_mbx_'
      ENV['SENDMUX_API_KEY'] = "#{prefix}legacy"
      assert_equal "#{prefix}legacy", Sendmux::SDK.public_send(surface).configuration.access_token
    end
    ENV['SENDMUX_API_KEY'] = ''
    error = assert_raises(ArgumentError) { Sendmux::SDK.sending }
    assert_match(/API keys must start with/, error.message)
  ensure
    previous.each { |name, value| value.nil? ? ENV.delete(name) : ENV[name] = value }
  end

  def test_empty_qubrics_access_token_uses_legacy_value
    names = %w[SENDMUX_API_KEY SENDMUX_ACCESS_TOKEN QUBRICS_API_KEY QUBRICS_ACCESS_TOKEN]
    previous = names.to_h { |name| [name, ENV.fetch(name, nil)] }
    names.each { |name| ENV.delete(name) }
    ENV['QUBRICS_ACCESS_TOKEN'] = ''
    ENV['SENDMUX_ACCESS_TOKEN'] = 'legacy-token'
    %i[mailbox management sending].each do |surface|
      assert_equal 'legacy-token', Sendmux::SDK.public_send(surface).configuration.access_token
    end
    ENV['SENDMUX_ACCESS_TOKEN'] = ''
    error = assert_raises(ArgumentError) { Sendmux::SDK.sending }
    assert_match(/valid bare access token/, error.message)
  ensure
    previous.each { |name, value| value.nil? ? ENV.delete(name) : ENV[name] = value }
  end

  def test_empty_qubrics_base_url_uses_legacy_value
    names = %w[SENDMUX_BASE_URL QUBRICS_BASE_URL]
    previous = names.to_h { |name| [name, ENV.fetch(name, nil)] }
    ENV['QUBRICS_BASE_URL'] = ''
    ENV['SENDMUX_BASE_URL'] = 'https://legacy.fixture.test/api/v1'
    %i[mailbox management sending].each do |surface|
      prefix = surface == :management ? 'smx_root_' : 'smx_mbx_'
      client = Sendmux::SDK.public_send(surface, api_key: "#{prefix}explicit")
      assert_equal 'https://legacy.fixture.test/api/v1', client.configuration.base_url
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
