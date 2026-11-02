package sending_test

import (
	"context"
	"errors"
	"io"
	"net/http"
	"net/http/httptest"
	"strings"
	"sync/atomic"
	"testing"

	"github.com/ogen-go/ogen/ogenerrors"
	"sendmux.ai/go/v3/sending"
)

type optionalUploadTokens struct{ legacySendingSecurity }

func (optionalUploadTokens) UploadTokenQubrics(context.Context, sending.OperationName) (sending.UploadTokenQubrics, error) {
	return sending.UploadTokenQubrics{APIKey: "different-source-token"}, nil
}

func (optionalUploadTokens) UploadTokenSendmux(context.Context, sending.OperationName) (sending.UploadTokenSendmux, error) {
	return sending.UploadTokenSendmux{APIKey: "different-source-token"}, nil
}

func TestDelegatedUploadPreservesEitherTokenHeaderAndRejectsMissingToken(t *testing.T) {
	for _, fixture := range []struct {
		name, header, token, twinToken string
		optionalSource, wantUnauthorized bool
	}{
		{name: "qubrics", header: "X-Qubrics-Upload-Token", token: "upload-token"},
		{name: "sendmux", header: "X-Sendmux-Upload-Token", token: "upload-token"},
		{name: "missing"},
		{name: "invalid", header: "X-Qubrics-Upload-Token", token: "invalid-token", wantUnauthorized: true},
		{name: "qubrics-before-source", header: "X-Qubrics-Upload-Token", token: "upload-token", optionalSource: true},
		{name: "sendmux-before-source", header: "X-Sendmux-Upload-Token", token: "upload-token", optionalSource: true},
		{name: "conflicting", header: "X-Qubrics-Upload-Token", token: "upload-token", twinToken: "conflicting-token", wantUnauthorized: true},
	} {
		t.Run(fixture.name, func(t *testing.T) {
			var requests atomic.Int32
			server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				requests.Add(1)
				if r.Header.Get("Authorization") != "" {
					t.Error("delegated upload leaked the API credential")
				}
				if r.Header.Get(fixture.header) != fixture.token {
					t.Error("upload token header was overwritten")
				}
				w.Header().Set("Content-Type", "application/json")
				qubrics, sendmux := r.Header.Get("X-Qubrics-Upload-Token"), r.Header.Get("X-Sendmux-Upload-Token")
				if fixture.token != "upload-token" || (qubrics != "" && sendmux != "" && qubrics != sendmux) {
					w.WriteHeader(http.StatusUnauthorized)
					_, _ = io.WriteString(w, `{"ok":false,"error":{"code":"authentication_required","message":"Invalid upload token","retryable":false},"meta":{"request_id":"req_upload"}}`)
					return
				}
				w.Header().Set("Location", "/emails/attachments/att_aaaaaaaaaaaaaaaaaaaaaaaa")
				w.WriteHeader(http.StatusCreated)
				_, _ = io.WriteString(w, `{"ok":true,"data":{"attachment_id":"att_aaaaaaaaaaaaaaaaaaaaaaaa","filename":"test.txt","content_type":"text/plain","size_bytes":4,"expires_at":"2026-11-03T00:00:00Z"},"meta":{"request_id":"req_upload"}}`)
			}))
			defer server.Close()
			client, err := sending.New("smx_mbx_never-upload-token", sending.WithBaseURL(server.URL))
			if fixture.optionalSource {
				client, err = sending.NewClient(server.URL, optionalUploadTokens{})
			}
			if err != nil {
				t.Fatal(err)
			}
			params := sending.SendingCompleteAttachmentUploadParams{UploadID: "upl_aaaaaaaaaaaaaaaaaaaaaaaa", ContentLength: 4}
			if fixture.header == "X-Qubrics-Upload-Token" {
				params.XQubricsUploadToken = sending.NewOptString(fixture.token)
			} else if fixture.header != "" {
				params.XSendmuxUploadToken = sending.NewOptString(fixture.token)
			}
			if fixture.twinToken != "" {
				params.XSendmuxUploadToken = sending.NewOptString(fixture.twinToken)
			}
			response, err := client.SendingCompleteAttachmentUpload(context.Background(), sending.SendingCompleteAttachmentUploadReq{Data: strings.NewReader("test")}, params)
			if fixture.name == "missing" {
				if !errors.Is(err, ogenerrors.ErrSecurityRequirementIsNotSatisfied) || requests.Load() != 0 {
					t.Fatalf("missing token reached upload: response=%T err=%v requests=%d", response, err, requests.Load())
				}
				return
			}
			if err != nil {
				t.Fatal(err)
			}
			if fixture.wantUnauthorized {
				if _, ok := response.(*sending.SendingCompleteAttachmentUploadUnauthorized); !ok {
					t.Fatalf("invalid token accepted: %T", response)
				}
			} else if _, ok := response.(*sending.AttachmentUploadResponseHeaders); !ok {
				t.Fatalf("valid upload failed: %T", response)
			}
		})
	}
}
