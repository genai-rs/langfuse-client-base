# CreateBlobStorageIntegrationRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_id** | **String** | ID of the project in which to configure the blob storage integration | 
**r#type** | [**models::BlobStorageIntegrationType**](BlobStorageIntegrationType.md) |  | 
**bucket_name** | **String** | Name of the storage bucket | 
**endpoint** | Option<**String**> | Custom endpoint URL (required for S3_COMPATIBLE type) | [optional]
**region** | **String** | Storage region | 
**access_key_id** | Option<**String**> | Access key ID for authentication | [optional]
**secret_access_key** | Option<**String**> | Secret access key for authentication (will be encrypted when stored) | [optional]
**prefix** | Option<**String**> | Path prefix for exported files (must end with forward slash if provided) | [optional]
**export_frequency** | [**models::BlobStorageExportFrequency**](BlobStorageExportFrequency.md) |  | 
**enabled** | **bool** | Whether the integration is active | 
**force_path_style** | **bool** | Use path-style URLs for S3 requests | 
**file_type** | [**models::BlobStorageIntegrationFileType**](BlobStorageIntegrationFileType.md) |  | 
**export_mode** | [**models::BlobStorageExportMode**](BlobStorageExportMode.md) |  | 
**export_start_date** | Option<**String**> | Custom start date for exports (required when exportMode is FROM_CUSTOM_DATE) | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


