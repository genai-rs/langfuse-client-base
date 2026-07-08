# \ExperimentsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**experiments_list**](ExperimentsApi.md#experiments_list) | **GET** /api/public/experiments | 
[**experiments_list_items**](ExperimentsApi.md#experiments_list_items) | **GET** /api/public/experiment-items | 



## experiments_list

> models::ExperimentsResponse experiments_list(from_start_time, fields, limit, score_limit, cursor, to_start_time, id, name, dataset_id, filter)


List experiments with cursor-based pagination. Results are ordered by latest experiment activity descending.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**from_start_time** | **chrono::DateTime<chrono::FixedOffset>** | Retrieve only experiments on or after this datetime. | [required] |
**fields** | Option<**String**> | Comma-separated list of field groups to include. Available groups: `core`, `metadata`, `scores`. If omitted, `core` is returned. |  |
**limit** | Option<**i32**> | Number of experiments to return per page. Maximum 100, default 50. |  |
**score_limit** | Option<**i32**> | Number of scores to return per experiment when `fields=scores` is requested. Maximum 50, default 50. |  |
**cursor** | Option<**String**> | Versioned base64url cursor from the previous response page. |  |
**to_start_time** | Option<**chrono::DateTime<chrono::FixedOffset>**> | Retrieve only experiments before this datetime. |  |
**id** | Option<**String**> | Comma-separated list of experiment IDs. |  |
**name** | Option<**String**> | Comma-separated list of experiment names. |  |
**dataset_id** | Option<**String**> | Comma-separated list of dataset IDs. |  |
**filter** | Option<**String**> | JSON string containing an array of structured filter conditions. Supported columns are `id`, `name`, and `datasetId`. |  |

### Return type

[**models::ExperimentsResponse**](ExperimentsResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## experiments_list_items

> models::ExperimentItemsResponse experiments_list_items(from_start_time, fields, limit, score_limit, cursor, to_start_time, experiment_id, experiment_name, experiment_item_id, dataset_id, filter)


List experiment items with cursor-based pagination. Use this endpoint to export experiment item inputs, outputs, expected outputs, metadata, and optionally item/trace scores. Results are ordered by time descending.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**from_start_time** | **chrono::DateTime<chrono::FixedOffset>** | Retrieve only experiment items started on or after this datetime. | [required] |
**fields** | Option<**String**> | Comma-separated list of field groups to include. Available groups: `core`, `dataset`, `io`, `metadata`, `itemMetadata`, `experimentMetadata`, `scores`. If omitted, `core,dataset` is returned. |  |
**limit** | Option<**i32**> | Number of experiment items to return per page. Maximum 100, default 50. |  |
**score_limit** | Option<**i32**> | Number of scores to return per experiment item when `fields=scores` is requested. Maximum 50, default 50. |  |
**cursor** | Option<**String**> | Versioned base64url cursor from the previous response page. |  |
**to_start_time** | Option<**chrono::DateTime<chrono::FixedOffset>**> | Retrieve only experiment items started before this datetime. |  |
**experiment_id** | Option<**String**> | Comma-separated list of experiment IDs. |  |
**experiment_name** | Option<**String**> | Comma-separated list of experiment names. |  |
**experiment_item_id** | Option<**String**> | Comma-separated list of experiment item IDs. |  |
**dataset_id** | Option<**String**> | Comma-separated list of dataset IDs. |  |
**filter** | Option<**String**> | JSON string containing an array of structured filter conditions. Supported columns are `experimentId`, `experimentName`, `experimentItemId`, and `datasetId`. |  |

### Return type

[**models::ExperimentItemsResponse**](ExperimentItemsResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

