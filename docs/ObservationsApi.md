# \ObservationsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**observations_get**](ObservationsApi.md#observations_get) | **GET** /api/public/observations/{observationId} | 
[**observations_get_many**](ObservationsApi.md#observations_get_many) | **GET** /api/public/observations | 



## observations_get

> models::ObservationsView observations_get(observation_id)


Get a observation

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**observation_id** | **String** | The unique langfuse identifier of an observation, can be an event, span or generation | [required] |

### Return type

[**models::ObservationsView**](ObservationsView.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## observations_get_many

> models::ObservationsViews observations_get_many(page, limit, name, user_id, r#type, trace_id, level, parent_observation_id, environment, from_start_time, to_start_time, version, filter)


Get a list of observations

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**page** | Option<**i32**> | Page number, starts at 1. |  |
**limit** | Option<**i32**> | Limit of items per page. If you encounter api issues due to too large page sizes, try to reduce the limit. |  |
**name** | Option<**String**> |  |  |
**user_id** | Option<**String**> |  |  |
**r#type** | Option<**String**> |  |  |
**trace_id** | Option<**String**> |  |  |
**level** | Option<[**ObservationLevel**](.md)> | Optional filter for observations with a specific level (e.g. \"DEBUG\", \"DEFAULT\", \"WARNING\", \"ERROR\"). |  |
**parent_observation_id** | Option<**String**> |  |  |
**environment** | Option<[**Vec<String>**](String.md)> | Optional filter for observations where the environment is one of the provided values. |  |
**from_start_time** | Option<**String**> | Retrieve only observations with a start_time on or after this datetime (ISO 8601). |  |
**to_start_time** | Option<**String**> | Retrieve only observations with a start_time before this datetime (ISO 8601). |  |
**version** | Option<**String**> | Optional filter to only include observations with a certain version. |  |
**filter** | Option<**String**> | JSON string containing an array of filter conditions. When provided, this takes precedence over query parameter filters (userId, name, type, level, environment, fromStartTime, ...).  ## Filter Structure Each filter condition has the following structure: ```json [   {     \"type\": string,           // Required. One of: \"datetime\", \"string\", \"number\", \"stringOptions\", \"categoryOptions\", \"arrayOptions\", \"stringObject\", \"numberObject\", \"boolean\", \"null\"     \"column\": string,         // Required. Column to filter on (see available columns below)     \"operator\": string,       // Required. Operator based on type:                               // - datetime: \">\", \"<\", \">=\", \"<=\"                               // - string: \"=\", \"contains\", \"does not contain\", \"starts with\", \"ends with\"                               // - stringOptions: \"any of\", \"none of\"                               // - categoryOptions: \"any of\", \"none of\"                               // - arrayOptions: \"any of\", \"none of\", \"all of\"                               // - number: \"=\", \">\", \"<\", \">=\", \"<=\"                               // - stringObject: \"=\", \"contains\", \"does not contain\", \"starts with\", \"ends with\"                               // - numberObject: \"=\", \">\", \"<\", \">=\", \"<=\"                               // - boolean: \"=\", \"<>\"                               // - null: \"is null\", \"is not null\"     \"value\": any,             // Required (except for null type). Value to compare against. Type depends on filter type     \"key\": string             // Required only for stringObject, numberObject, and categoryOptions types when filtering on nested fields like metadata   } ] ```  ## Available Columns  ### Core Observation Fields - `id` (string) - Observation ID - `type` (string) - Observation type (SPAN, GENERATION, EVENT) - `name` (string) - Observation name - `traceId` (string) - Associated trace ID - `startTime` (datetime) - Observation start time - `endTime` (datetime) - Observation end time - `environment` (string) - Environment tag - `level` (string) - Log level (DEBUG, DEFAULT, WARNING, ERROR) - `statusMessage` (string) - Status message - `version` (string) - Version tag  ### Performance Metrics - `latency` (number) - Latency in seconds (calculated: end_time - start_time) - `timeToFirstToken` (number) - Time to first token in seconds - `tokensPerSecond` (number) - Output tokens per second  ### Token Usage - `inputTokens` (number) - Number of input tokens - `outputTokens` (number) - Number of output tokens - `totalTokens` (number) - Total tokens (alias: `tokens`)  ### Cost Metrics - `inputCost` (number) - Input cost in USD - `outputCost` (number) - Output cost in USD - `totalCost` (number) - Total cost in USD  ### Model Information - `model` (string) - Provided model name - `promptName` (string) - Associated prompt name - `promptVersion` (number) - Associated prompt version  ### Structured Data - `metadata` (stringObject/numberObject/categoryOptions) - Metadata key-value pairs. Use `key` parameter to filter on specific metadata keys.  ### Associated Trace Fields (requires join with traces table) - `userId` (string) - User ID from associated trace - `traceName` (string) - Name from associated trace - `traceEnvironment` (string) - Environment from associated trace - `traceTags` (arrayOptions) - Tags from associated trace  ## Filter Examples ```json [   {     \"type\": \"string\",     \"column\": \"type\",     \"operator\": \"=\",     \"value\": \"GENERATION\"   },   {     \"type\": \"number\",     \"column\": \"latency\",     \"operator\": \">=\",     \"value\": 2.5   },   {     \"type\": \"stringObject\",     \"column\": \"metadata\",     \"key\": \"environment\",     \"operator\": \"=\",     \"value\": \"production\"   } ] ``` |  |

### Return type

[**models::ObservationsViews**](ObservationsViews.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

