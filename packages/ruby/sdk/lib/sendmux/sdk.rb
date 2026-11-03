# frozen_string_literal: true

require 'sendmux/core'
require 'sendmux/mailbox'
require 'sendmux/management'
require 'sendmux/sending'
require 'sendmux/sdk/version'

module Sendmux
  module SDK
    def self.sending(api_key: nil, access_token: nil, base_url: nil, retry_options: nil)
      Sendmux::Sending::Client.new(api_key: api_key, access_token: access_token,
                                   base_url: base_url, retry_options: retry_options)
    end

    def self.mailbox(api_key: nil, access_token: nil, base_url: nil, retry_options: nil)
      Sendmux::Mailbox::Client.new(api_key: api_key, access_token: access_token,
                                   base_url: base_url, retry_options: retry_options)
    end

    def self.management(api_key: nil, access_token: nil, base_url: nil,
                        retry_options: nil)
      Sendmux::Management::Client.new(api_key: api_key, access_token: access_token,
                                      base_url: base_url, retry_options: retry_options)
    end
  end

  Sdk = SDK
end
