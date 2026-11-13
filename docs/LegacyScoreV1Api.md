# \LegacyScoreV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**legacy_score_v1_delete**](LegacyScoreV1Api.md#legacy_score_v1_delete) | **DELETE** /api/public/scores/{scoreId} | 



## legacy_score_v1_delete

> legacy_score_v1_delete(score_id, options)


Delete a score (supports both trace and session scores)

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**score_id** | **String** | The unique langfuse identifier of a score | [required] |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
legacy_score_v1_delete().configuration(&configuration).score_id(..).options(&options).call().await
```

### Return type

 (empty response body)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

