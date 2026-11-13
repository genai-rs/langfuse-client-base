# \DatasetsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**datasets_create**](DatasetsApi.md#datasets_create) | **POST** /api/public/v2/datasets | 
[**datasets_delete_run**](DatasetsApi.md#datasets_delete_run) | **DELETE** /api/public/datasets/{datasetName}/runs/{runName} | 
[**datasets_get**](DatasetsApi.md#datasets_get) | **GET** /api/public/v2/datasets/{datasetName} | 
[**datasets_get_run**](DatasetsApi.md#datasets_get_run) | **GET** /api/public/datasets/{datasetName}/runs/{runName} | 
[**datasets_get_runs**](DatasetsApi.md#datasets_get_runs) | **GET** /api/public/datasets/{datasetName}/runs | 
[**datasets_list**](DatasetsApi.md#datasets_list) | **GET** /api/public/v2/datasets | 



## datasets_create

> models::Dataset datasets_create(create_dataset_request, options)


Create a dataset

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**create_dataset_request** | [**CreateDatasetRequest**](CreateDatasetRequest.md) |  | [required] |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
datasets_create().configuration(&configuration).create_dataset_request(..).options(&options).call().await
```

### Return type

[**models::Dataset**](Dataset.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## datasets_delete_run

> models::DeleteDatasetRunResponse datasets_delete_run(dataset_name, run_name, options)


**Deprecated:** On Langfuse Cloud, Langfuse v3 is deprecated and this endpoint will be removed on November 16, 2026. In Langfuse v4, dataset runs are replaced by experiments. Self-hosted deployments are unaffected by this date; the endpoint becomes unavailable when they upgrade to Langfuse v4. See the [Langfuse v3 to v4 upgrade guide](https://langfuse.com/self-hosting/upgrade/upgrade-guides/upgrade-v3-to-v4).  Delete a dataset run and all its run items. This action is irreversible.

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**dataset_name** | **String** |  | [required] |
**run_name** | **String** |  | [required] |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
datasets_delete_run().configuration(&configuration).dataset_name(..).run_name(..).options(&options).call().await
```

### Return type

[**models::DeleteDatasetRunResponse**](DeleteDatasetRunResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## datasets_get

> models::Dataset datasets_get(dataset_name, options)


Get a dataset

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**dataset_name** | **String** |  | [required] |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
datasets_get().configuration(&configuration).dataset_name(..).options(&options).call().await
```

### Return type

[**models::Dataset**](Dataset.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## datasets_get_run

> models::DatasetRunWithItems datasets_get_run(dataset_name, run_name, options)


**Deprecated:** On Langfuse Cloud, Langfuse v3 is deprecated and this endpoint will be removed on November 16, 2026. In Langfuse v4, dataset runs are replaced by experiments; use GET /api/public/experiments instead. Self-hosted deployments are unaffected by this date; the endpoint becomes unavailable when they upgrade to Langfuse v4. See the [Langfuse v3 to v4 upgrade guide](https://langfuse.com/self-hosting/upgrade/upgrade-guides/upgrade-v3-to-v4).  Get a dataset run and its items

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**dataset_name** | **String** |  | [required] |
**run_name** | **String** |  | [required] |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
datasets_get_run().configuration(&configuration).dataset_name(..).run_name(..).options(&options).call().await
```

### Return type

[**models::DatasetRunWithItems**](DatasetRunWithItems.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## datasets_get_runs

> models::PaginatedDatasetRuns datasets_get_runs(dataset_name, page, limit, options)


**Deprecated:** On Langfuse Cloud, Langfuse v3 is deprecated and this endpoint will be removed on November 16, 2026. In Langfuse v4, dataset runs are replaced by experiments; use GET /api/public/experiments instead. Self-hosted deployments are unaffected by this date; the endpoint becomes unavailable when they upgrade to Langfuse v4. See the [Langfuse v3 to v4 upgrade guide](https://langfuse.com/self-hosting/upgrade/upgrade-guides/upgrade-v3-to-v4).  Get dataset runs

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**dataset_name** | **String** |  | [required] |
**page** | Option<**i64**> | page number, starts at 1 |  |
**limit** | Option<**i64**> | limit of items per page |  |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
datasets_get_runs().configuration(&configuration).dataset_name(..).options(&options).call().await
```

### Return type

[**models::PaginatedDatasetRuns**](PaginatedDatasetRuns.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## datasets_list

> models::PaginatedDatasets datasets_list(page, limit, options)


Get all datasets

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**page** | Option<**i64**> | page number, starts at 1 |  |
**limit** | Option<**i64**> | limit of items per page |  |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
datasets_list().configuration(&configuration).options(&options).call().await
```

### Return type

[**models::PaginatedDatasets**](PaginatedDatasets.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

