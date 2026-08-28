# LlmAsJudgeEvaluatorVersion

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** | Stable identifier of this evaluator version. | 
**version** | **i32** | Monotonically increasing evaluator version number. | 
**created_at** | **chrono::DateTime<chrono::FixedOffset>** | Timestamp when this evaluator version was created. | 
**created_by** | [**models::Creator**](Creator.md) |  | 
**r#type** | **String** | Evaluator type. | 
**prompt** | [**Vec<models::EvaluatorChatMessage>**](EvaluatorChatMessage.md) | A list containing exactly one user chat message. | 
**variables** | **Vec<String>** | Variables extracted from the prompt and available for evaluation-rule mappings.  Every variable must be mapped exactly once when a rule provides an explicit mapping. | 
**variable_mapping** | Option<[**Vec<models::PromptVariableMappingRead>**](PromptVariableMappingRead.md)> | Default variable mapping for this evaluator version, or `null` when no default is configured. | 
**model_config** | [**models::EvaluatorModelConfig**](EvaluatorModelConfig.md) |  | 
**output_definition** | [**models::PublicEvaluatorOutputDefinition**](PublicEvaluatorOutputDefinition.md) |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


