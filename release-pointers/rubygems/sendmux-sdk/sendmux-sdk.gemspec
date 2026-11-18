# frozen_string_literal: true

Gem::Specification.new do |spec|
  spec.name = 'sendmux-sdk'
  spec.version = '3.0.0'
  spec.authors = ['Qubrics']
  spec.summary = 'Dependency-only package.'
  spec.description = 'Installs the required dependency.'
  spec.homepage = 'https://github.com/qubrics/qubrics-sdk'
  spec.license = 'MIT'
  spec.required_ruby_version = '>= 3.1'
  spec.files = []
  spec.add_dependency 'qubrics-sdk', '>= 3.0.0', '< 4.0'
end
