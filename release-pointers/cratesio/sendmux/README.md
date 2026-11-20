# sendmux

`sendmux` 1.0.0 re-exports the public API of `qubrics` 1.0.0.

Package tests pass on Rust 1.82 with the included lockfile. Use stable Rust to resolve dependencies for a fresh application.

```toml
[dependencies]
sendmux = "=1.0.0"
```

Use `sendmux::SendingClient`, `sendmux::MailboxClient` and `sendmux::ManagementClient`.

[API documentation](https://docs.rs/qubrics/1.0.0/qubrics/)
