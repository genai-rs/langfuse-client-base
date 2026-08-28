# LegacyPromptVariableMapping

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**mapping_type** | **String** | Explicitly marks this as a legacy mapping. | 
**variable** | **String** | Prompt variable name without braces. | 
**langfuse_object** | [**models::LegacyEvaluationObject**](LegacyEvaluationObject.md) |  | 
**object_name** | Option<**String**> | Observation name to match, or `null` when `langfuseObject` is `trace` or `dataset_item`. | 
**source** | **String** | Field selected from the legacy object. | 
**json_path** | Option<**String**> | Optional JSONPath selector applied to the selected field. | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


