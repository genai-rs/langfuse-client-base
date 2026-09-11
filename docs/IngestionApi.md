# \IngestionApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**ingestion_batch**](IngestionApi.md#ingestion_batch) | **POST** /api/public/ingestion | 



## ingestion_batch

> models::IngestionResponse ingestion_batch(ingestion_batch_request)


**Deprecated:** On Langfuse Cloud, Langfuse v3 is deprecated and v4-only write mode begins on November 16, 2026. This endpoint is never shut down; it continues to accept score events. Trace and observation events fail only in v4-only write mode, not in dual or legacy mode. Always prefer upgrading to the current Python and JS SDKs. If you use custom auto-instrumentation, only then send data via the OpenTelemetry endpoint at `POST /api/public/otel/v1/traces` (for example with curl); see the [OpenTelemetry integration docs](https://langfuse.com/integrations/native/opentelemetry). Self-hosted deployments are unaffected by this date; they reject trace and observation events only in v4-only write mode, not dual or legacy. See the [Langfuse v3 to v4 upgrade guide](https://langfuse.com/self-hosting/upgrade/upgrade-guides/upgrade-v3-to-v4).  **Legacy endpoint for batch ingestion for Langfuse Observability.**  This endpoint is never shut down. Trace and observation events are rejected only in v4-only write mode (not dual or legacy); score events continue to be accepted. Always prefer upgrading to the current Python and JS SDKs. If you use custom auto-instrumentation, only then send traces via the OpenTelemetry endpoint (`POST /api/public/otel/v1/traces`), for example with curl. Learn more: https://langfuse.com/integrations/native/opentelemetry  Within each batch, there can be multiple events. Each event has a type, an id, a timestamp, metadata and a body. Internally, we refer to this as the \"event envelope\" as it tells us something about the event but not the trace. We use the event id within this envelope to deduplicate messages to avoid processing the same event twice, i.e. the event id should be unique per request. The event.body.id is the ID of the actual trace and will be used for updates and will be visible within the Langfuse App. I.e. if you want to update a trace, you'd use the same body id, but separate event IDs.  Notes: - Introduction to data model: https://langfuse.com/docs/observability/data-model - Batch sizes are limited to 3.5 MB in total. You need to adjust the number of events per batch accordingly. - The API does not return a 4xx status code for input errors. Instead, it responds with a 207 status code, which includes a list of the encountered errors.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**ingestion_batch_request** | [**IngestionBatchRequest**](IngestionBatchRequest.md) |  | [required] |

### Return type

[**models::IngestionResponse**](IngestionResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

