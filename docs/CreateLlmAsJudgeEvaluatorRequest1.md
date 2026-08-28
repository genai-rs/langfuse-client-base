# CreateLlmAsJudgeEvaluatorRequest1

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **String** | Human-readable evaluator name. Names are not identifiers and do not need to be unique. | 
**description** | Option<**String**> | Optional human-readable evaluator description. | [optional]
**r#type** | **Type** |  (enum: llm_as_judge) | 
**prompt** | [**models::EvaluatorChatPromptInput**](EvaluatorChatPromptInput.md) |  | 
**model_config** | Option<[**models::EvaluatorModelConfig**](EvaluatorModelConfig.md)> |  | [optional]
**variable_mapping** | Option<[**Vec<models::PromptVariableMappingInput>**](PromptVariableMappingInput.md)> | Default prompt-variable mapping, or `null` when no default is configured. | [optional]
**output_definition** | [**models::EvaluatorOutputDefinition**](EvaluatorOutputDefinition.md) |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


