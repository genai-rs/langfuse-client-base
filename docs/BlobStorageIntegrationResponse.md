# BlobStorageIntegrationResponse

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** |  | 
**project_id** | **String** |  | 
**r#type** | [**models::BlobStorageIntegrationType**](BlobStorageIntegrationType.md) |  | 
**bucket_name** | **String** |  | 
**endpoint** | Option<**String**> |  | [optional]
**region** | **String** |  | 
**access_key_id** | Option<**String**> |  | [optional]
**prefix** | **String** |  | 
**export_frequency** | [**models::BlobStorageExportFrequency**](BlobStorageExportFrequency.md) |  | 
**enabled** | **bool** |  | 
**force_path_style** | **bool** |  | 
**file_type** | [**models::BlobStorageIntegrationFileType**](BlobStorageIntegrationFileType.md) |  | 
**export_mode** | [**models::BlobStorageExportMode**](BlobStorageExportMode.md) |  | 
**export_start_date** | Option<**chrono::DateTime<chrono::FixedOffset>**> |  | [optional]
**compressed** | **bool** |  | 
**export_source** | [**models::BlobStorageExportSource**](BlobStorageExportSource.md) |  | 
**export_field_groups** | Option<[**Vec<models::BlobStorageExportFieldGroup>**](BlobStorageExportFieldGroup.md)> | Field groups included in each exported row for `EVENTS` / `TRACES_OBSERVATIONS_EVENTS` sources. Always `null` when exportSource is `TRACES_OBSERVATIONS` (the field does not apply to that source; any legacy DB value is hidden from the public surface). | [optional]
**next_sync_at** | Option<**chrono::DateTime<chrono::FixedOffset>**> |  | [optional]
**last_sync_at** | Option<**chrono::DateTime<chrono::FixedOffset>**> |  | [optional]
**last_error** | Option<**String**> |  | [optional]
**last_error_at** | Option<**chrono::DateTime<chrono::FixedOffset>**> |  | [optional]
**created_at** | **chrono::DateTime<chrono::FixedOffset>** |  | 
**updated_at** | **chrono::DateTime<chrono::FixedOffset>** |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


