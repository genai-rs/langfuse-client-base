# \BlobStorageIntegrationsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**blob_storage_integrations_delete_blob_storage_integration**](BlobStorageIntegrationsApi.md#blob_storage_integrations_delete_blob_storage_integration) | **DELETE** /api/public/integrations/blob-storage/{id} | 
[**blob_storage_integrations_get_blob_storage_integrations**](BlobStorageIntegrationsApi.md#blob_storage_integrations_get_blob_storage_integrations) | **GET** /api/public/integrations/blob-storage | 
[**blob_storage_integrations_upsert_blob_storage_integration**](BlobStorageIntegrationsApi.md#blob_storage_integrations_upsert_blob_storage_integration) | **PUT** /api/public/integrations/blob-storage | 



## blob_storage_integrations_delete_blob_storage_integration

> models::BlobStorageIntegrationDeletionResponse blob_storage_integrations_delete_blob_storage_integration(id)


Delete a blob storage integration by ID (requires organization-scoped API key)

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**id** | **String** |  | [required] |

### Return type

[**models::BlobStorageIntegrationDeletionResponse**](BlobStorageIntegrationDeletionResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## blob_storage_integrations_get_blob_storage_integrations

> models::BlobStorageIntegrationsResponse blob_storage_integrations_get_blob_storage_integrations()


Get all blob storage integrations for the organization (requires organization-scoped API key)

### Parameters

This endpoint does not need any parameter.

### Return type

[**models::BlobStorageIntegrationsResponse**](BlobStorageIntegrationsResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## blob_storage_integrations_upsert_blob_storage_integration

> models::BlobStorageIntegrationResponse blob_storage_integrations_upsert_blob_storage_integration(create_blob_storage_integration_request)


Create or update a blob storage integration for a specific project (requires organization-scoped API key). The configuration is validated by performing a test upload to the bucket.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**create_blob_storage_integration_request** | [**CreateBlobStorageIntegrationRequest**](CreateBlobStorageIntegrationRequest.md) |  | [required] |

### Return type

[**models::BlobStorageIntegrationResponse**](BlobStorageIntegrationResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

