package sending_test

import (
	"context"
	"io"
	"net/http"
	"net/http/httptest"
	"testing"

	"qubrics.com/go/v4/sending"
)

func TestEnvironmentDefaultsPreferQubricsAndPreserveExplicitConfiguration(t *testing.T) {
	var received []string
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		received = append(received, r.Header.Get("Authorization"))
		w.Header().Set("Content-Type", "application/json")
		_, _ = io.WriteString(w, oauthConnection)
	}))
	defer server.Close()
	t.Setenv("QUBRICS_API_KEY", "")
	t.Setenv("QUBRICS_BASE_URL", "")
	t.Setenv("SENDMUX_API_KEY", "smx_mbx_legacy")
	t.Setenv("SENDMUX_BASE_URL", server.URL)
	legacy, err := sending.New("")
	if err != nil {
		t.Fatal(err)
	}
	if _, err := legacy.SendingGetConnection(context.Background(), sending.SendingGetConnectionParams{}); err != nil {
		t.Fatal(err)
	}
	t.Setenv("QUBRICS_API_KEY", "smx_mbx_current")
	t.Setenv("QUBRICS_BASE_URL", server.URL)
	t.Setenv("SENDMUX_BASE_URL", "https://unused.fixture.test/api/v1")
	current, err := sending.New("")
	if err != nil {
		t.Fatal(err)
	}
	if _, err := current.SendingGetConnection(context.Background(), sending.SendingGetConnectionParams{}); err != nil {
		t.Fatal(err)
	}
	t.Setenv("QUBRICS_BASE_URL", "https://unused.fixture.test/api/v1")
	explicit, err := sending.New("smx_mbx_explicit", sending.WithBaseURL(server.URL))
	if err != nil {
		t.Fatal(err)
	}
	if _, err := explicit.SendingGetConnection(context.Background(), sending.SendingGetConnectionParams{}); err != nil {
		t.Fatal(err)
	}
	for index, expected := range []string{"Bearer smx_mbx_legacy", "Bearer smx_mbx_current", "Bearer smx_mbx_explicit"} {
		if received[index] != expected {
			t.Errorf("request %d authorization=%q, expected %q", index, received[index], expected)
		}
	}
}
