# \OpentelemetryApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**opentelemetry_export_traces**](OpentelemetryApi.md#opentelemetry_export_traces) | **POST** /api/public/otel/v1/traces | 



## opentelemetry_export_traces

> serde_json::Value opentelemetry_export_traces(opentelemetry_export_traces_request)


**OpenTelemetry Traces Ingestion Endpoint**  This endpoint implements the OTLP/HTTP specification for trace ingestion, providing native OpenTelemetry integration for Langfuse Observability.  **Supported Formats:** - Binary Protobuf: `Content-Type: application/x-protobuf` - JSON Protobuf: `Content-Type: application/json` - Supports gzip compression via `Content-Encoding: gzip` header  **Specification Compliance:** - Conforms to [OTLP/HTTP Trace Export](https://opentelemetry.io/docs/specs/otlp/#otlphttp) - Implements `ExportTraceServiceRequest` message format  **Documentation:** - Integration guide: https://langfuse.com/integrations/native/opentelemetry - Data model: https://langfuse.com/docs/observability/data-model

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**opentelemetry_export_traces_request** | [**OpentelemetryExportTracesRequest**](OpentelemetryExportTracesRequest.md) |  | [required] |

### Return type

[**serde_json::Value**](serde_json::Value.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

