# \UnstableTopicsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**unstable_topics_get**](UnstableTopicsApi.md#unstable_topics_get) | **GET** /api/public/unstable/topics/{topicId} | 
[**unstable_topics_get_facet**](UnstableTopicsApi.md#unstable_topics_get_facet) | **GET** /api/public/unstable/topic-facets/{facetId} | 
[**unstable_topics_get_rule**](UnstableTopicsApi.md#unstable_topics_get_rule) | **GET** /api/public/unstable/topic-rules/{ruleId} | 
[**unstable_topics_list**](UnstableTopicsApi.md#unstable_topics_list) | **GET** /api/public/unstable/topics | 
[**unstable_topics_list_assignments**](UnstableTopicsApi.md#unstable_topics_list_assignments) | **GET** /api/public/unstable/topic-assignments | 
[**unstable_topics_list_facets**](UnstableTopicsApi.md#unstable_topics_list_facets) | **GET** /api/public/unstable/topic-facets | 
[**unstable_topics_list_rules**](UnstableTopicsApi.md#unstable_topics_list_rules) | **GET** /api/public/unstable/topic-rules | 
[**unstable_topics_list_summaries**](UnstableTopicsApi.md#unstable_topics_list_summaries) | **GET** /api/public/unstable/topic-summaries | 



## unstable_topics_get

> models::UnstableTopicWithStatus unstable_topics_get(topic_id, from_timestamp, to_timestamp)


Unstable: Topics is in closed beta. The shape may change without notice.  Get one topic of a facet's current map by its stable id. Retired topics are not found.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**topic_id** | **String** |  | [required] |
**from_timestamp** | Option<**chrono::DateTime<chrono::FixedOffset>**> | Start of the window used for `traceCount`. Defaults to 7 days before `toTimestamp`. |  |
**to_timestamp** | Option<**chrono::DateTime<chrono::FixedOffset>**> | End of the window used for `traceCount`. Defaults to now. |  |

### Return type

[**models::UnstableTopicWithStatus**](unstableTopicWithStatus.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## unstable_topics_get_facet

> models::UnstableTopicFacet unstable_topics_get_facet(facet_id)


Unstable: Topics is in closed beta. The shape may change without notice.  Get one Topics facet by id, including inactive facets.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**facet_id** | **String** |  | [required] |

### Return type

[**models::UnstableTopicFacet**](unstableTopicFacet.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## unstable_topics_get_rule

> models::UnstableTopicRule unstable_topics_get_rule(rule_id)


Unstable: Topics is in closed beta. The shape may change without notice.  Get one Topics rule by id.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**rule_id** | **String** |  | [required] |

### Return type

[**models::UnstableTopicRule**](unstableTopicRule.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## unstable_topics_list

> models::UnstableTopicList unstable_topics_list(from_timestamp, to_timestamp, filter, order_by, page, limit)


Unstable: Topics is in closed beta. The shape may change without notice.  List the topics of each active facet's live map, with the number of traces currently assigned to each topic in the window. Retired topics are not listed. `facets` holds per-facet trace counts by topic status.  The window applies to the trace start time. It defaults to the last 7 days and can span at most 93 days.  `filter` is a JSON array of filter conditions combined with AND. String matching is case-insensitive. Columns: `facetId` (stringOptions), `facetName` (string, stringOptions), `ruleId` (stringOptions), `id` (stringOptions), `name` (string, stringOptions). Facet and rule conditions also restrict `facets`.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**from_timestamp** | Option<**chrono::DateTime<chrono::FixedOffset>**> | Start of the window (trace start time, inclusive). Defaults to 7 days before `toTimestamp`. |  |
**to_timestamp** | Option<**chrono::DateTime<chrono::FixedOffset>**> | End of the window (trace start time, exclusive). Defaults to now. |  |
**filter** | Option<**String**> | JSON array of filter conditions, for example `[{\"type\":\"stringOptions\",\"column\":\"facetName\",\"operator\":\"any of\",\"value\":[\"Issues\"]}]`. |  |
**order_by** | Option<[**UnstableTopicsOrderBy**](UnstableTopicsOrderBy.md)> | Defaults to `traceCount.desc`. |  |
**page** | Option<**i64**> | 1-based page number. Defaults to `1`. |  |
**limit** | Option<**i64**> | Maximum number of items per page. Defaults to `50`, at most `100`. |  |

### Return type

[**models::UnstableTopicList**](unstableTopicList.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## unstable_topics_list_assignments

> models::UnstableTopicAssignmentList unstable_topics_list_assignments(from_timestamp, to_timestamp, filter, order_by, limit, cursor)


Unstable: Topics is in closed beta. The shape may change without notice.  List the current topic per trace, facet and rule on each rule's live map: `assigned` with its topic, or `outlier` when no topic fits. Summarized traces that are not assigned yet are not listed; find them through `GET /topic-summaries` with `assignmentStatus`.  The window applies to the trace start time. It defaults to the last 7 days and can span at most 30 days, starting no earlier than the plan's data access window. Without `fromTimestamp` and `toTimestamp`, a `traceId` `any of` filter reads the listed traces at their own start time within the last 93 days. Rows are ordered by trace start time.  Each request scans a bounded number of candidate rows. A page shorter than `limit` (even an empty one) with a `meta.cursor` does not indicate completion; continue with the cursor until it is null.  Only active facets (attached to a Topics rule, or all facets if the project has no rule) are read. Traces Topics never processed are not listed.  `filter` is a JSON array of filter conditions combined with AND, with at most 100 `traceId` values. Columns: `traceId`, `facetId`, `facetName`, `ruleId`, `environment`, `topicId`, `topicName` (stringOptions), `status` (stringOptions, `any of` only: `assigned`, `outlier`), `timestamp` (datetime). An unknown `topicName` matches nothing under `any of` and is ignored under `none of`.  Common questions: - Topics of specific traces: `traceId` `any of` the trace ids. - Traces in a topic: `topicId` or `topicName`.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**from_timestamp** | Option<**chrono::DateTime<chrono::FixedOffset>**> | Start of the window (trace start time, inclusive). Defaults to 7 days before `toTimestamp`. |  |
**to_timestamp** | Option<**chrono::DateTime<chrono::FixedOffset>**> | End of the window (trace start time, exclusive). Defaults to now. |  |
**filter** | Option<**String**> | JSON array of filter conditions, for example `[{\"type\":\"stringOptions\",\"column\":\"topicName\",\"operator\":\"any of\",\"value\":[\"Refunds\"]}]`. |  |
**order_by** | Option<[**UnstableTopicResultsOrderBy**](UnstableTopicResultsOrderBy.md)> | Defaults to `timestamp.desc`. |  |
**limit** | Option<**i64**> | Maximum number of rows per page. Defaults to `50`, at most `100`. |  |
**cursor** | Option<**String**> | The `meta.cursor` of the previous page. |  |

### Return type

[**models::UnstableTopicAssignmentList**](unstableTopicAssignmentList.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## unstable_topics_list_facets

> models::UnstableTopicFacetList unstable_topics_list_facets(filter, page, limit)


Unstable: Topics is in closed beta. The shape may change without notice.  List the project's Topics facets. Only active facets (run by a Topics rule, or all facets if the project has no rule) are returned unless `filter` contains an `active` condition.  `filter` is a JSON array of filter conditions combined with AND. String matching is case-insensitive. Columns: `id` (stringOptions), `name` (string, stringOptions), `description` (string), `isBuiltIn` (boolean), `active` (boolean).

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**filter** | Option<**String**> | JSON array of filter conditions, for example `[{\"type\":\"string\",\"column\":\"name\",\"operator\":\"contains\",\"value\":\"issue\"}]`. |  |
**page** | Option<**i64**> | 1-based page number. Defaults to `1`. |  |
**limit** | Option<**i64**> | Maximum number of items per page. Defaults to `50`, at most `100`. |  |

### Return type

[**models::UnstableTopicFacetList**](unstableTopicFacetList.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## unstable_topics_list_rules

> models::UnstableTopicRuleList unstable_topics_list_rules(filter, page, limit)


Unstable: Topics is in closed beta. The shape may change without notice.  List the project's Topics rules. A rule selects traces with an observation filter and a sampling rate, runs the facets in `facetIds` and keeps its own live topic map.  `filter` is a JSON array of filter conditions combined with AND. String matching is case-insensitive. Columns: `id` (stringOptions), `name` (string, stringOptions).

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**filter** | Option<**String**> | JSON array of filter conditions, for example `[{\"type\":\"string\",\"column\":\"name\",\"operator\":\"contains\",\"value\":\"support\"}]`. |  |
**page** | Option<**i64**> | 1-based page number. Defaults to `1`. |  |
**limit** | Option<**i64**> | Maximum number of items per page. Defaults to `50`, at most `100`. |  |

### Return type

[**models::UnstableTopicRuleList**](unstableTopicRuleList.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## unstable_topics_list_summaries

> models::UnstableTopicSummaryList unstable_topics_list_summaries(from_timestamp, to_timestamp, filter, truncate_summaries, order_by, limit, cursor)


Unstable: Topics is in closed beta. The shape may change without notice.  List the current Topics summary per trace and facet: what the trace is about from the facet's perspective. Summaries are shared by all rules. A trace that was re-summarized lists only its latest summary.  The window applies to the trace start time. It defaults to the last 7 days and can span at most 30 days, starting no earlier than the plan's data access window. Without `fromTimestamp` and `toTimestamp`, a `traceId` `any of` filter reads the listed traces at their own start time within the last 93 days. Rows are ordered by trace start time.  Each request scans a bounded number of candidate rows. A page shorter than `limit` (even an empty one) with a `meta.cursor` does not indicate completion; continue with the cursor until it is null.  Only active facets (attached to a Topics rule, or all facets if the project has no rule) are read. Traces Topics never processed are not listed.  `filter` is a JSON array of filter conditions combined with AND, with at most 100 `traceId` values. Columns: `traceId`, `facetId`, `facetName`, `ruleId`, `environment` (stringOptions), `timestamp`, `processedAt` (datetime), `state`, `topicId`, `topicName` (stringOptions), `assignmentStatus` (stringOptions, `any of` only). An unknown `topicName` matches nothing under `any of` and is ignored under `none of`.  `state` values: `complete` (summarized), `not_applicable` (the facet does not apply to the trace), `insufficient_input` (too little input to summarize). `assignmentStatus` values: `assigned`, `outlier` (no topic fits), `awaiting_map` (summarized, not yet assigned).  Common questions: - Summaries of specific traces: `traceId` `any of` the trace ids. - Summaries of a topic's traces: `topicId` or `topicName`. - Traces without a topic yet: `assignmentStatus` `any of` `[\"awaiting_map\", \"outlier\"]`.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**from_timestamp** | Option<**chrono::DateTime<chrono::FixedOffset>**> | Start of the window (trace start time, inclusive). Defaults to 7 days before `toTimestamp`. |  |
**to_timestamp** | Option<**chrono::DateTime<chrono::FixedOffset>**> | End of the window (trace start time, exclusive). Defaults to now. |  |
**filter** | Option<**String**> | JSON array of filter conditions, for example `[{\"type\":\"stringOptions\",\"column\":\"traceId\",\"operator\":\"any of\",\"value\":[\"<trace id>\"]}]`. |  |
**truncate_summaries** | Option<**bool**> | Whether to truncate summaries to 500 characters. Defaults to `false`. |  |
**order_by** | Option<[**UnstableTopicResultsOrderBy**](UnstableTopicResultsOrderBy.md)> | Defaults to `timestamp.desc`. |  |
**limit** | Option<**i64**> | Maximum number of rows per page. Defaults to `50`, at most `100`. |  |
**cursor** | Option<**String**> | The `meta.cursor` of the previous page. |  |

### Return type

[**models::UnstableTopicSummaryList**](unstableTopicSummaryList.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

