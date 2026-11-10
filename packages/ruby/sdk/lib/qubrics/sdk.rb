# frozen_string_literal: true

require 'qubrics/core'
require 'qubrics/mailbox'
require 'qubrics/management'
require 'qubrics/sending'
require 'qubrics/sdk/version'

module Qubrics
  module SDK
    def self.sending(api_key: nil, access_token: nil, base_url: nil, retry_options: nil)
      Qubrics::Sending::Client.new(api_key: api_key, access_token: access_token,
                                   base_url: base_url, retry_options: retry_options)
    end

    def self.mailbox(api_key: nil, access_token: nil, base_url: nil, retry_options: nil)
      Qubrics::Mailbox::Client.new(api_key: api_key, access_token: access_token,
                                   base_url: base_url, retry_options: retry_options)
    end

    def self.management(api_key: nil, access_token: nil, base_url: nil,
                        retry_options: nil)
      Qubrics::Management::Client.new(api_key: api_key, access_token: access_token,
                                      base_url: base_url, retry_options: retry_options)
    end
  end

  Sdk = SDK
end
