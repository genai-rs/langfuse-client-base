# langfuse-client-base 0.18.0 → 0.19.0: request bodies by reference, boxed errors with headers, validation

This release generates with `timvw-rust` 0.21.0. The Langfuse spec (`openapi.yml`) and openapi-generator (7.27.0) are
unchanged. The machine-readable census is `api-diff-0.18.0-to-0.19.0.json` in this folder (`compare_public_api.py`
against 0.18.0).

`timvw-rust` 0.21.0 makes the renderings this crate already switched on (`boxOnlyCycles`, `defaultOnlyWhereValid`,
`enumFromStr`, `noStructDisplay`, `integersAsI64`, `qualifiedInlineNames`, `modelUnions`, `unionDispatch`, `openEnums`,
`schemaDefaultDocs` and `nullableUnionFields`) the only rendering, so `scripts/generate-openapi-client.sh` no longer
passes them. That part changes nothing in the crate.

## What stays the same

- Every model, field and enum. No type is added, removed or renamed (except the new `models::validation` module below).
- Every operation keeps its module and function name, and every parameter that is not a request body keeps its type.
- The JSON bodies sent and received.

## What changes

**Request bodies are borrowed.** 46 functions take their JSON body by reference: `item: models::Item` becomes
`item: &models::Item`. Path, query and header parameters are unchanged.

**The response error is boxed and carries the headers.** `Error::ResponseError` holds `Box<apis::ResponseContent<T>>`
instead of `ResponseContent<T>`, and `ResponseContent<T>` gets `headers: reqwest::header::HeaderMap`, filled on every
error status (`retry-after`, `x-request-id`, ...). `{:?}` of an error now prints these headers; `Display` is unchanged.

**The error variant follows the status.** `entity` holds the variant of the response's status code (`Status404` for a
404), and `UnknownValue` for a status the spec does not list. Before, the body went into the first variant whose type
accepted it; every Langfuse error type is `serde_json::Value`, so every JSON error body came back as `Status400`. The
error enums do not change.

**`date-time` query parameters are sent in RFC 3339.** `fromTimestamp`, `toTimestamp`, `fromStartTime`, `toStartTime`,
`fromUpdatedAt` and `toUpdatedAt` went out as chrono's `Display` (`2026-01-02 03:04:05 UTC`) and now as
`2026-01-02T03:04:05+00:00`. Signatures do not change.

**Path values encode a space as `%20`** instead of `+`.

**Every model implements `models::validation::Validate`.** `validate()` checks the spec's `minLength`, `maxLength`,
`minimum`, `maximum`, `minItems`, `maxItems`, ... recursively and returns the first
`models::validation::ValidationError` (path, rule, value). Nothing calls it for you.

## Migrating

- Pass request bodies by reference: `.ingestion_batch_request(&request)`, `.create_scores_request(&request)`. The value
  stays yours to reuse.
- Code that matches `Error::ResponseError(response)` and reads `response.status` or `response.content` is unchanged (the
  `Box` derefs). Code that moves the `ResponseContent` out uses `*response`; code that builds the variant wraps it,
  `Error::ResponseError(Box::new(content))`, and a `ResponseContent` struct literal adds
  `headers: reqwest::header::HeaderMap::new()`.
- Code that matches `Status400` to catch any error response now gets the variant of the actual status.
- To check a request before sending it: `use langfuse_client_base::models::validation::Validate;` then
  `request.validate()?`.
