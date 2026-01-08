# \ObservationsV2Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**observations_v2_get_many**](ObservationsV2Api.md#observations_v2_get_many) | **GET** /api/public/v2/observations | 



## observations_v2_get_many

> models::ObservationsV2Response observations_v2_get_many(fields, expand_metadata, limit, cursor, parse_io_as_json, name, user_id, r#type, trace_id, level, parent_observation_id, environment, from_start_time, to_start_time, version, filter)


Get a list of observations with cursor-based pagination and flexible field selection.  ## Cursor-based Pagination This endpoint uses cursor-based pagination for efficient traversal of large datasets. The cursor is returned in the response metadata and should be passed in subsequent requests to retrieve the next page of results.  ## Field Selection Use the `fields` parameter to control which observation fields are returned: - `core` - Always included: id, traceId, startTime, endTime, projectId, parentObservationId, type - `basic` - name, level, statusMessage, version, environment, bookmarked, public, userId, sessionId - `time` - completionStartTime, createdAt, updatedAt - `io` - input, output - `metadata` - metadata (truncated to 200 chars by default, use `expandMetadata` to get full values) - `model` - providedModelName, internalModelId, modelParameters - `usage` - usageDetails, costDetails, totalCost - `prompt` - promptId, promptName, promptVersion - `metrics` - latency, timeToFirstToken  If not specified, `core` and `basic` field groups are returned.  ## Filters Multiple filtering options are available via query parameters or the structured `filter` parameter. When using the `filter` parameter, it takes precedence over individual query parameter filters.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**fields** | Option<**String**> | Comma-separated list of field groups to include in the response. Available groups: core, basic, time, io, metadata, model, usage, prompt, metrics. If not specified, `core` and `basic` field groups are returned. Example: \"basic,usage,model\" |  |
**expand_metadata** | Option<**String**> | Comma-separated list of metadata keys to return non-truncated. By default, metadata values over 200 characters are truncated. Use this parameter to retrieve full values for specific keys. Example: \"key1,key2\" |  |
**limit** | Option<**i32**> | Number of items to return per page. Maximum 1000, default 50. |  |
**cursor** | Option<**String**> | Base64-encoded cursor for pagination. Use the cursor from the previous response to get the next page. |  |
**parse_io_as_json** | Option<**bool**> | Set to `true` to parse input/output fields as JSON, or `false` to return raw strings. Defaults to `false` if not provided. |  |
**name** | Option<**String**> |  |  |
**user_id** | Option<**String**> |  |  |
**r#type** | Option<**String**> | Filter by observation type (e.g., \"GENERATION\", \"SPAN\", \"EVENT\", \"AGENT\", \"TOOL\", \"CHAIN\", \"RETRIEVER\", \"EVALUATOR\", \"EMBEDDING\", \"GUARDRAIL\") |  |
**trace_id** | Option<**String**> |  |  |
**level** | Option<[**ObservationLevel**](.md)> | Optional filter for observations with a specific level (e.g. \"DEBUG\", \"DEFAULT\", \"WARNING\", \"ERROR\"). |  |
**parent_observation_id** | Option<**String**> |  |  |
**environment** | Option<[**Vec<String>**](String.md)> | Optional filter for observations where the environment is one of the provided values. |  |
**from_start_time** | Option<**String**> | Retrieve only observations with a start_time on or after this datetime (ISO 8601). |  |
**to_start_time** | Option<**String**> | Retrieve only observations with a start_time before this datetime (ISO 8601). |  |
**version** | Option<**String**> | Optional filter to only include observations with a certain version. |  |
**filter** | Option<**String**> | JSON string containing an array of filter conditions. When provided, this takes precedence over query parameter filters (userId, name, type, level, environment, fromStartTime, ...).  ## Filter Structure Each filter condition has the following structure: ```json [   {     \"type\": string,           // Required. One of: \"datetime\", \"string\", \"number\", \"stringOptions\", \"categoryOptions\", \"arrayOptions\", \"stringObject\", \"numberObject\", \"boolean\", \"null\"     \"column\": string,         // Required. Column to filter on (see available columns below)     \"operator\": string,       // Required. Operator based on type:                               // - datetime: \">\", \"<\", \">=\", \"<=\"                               // - string: \"=\", \"contains\", \"does not contain\", \"starts with\", \"ends with\"                               // - stringOptions: \"any of\", \"none of\"                               // - categoryOptions: \"any of\", \"none of\"                               // - arrayOptions: \"any of\", \"none of\", \"all of\"                               // - number: \"=\", \">\", \"<\", \">=\", \"<=\"                               // - stringObject: \"=\", \"contains\", \"does not contain\", \"starts with\", \"ends with\"                               // - numberObject: \"=\", \">\", \"<\", \">=\", \"<=\"                               // - boolean: \"=\", \"<>\"                               // - null: \"is null\", \"is not null\"     \"value\": any,             // Required (except for null type). Value to compare against. Type depends on filter type     \"key\": string             // Required only for stringObject, numberObject, and categoryOptions types when filtering on nested fields like metadata   } ] ```  ## Available Columns  ### Core Observation Fields - `id` (string) - Observation ID - `type` (string) - Observation type (SPAN, GENERATION, EVENT) - `name` (string) - Observation name - `traceId` (string) - Associated trace ID - `startTime` (datetime) - Observation start time - `endTime` (datetime) - Observation end time - `environment` (string) - Environment tag - `level` (string) - Log level (DEBUG, DEFAULT, WARNING, ERROR) - `statusMessage` (string) - Status message - `version` (string) - Version tag - `userId` (string) - User ID - `sessionId` (string) - Session ID  ### Trace-Related Fields - `traceName` (string) - Name of the parent trace - `traceTags` (arrayOptions) - Tags from the parent trace - `tags` (arrayOptions) - Alias for traceTags  ### Performance Metrics - `latency` (number) - Latency in seconds (calculated: end_time - start_time) - `timeToFirstToken` (number) - Time to first token in seconds - `tokensPerSecond` (number) - Output tokens per second  ### Token Usage - `inputTokens` (number) - Number of input tokens - `outputTokens` (number) - Number of output tokens - `totalTokens` (number) - Total tokens (alias: `tokens`)  ### Cost Metrics - `inputCost` (number) - Input cost in USD - `outputCost` (number) - Output cost in USD - `totalCost` (number) - Total cost in USD  ### Model Information - `model` (string) - Provided model name (alias: `providedModelName`) - `promptName` (string) - Associated prompt name - `promptVersion` (number) - Associated prompt version  ### Structured Data - `metadata` (stringObject/numberObject/categoryOptions) - Metadata key-value pairs. Use `key` parameter to filter on specific metadata keys.  ## Filter Examples ```json [   {     \"type\": \"string\",     \"column\": \"type\",     \"operator\": \"=\",     \"value\": \"GENERATION\"   },   {     \"type\": \"number\",     \"column\": \"latency\",     \"operator\": \">=\",     \"value\": 2.5   },   {     \"type\": \"stringObject\",     \"column\": \"metadata\",     \"key\": \"environment\",     \"operator\": \"=\",     \"value\": \"production\"   } ] ``` |  |

### Return type

[**models::ObservationsV2Response**](ObservationsV2Response.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

