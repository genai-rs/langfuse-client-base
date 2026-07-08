# BlobStorageIntegrationResponse

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** |  | 
**project_id** | **String** |  | 
**r#type** | [**models::BlobStorageIntegrationType**](BlobStorageIntegrationType.md) |  | 
**bucket_name** | **String** |  | 
**endpoint** | Option<**String**> |  | 
**region** | **String** |  | 
**access_key_id** | Option<**String**> |  | 
**prefix** | **String** |  | 
**export_frequency** | [**models::BlobStorageExportFrequency**](BlobStorageExportFrequency.md) |  | 
**enabled** | **bool** |  | 
**force_path_style** | **bool** |  | 
**file_type** | [**models::BlobStorageIntegrationFileTypeResponse**](BlobStorageIntegrationFileTypeResponse.md) |  | 
**export_mode** | [**models::BlobStorageExportMode**](BlobStorageExportMode.md) |  | 
**export_start_date** | Option<**chrono::DateTime<chrono::FixedOffset>**> |  | 
**compressed** | **bool** |  | 
**export_source** | [**models::BlobStorageExportSource**](BlobStorageExportSource.md) |  | 
**export_field_groups** | Option<[**Vec<models::BlobStorageExportFieldGroup>**](BlobStorageExportFieldGroup.md)> | Field groups included in each exported observation row. An empty list is treated as all groups during export. | 
**next_sync_at** | Option<**chrono::DateTime<chrono::FixedOffset>**> |  | 
**last_sync_at** | Option<**chrono::DateTime<chrono::FixedOffset>**> |  | 
**last_error** | Option<**String**> |  | 
**last_error_at** | Option<**chrono::DateTime<chrono::FixedOffset>**> |  | 
**created_at** | **chrono::DateTime<chrono::FixedOffset>** |  | 
**updated_at** | **chrono::DateTime<chrono::FixedOffset>** |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


