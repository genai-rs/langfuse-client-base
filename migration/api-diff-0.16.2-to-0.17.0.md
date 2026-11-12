# langfuse-client-base 0.16.2 → 0.17.0: the timvw-rust Milestone 3 rendering

This release generates with `timvw-rust` 0.14.0 (was 0.2.0) on openapi-generator 7.27.0 (was 7.25.0), and turns on the
Milestone 3 options of the [generator](https://github.com/timvw/openapi-generator-timvw-rust#readme) that
openai-client-base adopted in 0.18.0 to 0.22.0: `boxOnlyCycles`, `defaultOnlyWhereValid`, `enumFromStr`,
`noStructDisplay`, `qualifiedInlineNames`, `modelUnions`, `unionDispatch`, `integersAsI64` and `openEnums`. The Langfuse
spec and its v3 compatibility layer are unchanged. The machine-readable census is `api-diff-0.16.2-to-0.17.0.json` in
this folder (`compare_public_api.py` against 0.16.2).

## What stays the same

- Every operation keeps its module, function name and parameters, apart from the integer types below.
- Known values serialize to the same JSON. Every struct keeps its fields, a union's struct keeps its tag field.
- Component schemas keep their names (`TraceBody`, `ScoreBody`, `Prompt`, `CreateScoreRequest`, ...).

## What changes

**No `Box` around model references (`boxOnlyCycles`).** No Langfuse type contains itself, so all 314 boxed references
are now held by value: struct fields such as `IngestionEventTraceEvent::body: TraceBody` and union variants such as
`CreateScoresRequest::CreateScoreRequest(CreateScoreRequest)`. Drop the `Box::new(..)`.

**Stable names for inline schemas and union variants (`qualifiedInlineNames`, `modelUnions`).** The numbered models
the stock generator invented for union branches are named after the union that holds them, and the variants after the
branch, without the suffix:

| 0.16 | 0.17 |
| --- | --- |
| `IngestionEvent::TraceEvent1(Box<TraceEvent1>)` | `IngestionEvent::TraceEvent(IngestionEventTraceEvent)` |
| `IngestionEvent::ScoreEvent1`, `CreateSpanEvent1`, `UpdateSpanEvent1`, `CreateGenerationEvent1`, `UpdateGenerationEvent1`, `CreateEventEvent1`, `CreateObservationEvent1`, `UpdateObservationEvent1` | `ScoreEvent(IngestionEventScoreEvent)`, `CreateSpanEvent(IngestionEventCreateSpanEvent)`, ... likewise |
| `models::trace_event_1::Type` (and the other `*_event_1` modules) | `models::ingestion_event_trace_event::Type`, ... |
| `Score::NumericScore1(Box<NumericScore1>)`, ... | `Score::NumericScore(ScoreNumericScore)`, ... (also `ScoreV1`, `ScoreV3`, `GetScoresResponseData`, `ScoreSubjectV3`) |
| `Prompt::ChatPrompt1`, `Prompt::TextPrompt1` | `Prompt::ChatPrompt(PromptChatPrompt)`, `Prompt::TextPrompt(PromptTextPrompt)` |
| `Evaluator*`, `EvaluationRuleFilter*`, `CreateEvaluatorRequest*`, `UnstableDashboardPlacement*` branches `...1` | `<Union><Branch>` |

53 such models are renamed (see `model_exports_removed` / `model_exports_added` in the JSON). 6 API files and 143 model
files that 0.16 shipped without declaring them in `mod.rs` (left behind by earlier generator runs) are gone; the
pipeline now clears `src/apis`, `src/models` and `docs/` before generating.

**Unions decode by their tag (`unionDispatch`).** The 10 unions with a tag (`IngestionEvent`, `Score`, `ScoreV1`,
`ScoreV3`, `ScoreSubjectV3`, `GetScoresResponseData`, `Prompt`, `EvaluationRuleFilter`, `UnstableDashboardPlacement`,
...) read the tag and decode the variant it selects, with an error naming the union, variant and field instead of
`data did not match any variant`. They still serialize untagged, so the JSON is unchanged.

**Integers are `i64` unless the spec says `format: int32` (`integersAsI64`).** All 286 `i32` in the crate are now
`i64`: `page`, `limit` and `version` parameters, usage counts (`UsageDetails::Object(HashMap<String, i64>)`, `Usage`),
latencies, counts and union variants. Values that fit in `i32` are unchanged on the wire.

**`Default` only where it is valid (`defaultOnlyWhereValid`).** A struct derives `Default` only when it has no required
field, and no enum or union implements it (257 `impl Default` removed). Build the others with `new(..)` or the builder;
for example `CreateChatPromptRequest::new(name, prompt, CreateChatPromptType::Chat)`.

**`FromStr` on enums, no `Display` on structs (`enumFromStr`, `noStructDisplay`).** Closed enums implement `FromStr`,
`TryFrom<&str>`, `TryFrom<&String>` and `TryFrom<String>`, failing with the new `models::ParseEnumError`. Structs lose
their JSON `Display`; serialize with `serde_json::to_string`. Unions keep `Display`.

**A new value no longer fails a response (`openEnums`).** An enum a response can hold gains `Unknown`
(`#[serde(other)]`, 64 enums, e.g. `ObservationLevel`, `ScoreDataType`, `ChatMessageType`), and a tagged union a
response can hold gains `Unknown(serde_json::Value)` (7 unions, e.g. `Score`, `ScoreV3`, `Prompt`). `Unknown`
serializes as `"unknown"` (the original string is not kept), `Unknown(Value)` as the JSON it holds; `FromStr` never
produces either. Request-only types such as `IngestionEvent` stay closed. Because a request type that a response also
uses is open, decoding caller input into it no longer rejects an unknown value: check for `Unknown` where that matters.
An exhaustive `match` on one of these types needs a new arm.

**openapi-generator 7.27.0.** `apis::configuration` re-exports `reqwest_middleware::ClientWithMiddleware`, and
`Configuration` and `ApiKey` implement `Debug` by hand, printing `[REDACTED]` in place of passwords, tokens and keys.

## Migrating

```rust
// 0.16
let event = IngestionEvent::TraceEvent1(Box::new(TraceEvent1 {
    body: Box::new(trace_body),
    id, timestamp, metadata: None,
    r#type: models::trace_event_1::Type::TraceCreate,
}));

// 0.17
let event = IngestionEvent::TraceEvent(IngestionEventTraceEvent {
    body: trace_body,
    id, timestamp, metadata: None,
    r#type: models::ingestion_event_trace_event::Type::TraceCreate,
});
```

- Remove `Box::new` around model values and replace `*1` variants and types by the names above.
- Widen integers passed to operations and models with `i64::from(..)`.
- Replace `..Default::default()` on structs with required fields by `new(..)` or the builder.
- Add an `Unknown` arm (or a wildcard) to exhaustive matches on response enums and tagged unions.

langfuse-ergonomic adopts this release with these changes and keeps its own builder signatures.
