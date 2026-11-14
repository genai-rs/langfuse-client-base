# langfuse-client-base 0.24 → 0.25.0: Langfuse spec update

This release regenerates the client from the current Langfuse OpenAPI spec. The generator (`timvw-rust` 0.29.0,
openapi-generator 7.27.0) and `timvw-rust-runtime` 0.4 are unchanged. The census is
`api-diff-0.24.0-to-0.25.0.json`.

## What changes

- **`PromptVersionUpdateRequest`** (`PATCH /api/public/v2/prompts/{name}/versions/{version}`):
  - `new_labels` changes from `Vec<String>` to `Option<Option<Vec<String>>>`. The field may now be left out, and it
    is not sent when it is `None`.
  - The new `remove_labels: Option<Option<Vec<String>>>` removes labels from the version.
  - `PromptVersionUpdateRequest::new()` takes no arguments, and the struct derives `Default`.
- **Documentation only**:
  - `NullEvaluationRuleFilter`, `EvaluationRuleFilterNullEvaluationRuleFilter` and `UnstableDashboardWidgetFilter`:
    the empty-string `value` of a `null` filter can be left out on Langfuse servers newer than v4.78.0. The field
    types do not change.
  - `observations_api::get_observations_v2`: a condition in `filter` replaces the query parameter for the same field
    only. Other query parameters still apply.

## Upgrading

- `PromptVersionUpdateRequest::new(labels)` becomes
  `PromptVersionUpdateRequest { new_labels: Some(Some(labels)), ..Default::default() }`, or use the builder:
  `PromptVersionUpdateRequest::builder().new_labels(Some(labels)).build()`.
- Code that reads `new_labels` from a request it built matches on the two `Option` levels.
