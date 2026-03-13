# BlobStorageIntegrationStatusResponse

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** |  | 
**project_id** | **String** |  | 
**sync_status** | [**models::BlobStorageSyncStatus**](BlobStorageSyncStatus.md) |  | 
**enabled** | **bool** |  | 
**last_sync_at** | Option<**String**> | End of the last successfully exported time window. Compare against your ETL bookmark to determine if new data is available. Null if the integration has never synced. | [optional]
**next_sync_at** | Option<**String**> | When the next export is scheduled. Null if no sync has occurred yet. | [optional]
**last_error** | Option<**String**> | Raw error message from the storage provider (S3/Azure/GCS) if the last export failed. Cleared on successful export. | [optional]
**last_error_at** | Option<**String**> | When the last error occurred. Cleared on successful export. | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


