// Package core contains shared Qubrics Go SDK runtime helpers.
//
// The package provides API-key prefix validation, retry-aware HTTP clients,
// shared success and error envelope types, and a generic cursor iterator for
// code that adapts response pages to the Page interface. Applications usually
// import a surface package such as qubrics.com/go/v4/sending, qubrics.com/go/v4/mailbox,
// or qubrics.com/go/v4/management; those packages apply the core helpers for you.
package core
