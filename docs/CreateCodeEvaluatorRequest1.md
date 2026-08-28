# CreateCodeEvaluatorRequest1

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **String** | Human-readable evaluator name. Names are not identifiers and do not need to be unique. | 
**description** | Option<**String**> | Optional human-readable evaluator description. | [optional]
**r#type** | **Type** |  (enum: code) | 
**source_code** | **String** | Source code executed for each matched observation. | 
**source_code_language** | [**models::CodeEvaluatorSourceCodeLanguage**](CodeEvaluatorSourceCodeLanguage.md) |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


