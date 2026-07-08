# DatasetItem

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** |  | 
**status** | [**models::DatasetStatus**](DatasetStatus.md) |  | 
**input** | Option<**serde_json::Value**> | Input data for the dataset item | 
**expected_output** | Option<**serde_json::Value**> | Expected output for the dataset item | 
**metadata** | Option<**serde_json::Value**> | Metadata associated with the dataset item | 
**source_trace_id** | Option<**String**> | The trace ID that sourced this dataset item | 
**source_observation_id** | Option<**String**> | The observation ID that sourced this dataset item | 
**dataset_id** | **String** |  | 
**dataset_name** | **String** |  | 
**created_at** | **chrono::DateTime<chrono::FixedOffset>** |  | 
**updated_at** | **chrono::DateTime<chrono::FixedOffset>** |  | 
**media_references** | [**Vec<models::DatasetItemMediaReference>**](DatasetItemMediaReference.md) | Resolved Langfuse media references found in input, expectedOutput, and metadata. | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


