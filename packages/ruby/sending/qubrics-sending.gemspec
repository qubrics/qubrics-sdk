# frozen_string_literal: true

require_relative 'lib/qubrics/sending/version'

Gem::Specification.new do |spec|
  spec.name = 'qubrics-sending'
  spec.version = Qubrics::Sending::VERSION
  spec.authors = ['Qubrics']
  spec.email = ['contact@qubrics.com']
  spec.summary = 'Ruby SDK for the Qubrics Sending API.'
  spec.homepage = 'https://github.com/qubrics/qubrics-sdk'
  spec.license = 'MIT'
  spec.required_ruby_version = '>= 3.1'
  spec.metadata = {
    'homepage_uri' => spec.homepage,
    'source_code_uri' => "#{spec.homepage}/tree/main/packages/ruby/sending",
    'changelog_uri' => "#{spec.homepage}/blob/main/packages/ruby/sending/CHANGELOG.md"
  }
  spec.files = Dir.chdir(__dir__) { Dir['lib/**/*.rb', 'README.md', 'CHANGELOG.md', 'LICENSE'] }
  spec.require_paths = ['lib']
  spec.add_dependency 'faraday', '~> 2.0'
  spec.add_dependency 'faraday-multipart', '~> 1.0'
  spec.add_dependency 'faraday-retry', '>= 2.4', '< 3.0'
  spec.add_dependency 'marcel', '~> 1.0'
  spec.add_dependency 'qubrics-core', '>= 1.3.0', '< 2.0'
end
