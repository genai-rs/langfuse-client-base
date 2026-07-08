# CreateBlobStorageIntegrationRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_id** | **String** | ID of the project in which to configure the blob storage integration | 
**r#type** | [**models::BlobStorageIntegrationType**](BlobStorageIntegrationType.md) |  | 
**bucket_name** | **String** | Name of the storage bucket. For AZURE_BLOB_STORAGE, must be a valid Azure container name (3-63 chars, lowercase letters, numbers, and hyphens only, must start and end with a letter or number, no consecutive hyphens). | 
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
**export_start_date** | Option<**chrono::DateTime<chrono::FixedOffset>**> | Custom start date for exports (required when exportMode is FROM_CUSTOM_DATE). Must not be in the future (27 h tolerance for timezone differences). | [optional]
**compressed** | Option<**bool**> | Enable gzip compression for exported files (.csv.gz, .json.gz, .jsonl.gz). Defaults to true. | [optional]
**export_source** | Option<[**models::BlobStorageExportSource**](BlobStorageExportSource.md)> |  | [optional]
**export_field_groups** | Option<[**Vec<models::BlobStorageExportFieldGroup>**](BlobStorageExportFieldGroup.md)> | Field groups to include in each exported observation row. Applies to all export sources; must include `core` if provided. When omitted on create, the column default (all groups) applies. When omitted on update, the existing value is preserved.  `exportFieldGroups` requires `exportSource` to be provided in the same request. | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


