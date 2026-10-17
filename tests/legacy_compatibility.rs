#![allow(deprecated)]

use langfuse_client_base::{apis, models};
use serde_json::json;

#[test]
fn published_legacy_operations_remain_accessible() {
    let _ = apis::ingestion_api::ingestion_batch;
    let _ = apis::dataset_run_items_api::dataset_run_items_create;
    let _ = apis::dataset_run_items_api::dataset_run_items_list;
    let _ = apis::datasets_api::datasets_get_run;
    let _ = apis::datasets_api::datasets_get_runs;
    let _ = apis::datasets_api::datasets_delete_run;
    let _ = apis::legacy_metrics_v1_api::legacy_metrics_v1_metrics;
    let _ = apis::legacy_observations_v1_api::legacy_observations_v1_get;
    let _ = apis::legacy_observations_v1_api::legacy_observations_v1_get_many;
    let _ = apis::legacy_score_v1_api::legacy_score_v1_delete;
    let _ = apis::scores_v3_api::scores_v3_get_many_v3;
    let _ = apis::scores_api::scores_get_many;
    let _ = apis::scores_api::scores_get_by_id;
    let _ = apis::sessions_api::sessions_get;
    let _ = apis::sessions_api::sessions_list;
    let _ = apis::trace_api::trace_get;
    let _ = apis::trace_api::trace_list;
}

#[test]
fn legacy_single_score_and_current_batches_keep_their_wire_shapes() {
    let score = json!({"name": "quality", "value": 1.0});
    let single: models::CreateScoresRequest = serde_json::from_value(score.clone()).unwrap();
    assert!(matches!(
        single,
        models::CreateScoresRequest::CreateScoreRequest(_)
    ));
    assert_eq!(serde_json::to_value(&single).unwrap(), score);

    let batch: models::CreateScoresRequest =
        serde_json::from_value(json!([score.clone()])).unwrap();
    assert!(matches!(
        batch,
        models::CreateScoresRequest::CreateScoreBatchRequest(_)
    ));
    assert_eq!(serde_json::to_value(&batch).unwrap(), json!([score]));

    let response: models::CreateScoresResponse =
        serde_json::from_value(json!({"id": "legacy-score"})).unwrap();
    assert!(matches!(
        response,
        models::CreateScoresResponse::CreateScoreResponse(_)
    ));
}
