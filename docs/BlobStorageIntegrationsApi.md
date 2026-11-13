# \BlobStorageIntegrationsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**blob_storage_integrations_delete_blob_storage_integration**](BlobStorageIntegrationsApi.md#blob_storage_integrations_delete_blob_storage_integration) | **DELETE** /api/public/integrations/blob-storage/{id} | 
[**blob_storage_integrations_get_blob_storage_integration_status**](BlobStorageIntegrationsApi.md#blob_storage_integrations_get_blob_storage_integration_status) | **GET** /api/public/integrations/blob-storage/{id} | 
[**blob_storage_integrations_get_blob_storage_integrations**](BlobStorageIntegrationsApi.md#blob_storage_integrations_get_blob_storage_integrations) | **GET** /api/public/integrations/blob-storage | 
[**blob_storage_integrations_upsert_blob_storage_integration**](BlobStorageIntegrationsApi.md#blob_storage_integrations_upsert_blob_storage_integration) | **PUT** /api/public/integrations/blob-storage | 



## blob_storage_integrations_delete_blob_storage_integration

> models::BlobStorageIntegrationDeletionResponse blob_storage_integrations_delete_blob_storage_integration(id, options)


Delete a blob storage integration by ID (requires organization-scoped API key)

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**id** | **String** |  | [required] |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
blob_storage_integrations_delete_blob_storage_integration().configuration(&configuration).id(..).options(&options).call().await
```

### Return type

[**models::BlobStorageIntegrationDeletionResponse**](BlobStorageIntegrationDeletionResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## blob_storage_integrations_get_blob_storage_integration_status

> models::BlobStorageIntegrationStatusResponse blob_storage_integrations_get_blob_storage_integration_status(id, options)


Get the sync status of a blob storage integration by integration ID (requires organization-scoped API key)

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**id** | **String** |  | [required] |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
blob_storage_integrations_get_blob_storage_integration_status().configuration(&configuration).id(..).options(&options).call().await
```

### Return type

[**models::BlobStorageIntegrationStatusResponse**](BlobStorageIntegrationStatusResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## blob_storage_integrations_get_blob_storage_integrations

> models::BlobStorageIntegrationsResponse blob_storage_integrations_get_blob_storage_integrations(options)


Get all blob storage integrations for the organization (requires organization-scoped API key)

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
blob_storage_integrations_get_blob_storage_integrations().configuration(&configuration).options(&options).call().await
```

### Return type

[**models::BlobStorageIntegrationsResponse**](BlobStorageIntegrationsResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## blob_storage_integrations_upsert_blob_storage_integration

> models::BlobStorageIntegrationResponse blob_storage_integrations_upsert_blob_storage_integration(create_blob_storage_integration_request, options)


Create or update a blob storage integration for a specific project (requires organization-scoped API key). The configuration is validated by performing a test upload to the bucket.

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**create_blob_storage_integration_request** | [**CreateBlobStorageIntegrationRequest**](CreateBlobStorageIntegrationRequest.md) |  | [required] |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
blob_storage_integrations_upsert_blob_storage_integration().configuration(&configuration).create_blob_storage_integration_request(..).options(&options).call().await
```

### Return type

[**models::BlobStorageIntegrationResponse**](BlobStorageIntegrationResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

