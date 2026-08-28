# UpdateLlmAsJudgeEvaluatorRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | Option<**String**> | New human-readable evaluator name. | [optional]
**description** | Option<**String**> | New description. Set to `null` to clear it. | [optional]
**r#type** | **String** | Evaluator type. The type of an existing evaluator cannot change. | 
**prompt** | [**models::EvaluatorChatPromptInput**](EvaluatorChatPromptInput.md) |  | 
**model_config** | Option<[**models::EvaluatorModelConfig**](EvaluatorModelConfig.md)> |  | [optional]
**variable_mapping** | Option<[**Vec<models::PromptVariableMappingInput>**](PromptVariableMappingInput.md)> | Complete replacement default variable mapping, or `null` when no default is configured. | [optional]
**output_definition** | [**models::EvaluatorOutputDefinition**](EvaluatorOutputDefinition.md) |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


