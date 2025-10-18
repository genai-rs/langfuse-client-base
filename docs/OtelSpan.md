# OtelSpan

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**trace_id** | Option<[**serde_json::Value**](.md)> | Trace ID (16 bytes, hex-encoded string in JSON or Buffer in binary) | [optional]
**span_id** | Option<[**serde_json::Value**](.md)> | Span ID (8 bytes, hex-encoded string in JSON or Buffer in binary) | [optional]
**parent_span_id** | Option<[**serde_json::Value**](.md)> | Parent span ID if this is a child span | [optional]
**name** | Option<**String**> | Span name describing the operation | [optional]
**kind** | Option<**i32**> | Span kind (1=INTERNAL, 2=SERVER, 3=CLIENT, 4=PRODUCER, 5=CONSUMER) | [optional]
**start_time_unix_nano** | Option<[**serde_json::Value**](.md)> | Start time in nanoseconds since Unix epoch | [optional]
**end_time_unix_nano** | Option<[**serde_json::Value**](.md)> | End time in nanoseconds since Unix epoch | [optional]
**attributes** | Option<[**Vec<models::OtelAttribute>**](OtelAttribute.md)> | Span attributes including Langfuse-specific attributes (langfuse.observation.*) | [optional]
**status** | Option<[**serde_json::Value**](.md)> | Span status object | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


