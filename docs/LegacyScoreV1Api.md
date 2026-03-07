# \LegacyScoreV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**legacy_score_v1_create**](LegacyScoreV1Api.md#legacy_score_v1_create) | **POST** /api/public/scores | 
[**legacy_score_v1_delete**](LegacyScoreV1Api.md#legacy_score_v1_delete) | **DELETE** /api/public/scores/{scoreId} | 



## legacy_score_v1_create

> models::LegacyCreateScoreResponse legacy_score_v1_create(legacy_create_score_request)


Create a score (supports both trace and session scores)

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**legacy_create_score_request** | [**LegacyCreateScoreRequest**](LegacyCreateScoreRequest.md) |  | [required] |

### Return type

[**models::LegacyCreateScoreResponse**](legacyCreateScoreResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## legacy_score_v1_delete

> legacy_score_v1_delete(score_id)


Delete a score (supports both trace and session scores)

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**score_id** | **String** | The unique langfuse identifier of a score | [required] |

### Return type

 (empty response body)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

