//! A required, nullable property reads a missing key as `None` (timvw-rust 0.39.0):
//! lenient on input, strict on output (`None` is still written as `null`). A required
//! property that cannot be null still has to be present.
use langfuse_client_base::models::{Observation, ObservationLevel};
use serde_json::{json, Value};

/// An observation with only its required, non-nullable fields.
fn minimal_observation() -> Value {
    json!({
        "id": "obs-1",
        "type": "GENERATION",
        "startTime": "2026-11-19T08:00:00Z",
        "usage": { "input": 1, "output": 2, "total": 3 },
        "level": "DEFAULT",
        "usageDetails": { "input": 1 },
        "costDetails": {},
        "environment": "default"
    })
}

#[test]
fn missing_required_nullable_fields_decode_as_none() {
    let observation: Observation = serde_json::from_value(minimal_observation()).unwrap();
    assert_eq!(observation.id, "obs-1");
    assert_eq!(observation.level, ObservationLevel::Default);
    assert_eq!(observation.trace_id, None);
    assert_eq!(observation.name, None);
    assert_eq!(observation.end_time, None);
    assert_eq!(observation.completion_start_time, None);
    assert_eq!(observation.model, None);
    assert_eq!(observation.input, None);
    assert_eq!(observation.output, None);
    assert_eq!(observation.parent_observation_id, None);
    assert_eq!(observation.prompt_id, None);
}

#[test]
fn explicit_null_and_values_still_decode() {
    let mut body = minimal_observation();
    body["traceId"] = Value::Null;
    body["parentObservationId"] = json!("obs-0");
    body["endTime"] = json!("2026-11-19T08:00:01Z");
    let observation: Observation = serde_json::from_value(body).unwrap();
    assert_eq!(observation.trace_id, None);
    assert_eq!(observation.parent_observation_id.as_deref(), Some("obs-0"));
    assert_eq!(
        observation.end_time,
        Some("2026-11-19T08:00:01Z".parse().unwrap())
    );
}

#[test]
fn none_is_still_written_as_null() {
    let observation: Observation = serde_json::from_value(minimal_observation()).unwrap();
    let written = serde_json::to_value(&observation).unwrap();
    assert_eq!(written["traceId"], Value::Null);
    assert_eq!(written["parentObservationId"], Value::Null);
    assert!(written
        .as_object()
        .unwrap()
        .contains_key("parentObservationId"));
}

#[test]
fn missing_required_non_nullable_field_still_fails() {
    for field in ["id", "startTime", "level", "environment"] {
        let mut body = minimal_observation();
        body.as_object_mut().unwrap().remove(field);
        let error = serde_json::from_value::<Observation>(body).unwrap_err();
        assert!(
            error
                .to_string()
                .contains(&format!("missing field `{field}`")),
            "{field}: {error}"
        );
    }
}
