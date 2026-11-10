// Package sending contains the Qubrics Sending API client.
//
// Create a client with New and a send-capable smx_mbx_ key or owner-approved smx_agent_ token
// prefix. The client exposes generated methods for the Sending API, typed
// request and response models, idempotency header helpers, retry configuration,
// and API error mapping through APIErrorFromResponse.
package sending

// DefaultBaseURL is the production Qubrics Sending API base URL.
const DefaultBaseURL = "https://smtp.qubrics.com/api/v1"
