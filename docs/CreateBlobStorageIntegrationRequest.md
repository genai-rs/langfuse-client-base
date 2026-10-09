# CreateBlobStorageIntegrationRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_id** | **String** | ID of the project in which to configure the blob storage integration | 
**r#type** | [**models::BlobStorageIntegrationType**](BlobStorageIntegrationType.md) |  | 
**bucket_name** | **String** | Name of the storage bucket. For AZURE_BLOB_STORAGE, must be a valid Azure container name (3-63 chars, lowercase letters, numbers, and hyphens only, must start and end with a letter or number, no consecutive hyphens). For GOOGLE_CLOUD_STORAGE with default credentials, the bucket must be listed in `LANGFUSE_BLOB_STORAGE_GCS_ALLOWED_BUCKETS`. | 
**endpoint** | Option<**String**> | Custom endpoint URL (required for S3_COMPATIBLE type). Ignored for GOOGLE_CLOUD_STORAGE. | [optional]
**region** | **String** | Storage region used by S3-compatible clients (AWS, GCS, Cloudflare R2, MinIO, Azure location IDs such as eastus, OCI). Leading and trailing whitespace is removed. The remaining value must be 1-63 letters, numbers, or hyphens, and cannot start or end with a hyphen. Examples: us-east-1, europe-west1, eastus, auto. Not used by GOOGLE_CLOUD_STORAGE; pass auto. | 
**access_key_id** | Option<**String**> | Access key ID for authentication. Not used for GOOGLE_CLOUD_STORAGE. | [optional]
**secret_access_key** | Option<**String**> | Secret access key for authentication (will be encrypted when stored). When omitted on update, the stored secret is kept, unless the type changes between GOOGLE_CLOUD_STORAGE and another type.  For GOOGLE_CLOUD_STORAGE, a GCP service account JSON key. On self-hosted deployments, pass `__GCS_DEFAULT_CREDENTIALS__` instead to use the deployment's Application Default Credentials; the bucket must then be listed in `LANGFUSE_BLOB_STORAGE_GCS_ALLOWED_BUCKETS`. Default credentials are not available on Langfuse Cloud. | [optional]
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


