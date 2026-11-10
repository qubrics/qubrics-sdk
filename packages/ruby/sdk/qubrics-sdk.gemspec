# frozen_string_literal: true

require_relative 'lib/qubrics/sdk/version'

Gem::Specification.new do |spec|
  spec.name = 'qubrics-sdk'
  spec.version = Qubrics::SDK::VERSION
  spec.authors = ['Qubrics']
  spec.email = ['contact@qubrics.com']
  spec.summary = 'Umbrella Ruby SDK for Qubrics.'
  spec.homepage = 'https://github.com/qubrics/qubrics-sdk'
  spec.license = 'MIT'
  spec.required_ruby_version = '>= 3.1'
  spec.metadata = {
    'homepage_uri' => spec.homepage,
    'source_code_uri' => "#{spec.homepage}/tree/main/packages/ruby/sdk",
    'changelog_uri' => "#{spec.homepage}/blob/main/packages/ruby/sdk/CHANGELOG.md"
  }
  spec.files = Dir.chdir(__dir__) { Dir['lib/**/*.rb', 'README.md', 'CHANGELOG.md', 'LICENSE'] }
  spec.require_paths = ['lib']
  spec.add_dependency 'qubrics-core', '>= 1.3.0', '< 2.0'
  spec.add_dependency 'qubrics-mailbox', '>= 2.0.2', '< 3.0'
  spec.add_dependency 'qubrics-management', '>= 2.0.1', '< 3.0'
  spec.add_dependency 'qubrics-sending', '>= 1.5.0', '< 2.0'
end
