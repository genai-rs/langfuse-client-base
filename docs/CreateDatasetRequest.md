# CreateDatasetRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **String** |  | 
**description** | Option<**String**> |  | [optional]
**metadata** | Option<[**serde_json::Value**](.md)> |  | [optional]
**input_schema** | Option<[**serde_json::Value**](.md)> | JSON Schema for validating dataset item inputs. When set, all new and existing dataset items will be validated against this schema. | [optional]
**expected_output_schema** | Option<[**serde_json::Value**](.md)> | JSON Schema for validating dataset item expected outputs. When set, all new and existing dataset items will be validated against this schema. | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


