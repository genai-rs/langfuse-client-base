//! Mocked-HTTP smoke tests: no network needed, requests go to a local wiremock server.

use langfuse_client_base::apis::{
    configuration::Configuration, projects_api, scores_api, trace_api, Error,
};
use langfuse_client_base::models;
use serde_json::json;
use wiremock::matchers::{header, method, path, query_param};
use wiremock::{Mock, MockServer, Request, ResponseTemplate};

const USER_AGENT: &str = "langfuse-client-base-smoke/1.0";
// base64("pk-lf-test:sk-lf-test")
const BASIC: &str = "Basic cGstbGYtdGVzdDpzay1sZi10ZXN0";

fn config(server: &MockServer) -> Configuration {
    Configuration {
        base_path: server.uri(),
        user_agent: Some(USER_AGENT.to_owned()),
        basic_auth: Some(("pk-lf-test".to_owned(), Some("sk-lf-test".to_owned()))),
        ..Configuration::default()
    }
}

#[tokio::test]
async fn projects_get_sends_auth_and_user_agent_and_parses_body() {
    let server = MockServer::start().await;
    Mock::given(method("GET"))
        .and(path("/api/public/projects"))
        .and(header("authorization", BASIC))
        .and(header("user-agent", USER_AGENT))
        .respond_with(ResponseTemplate::new(200).set_body_json(json!({
            "data": [{
                "id": "proj-1",
                "name": "My Project",
                "organization": {"id": "org-1", "name": "My Org"},
                "metadata": {"k": "v"},
                "retentionDays": 30
            }]
        })))
        .expect(1)
        .mount(&server)
        .await;

    let projects = projects_api::projects_get()
        .configuration(&config(&server))
        .call()
        .await
        .expect("200 response should deserialise");

    assert_eq!(projects.data.len(), 1);
    let project = &projects.data[0];
    assert_eq!(project.id, "proj-1");
    assert_eq!(project.name, "My Project");
    assert_eq!(project.organization.name, "My Org");
    assert_eq!(project.metadata["k"], json!("v"));
    assert_eq!(project.retention_days, Some(Some(30)));
}

#[tokio::test]
async fn projects_get_401_yields_response_error_with_entity() {
    let server = MockServer::start().await;
    Mock::given(method("GET"))
        .and(path("/api/public/projects"))
        .respond_with(ResponseTemplate::new(401).set_body_json(json!({"message": "Unauthorized"})))
        .mount(&server)
        .await;

    let err = projects_api::projects_get()
        .configuration(&config(&server))
        .call()
        .await
        .expect_err("401 must be an error");

    match err {
        Error::ResponseError(resp) => {
            assert_eq!(resp.status.as_u16(), 401);
            assert!(resp.content.contains("Unauthorized"));
            // The error enum is `#[serde(untagged)]` over `serde_json::Value`, so the
            // variant is always the first one; only the payload is meaningful.
            let entity = resp.entity.expect("spec defines an error entity");
            let payload = match entity {
                projects_api::ProjectsGetError::Status400(v)
                | projects_api::ProjectsGetError::Status401(v) => v,
                other => panic!("unexpected entity: {other:?}"),
            };
            assert_eq!(payload, json!({"message": "Unauthorized"}));
        }
        other => panic!("expected ResponseError, got {other:?}"),
    }
}

#[tokio::test]
#[allow(deprecated)]
async fn trace_list_encodes_query_parameters_exactly() {
    let server = MockServer::start().await;
    Mock::given(method("GET"))
        .and(path("/api/public/traces"))
        .and(header("authorization", BASIC))
        .and(header("user-agent", USER_AGENT))
        .and(query_param("name", "my trace & more"))
        .respond_with(ResponseTemplate::new(200).set_body_json(json!({
            "data": [],
            "meta": {"page": 2, "limit": 10, "totalItems": 0, "totalPages": 0}
        })))
        .expect(1)
        .mount(&server)
        .await;

    let traces = trace_api::trace_list()
        .configuration(&config(&server))
        .page(2)
        .limit(10)
        .name("my trace & more")
        .tags(vec!["a b".to_owned(), "c,d".to_owned()])
        .environment(vec!["prod".to_owned(), "staging".to_owned()])
        .call()
        .await
        .expect("200 response should deserialise");

    assert!(traces.data.is_empty());
    assert_eq!(traces.meta.page, 2);
    assert_eq!(traces.meta.limit, 10);

    // Array parameters use the `multi` style: one repeated key per item, in order.
    let received: Vec<Request> = server.received_requests().await.unwrap();
    assert_eq!(received.len(), 1);
    assert_eq!(
        received[0].url.query(),
        Some(
            "page=2&limit=10&name=my+trace+%26+more&tags=a+b&tags=c%2Cd\
             &environment=prod&environment=staging"
        )
    );
}

#[tokio::test]
async fn scores_create_posts_json_and_parses_response() {
    let server = MockServer::start().await;
    Mock::given(method("POST"))
        .and(path("/api/public/scores"))
        .and(header("authorization", BASIC))
        .and(header("user-agent", USER_AGENT))
        .and(wiremock::matchers::body_json(json!({
            "traceId": "trace-1",
            "name": "quality",
            "value": 0.5
        })))
        .respond_with(ResponseTemplate::new(200).set_body_json(json!({"id": "score-1"})))
        .expect(1)
        .mount(&server)
        .await;

    let mut request = models::CreateScoreRequest::new(
        "quality".to_owned(),
        models::CreateScoreValue::DoubleNumber(0.5),
    );
    request.trace_id = Some(Some("trace-1".to_owned()));

    let response = scores_api::scores_create()
        .configuration(&config(&server))
        .create_scores_request(models::CreateScoresRequest::CreateScoreRequest(Box::new(
            request,
        )))
        .call()
        .await
        .expect("200 response should deserialise");

    match response {
        models::CreateScoresResponse::CreateScoreResponse(r) => assert_eq!(r.id, "score-1"),
        other => panic!("unexpected variant: {other:?}"),
    }
}

#[tokio::test]
async fn scores_create_400_yields_response_error_with_entity() {
    let server = MockServer::start().await;
    Mock::given(method("POST"))
        .and(path("/api/public/scores"))
        .respond_with(ResponseTemplate::new(400).set_body_json(json!({"error": "bad score"})))
        .mount(&server)
        .await;

    let request = models::CreateScoreRequest::new(
        "quality".to_owned(),
        models::CreateScoreValue::String("good".to_owned()),
    );
    let err = scores_api::scores_create()
        .configuration(&config(&server))
        .create_scores_request(models::CreateScoresRequest::CreateScoreRequest(Box::new(
            request,
        )))
        .call()
        .await
        .expect_err("400 must be an error");

    match err {
        Error::ResponseError(resp) => {
            assert_eq!(resp.status.as_u16(), 400);
            assert_eq!(resp.content, r#"{"error":"bad score"}"#);
            assert!(matches!(
                resp.entity,
                Some(scores_api::ScoresCreateError::Status400(_))
            ));
        }
        other => panic!("expected ResponseError, got {other:?}"),
    }
}
