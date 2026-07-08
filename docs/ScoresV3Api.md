# \ScoresV3Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**scores_v3_get_many_v3**](ScoresV3Api.md#scores_v3_get_many_v3) | **GET** /api/public/v3/scores | 



## scores_v3_get_many_v3

> models::GetScoresV3Response scores_v3_get_many_v3(limit, cursor, fields, id, name, source, data_type, environment, config_id, queue_id, author_user_id, value, value_min, value_max, trace_id, session_id, observation_id, experiment_id, from_timestamp, to_timestamp)


Get a list of scores with a polymorphic `value` field (v3).  The `value` field type depends on `dataType`: - `NUMERIC` → number - `BOOLEAN` → boolean - `CATEGORICAL`, `TEXT`, `CORRECTION` → string  The response always includes the core fields: id, projectId, name, value, dataType, source, timestamp, environment, createdAt, updatedAt.  Additional field groups can be requested via the `fields` parameter: - `details` — adds comment, configId, metadata - `subject` — adds the subject object describing the entity the score   is attached to: kind (trace, observation, session, or experiment),   id, and traceId for observation-level scores - `annotation` — adds authorUserId, queueId  Unknown group names return HTTP 400.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**limit** | Option<**i32**> | Number of items per page. Maximum 100, default 50. Requests with a limit greater than 100 return HTTP 400. |  |
**cursor** | Option<**String**> | URL-safe base64 (base64url) cursor for pagination. Use the cursor from the previous response to get the next page. Absent on the final page. |  |
**fields** | Option<**String**> | Comma-separated field groups to include in addition to the always-returned core fields. Allowed: details, subject, annotation — see the endpoint description for the fields each group adds. Unknown names return HTTP 400. |  |
**id** | Option<**String**> | Comma-separated list of score IDs to filter by (OR within, AND across filters). |  |
**name** | Option<**String**> | Comma-separated list of score names to filter by. |  |
**source** | Option<**String**> | Comma-separated list of score sources to filter by (e.g. API, ANNOTATION, EVAL). Case-insensitive — `api` and `API` are equivalent. |  |
**data_type** | Option<**String**> | Comma-separated list of data types to filter by (NUMERIC, BOOLEAN, CATEGORICAL, TEXT, CORRECTION). Case-insensitive — `numeric` and `NUMERIC` are equivalent. Must be a single value when used with value, valueMin, or valueMax; otherwise the request returns HTTP 400. Must be NUMERIC when used with valueMin or valueMax. |  |
**environment** | Option<**String**> | Comma-separated list of environments to filter by. |  |
**config_id** | Option<**String**> | Comma-separated list of score config IDs to filter by. |  |
**queue_id** | Option<**String**> | Comma-separated list of annotation queue IDs to filter by. |  |
**author_user_id** | Option<**String**> | Comma-separated list of author user IDs to filter by. |  |
**value** | Option<**String**> | Comma-separated list of exact values to filter by. Requires a single dataType from NUMERIC, BOOLEAN, or CATEGORICAL; any other dataType, multiple dataTypes, or omitting dataType returns HTTP 400. For BOOLEAN, each value must be \"true\" or \"false\"; for NUMERIC, each value must be a finite number. Otherwise the request returns HTTP 400. |  |
**value_min** | Option<**f64**> | Inclusive lower bound on the numeric value. Requires dataType=NUMERIC as a single value; otherwise the request returns HTTP 400. |  |
**value_max** | Option<**f64**> | Inclusive upper bound on the numeric value. Requires dataType=NUMERIC as a single value; otherwise the request returns HTTP 400. |  |
**trace_id** | Option<**String**> | Comma-separated list of trace IDs to filter by. Mutually exclusive with sessionId, experimentId. May be combined with observationId to scope the observation lookup to a specific trace. |  |
**session_id** | Option<**String**> | Comma-separated list of session IDs to filter by. Mutually exclusive with traceId, observationId, experimentId. |  |
**observation_id** | Option<**String**> | Comma-separated list of observation IDs to filter by. Requires traceId to be specified, because observation IDs are scoped to a trace. Mutually exclusive with sessionId, experimentId. Returns HTTP 400 when used without traceId. |  |
**experiment_id** | Option<**String**> | Comma-separated list of dataset run IDs (experiment IDs) to filter by. Mutually exclusive with traceId, sessionId, observationId. |  |
**from_timestamp** | Option<**chrono::DateTime<chrono::FixedOffset>**> | Inclusive lower bound on the score timestamp. |  |
**to_timestamp** | Option<**chrono::DateTime<chrono::FixedOffset>**> | Exclusive upper bound on the score timestamp. |  |

### Return type

[**models::GetScoresV3Response**](GetScoresV3Response.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

