# frozen_string_literal: true

Gem::Specification.new do |spec|
  spec.name = 'sendmux-core'
  spec.version = '2.0.0'
  spec.authors = ['Qubrics']
  spec.summary = 'Dependency-only package.'
  spec.description = 'Installs the required dependency.'
  spec.homepage = 'https://github.com/qubrics/qubrics-sdk'
  spec.license = 'MIT'
  spec.required_ruby_version = '>= 3.1'
  spec.files = []
  spec.add_dependency 'qubrics-core', '>= 2.0.0', '< 3.0'
end
