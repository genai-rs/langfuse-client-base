# Dataset

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** |  | 
**name** | **String** |  | 
**description** | Option<**String**> | Description of the dataset | 
**metadata** | Option<**serde_json::Value**> | Metadata associated with the dataset | 
**input_schema** | Option<**std::collections::HashMap<String, serde_json::Value>**> | JSON Schema for validating dataset item inputs | 
**expected_output_schema** | Option<**std::collections::HashMap<String, serde_json::Value>**> | JSON Schema for validating dataset item expected outputs | 
**project_id** | **String** |  | 
**created_at** | **jiff::Timestamp** |  | 
**updated_at** | **jiff::Timestamp** |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


