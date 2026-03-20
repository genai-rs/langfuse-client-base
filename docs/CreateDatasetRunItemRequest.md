# CreateDatasetRunItemRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**run_name** | **String** |  | 
**run_description** | Option<**String**> | Description of the run. If run exists, description will be updated. | [optional]
**metadata** | Option<**serde_json::Value**> | Metadata of the dataset run, updates run if run already exists | [optional]
**dataset_item_id** | **String** |  | 
**observation_id** | Option<**String**> |  | [optional]
**trace_id** | Option<**String**> | traceId should always be provided. For compatibility with older SDK versions it can also be inferred from the provided observationId. | [optional]
**dataset_version** | Option<**String**> | ISO 8601 timestamp (RFC 3339, Section 5.6) in UTC (e.g., \"2026-01-21T14:35:42Z\"). Specifies the dataset version to use for this experiment run.  If provided, the experiment will use dataset items as they existed at or before this timestamp. If not provided, uses the latest version of dataset items. | [optional]
**created_at** | Option<**String**> | Optional timestamp to set the createdAt field of the dataset run item. If not provided or null, defaults to current timestamp. | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


