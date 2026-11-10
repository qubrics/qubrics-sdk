# frozen_string_literal: true

Gem::Specification.new do |spec|
  spec.name = 'sendmux-sending'
  spec.version = '2.0.0'
  spec.authors = ['Qubrics']
  spec.summary = 'Deprecated: use qubrics-sending.'
  spec.description = 'sendmux-sending is deprecated. Install qubrics-sending and use Qubrics.'
  spec.homepage = 'https://github.com/qubrics/qubrics-sdk'
  spec.license = 'MIT'
  spec.required_ruby_version = '>= 3.1'
  spec.files = []
  spec.post_install_message = spec.description
  spec.add_dependency 'qubrics-sending', '>= 2.0.0', '< 3.0'
end
