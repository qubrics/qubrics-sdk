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

	"github.com/ogen-go/ogen/middleware"
	"github.com/ogen-go/ogen/ogenerrors"
	"qubrics.com/go/v4/sending"
)

type optionalUploadTokens struct{ legacySendingSecurity }

func (optionalUploadTokens) UploadTokenQubrics(context.Context, sending.OperationName) (sending.UploadTokenQubrics, error) {
	return sending.UploadTokenQubrics{APIKey: "different-source-token"}, nil
}

func (optionalUploadTokens) UploadTokenSendmux(context.Context, sending.OperationName) (sending.UploadTokenSendmux, error) {
	return sending.UploadTokenSendmux{APIKey: "different-source-token"}, nil
}

type uploadTokenServerSecurity struct {
	legacySendingSecurity
	checks int
}

func (s *uploadTokenServerSecurity) HandleUploadTokenQubrics(ctx context.Context, _ sending.OperationName, token sending.UploadTokenQubrics) (context.Context, error) {
	s.checks++
	if token.APIKey == "invalid-token" || token.APIKey == "single-use-token" && s.checks > 1 {
		return ctx, errors.New("invalid upload token")
	}
	return ctx, nil
}

func (s *uploadTokenServerSecurity) HandleUploadTokenSendmux(ctx context.Context, _ sending.OperationName, token sending.UploadTokenSendmux) (context.Context, error) {
	s.checks++
	if token.APIKey == "invalid-token" || token.APIKey == "single-use-token" && s.checks > 1 {
		return ctx, errors.New("invalid upload token")
	}
	return ctx, nil
}

type uploadTokenServerHandler struct {
	sending.UnimplementedHandler
	calls  int
	params sending.SendingCompleteAttachmentUploadParams
}

func TestDelegatedUploadServerAcceptsWhitespaceNormalisedTwinsOnWire(t *testing.T) {
	security := &uploadTokenServerSecurity{}
	handler := &uploadTokenServerHandler{}
	server, err := sending.NewServer(handler, security)
	if err != nil {
		t.Fatal(err)
	}
	fixture := httptest.NewServer(server)
	defer fixture.Close()
	request, err := http.NewRequest(http.MethodPut, fixture.URL+"/emails/attachment-uploads/upl_aaaaaaaaaaaaaaaaaaaaaaaa", strings.NewReader("test"))
	if err != nil {
		t.Fatal(err)
	}
	request.Header.Set("Content-Type", "application/octet-stream")
	request.Header.Set("X-Qubrics-Upload-Token", " \tupload-token\t ")
	request.Header.Set("X-Sendmux-Upload-Token", "upload-token")
	response, err := fixture.Client().Do(request)
	if err != nil {
		t.Fatal(err)
	}
	if err := response.Body.Close(); err != nil {
		t.Fatal(err)
	}
	fixture.Close()
	if response.StatusCode != http.StatusCreated || security.checks != 1 || handler.calls != 1 || handler.params.XSendmuxUploadToken != "upload-token" || handler.params.XQubricsUploadToken.Value != "upload-token" {
		t.Fatalf("normalised upload status=%d checks=%d calls=%d params=%+v", response.StatusCode, security.checks, handler.calls, handler.params)
	}
}

func (h *uploadTokenServerHandler) SendingCompleteAttachmentUpload(_ context.Context, _ sending.SendingCompleteAttachmentUploadReq, params sending.SendingCompleteAttachmentUploadParams) (sending.SendingCompleteAttachmentUploadRes, error) {
	h.calls++
	h.params = params
	return &sending.AttachmentUploadResponseHeaders{}, nil
}

func TestDelegatedUploadServerRejectsConflictingHeadersBeforeAuthentication(t *testing.T) {
	for _, fixture := range []struct {
		name                              string
		headers                           map[string]string
		wantStatus, wantChecks, wantCalls int
	}{
		{name: "qubrics", headers: map[string]string{"X-Qubrics-Upload-Token": "upload-token"}, wantStatus: 201, wantChecks: 1, wantCalls: 1},
		{name: "sendmux", headers: map[string]string{"X-Sendmux-Upload-Token": "upload-token"}, wantStatus: 201, wantChecks: 1, wantCalls: 1},
		{name: "equal", headers: map[string]string{"X-Qubrics-Upload-Token": "upload-token", "X-Sendmux-Upload-Token": "upload-token"}, wantStatus: 201, wantChecks: 1, wantCalls: 1},
		{name: "equal-single-use", headers: map[string]string{"X-Qubrics-Upload-Token": "single-use-token", "X-Sendmux-Upload-Token": "single-use-token"}, wantStatus: 201, wantChecks: 1, wantCalls: 1},
		{name: "conflicting", headers: map[string]string{"X-Qubrics-Upload-Token": "upload-token", "X-Sendmux-Upload-Token": "different-token"}, wantStatus: 401},
		{name: "empty-qubrics-twin", headers: map[string]string{"X-Qubrics-Upload-Token": "", "X-Sendmux-Upload-Token": "upload-token"}, wantStatus: 401},
		{name: "empty-sendmux-twin", headers: map[string]string{"X-Qubrics-Upload-Token": "upload-token", "X-Sendmux-Upload-Token": ""}, wantStatus: 401},
		{name: "missing", wantStatus: 401},
		{name: "both-empty", headers: map[string]string{"X-Qubrics-Upload-Token": "", "X-Sendmux-Upload-Token": ""}, wantStatus: 401},
		{name: "invalid", headers: map[string]string{"X-Qubrics-Upload-Token": "invalid-token"}, wantStatus: 401, wantChecks: 1},
	} {
		for _, withMiddleware := range []bool{false, true} {
			name := fixture.name + "/direct"
			var options []sending.ServerOption
			if withMiddleware {
				name = fixture.name + "/middleware"
				options = append(options, sending.WithMiddleware(func(req middleware.Request, next middleware.Next) (middleware.Response, error) {
					return next(req)
				}))
			}
			t.Run(name, func(t *testing.T) {
				security := &uploadTokenServerSecurity{}
				handler := &uploadTokenServerHandler{}
				server, err := sending.NewServer(handler, security, options...)
				if err != nil {
					t.Fatal(err)
				}
				request := httptest.NewRequest(http.MethodPut, "/emails/attachment-uploads/upl_aaaaaaaaaaaaaaaaaaaaaaaa", strings.NewReader("test"))
				request.Header.Set("Content-Type", "application/octet-stream")
				request.Header.Set("Content-Length", "4")
				for header, token := range fixture.headers {
					request.Header.Set(header, token)
				}
				response := httptest.NewRecorder()
				server.ServeHTTP(response, request)
				if response.Code != fixture.wantStatus || security.checks != fixture.wantChecks || handler.calls != fixture.wantCalls {
					t.Fatalf("upload status=%d checks=%d calls=%d; want status=%d checks=%d calls=%d", response.Code, security.checks, handler.calls, fixture.wantStatus, fixture.wantChecks, fixture.wantCalls)
				}
				if handler.calls > 0 && (handler.params.ContentLength != 4 || handler.params.UploadID != "upl_aaaaaaaaaaaaaaaaaaaaaaaa") {
					t.Fatalf("upload parameters changed: %+v", handler.params)
				}
				if handler.calls > 0 && handler.params.XSendmuxUploadToken != fixture.headers["X-Sendmux-Upload-Token"] {
					t.Fatalf("legacy upload token changed: %+v", handler.params)
				}
				if handler.calls > 0 {
					wantToken, wantPresent := fixture.headers["X-Qubrics-Upload-Token"]
					if token, present := handler.params.XQubricsUploadToken.Get(); token != wantToken || present != wantPresent {
						t.Fatalf("Qubrics upload token changed: %+v", handler.params)
					}
				}
			})
		}
	}
}

func TestDelegatedUploadPreservesEitherTokenHeaderAndRejectsMissingToken(t *testing.T) {
	for _, fixture := range []struct {
		name, header, token, twinToken   string
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
			params := sending.SendingCompleteAttachmentUploadParams{XSendmuxUploadToken: "", UploadID: "upl_aaaaaaaaaaaaaaaaaaaaaaaa", ContentLength: 4}
			if fixture.header == "X-Qubrics-Upload-Token" {
				params.XQubricsUploadToken = sending.NewOptString(fixture.token)
			} else if fixture.header != "" {
				params.XSendmuxUploadToken = fixture.token
			}
			if fixture.twinToken != "" {
				params.XSendmuxUploadToken = fixture.twinToken
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
