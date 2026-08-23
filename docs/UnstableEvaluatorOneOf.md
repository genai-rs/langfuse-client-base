# UnstableEvaluatorOneOf

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** | Stable identifier of this evaluator across all versions. | 
**name** | **String** | Evaluator name. | 
**version** | **i32** | Version number of this evaluator. | 
**variables** | **Vec<String>** | Variables that can be mapped when creating an evaluation rule.  LLM evaluators require every variable to be mapped exactly once. Code evaluators always expose the fixed runtime payload fields and Langfuse maps them automatically. | 
**mapping** | Option<[**Vec<models::UnstableEvaluationRuleReadMapping>**](UnstableEvaluationRuleReadMapping.md)> | Default variable mapping for this evaluator version, or `null` when no default is configured.  An entry's `source` is `null` when that variable was never fully configured, and sources are not restricted by rule `target` here, because the default is stored on the evaluator rather than on any one rule. | 
**evaluation_rule_count** | **i32** | Number of evaluation rules in the project that currently use this evaluator. | 
**created_at** | **chrono::DateTime<chrono::FixedOffset>** | Timestamp when this evaluator was created. | 
**updated_at** | **chrono::DateTime<chrono::FixedOffset>** | Timestamp when this evaluator was last updated. | 
**prompt** | **String** | Prompt template used during evaluation. | 
**output_definition** | [**models::UnstablePublicEvaluatorOutputDefinition**](UnstablePublicEvaluatorOutputDefinition.md) |  | 
**model_config** | [**models::UnstableEvaluatorModelConfig**](UnstableEvaluatorModelConfig.md) |  | 
**r#type** | **Type** |  (enum: llm_as_judge) | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


