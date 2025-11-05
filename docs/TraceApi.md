# \TraceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**trace_delete**](TraceApi.md#trace_delete) | **DELETE** /api/public/traces/{traceId} | 
[**trace_delete_multiple**](TraceApi.md#trace_delete_multiple) | **DELETE** /api/public/traces | 
[**trace_get**](TraceApi.md#trace_get) | **GET** /api/public/traces/{traceId} | 
[**trace_list**](TraceApi.md#trace_list) | **GET** /api/public/traces | 



## trace_delete

> models::DeleteTraceResponse trace_delete(trace_id)


Delete a specific trace

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**trace_id** | **String** | The unique langfuse identifier of the trace to delete | [required] |

### Return type

[**models::DeleteTraceResponse**](DeleteTraceResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## trace_delete_multiple

> models::DeleteTraceResponse trace_delete_multiple(trace_delete_multiple_request)


Delete multiple traces

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**trace_delete_multiple_request** | [**TraceDeleteMultipleRequest**](TraceDeleteMultipleRequest.md) |  | [required] |

### Return type

[**models::DeleteTraceResponse**](DeleteTraceResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## trace_get

> models::TraceWithFullDetails trace_get(trace_id)


Get a specific trace

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**trace_id** | **String** | The unique langfuse identifier of a trace | [required] |

### Return type

[**models::TraceWithFullDetails**](TraceWithFullDetails.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## trace_list

> models::Traces trace_list(page, limit, user_id, name, session_id, from_timestamp, to_timestamp, order_by, tags, version, release, environment, fields, filter)


Get list of traces

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**page** | Option<**i32**> | Page number, starts at 1 |  |
**limit** | Option<**i32**> | Limit of items per page. If you encounter api issues due to too large page sizes, try to reduce the limit. |  |
**user_id** | Option<**String**> |  |  |
**name** | Option<**String**> |  |  |
**session_id** | Option<**String**> |  |  |
**from_timestamp** | Option<**String**> | Optional filter to only include traces with a trace.timestamp on or after a certain datetime (ISO 8601) |  |
**to_timestamp** | Option<**String**> | Optional filter to only include traces with a trace.timestamp before a certain datetime (ISO 8601) |  |
**order_by** | Option<**String**> | Format of the string [field].[asc/desc]. Fields: id, timestamp, name, userId, release, version, public, bookmarked, sessionId. Example: timestamp.asc |  |
**tags** | Option<[**Vec<String>**](String.md)> | Only traces that include all of these tags will be returned. |  |
**version** | Option<**String**> | Optional filter to only include traces with a certain version. |  |
**release** | Option<**String**> | Optional filter to only include traces with a certain release. |  |
**environment** | Option<[**Vec<String>**](String.md)> | Optional filter for traces where the environment is one of the provided values. |  |
**fields** | Option<**String**> | Comma-separated list of fields to include in the response. Available field groups: 'core' (always included), 'io' (input, output, metadata), 'scores', 'observations', 'metrics'. If not specified, all fields are returned. Example: 'core,scores,metrics'. Note: Excluded 'observations' or 'scores' fields return empty arrays; excluded 'metrics' returns -1 for 'totalCost' and 'latency'. |  |
**filter** | Option<**String**> | JSON string containing an array of filter conditions. When provided, this takes precedence over query parameter filters (userId, name, sessionId, tags, version, release, environment, fromTimestamp, toTimestamp).  ## Filter Structure Each filter condition has the following structure: ```json [   {     \"type\": string,           // Required. One of: \"datetime\", \"string\", \"number\", \"stringOptions\", \"categoryOptions\", \"arrayOptions\", \"stringObject\", \"numberObject\", \"boolean\", \"null\"     \"column\": string,         // Required. Column to filter on (see available columns below)     \"operator\": string,       // Required. Operator based on type:                               // - datetime: \">\", \"<\", \">=\", \"<=\"                               // - string: \"=\", \"contains\", \"does not contain\", \"starts with\", \"ends with\"                               // - stringOptions: \"any of\", \"none of\"                               // - categoryOptions: \"any of\", \"none of\"                               // - arrayOptions: \"any of\", \"none of\", \"all of\"                               // - number: \"=\", \">\", \"<\", \">=\", \"<=\"                               // - stringObject: \"=\", \"contains\", \"does not contain\", \"starts with\", \"ends with\"                               // - numberObject: \"=\", \">\", \"<\", \">=\", \"<=\"                               // - boolean: \"=\", \"<>\"                               // - null: \"is null\", \"is not null\"     \"value\": any,             // Required (except for null type). Value to compare against. Type depends on filter type     \"key\": string             // Required only for stringObject, numberObject, and categoryOptions types when filtering on nested fields like metadata   } ] ```  ## Available Columns  ### Core Trace Fields - `id` (string) - Trace ID - `name` (string) - Trace name - `timestamp` (datetime) - Trace timestamp - `userId` (string) - User ID - `sessionId` (string) - Session ID - `environment` (string) - Environment tag - `version` (string) - Version tag - `release` (string) - Release tag - `tags` (arrayOptions) - Array of tags - `bookmarked` (boolean) - Bookmark status  ### Structured Data - `metadata` (stringObject/numberObject/categoryOptions) - Metadata key-value pairs. Use `key` parameter to filter on specific metadata keys.  ### Aggregated Metrics (from observations) These metrics are aggregated from all observations within the trace: - `latency` (number) - Latency in seconds (time from first observation start to last observation end) - `inputTokens` (number) - Total input tokens across all observations - `outputTokens` (number) - Total output tokens across all observations - `totalTokens` (number) - Total tokens (alias: `tokens`) - `inputCost` (number) - Total input cost in USD - `outputCost` (number) - Total output cost in USD - `totalCost` (number) - Total cost in USD  ### Observation Level Aggregations These fields aggregate observation levels within the trace: - `level` (string) - Highest severity level (ERROR > WARNING > DEFAULT > DEBUG) - `warningCount` (number) - Count of WARNING level observations - `errorCount` (number) - Count of ERROR level observations - `defaultCount` (number) - Count of DEFAULT level observations - `debugCount` (number) - Count of DEBUG level observations  ### Scores (requires join with scores table) - `scores_avg` (number) - Average of numeric scores (alias: `scores`) - `score_categories` (categoryOptions) - Categorical score values  ## Filter Examples ```json [   {     \"type\": \"datetime\",     \"column\": \"timestamp\",     \"operator\": \">=\",     \"value\": \"2024-01-01T00:00:00Z\"   },   {     \"type\": \"string\",     \"column\": \"userId\",     \"operator\": \"=\",     \"value\": \"user-123\"   },   {     \"type\": \"number\",     \"column\": \"totalCost\",     \"operator\": \">=\",     \"value\": 0.01   },   {     \"type\": \"arrayOptions\",     \"column\": \"tags\",     \"operator\": \"all of\",     \"value\": [\"production\", \"critical\"]   },   {     \"type\": \"stringObject\",     \"column\": \"metadata\",     \"key\": \"customer_tier\",     \"operator\": \"=\",     \"value\": \"enterprise\"   } ] ```  ## Performance Notes - Filtering on `userId`, `sessionId`, or `metadata` may enable skip indexes for better query performance - Score filters require a join with the scores table and may impact query performance |  |

### Return type

[**models::Traces**](Traces.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

