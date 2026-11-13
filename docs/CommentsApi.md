# \CommentsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**comments_create**](CommentsApi.md#comments_create) | **POST** /api/public/comments | 
[**comments_get**](CommentsApi.md#comments_get) | **GET** /api/public/comments | 
[**comments_get_by_id**](CommentsApi.md#comments_get_by_id) | **GET** /api/public/comments/{commentId} | 



## comments_create

> models::CreateCommentResponse comments_create(create_comment_request, options)


Create a comment. Comments may be attached to different object types (trace, observation, session, prompt).

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**create_comment_request** | [**CreateCommentRequest**](CreateCommentRequest.md) |  | [required] |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
comments_create().configuration(&configuration).create_comment_request(..).options(&options).call().await
```

### Return type

[**models::CreateCommentResponse**](CreateCommentResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## comments_get

> models::GetCommentsResponse comments_get(page, limit, object_type, object_id, author_user_id, options)


Get all comments

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**page** | Option<**i64**> | Page number, starts at 1. |  |
**limit** | Option<**i64**> | Limit of items per page. If you encounter api issues due to too large page sizes, try to reduce the limit |  |
**object_type** | Option<**String**> | Filter comments by object type (trace, observation, session, prompt). |  |
**object_id** | Option<**String**> | Filter comments by object id. If objectType is not provided, an error will be thrown. |  |
**author_user_id** | Option<**String**> | Filter comments by author user id. |  |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
comments_get().configuration(&configuration).options(&options).call().await
```

### Return type

[**models::GetCommentsResponse**](GetCommentsResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## comments_get_by_id

> models::Comment comments_get_by_id(comment_id, options)


Get a comment by id

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**comment_id** | **String** | The unique langfuse identifier of a comment | [required] |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
comments_get_by_id().configuration(&configuration).comment_id(..).options(&options).call().await
```

### Return type

[**models::Comment**](Comment.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

