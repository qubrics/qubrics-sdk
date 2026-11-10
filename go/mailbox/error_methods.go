package mailbox

import "qubrics.com/go/v4/core"

// APIError maps MailboxBatchDeleteMessagesBadRequest into the shared typed API error.
func (r *MailboxBatchDeleteMessagesBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxBatchDeleteMessagesConflict into the shared typed API error.
func (r *MailboxBatchDeleteMessagesConflict) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 409)
	return err
}

// APIError maps MailboxBatchDeleteMessagesRequestEntityTooLarge into the shared typed API error.
func (r *MailboxBatchDeleteMessagesRequestEntityTooLarge) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 413)
	return err
}

// APIError maps MailboxBatchGetMessagesBadRequest into the shared typed API error.
func (r *MailboxBatchGetMessagesBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxBatchGetMessagesNotFound into the shared typed API error.
func (r *MailboxBatchGetMessagesNotFound) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 404)
	return err
}

// APIError maps MailboxBatchGetMessagesRequestEntityTooLarge into the shared typed API error.
func (r *MailboxBatchGetMessagesRequestEntityTooLarge) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 413)
	return err
}

// APIError maps MailboxBatchUpdateMessagesBadRequest into the shared typed API error.
func (r *MailboxBatchUpdateMessagesBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxBatchUpdateMessagesConflict into the shared typed API error.
func (r *MailboxBatchUpdateMessagesConflict) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 409)
	return err
}

// APIError maps MailboxBatchUpdateMessagesRequestEntityTooLarge into the shared typed API error.
func (r *MailboxBatchUpdateMessagesRequestEntityTooLarge) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 413)
	return err
}

// APIError maps MailboxControlDraftScheduleBadRequest into the shared typed API error.
func (r *MailboxControlDraftScheduleBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxControlDraftScheduleConflict into the shared typed API error.
func (r *MailboxControlDraftScheduleConflict) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 409)
	return err
}

// APIError maps MailboxControlDraftScheduleForbidden into the shared typed API error.
func (r *MailboxControlDraftScheduleForbidden) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 403)
	return err
}

// APIError maps MailboxControlDraftScheduleInternalServerError into the shared typed API error.
func (r *MailboxControlDraftScheduleInternalServerError) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 500)
	return err
}

// APIError maps MailboxControlDraftScheduleNotFound into the shared typed API error.
func (r *MailboxControlDraftScheduleNotFound) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 404)
	return err
}

// APIError maps MailboxControlDraftScheduleRequestEntityTooLarge into the shared typed API error.
func (r *MailboxControlDraftScheduleRequestEntityTooLarge) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 413)
	return err
}

// APIError maps MailboxControlDraftScheduleServiceUnavailable into the shared typed API error.
func (r *MailboxControlDraftScheduleServiceUnavailable) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 503)
	return err
}

// APIError maps MailboxControlDraftScheduleTooManyRequests into the shared typed API error.
func (r *MailboxControlDraftScheduleTooManyRequests) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 429)
	return err
}

// APIError maps MailboxControlDraftScheduleUnauthorized into the shared typed API error.
func (r *MailboxControlDraftScheduleUnauthorized) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 401)
	return err
}

// APIError maps MailboxControlDraftScheduleUnprocessableEntity into the shared typed API error.
func (r *MailboxControlDraftScheduleUnprocessableEntity) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 422)
	return err
}

// APIError maps MailboxCreateAttachmentUploadBadRequest into the shared typed API error.
func (r *MailboxCreateAttachmentUploadBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxCreateAttachmentUploadRequestEntityTooLarge into the shared typed API error.
func (r *MailboxCreateAttachmentUploadRequestEntityTooLarge) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 413)
	return err
}

// APIError maps MailboxCreateAttachmentUploadServiceUnavailable into the shared typed API error.
func (r *MailboxCreateAttachmentUploadServiceUnavailable) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 503)
	return err
}

// APIError maps MailboxCreateCalendarBadRequest into the shared typed API error.
func (r *MailboxCreateCalendarBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxCreateCalendarConflict into the shared typed API error.
func (r *MailboxCreateCalendarConflict) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 409)
	return err
}

// APIError maps MailboxCreateCalendarEventBadRequest into the shared typed API error.
func (r *MailboxCreateCalendarEventBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxCreateCalendarEventConflict into the shared typed API error.
func (r *MailboxCreateCalendarEventConflict) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 409)
	return err
}

// APIError maps MailboxCreateCalendarEventForbidden into the shared typed API error.
func (r *MailboxCreateCalendarEventForbidden) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 403)
	return err
}

// APIError maps MailboxCreateCalendarEventInternalServerError into the shared typed API error.
func (r *MailboxCreateCalendarEventInternalServerError) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 500)
	return err
}

// APIError maps MailboxCreateCalendarEventNotFound into the shared typed API error.
func (r *MailboxCreateCalendarEventNotFound) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 404)
	return err
}

// APIError maps MailboxCreateCalendarEventRequestEntityTooLarge into the shared typed API error.
func (r *MailboxCreateCalendarEventRequestEntityTooLarge) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 413)
	return err
}

// APIError maps MailboxCreateCalendarEventServiceUnavailable into the shared typed API error.
func (r *MailboxCreateCalendarEventServiceUnavailable) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 503)
	return err
}

// APIError maps MailboxCreateCalendarEventTooManyRequests into the shared typed API error.
func (r *MailboxCreateCalendarEventTooManyRequests) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 429)
	return err
}

// APIError maps MailboxCreateCalendarEventUnauthorized into the shared typed API error.
func (r *MailboxCreateCalendarEventUnauthorized) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 401)
	return err
}

// APIError maps MailboxCreateCalendarEventUnprocessableEntity into the shared typed API error.
func (r *MailboxCreateCalendarEventUnprocessableEntity) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 422)
	return err
}

// APIError maps MailboxCreateCalendarForbidden into the shared typed API error.
func (r *MailboxCreateCalendarForbidden) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 403)
	return err
}

// APIError maps MailboxCreateCalendarInternalServerError into the shared typed API error.
func (r *MailboxCreateCalendarInternalServerError) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 500)
	return err
}

// APIError maps MailboxCreateCalendarNotFound into the shared typed API error.
func (r *MailboxCreateCalendarNotFound) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 404)
	return err
}

// APIError maps MailboxCreateCalendarRequestEntityTooLarge into the shared typed API error.
func (r *MailboxCreateCalendarRequestEntityTooLarge) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 413)
	return err
}

// APIError maps MailboxCreateCalendarServiceUnavailable into the shared typed API error.
func (r *MailboxCreateCalendarServiceUnavailable) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 503)
	return err
}

// APIError maps MailboxCreateCalendarTooManyRequests into the shared typed API error.
func (r *MailboxCreateCalendarTooManyRequests) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 429)
	return err
}

// APIError maps MailboxCreateCalendarUnauthorized into the shared typed API error.
func (r *MailboxCreateCalendarUnauthorized) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 401)
	return err
}

// APIError maps MailboxCreateCalendarUnprocessableEntity into the shared typed API error.
func (r *MailboxCreateCalendarUnprocessableEntity) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 422)
	return err
}

// APIError maps MailboxCreateDraftBadRequest into the shared typed API error.
func (r *MailboxCreateDraftBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxCreateDraftConflict into the shared typed API error.
func (r *MailboxCreateDraftConflict) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 409)
	return err
}

// APIError maps MailboxCreateDraftForbidden into the shared typed API error.
func (r *MailboxCreateDraftForbidden) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 403)
	return err
}

// APIError maps MailboxCreateDraftInternalServerError into the shared typed API error.
func (r *MailboxCreateDraftInternalServerError) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 500)
	return err
}

// APIError maps MailboxCreateDraftNotFound into the shared typed API error.
func (r *MailboxCreateDraftNotFound) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 404)
	return err
}

// APIError maps MailboxCreateDraftRequestEntityTooLarge into the shared typed API error.
func (r *MailboxCreateDraftRequestEntityTooLarge) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 413)
	return err
}

// APIError maps MailboxCreateDraftServiceUnavailable into the shared typed API error.
func (r *MailboxCreateDraftServiceUnavailable) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 503)
	return err
}

// APIError maps MailboxCreateDraftTooManyRequests into the shared typed API error.
func (r *MailboxCreateDraftTooManyRequests) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 429)
	return err
}

// APIError maps MailboxCreateDraftUnauthorized into the shared typed API error.
func (r *MailboxCreateDraftUnauthorized) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 401)
	return err
}

// APIError maps MailboxCreateDraftUnprocessableEntity into the shared typed API error.
func (r *MailboxCreateDraftUnprocessableEntity) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 422)
	return err
}

// APIError maps MailboxCreateFolderBadRequest into the shared typed API error.
func (r *MailboxCreateFolderBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxCreateFolderRequestEntityTooLarge into the shared typed API error.
func (r *MailboxCreateFolderRequestEntityTooLarge) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 413)
	return err
}

// APIError maps MailboxCreateFolderUnprocessableEntity into the shared typed API error.
func (r *MailboxCreateFolderUnprocessableEntity) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 422)
	return err
}

// APIError maps MailboxDeleteCalendarBadRequest into the shared typed API error.
func (r *MailboxDeleteCalendarBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxDeleteCalendarConflict into the shared typed API error.
func (r *MailboxDeleteCalendarConflict) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 409)
	return err
}

// APIError maps MailboxDeleteCalendarEventBadRequest into the shared typed API error.
func (r *MailboxDeleteCalendarEventBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxDeleteCalendarEventConflict into the shared typed API error.
func (r *MailboxDeleteCalendarEventConflict) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 409)
	return err
}

// APIError maps MailboxDeleteCalendarEventForbidden into the shared typed API error.
func (r *MailboxDeleteCalendarEventForbidden) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 403)
	return err
}

// APIError maps MailboxDeleteCalendarEventInternalServerError into the shared typed API error.
func (r *MailboxDeleteCalendarEventInternalServerError) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 500)
	return err
}

// APIError maps MailboxDeleteCalendarEventNotFound into the shared typed API error.
func (r *MailboxDeleteCalendarEventNotFound) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 404)
	return err
}

// APIError maps MailboxDeleteCalendarEventRequestEntityTooLarge into the shared typed API error.
func (r *MailboxDeleteCalendarEventRequestEntityTooLarge) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 413)
	return err
}

// APIError maps MailboxDeleteCalendarEventServiceUnavailable into the shared typed API error.
func (r *MailboxDeleteCalendarEventServiceUnavailable) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 503)
	return err
}

// APIError maps MailboxDeleteCalendarEventTooManyRequests into the shared typed API error.
func (r *MailboxDeleteCalendarEventTooManyRequests) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 429)
	return err
}

// APIError maps MailboxDeleteCalendarEventUnauthorized into the shared typed API error.
func (r *MailboxDeleteCalendarEventUnauthorized) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 401)
	return err
}

// APIError maps MailboxDeleteCalendarEventUnprocessableEntity into the shared typed API error.
func (r *MailboxDeleteCalendarEventUnprocessableEntity) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 422)
	return err
}

// APIError maps MailboxDeleteCalendarForbidden into the shared typed API error.
func (r *MailboxDeleteCalendarForbidden) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 403)
	return err
}

// APIError maps MailboxDeleteCalendarInternalServerError into the shared typed API error.
func (r *MailboxDeleteCalendarInternalServerError) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 500)
	return err
}

// APIError maps MailboxDeleteCalendarNotFound into the shared typed API error.
func (r *MailboxDeleteCalendarNotFound) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 404)
	return err
}

// APIError maps MailboxDeleteCalendarRequestEntityTooLarge into the shared typed API error.
func (r *MailboxDeleteCalendarRequestEntityTooLarge) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 413)
	return err
}

// APIError maps MailboxDeleteCalendarServiceUnavailable into the shared typed API error.
func (r *MailboxDeleteCalendarServiceUnavailable) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 503)
	return err
}

// APIError maps MailboxDeleteCalendarTooManyRequests into the shared typed API error.
func (r *MailboxDeleteCalendarTooManyRequests) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 429)
	return err
}

// APIError maps MailboxDeleteCalendarUnauthorized into the shared typed API error.
func (r *MailboxDeleteCalendarUnauthorized) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 401)
	return err
}

// APIError maps MailboxDeleteCalendarUnprocessableEntity into the shared typed API error.
func (r *MailboxDeleteCalendarUnprocessableEntity) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 422)
	return err
}

// APIError maps MailboxDeleteDraftBadRequest into the shared typed API error.
func (r *MailboxDeleteDraftBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxDeleteDraftConflict into the shared typed API error.
func (r *MailboxDeleteDraftConflict) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 409)
	return err
}

// APIError maps MailboxDeleteDraftForbidden into the shared typed API error.
func (r *MailboxDeleteDraftForbidden) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 403)
	return err
}

// APIError maps MailboxDeleteDraftInternalServerError into the shared typed API error.
func (r *MailboxDeleteDraftInternalServerError) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 500)
	return err
}

// APIError maps MailboxDeleteDraftNotFound into the shared typed API error.
func (r *MailboxDeleteDraftNotFound) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 404)
	return err
}

// APIError maps MailboxDeleteDraftRequestEntityTooLarge into the shared typed API error.
func (r *MailboxDeleteDraftRequestEntityTooLarge) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 413)
	return err
}

// APIError maps MailboxDeleteDraftServiceUnavailable into the shared typed API error.
func (r *MailboxDeleteDraftServiceUnavailable) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 503)
	return err
}

// APIError maps MailboxDeleteDraftTooManyRequests into the shared typed API error.
func (r *MailboxDeleteDraftTooManyRequests) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 429)
	return err
}

// APIError maps MailboxDeleteDraftUnauthorized into the shared typed API error.
func (r *MailboxDeleteDraftUnauthorized) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 401)
	return err
}

// APIError maps MailboxDeleteDraftUnprocessableEntity into the shared typed API error.
func (r *MailboxDeleteDraftUnprocessableEntity) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 422)
	return err
}

// APIError maps MailboxDeleteMessageConflict into the shared typed API error.
func (r *MailboxDeleteMessageConflict) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 409)
	return err
}

// APIError maps MailboxDeleteMessageNotFound into the shared typed API error.
func (r *MailboxDeleteMessageNotFound) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 404)
	return err
}

// APIError maps MailboxDownloadRawMessageForbidden into the shared typed API error.
func (r *MailboxDownloadRawMessageForbidden) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 403)
	return err
}

// APIError maps MailboxDownloadRawMessageInternalServerError into the shared typed API error.
func (r *MailboxDownloadRawMessageInternalServerError) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 500)
	return err
}

// APIError maps MailboxDownloadRawMessageNotFound into the shared typed API error.
func (r *MailboxDownloadRawMessageNotFound) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 404)
	return err
}

// APIError maps MailboxDownloadRawMessageServiceUnavailable into the shared typed API error.
func (r *MailboxDownloadRawMessageServiceUnavailable) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 503)
	return err
}

// APIError maps MailboxDownloadRawMessageTooManyRequests into the shared typed API error.
func (r *MailboxDownloadRawMessageTooManyRequests) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 429)
	return err
}

// APIError maps MailboxDownloadRawMessageUnauthorized into the shared typed API error.
func (r *MailboxDownloadRawMessageUnauthorized) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 401)
	return err
}

// APIError maps MailboxGetAttachmentTextBadRequest into the shared typed API error.
func (r *MailboxGetAttachmentTextBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxGetAttachmentTextForbidden into the shared typed API error.
func (r *MailboxGetAttachmentTextForbidden) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 403)
	return err
}

// APIError maps MailboxGetAttachmentTextInternalServerError into the shared typed API error.
func (r *MailboxGetAttachmentTextInternalServerError) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 500)
	return err
}

// APIError maps MailboxGetAttachmentTextNotFound into the shared typed API error.
func (r *MailboxGetAttachmentTextNotFound) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 404)
	return err
}

// APIError maps MailboxGetAttachmentTextServiceUnavailable into the shared typed API error.
func (r *MailboxGetAttachmentTextServiceUnavailable) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 503)
	return err
}

// APIError maps MailboxGetAttachmentTextTooManyRequests into the shared typed API error.
func (r *MailboxGetAttachmentTextTooManyRequests) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 429)
	return err
}

// APIError maps MailboxGetAttachmentTextUnauthorized into the shared typed API error.
func (r *MailboxGetAttachmentTextUnauthorized) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 401)
	return err
}

// APIError maps MailboxGetCalendarBadRequest into the shared typed API error.
func (r *MailboxGetCalendarBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxGetCalendarConflict into the shared typed API error.
func (r *MailboxGetCalendarConflict) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 409)
	return err
}

// APIError maps MailboxGetCalendarEventBadRequest into the shared typed API error.
func (r *MailboxGetCalendarEventBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxGetCalendarEventChangesBadRequest into the shared typed API error.
func (r *MailboxGetCalendarEventChangesBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxGetCalendarEventChangesConflict into the shared typed API error.
func (r *MailboxGetCalendarEventChangesConflict) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 409)
	return err
}

// APIError maps MailboxGetCalendarEventChangesForbidden into the shared typed API error.
func (r *MailboxGetCalendarEventChangesForbidden) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 403)
	return err
}

// APIError maps MailboxGetCalendarEventChangesInternalServerError into the shared typed API error.
func (r *MailboxGetCalendarEventChangesInternalServerError) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 500)
	return err
}

// APIError maps MailboxGetCalendarEventChangesNotFound into the shared typed API error.
func (r *MailboxGetCalendarEventChangesNotFound) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 404)
	return err
}

// APIError maps MailboxGetCalendarEventChangesRequestEntityTooLarge into the shared typed API error.
func (r *MailboxGetCalendarEventChangesRequestEntityTooLarge) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 413)
	return err
}

// APIError maps MailboxGetCalendarEventChangesServiceUnavailable into the shared typed API error.
func (r *MailboxGetCalendarEventChangesServiceUnavailable) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 503)
	return err
}

// APIError maps MailboxGetCalendarEventChangesTooManyRequests into the shared typed API error.
func (r *MailboxGetCalendarEventChangesTooManyRequests) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 429)
	return err
}

// APIError maps MailboxGetCalendarEventChangesUnauthorized into the shared typed API error.
func (r *MailboxGetCalendarEventChangesUnauthorized) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 401)
	return err
}

// APIError maps MailboxGetCalendarEventChangesUnprocessableEntity into the shared typed API error.
func (r *MailboxGetCalendarEventChangesUnprocessableEntity) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 422)
	return err
}

// APIError maps MailboxGetCalendarEventConflict into the shared typed API error.
func (r *MailboxGetCalendarEventConflict) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 409)
	return err
}

// APIError maps MailboxGetCalendarEventForbidden into the shared typed API error.
func (r *MailboxGetCalendarEventForbidden) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 403)
	return err
}

// APIError maps MailboxGetCalendarEventInternalServerError into the shared typed API error.
func (r *MailboxGetCalendarEventInternalServerError) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 500)
	return err
}

// APIError maps MailboxGetCalendarEventNotFound into the shared typed API error.
func (r *MailboxGetCalendarEventNotFound) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 404)
	return err
}

// APIError maps MailboxGetCalendarEventRequestEntityTooLarge into the shared typed API error.
func (r *MailboxGetCalendarEventRequestEntityTooLarge) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 413)
	return err
}

// APIError maps MailboxGetCalendarEventServiceUnavailable into the shared typed API error.
func (r *MailboxGetCalendarEventServiceUnavailable) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 503)
	return err
}

// APIError maps MailboxGetCalendarEventTooManyRequests into the shared typed API error.
func (r *MailboxGetCalendarEventTooManyRequests) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 429)
	return err
}

// APIError maps MailboxGetCalendarEventUnauthorized into the shared typed API error.
func (r *MailboxGetCalendarEventUnauthorized) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 401)
	return err
}

// APIError maps MailboxGetCalendarEventUnprocessableEntity into the shared typed API error.
func (r *MailboxGetCalendarEventUnprocessableEntity) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 422)
	return err
}

// APIError maps MailboxGetCalendarForbidden into the shared typed API error.
func (r *MailboxGetCalendarForbidden) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 403)
	return err
}

// APIError maps MailboxGetCalendarInternalServerError into the shared typed API error.
func (r *MailboxGetCalendarInternalServerError) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 500)
	return err
}

// APIError maps MailboxGetCalendarNotFound into the shared typed API error.
func (r *MailboxGetCalendarNotFound) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 404)
	return err
}

// APIError maps MailboxGetCalendarRequestEntityTooLarge into the shared typed API error.
func (r *MailboxGetCalendarRequestEntityTooLarge) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 413)
	return err
}

// APIError maps MailboxGetCalendarServiceUnavailable into the shared typed API error.
func (r *MailboxGetCalendarServiceUnavailable) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 503)
	return err
}

// APIError maps MailboxGetCalendarTooManyRequests into the shared typed API error.
func (r *MailboxGetCalendarTooManyRequests) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 429)
	return err
}

// APIError maps MailboxGetCalendarUnauthorized into the shared typed API error.
func (r *MailboxGetCalendarUnauthorized) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 401)
	return err
}

// APIError maps MailboxGetCalendarUnprocessableEntity into the shared typed API error.
func (r *MailboxGetCalendarUnprocessableEntity) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 422)
	return err
}

// APIError maps MailboxGetConnectionForbidden into the shared typed API error.
func (r *MailboxGetConnectionForbidden) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(&r.Response, 403)
	return err
}

// APIError maps MailboxGetConnectionInternalServerError into the shared typed API error.
func (r *MailboxGetConnectionInternalServerError) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(&r.Response, 500)
	return err
}

// APIError maps MailboxGetConnectionServiceUnavailable into the shared typed API error.
func (r *MailboxGetConnectionServiceUnavailable) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(&r.Response, 503)
	return err
}

// APIError maps MailboxGetConnectionTooManyRequests into the shared typed API error.
func (r *MailboxGetConnectionTooManyRequests) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(&r.Response, 429)
	return err
}

// APIError maps MailboxGetConnectionUnauthorized into the shared typed API error.
func (r *MailboxGetConnectionUnauthorized) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(&r.Response, 401)
	return err
}

// APIError maps MailboxGetDraftBadRequest into the shared typed API error.
func (r *MailboxGetDraftBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxGetDraftConflict into the shared typed API error.
func (r *MailboxGetDraftConflict) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 409)
	return err
}

// APIError maps MailboxGetDraftForbidden into the shared typed API error.
func (r *MailboxGetDraftForbidden) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 403)
	return err
}

// APIError maps MailboxGetDraftInternalServerError into the shared typed API error.
func (r *MailboxGetDraftInternalServerError) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 500)
	return err
}

// APIError maps MailboxGetDraftNotFound into the shared typed API error.
func (r *MailboxGetDraftNotFound) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 404)
	return err
}

// APIError maps MailboxGetDraftRequestEntityTooLarge into the shared typed API error.
func (r *MailboxGetDraftRequestEntityTooLarge) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 413)
	return err
}

// APIError maps MailboxGetDraftServiceUnavailable into the shared typed API error.
func (r *MailboxGetDraftServiceUnavailable) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 503)
	return err
}

// APIError maps MailboxGetDraftTooManyRequests into the shared typed API error.
func (r *MailboxGetDraftTooManyRequests) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 429)
	return err
}

// APIError maps MailboxGetDraftUnauthorized into the shared typed API error.
func (r *MailboxGetDraftUnauthorized) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 401)
	return err
}

// APIError maps MailboxGetDraftUnprocessableEntity into the shared typed API error.
func (r *MailboxGetDraftUnprocessableEntity) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 422)
	return err
}

// APIError maps MailboxGetIdentityForbidden into the shared typed API error.
func (r *MailboxGetIdentityForbidden) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 403)
	return err
}

// APIError maps MailboxGetIdentityServiceUnavailable into the shared typed API error.
func (r *MailboxGetIdentityServiceUnavailable) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 503)
	return err
}

// APIError maps MailboxGetIdentityUnauthorized into the shared typed API error.
func (r *MailboxGetIdentityUnauthorized) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 401)
	return err
}

// APIError maps MailboxGetMeForbidden into the shared typed API error.
func (r *MailboxGetMeForbidden) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 403)
	return err
}

// APIError maps MailboxGetMeNotFound into the shared typed API error.
func (r *MailboxGetMeNotFound) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 404)
	return err
}

// APIError maps MailboxGetMeUnauthorized into the shared typed API error.
func (r *MailboxGetMeUnauthorized) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 401)
	return err
}

// APIError maps MailboxGetMessageAttachmentBadRequest into the shared typed API error.
func (r *MailboxGetMessageAttachmentBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxGetMessageAttachmentNotFound into the shared typed API error.
func (r *MailboxGetMessageAttachmentNotFound) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 404)
	return err
}

// APIError maps MailboxGetSenderChoicesBadRequest into the shared typed API error.
func (r *MailboxGetSenderChoicesBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxGetSenderChoicesForbidden into the shared typed API error.
func (r *MailboxGetSenderChoicesForbidden) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 403)
	return err
}

// APIError maps MailboxGetSenderChoicesInternalServerError into the shared typed API error.
func (r *MailboxGetSenderChoicesInternalServerError) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 500)
	return err
}

// APIError maps MailboxGetSenderChoicesNotFound into the shared typed API error.
func (r *MailboxGetSenderChoicesNotFound) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 404)
	return err
}

// APIError maps MailboxGetSenderChoicesServiceUnavailable into the shared typed API error.
func (r *MailboxGetSenderChoicesServiceUnavailable) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 503)
	return err
}

// APIError maps MailboxGetSenderChoicesTooManyRequests into the shared typed API error.
func (r *MailboxGetSenderChoicesTooManyRequests) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 429)
	return err
}

// APIError maps MailboxGetSenderChoicesUnauthorized into the shared typed API error.
func (r *MailboxGetSenderChoicesUnauthorized) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 401)
	return err
}

// APIError maps MailboxGetSessionForbidden into the shared typed API error.
func (r *MailboxGetSessionForbidden) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 403)
	return err
}

// APIError maps MailboxGetSessionServiceUnavailable into the shared typed API error.
func (r *MailboxGetSessionServiceUnavailable) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 503)
	return err
}

// APIError maps MailboxGetSessionUnauthorized into the shared typed API error.
func (r *MailboxGetSessionUnauthorized) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 401)
	return err
}

// APIError maps MailboxGetThreadContentBadRequest into the shared typed API error.
func (r *MailboxGetThreadContentBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxGetThreadContentNotFound into the shared typed API error.
func (r *MailboxGetThreadContentNotFound) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 404)
	return err
}

// APIError maps MailboxListBodyBadRequest into the shared typed API error.
func (r *MailboxListBodyBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxListBodyNotFound into the shared typed API error.
func (r *MailboxListBodyNotFound) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 404)
	return err
}

// APIError maps MailboxListCalendarEventsBadRequest into the shared typed API error.
func (r *MailboxListCalendarEventsBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxListCalendarEventsConflict into the shared typed API error.
func (r *MailboxListCalendarEventsConflict) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 409)
	return err
}

// APIError maps MailboxListCalendarEventsForbidden into the shared typed API error.
func (r *MailboxListCalendarEventsForbidden) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 403)
	return err
}

// APIError maps MailboxListCalendarEventsInternalServerError into the shared typed API error.
func (r *MailboxListCalendarEventsInternalServerError) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 500)
	return err
}

// APIError maps MailboxListCalendarEventsNotFound into the shared typed API error.
func (r *MailboxListCalendarEventsNotFound) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 404)
	return err
}

// APIError maps MailboxListCalendarEventsRequestEntityTooLarge into the shared typed API error.
func (r *MailboxListCalendarEventsRequestEntityTooLarge) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 413)
	return err
}

// APIError maps MailboxListCalendarEventsServiceUnavailable into the shared typed API error.
func (r *MailboxListCalendarEventsServiceUnavailable) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 503)
	return err
}

// APIError maps MailboxListCalendarEventsTooManyRequests into the shared typed API error.
func (r *MailboxListCalendarEventsTooManyRequests) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 429)
	return err
}

// APIError maps MailboxListCalendarEventsUnauthorized into the shared typed API error.
func (r *MailboxListCalendarEventsUnauthorized) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 401)
	return err
}

// APIError maps MailboxListCalendarEventsUnprocessableEntity into the shared typed API error.
func (r *MailboxListCalendarEventsUnprocessableEntity) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 422)
	return err
}

// APIError maps MailboxListCalendarsBadRequest into the shared typed API error.
func (r *MailboxListCalendarsBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxListCalendarsConflict into the shared typed API error.
func (r *MailboxListCalendarsConflict) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 409)
	return err
}

// APIError maps MailboxListCalendarsForbidden into the shared typed API error.
func (r *MailboxListCalendarsForbidden) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 403)
	return err
}

// APIError maps MailboxListCalendarsInternalServerError into the shared typed API error.
func (r *MailboxListCalendarsInternalServerError) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 500)
	return err
}

// APIError maps MailboxListCalendarsNotFound into the shared typed API error.
func (r *MailboxListCalendarsNotFound) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 404)
	return err
}

// APIError maps MailboxListCalendarsRequestEntityTooLarge into the shared typed API error.
func (r *MailboxListCalendarsRequestEntityTooLarge) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 413)
	return err
}

// APIError maps MailboxListCalendarsServiceUnavailable into the shared typed API error.
func (r *MailboxListCalendarsServiceUnavailable) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 503)
	return err
}

// APIError maps MailboxListCalendarsTooManyRequests into the shared typed API error.
func (r *MailboxListCalendarsTooManyRequests) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 429)
	return err
}

// APIError maps MailboxListCalendarsUnauthorized into the shared typed API error.
func (r *MailboxListCalendarsUnauthorized) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 401)
	return err
}

// APIError maps MailboxListCalendarsUnprocessableEntity into the shared typed API error.
func (r *MailboxListCalendarsUnprocessableEntity) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 422)
	return err
}

// APIError maps MailboxListContentBadRequest into the shared typed API error.
func (r *MailboxListContentBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxListContentNotFound into the shared typed API error.
func (r *MailboxListContentNotFound) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 404)
	return err
}

// APIError maps MailboxListDraftsBadRequest into the shared typed API error.
func (r *MailboxListDraftsBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxListDraftsConflict into the shared typed API error.
func (r *MailboxListDraftsConflict) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 409)
	return err
}

// APIError maps MailboxListDraftsForbidden into the shared typed API error.
func (r *MailboxListDraftsForbidden) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 403)
	return err
}

// APIError maps MailboxListDraftsInternalServerError into the shared typed API error.
func (r *MailboxListDraftsInternalServerError) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 500)
	return err
}

// APIError maps MailboxListDraftsNotFound into the shared typed API error.
func (r *MailboxListDraftsNotFound) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 404)
	return err
}

// APIError maps MailboxListDraftsRequestEntityTooLarge into the shared typed API error.
func (r *MailboxListDraftsRequestEntityTooLarge) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 413)
	return err
}

// APIError maps MailboxListDraftsServiceUnavailable into the shared typed API error.
func (r *MailboxListDraftsServiceUnavailable) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 503)
	return err
}

// APIError maps MailboxListDraftsTooManyRequests into the shared typed API error.
func (r *MailboxListDraftsTooManyRequests) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 429)
	return err
}

// APIError maps MailboxListDraftsUnauthorized into the shared typed API error.
func (r *MailboxListDraftsUnauthorized) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 401)
	return err
}

// APIError maps MailboxListDraftsUnprocessableEntity into the shared typed API error.
func (r *MailboxListDraftsUnprocessableEntity) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 422)
	return err
}

// APIError maps MailboxListGrantedMailboxesForbidden into the shared typed API error.
func (r *MailboxListGrantedMailboxesForbidden) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 403)
	return err
}

// APIError maps MailboxListGrantedMailboxesUnauthorized into the shared typed API error.
func (r *MailboxListGrantedMailboxesUnauthorized) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 401)
	return err
}

// APIError maps MailboxListIdentitiesBadRequest into the shared typed API error.
func (r *MailboxListIdentitiesBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxListIdentitiesForbidden into the shared typed API error.
func (r *MailboxListIdentitiesForbidden) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 403)
	return err
}

// APIError maps MailboxListIdentitiesUnauthorized into the shared typed API error.
func (r *MailboxListIdentitiesUnauthorized) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 401)
	return err
}

// APIError maps MailboxListMessagesBadRequest into the shared typed API error.
func (r *MailboxListMessagesBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxListMessagesForbidden into the shared typed API error.
func (r *MailboxListMessagesForbidden) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 403)
	return err
}

// APIError maps MailboxListMessagesUnauthorized into the shared typed API error.
func (r *MailboxListMessagesUnauthorized) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 401)
	return err
}

// APIError maps MailboxListThreadMessagesBadRequest into the shared typed API error.
func (r *MailboxListThreadMessagesBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxListThreadMessagesNotFound into the shared typed API error.
func (r *MailboxListThreadMessagesNotFound) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 404)
	return err
}

// APIError maps MailboxListThreadsBadRequest into the shared typed API error.
func (r *MailboxListThreadsBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxListThreadsForbidden into the shared typed API error.
func (r *MailboxListThreadsForbidden) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 403)
	return err
}

// APIError maps MailboxListThreadsUnauthorized into the shared typed API error.
func (r *MailboxListThreadsUnauthorized) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 401)
	return err
}

// APIError maps MailboxRequestAttachmentTextBadRequest into the shared typed API error.
func (r *MailboxRequestAttachmentTextBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxRequestAttachmentTextForbidden into the shared typed API error.
func (r *MailboxRequestAttachmentTextForbidden) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 403)
	return err
}

// APIError maps MailboxRequestAttachmentTextInternalServerError into the shared typed API error.
func (r *MailboxRequestAttachmentTextInternalServerError) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 500)
	return err
}

// APIError maps MailboxRequestAttachmentTextNotFound into the shared typed API error.
func (r *MailboxRequestAttachmentTextNotFound) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 404)
	return err
}

// APIError maps MailboxRequestAttachmentTextServiceUnavailable into the shared typed API error.
func (r *MailboxRequestAttachmentTextServiceUnavailable) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 503)
	return err
}

// APIError maps MailboxRequestAttachmentTextTooManyRequests into the shared typed API error.
func (r *MailboxRequestAttachmentTextTooManyRequests) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 429)
	return err
}

// APIError maps MailboxRequestAttachmentTextUnauthorized into the shared typed API error.
func (r *MailboxRequestAttachmentTextUnauthorized) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 401)
	return err
}

// APIError maps MailboxSendDraftBadRequest into the shared typed API error.
func (r *MailboxSendDraftBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxSendDraftConflict into the shared typed API error.
func (r *MailboxSendDraftConflict) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 409)
	return err
}

// APIError maps MailboxSendDraftForbidden into the shared typed API error.
func (r *MailboxSendDraftForbidden) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 403)
	return err
}

// APIError maps MailboxSendDraftInternalServerError into the shared typed API error.
func (r *MailboxSendDraftInternalServerError) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 500)
	return err
}

// APIError maps MailboxSendDraftNotFound into the shared typed API error.
func (r *MailboxSendDraftNotFound) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 404)
	return err
}

// APIError maps MailboxSendDraftRequestEntityTooLarge into the shared typed API error.
func (r *MailboxSendDraftRequestEntityTooLarge) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 413)
	return err
}

// APIError maps MailboxSendDraftServiceUnavailable into the shared typed API error.
func (r *MailboxSendDraftServiceUnavailable) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 503)
	return err
}

// APIError maps MailboxSendDraftTooManyRequests into the shared typed API error.
func (r *MailboxSendDraftTooManyRequests) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 429)
	return err
}

// APIError maps MailboxSendDraftUnauthorized into the shared typed API error.
func (r *MailboxSendDraftUnauthorized) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 401)
	return err
}

// APIError maps MailboxSendDraftUnprocessableEntity into the shared typed API error.
func (r *MailboxSendDraftUnprocessableEntity) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 422)
	return err
}

// APIError maps MailboxSendMessageBadRequest into the shared typed API error.
func (r *MailboxSendMessageBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxSendMessageConflict into the shared typed API error.
func (r *MailboxSendMessageConflict) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 409)
	return err
}

// APIError maps MailboxSendMessageRequestEntityTooLarge into the shared typed API error.
func (r *MailboxSendMessageRequestEntityTooLarge) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 413)
	return err
}

// APIError maps MailboxSendMessageServiceUnavailable into the shared typed API error.
func (r *MailboxSendMessageServiceUnavailable) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 503)
	return err
}

// APIError maps MailboxSendMessageUnprocessableEntity into the shared typed API error.
func (r *MailboxSendMessageUnprocessableEntity) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 422)
	return err
}

// APIError maps MailboxStreamEventsBadRequest into the shared typed API error.
func (r *MailboxStreamEventsBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxStreamEventsForbidden into the shared typed API error.
func (r *MailboxStreamEventsForbidden) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 403)
	return err
}

// APIError maps MailboxStreamEventsServiceUnavailable into the shared typed API error.
func (r *MailboxStreamEventsServiceUnavailable) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 503)
	return err
}

// APIError maps MailboxStreamEventsTooManyRequests into the shared typed API error.
func (r *MailboxStreamEventsTooManyRequests) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 429)
	return err
}

// APIError maps MailboxStreamEventsUnauthorized into the shared typed API error.
func (r *MailboxStreamEventsUnauthorized) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 401)
	return err
}

// APIError maps MailboxUpdateCalendarEventBadRequest into the shared typed API error.
func (r *MailboxUpdateCalendarEventBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxUpdateCalendarEventConflict into the shared typed API error.
func (r *MailboxUpdateCalendarEventConflict) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 409)
	return err
}

// APIError maps MailboxUpdateCalendarEventForbidden into the shared typed API error.
func (r *MailboxUpdateCalendarEventForbidden) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 403)
	return err
}

// APIError maps MailboxUpdateCalendarEventInternalServerError into the shared typed API error.
func (r *MailboxUpdateCalendarEventInternalServerError) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 500)
	return err
}

// APIError maps MailboxUpdateCalendarEventNotFound into the shared typed API error.
func (r *MailboxUpdateCalendarEventNotFound) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 404)
	return err
}

// APIError maps MailboxUpdateCalendarEventRequestEntityTooLarge into the shared typed API error.
func (r *MailboxUpdateCalendarEventRequestEntityTooLarge) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 413)
	return err
}

// APIError maps MailboxUpdateCalendarEventServiceUnavailable into the shared typed API error.
func (r *MailboxUpdateCalendarEventServiceUnavailable) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 503)
	return err
}

// APIError maps MailboxUpdateCalendarEventTooManyRequests into the shared typed API error.
func (r *MailboxUpdateCalendarEventTooManyRequests) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 429)
	return err
}

// APIError maps MailboxUpdateCalendarEventUnauthorized into the shared typed API error.
func (r *MailboxUpdateCalendarEventUnauthorized) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 401)
	return err
}

// APIError maps MailboxUpdateCalendarEventUnprocessableEntity into the shared typed API error.
func (r *MailboxUpdateCalendarEventUnprocessableEntity) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 422)
	return err
}

// APIError maps MailboxUpdateDraftBadRequest into the shared typed API error.
func (r *MailboxUpdateDraftBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxUpdateDraftConflict into the shared typed API error.
func (r *MailboxUpdateDraftConflict) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 409)
	return err
}

// APIError maps MailboxUpdateDraftForbidden into the shared typed API error.
func (r *MailboxUpdateDraftForbidden) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 403)
	return err
}

// APIError maps MailboxUpdateDraftInternalServerError into the shared typed API error.
func (r *MailboxUpdateDraftInternalServerError) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 500)
	return err
}

// APIError maps MailboxUpdateDraftNotFound into the shared typed API error.
func (r *MailboxUpdateDraftNotFound) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 404)
	return err
}

// APIError maps MailboxUpdateDraftRequestEntityTooLarge into the shared typed API error.
func (r *MailboxUpdateDraftRequestEntityTooLarge) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 413)
	return err
}

// APIError maps MailboxUpdateDraftServiceUnavailable into the shared typed API error.
func (r *MailboxUpdateDraftServiceUnavailable) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 503)
	return err
}

// APIError maps MailboxUpdateDraftTooManyRequests into the shared typed API error.
func (r *MailboxUpdateDraftTooManyRequests) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 429)
	return err
}

// APIError maps MailboxUpdateDraftUnauthorized into the shared typed API error.
func (r *MailboxUpdateDraftUnauthorized) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 401)
	return err
}

// APIError maps MailboxUpdateDraftUnprocessableEntity into the shared typed API error.
func (r *MailboxUpdateDraftUnprocessableEntity) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 422)
	return err
}

// APIError maps MailboxUpdateFolderBadRequest into the shared typed API error.
func (r *MailboxUpdateFolderBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxUpdateFolderConflict into the shared typed API error.
func (r *MailboxUpdateFolderConflict) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 409)
	return err
}

// APIError maps MailboxUpdateFolderNotFound into the shared typed API error.
func (r *MailboxUpdateFolderNotFound) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 404)
	return err
}

// APIError maps MailboxUpdateFolderRequestEntityTooLarge into the shared typed API error.
func (r *MailboxUpdateFolderRequestEntityTooLarge) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 413)
	return err
}

// APIError maps MailboxUpdateIdentityBadRequest into the shared typed API error.
func (r *MailboxUpdateIdentityBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxUpdateIdentityForbidden into the shared typed API error.
func (r *MailboxUpdateIdentityForbidden) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 403)
	return err
}

// APIError maps MailboxUpdateIdentityRequestEntityTooLarge into the shared typed API error.
func (r *MailboxUpdateIdentityRequestEntityTooLarge) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 413)
	return err
}

// APIError maps MailboxUpdateIdentityServiceUnavailable into the shared typed API error.
func (r *MailboxUpdateIdentityServiceUnavailable) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 503)
	return err
}

// APIError maps MailboxUpdateIdentityUnauthorized into the shared typed API error.
func (r *MailboxUpdateIdentityUnauthorized) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 401)
	return err
}

// APIError maps MailboxUpdateIdentityUnprocessableEntity into the shared typed API error.
func (r *MailboxUpdateIdentityUnprocessableEntity) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 422)
	return err
}

// APIError maps MailboxUpdateMessageBadRequest into the shared typed API error.
func (r *MailboxUpdateMessageBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxUpdateMessageConflict into the shared typed API error.
func (r *MailboxUpdateMessageConflict) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 409)
	return err
}

// APIError maps MailboxUpdateMessageNotFound into the shared typed API error.
func (r *MailboxUpdateMessageNotFound) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 404)
	return err
}

// APIError maps MailboxUpdateMessageRequestEntityTooLarge into the shared typed API error.
func (r *MailboxUpdateMessageRequestEntityTooLarge) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 413)
	return err
}

// APIError maps MailboxUploadAttachmentBadRequest into the shared typed API error.
func (r *MailboxUploadAttachmentBadRequest) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 400)
	return err
}

// APIError maps MailboxUploadAttachmentRequestEntityTooLarge into the shared typed API error.
func (r *MailboxUploadAttachmentRequestEntityTooLarge) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 413)
	return err
}

// APIError maps MailboxUploadAttachmentServiceUnavailable into the shared typed API error.
func (r *MailboxUploadAttachmentServiceUnavailable) APIError() *core.APIError {
	err, _ := core.APIErrorFromResponse(r, 503)
	return err
}
