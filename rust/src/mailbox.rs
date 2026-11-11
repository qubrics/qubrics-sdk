use crate::core::{
    encode_path_segment, ApiKeySurface, Connection, RequestOptions, Response, Result, Transport,
};
use reqwest::Client;
use serde::Serialize;

pub const DEFAULT_BASE_URL: &str = "https://app.sendmux.ai/api/v1";

/// Async Sendmux Mailbox API client.
#[derive(Clone)]
pub struct MailboxClient {
    transport: Transport,
}

impl MailboxClient {
    pub fn new(api_key: impl Into<String>) -> Result<Self> {
        Ok(Self {
            transport: Transport::new(api_key, ApiKeySurface::Mailbox, DEFAULT_BASE_URL)?,
        })
    }

    /// Creates a client using an OAuth access token instead of an API key.
    pub fn new_with_access_token(token: impl Into<String>) -> Result<Self> {
        Ok(Self {
            transport: Transport::new_with_access_token(token, DEFAULT_BASE_URL)?,
        })
    }

    /// Resolves an async token provider for each request, including requests from cloned clients.
    pub fn new_with_token_provider<F, Fut>(provider: F) -> Result<Self>
    where
        F: Fn() -> Fut + Send + Sync + 'static,
        Fut: std::future::Future<Output = Result<String>> + Send + 'static,
    {
        Ok(Self {
            transport: Transport::new_with_token_provider(provider, DEFAULT_BASE_URL)?,
        })
    }

    pub fn with_base_url(mut self, base_url: impl AsRef<str>) -> Result<Self> {
        self.transport = self.transport.with_base_url(base_url)?;
        Ok(self)
    }

    pub fn with_http_client(mut self, client: Client) -> Self {
        self.transport = self.transport.with_http_client(client);
        self
    }

    pub fn with_user_agent(mut self, user_agent: impl AsRef<str>) -> Result<Self> {
        self.transport = self.transport.with_user_agent(user_agent)?;
        Ok(self)
    }

    pub async fn get_connection(&self) -> Result<Response<Connection>> {
        self.transport.get_json("/mailbox/connection").await
    }

    pub async fn get_me(&self) -> Result<Response<serde_json::Value>> {
        self.raw_get("/mailbox/me").await
    }

    pub async fn list_folders(&self) -> Result<Response<serde_json::Value>> {
        self.list_folders_with_cursor(None).await
    }

    /// Lists a page using the preceding response's next_cursor, or the first page with None.
    pub async fn list_folders_with_cursor(
        &self,
        cursor: Option<&str>,
    ) -> Result<Response<serde_json::Value>> {
        self.transport.get_page("/mailbox/folders", cursor).await
    }

    pub async fn list_messages(&self) -> Result<Response<serde_json::Value>> {
        self.list_messages_with_cursor(None).await
    }

    /// Lists a page using the preceding response's next_cursor, or the first page with None.
    pub async fn list_messages_with_cursor(
        &self,
        cursor: Option<&str>,
    ) -> Result<Response<serde_json::Value>> {
        self.transport.get_page("/mailbox/messages", cursor).await
    }

    pub async fn get_message(&self, message_id: &str) -> Result<Response<serde_json::Value>> {
        self.raw_get(&message_path(message_id)).await
    }

    pub async fn send_message<B>(&self, body: &B) -> Result<Response<serde_json::Value>>
    where
        B: Serialize + ?Sized,
    {
        self.raw_post("/mailbox/messages/send", body, &RequestOptions::default())
            .await
    }

    pub async fn list_calendars(&self) -> Result<Response<serde_json::Value>> {
        self.list_calendars_with_cursor(None).await
    }

    pub async fn list_calendars_with_cursor(
        &self,
        cursor: Option<&str>,
    ) -> Result<Response<serde_json::Value>> {
        self.transport.get_page("/mailbox/calendars", cursor).await
    }

    pub async fn create_calendar<B>(
        &self,
        body: &B,
        options: &RequestOptions,
    ) -> Result<Response<serde_json::Value>>
    where
        B: Serialize + ?Sized,
    {
        self.raw_post("/mailbox/calendars", body, options).await
    }

    pub async fn get_calendar(&self, calendar_id: &str) -> Result<Response<serde_json::Value>> {
        self.raw_get(&calendar_path(calendar_id)).await
    }

    pub async fn delete_calendar(
        &self,
        calendar_id: &str,
        options: &RequestOptions,
    ) -> Result<Response<serde_json::Value>> {
        self.transport
            .delete_json_with_options(&calendar_path(calendar_id), options)
            .await
    }

    pub async fn list_calendar_events(&self) -> Result<Response<serde_json::Value>> {
        self.list_calendar_events_with_cursor(None).await
    }

    pub async fn list_calendar_events_with_cursor(
        &self,
        cursor: Option<&str>,
    ) -> Result<Response<serde_json::Value>> {
        self.transport
            .get_page("/mailbox/calendar-events", cursor)
            .await
    }

    pub async fn create_calendar_event<B>(
        &self,
        body: &B,
        options: &RequestOptions,
    ) -> Result<Response<serde_json::Value>>
    where
        B: Serialize + ?Sized,
    {
        self.raw_post("/mailbox/calendar-events", body, options)
            .await
    }

    pub async fn get_calendar_event(&self, event_id: &str) -> Result<Response<serde_json::Value>> {
        self.raw_get(&calendar_event_path(event_id)).await
    }

    pub async fn update_calendar_event<B>(
        &self,
        event_id: &str,
        body: &B,
        options: &RequestOptions,
    ) -> Result<Response<serde_json::Value>>
    where
        B: Serialize + ?Sized,
    {
        self.raw_patch(&calendar_event_path(event_id), body, options)
            .await
    }

    pub async fn delete_calendar_event(
        &self,
        event_id: &str,
        options: &RequestOptions,
    ) -> Result<Response<serde_json::Value>> {
        self.transport
            .delete_json_with_options(&calendar_event_path(event_id), options)
            .await
    }

    pub async fn get_calendar_event_changes(
        &self,
        since_state: Option<&str>,
    ) -> Result<Response<serde_json::Value>> {
        self.raw_get(&calendar_event_changes_path(since_state))
            .await
    }

    pub async fn raw_get(&self, path: &str) -> Result<Response<serde_json::Value>> {
        self.transport.get_json(path).await
    }

    pub async fn raw_post<B>(
        &self,
        path: &str,
        body: &B,
        options: &RequestOptions,
    ) -> Result<Response<serde_json::Value>>
    where
        B: Serialize + ?Sized,
    {
        self.transport.post_json(path, body, Some(options)).await
    }

    pub async fn raw_patch<B>(
        &self,
        path: &str,
        body: &B,
        options: &RequestOptions,
    ) -> Result<Response<serde_json::Value>>
    where
        B: Serialize + ?Sized,
    {
        self.transport.patch_json(path, body, Some(options)).await
    }

    pub async fn raw_put<B>(
        &self,
        path: &str,
        body: &B,
        options: &RequestOptions,
    ) -> Result<Response<serde_json::Value>>
    where
        B: Serialize + ?Sized,
    {
        self.transport.put_json(path, body, Some(options)).await
    }

    pub async fn raw_delete(&self, path: &str) -> Result<Response<serde_json::Value>> {
        self.transport.delete_json(path).await
    }
}

fn message_path(message_id: &str) -> String {
    format!("/mailbox/messages/{}", encode_path_segment(message_id))
}

fn calendar_path(calendar_id: &str) -> String {
    format!("/mailbox/calendars/{}", encode_path_segment(calendar_id))
}

fn calendar_event_path(event_id: &str) -> String {
    format!("/mailbox/calendar-events/{}", encode_path_segment(event_id))
}

fn calendar_event_changes_path(since_state: Option<&str>) -> String {
    match since_state {
        Some(since_state) => format!(
            "/mailbox/calendar-events/changes?{}",
            url::form_urlencoded::Serializer::new(String::new())
                .append_pair("since_state", since_state)
                .finish()
        ),
        None => "/mailbox/calendar-events/changes".to_owned(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn message_path_encodes_message_id_as_one_segment() {
        assert_eq!(
            message_path("folder/a?b=1"),
            "/mailbox/messages/folder%2Fa%3Fb%3D1"
        );
    }
}
