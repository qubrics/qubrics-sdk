package sdk_test

import (
	"context"
	"io"
	"net/http"
	"strings"
	"testing"

	"qubrics.com/go/v4/mailbox"
	"qubrics.com/go/v4/management"
	"qubrics.com/go/v4/sending"
)

func TestClientsDefaultToQubricsOrigins(t *testing.T) {
	t.Setenv("QUBRICS_BASE_URL", "")
	t.Setenv("SENDMUX_BASE_URL", "")
	for _, surface := range []struct {
		name   string
		origin string
		call   func(*http.Client) error
	}{
		{"sending", "https://smtp.qubrics.com", func(httpClient *http.Client) error {
			client, err := sending.NewWithAccessToken("fixture-token", sending.WithHTTPClient(httpClient))
			if err != nil {
				return err
			}
			_, err = client.SendingGetConnection(context.Background(), sending.SendingGetConnectionParams{})
			return err
		}},
		{"mailbox", "https://app.qubrics.com", func(httpClient *http.Client) error {
			client, err := mailbox.NewWithAccessToken("fixture-token", mailbox.WithHTTPClient(httpClient))
			if err != nil {
				return err
			}
			_, err = client.MailboxGetConnection(context.Background(), mailbox.MailboxGetConnectionParams{})
			return err
		}},
		{"management", "https://app.qubrics.com", func(httpClient *http.Client) error {
			client, err := management.NewWithAccessToken("fixture-token", management.WithHTTPClient(httpClient))
			if err != nil {
				return err
			}
			_, err = client.ManagementGetConnection(context.Background(), management.ManagementGetConnectionParams{})
			return err
		}},
	} {
		t.Run(surface.name, func(t *testing.T) {
			var origin string
			httpClient := &http.Client{Transport: roundTripFunc(func(request *http.Request) (*http.Response, error) {
				origin = request.URL.Scheme + "://" + request.URL.Host
				return &http.Response{StatusCode: http.StatusUnauthorized, Header: make(http.Header), Body: io.NopCloser(strings.NewReader("{}"))}, nil
			})}
			_ = surface.call(httpClient)
			if origin != surface.origin {
				t.Fatalf("request origin = %q, expected %q", origin, surface.origin)
			}
		})
	}
}

type roundTripFunc func(*http.Request) (*http.Response, error)

func (f roundTripFunc) RoundTrip(request *http.Request) (*http.Response, error) {
	return f(request)
}
