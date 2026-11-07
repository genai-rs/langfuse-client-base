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
**auth_type** | [**models::BlobStorageIntegrationAuthType**](BlobStorageIntegrationAuthType.md) |  | 
**access_key_id** | Option<**String**> |  | 
**role_arn** | Option<**String**> | IAM role Langfuse assumes. May be set while `authType` is `ACCESS_KEYS` if the integration used `ROLE_ARN` before. | 
**external_id** | Option<**String**> | External ID Langfuse passes when assuming `roleArn`. Require it in the role's trust policy with an `sts:ExternalId` condition. Null until the integration first uses `ROLE_ARN`. | 
**cross_account_role_arn** | Option<**String**> | Langfuse role that must be trusted by `roleArn`. Null when the deployment does not support IAM role auth or the organization is not on an Enterprise plan. | 
**prefix** | **String** |  | 
**export_frequency** | [**models::BlobStorageExportFrequency**](BlobStorageExportFrequency.md) |  | 
**enabled** | **bool** |  | 
**force_path_style** | **bool** |  | 
**file_type** | [**models::BlobStorageIntegrationFileTypeResponse**](BlobStorageIntegrationFileTypeResponse.md) |  | 
**export_mode** | [**models::BlobStorageExportMode**](BlobStorageExportMode.md) |  | 
**export_start_date** | Option<**chrono::DateTime<chrono::FixedOffset>**> |  | 
**compressed** | **bool** |  | 
**export_source** | [**models::BlobStorageExportSource**](BlobStorageExportSource.md) |  | 
**export_field_groups** | Option<[**Vec<models::BlobStorageExportFieldGroup>**](BlobStorageExportFieldGroup.md)> | Field groups included in each exported observation and score row. An empty list is treated as all observation groups and no score groups during export. Core score columns are always exported. | 
**next_sync_at** | Option<**chrono::DateTime<chrono::FixedOffset>**> |  | 
**last_sync_at** | Option<**chrono::DateTime<chrono::FixedOffset>**> |  | 
**last_error** | Option<**String**> |  | 
**last_error_at** | Option<**chrono::DateTime<chrono::FixedOffset>**> |  | 
**created_at** | **chrono::DateTime<chrono::FixedOffset>** |  | 
**updated_at** | **chrono::DateTime<chrono::FixedOffset>** |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


