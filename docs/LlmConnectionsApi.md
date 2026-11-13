# \LlmConnectionsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**llm_connections_delete**](LlmConnectionsApi.md#llm_connections_delete) | **DELETE** /api/public/llm-connections/{id} | 
[**llm_connections_delete_organization**](LlmConnectionsApi.md#llm_connections_delete_organization) | **DELETE** /api/public/organizations/llm-connections/{id} | 
[**llm_connections_list**](LlmConnectionsApi.md#llm_connections_list) | **GET** /api/public/llm-connections | 
[**llm_connections_list_organization**](LlmConnectionsApi.md#llm_connections_list_organization) | **GET** /api/public/organizations/llm-connections | 
[**llm_connections_upsert**](LlmConnectionsApi.md#llm_connections_upsert) | **PUT** /api/public/llm-connections | 
[**llm_connections_upsert_organization**](LlmConnectionsApi.md#llm_connections_upsert_organization) | **PUT** /api/public/organizations/llm-connections | 



## llm_connections_delete

> models::DeleteLlmConnectionResponse llm_connections_delete(id, options)


Delete an LLM connection by id. Evaluators that depend on the deleted connection are automatically paused.

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**id** | **String** |  | [required] |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
llm_connections_delete().configuration(&configuration).id(..).options(&options).call().await
```

### Return type

[**models::DeleteLlmConnectionResponse**](DeleteLlmConnectionResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## llm_connections_delete_organization

> models::DeleteLlmConnectionResponse llm_connections_delete_organization(id, options)


Delete an organization-level LLM connection by id. Evaluators in projects without an override for the provider are automatically paused. Requires an organization-scoped API key.

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**id** | **String** |  | [required] |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
llm_connections_delete_organization().configuration(&configuration).id(..).options(&options).call().await
```

### Return type

[**models::DeleteLlmConnectionResponse**](DeleteLlmConnectionResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## llm_connections_list

> models::PaginatedLlmConnections llm_connections_list(page, limit, options)


Get all LLM connections in a project

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**page** | Option<**i64**> | page number, starts at 1 |  |
**limit** | Option<**i64**> | limit of items per page |  |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
llm_connections_list().configuration(&configuration).options(&options).call().await
```

### Return type

[**models::PaginatedLlmConnections**](PaginatedLlmConnections.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## llm_connections_list_organization

> models::PaginatedLlmConnections llm_connections_list_organization(page, limit, options)


Get all organization-level LLM connections. Requires an organization-scoped API key.

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**page** | Option<**i64**> | page number, starts at 1 |  |
**limit** | Option<**i64**> | limit of items per page |  |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
llm_connections_list_organization().configuration(&configuration).options(&options).call().await
```

### Return type

[**models::PaginatedLlmConnections**](PaginatedLlmConnections.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## llm_connections_upsert

> models::LlmConnection llm_connections_upsert(upsert_llm_connection_request, options)


Create or update an LLM connection. The connection is upserted on provider.

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**upsert_llm_connection_request** | [**UpsertLlmConnectionRequest**](UpsertLlmConnectionRequest.md) |  | [required] |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
llm_connections_upsert().configuration(&configuration).upsert_llm_connection_request(..).options(&options).call().await
```

### Return type

[**models::LlmConnection**](LlmConnection.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## llm_connections_upsert_organization

> models::LlmConnection llm_connections_upsert_organization(upsert_llm_connection_request, options)


Create or update an organization-level LLM connection. The connection is upserted on provider and inherited by projects without a provider override. Requires an organization-scoped API key.

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**upsert_llm_connection_request** | [**UpsertLlmConnectionRequest**](UpsertLlmConnectionRequest.md) |  | [required] |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
llm_connections_upsert_organization().configuration(&configuration).upsert_llm_connection_request(..).options(&options).call().await
```

### Return type

[**models::LlmConnection**](LlmConnection.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

