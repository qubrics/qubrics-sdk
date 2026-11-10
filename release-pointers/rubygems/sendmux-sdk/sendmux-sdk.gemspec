# frozen_string_literal: true

Gem::Specification.new do |spec|
  spec.name = 'sendmux-sdk'
  spec.version = '3.0.0'
  spec.authors = ['Qubrics']
  spec.summary = 'Deprecated: use qubrics-sdk.'
  spec.description = 'sendmux-sdk is deprecated. Install qubrics-sdk and use Qubrics.'
  spec.homepage = 'https://github.com/qubrics/qubrics-sdk'
  spec.license = 'MIT'
  spec.required_ruby_version = '>= 3.1'
  spec.files = []
  spec.post_install_message = spec.description
  spec.add_dependency 'qubrics-sdk', '>= 3.0.0', '< 4.0'
end
