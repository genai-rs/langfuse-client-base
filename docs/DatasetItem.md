# DatasetItem

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** |  | 
**status** | [**models::DatasetStatus**](DatasetStatus.md) |  | 
**input** | Option<[**serde_json::Value**](.md)> | Input data for the dataset item | 
**expected_output** | Option<[**serde_json::Value**](.md)> | Expected output for the dataset item | 
**metadata** | Option<[**serde_json::Value**](.md)> | Metadata associated with the dataset item | 
**source_trace_id** | Option<**String**> | The trace ID that sourced this dataset item | [optional]
**source_observation_id** | Option<**String**> | The observation ID that sourced this dataset item | [optional]
**dataset_id** | **String** |  | 
**dataset_name** | **String** |  | 
**created_at** | **String** |  | 
**updated_at** | **String** |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


