# \ScoreConfigsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**score_configs_create**](ScoreConfigsApi.md#score_configs_create) | **POST** /api/public/score-configs | 
[**score_configs_get**](ScoreConfigsApi.md#score_configs_get) | **GET** /api/public/score-configs | 
[**score_configs_get_by_id**](ScoreConfigsApi.md#score_configs_get_by_id) | **GET** /api/public/score-configs/{configId} | 
[**score_configs_update**](ScoreConfigsApi.md#score_configs_update) | **PATCH** /api/public/score-configs/{configId} | 



## score_configs_create

> models::ScoreConfig score_configs_create(create_score_config_request, options)


Create a score configuration (config). Score configs are used to define the structure of scores

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**create_score_config_request** | [**CreateScoreConfigRequest**](CreateScoreConfigRequest.md) |  | [required] |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
score_configs_create().configuration(&configuration).create_score_config_request(..).options(&options).call().await
```

### Return type

[**models::ScoreConfig**](ScoreConfig.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## score_configs_get

> models::ScoreConfigs score_configs_get(page, limit, options)


Get all score configs

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**page** | Option<**i64**> | Page number, starts at 1. |  |
**limit** | Option<**i64**> | Limit of items per page. If you encounter api issues due to too large page sizes, try to reduce the limit |  |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
score_configs_get().configuration(&configuration).options(&options).call().await
```

### Return type

[**models::ScoreConfigs**](ScoreConfigs.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## score_configs_get_by_id

> models::ScoreConfig score_configs_get_by_id(config_id, options)


Get a score config

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**config_id** | **String** | The unique langfuse identifier of a score config | [required] |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
score_configs_get_by_id().configuration(&configuration).config_id(..).options(&options).call().await
```

### Return type

[**models::ScoreConfig**](ScoreConfig.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## score_configs_update

> models::ScoreConfig score_configs_update(config_id, update_score_config_request, options)


Update a score config

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**config_id** | **String** | The unique langfuse identifier of a score config | [required] |
**update_score_config_request** | [**UpdateScoreConfigRequest**](UpdateScoreConfigRequest.md) |  | [required] |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
score_configs_update().configuration(&configuration).config_id(..).update_score_config_request(..).options(&options).call().await
```

### Return type

[**models::ScoreConfig**](ScoreConfig.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

