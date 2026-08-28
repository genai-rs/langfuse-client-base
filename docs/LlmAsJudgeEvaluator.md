# LlmAsJudgeEvaluator

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** | Stable identifier of this evaluator across all versions. | 
**name** | **String** | Human-readable evaluator name. Names are not identifiers and do not need to be unique. | 
**description** | Option<**String**> | Optional human-readable evaluator description. | 
**created_by** | [**models::Creator**](Creator.md) |  | 
**status** | [**models::EvaluatorStatus**](EvaluatorStatus.md) |  | 
**paused_at** | Option<**chrono::DateTime<chrono::FixedOffset>**> | Timestamp when the evaluator was paused, otherwise `null`. | 
**paused_reason** | Option<**String**> | Machine-readable reason when `status=paused`, otherwise `null`. | 
**paused_message** | Option<**String**> | Human-readable explanation when `status=paused`, otherwise `null`. | 
**evaluation_rule_assignments** | [**Vec<models::EvaluationRuleAssignment>**](EvaluationRuleAssignment.md) | All modern and legacy evaluation-rule assignments in newest-assignment-first order. Rule-specific mappings are exposed as `variableMappingOverride`; inherited defaults are omitted. | 
**created_at** | **chrono::DateTime<chrono::FixedOffset>** | Timestamp when the evaluator was created. | 
**updated_at** | **chrono::DateTime<chrono::FixedOffset>** | Timestamp when the evaluator was last updated. | 
**version_id** | **String** | Stable identifier of the latest evaluator version. | 
**version** | **i32** | Monotonically increasing latest evaluator version number. | 
**version_created_at** | **chrono::DateTime<chrono::FixedOffset>** | Timestamp when the latest evaluator version was created. | 
**version_created_by** | [**models::Creator**](Creator.md) |  | 
**r#type** | **String** | Evaluator type. | 
**prompt** | [**Vec<models::EvaluatorChatMessage>**](EvaluatorChatMessage.md) | A list containing exactly one user chat message. | 
**variables** | **Vec<String>** | Variables extracted from the latest prompt and available for evaluation-rule mappings. | 
**variable_mapping** | Option<[**Vec<models::PromptVariableMappingRead>**](PromptVariableMappingRead.md)> | Default variable mapping for the latest version, or `null` when no default is configured. | 
**model_config** | [**models::EvaluatorModelConfig**](EvaluatorModelConfig.md) |  | 
**output_definition** | [**models::PublicEvaluatorOutputDefinition**](PublicEvaluatorOutputDefinition.md) |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


