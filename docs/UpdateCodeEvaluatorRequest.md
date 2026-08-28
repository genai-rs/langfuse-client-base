# UpdateCodeEvaluatorRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | Option<**String**> | New human-readable evaluator name. | [optional]
**description** | Option<**String**> | New description. Set to `null` to clear it. | [optional]
**r#type** | **String** | Evaluator type. The type of an existing evaluator cannot change. | 
**source_code** | **String** | Complete replacement source code. | 
**source_code_language** | [**models::CodeEvaluatorSourceCodeLanguage**](CodeEvaluatorSourceCodeLanguage.md) |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


