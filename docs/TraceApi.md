# \TraceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**trace_delete**](TraceApi.md#trace_delete) | **DELETE** /api/public/traces/{traceId} | 
[**trace_delete_multiple**](TraceApi.md#trace_delete_multiple) | **DELETE** /api/public/traces | 



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

