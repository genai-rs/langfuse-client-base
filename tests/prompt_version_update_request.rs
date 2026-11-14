//! `PromptVersionUpdateRequest` sends only the label lists that are set (0.25 migration note).
use langfuse_client_base::models::PromptVersionUpdateRequest;

#[test]
fn only_set_label_lists_are_sent() {
    let add = PromptVersionUpdateRequest::builder()
        .new_labels(Some(vec!["production".to_string()]))
        .build();
    assert_eq!(
        serde_json::to_value(&add).unwrap(),
        serde_json::json!({ "newLabels": ["production"] })
    );

    let remove = PromptVersionUpdateRequest {
        remove_labels: Some(Some(vec!["staging".to_string()])),
        ..Default::default()
    };
    assert_eq!(
        serde_json::to_value(&remove).unwrap(),
        serde_json::json!({ "removeLabels": ["staging"] })
    );

    let clear = PromptVersionUpdateRequest {
        new_labels: Some(None),
        ..Default::default()
    };
    assert_eq!(
        serde_json::to_value(&clear).unwrap(),
        serde_json::json!({ "newLabels": null })
    );
}
