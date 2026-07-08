# UnstableCodeEvaluator

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** | Identifier of this evaluator. | 
**name** | **String** | Evaluator name. | 
**version** | **i32** | Version number of this evaluator. | 
**scope** | [**models::UnstableEvaluatorScope**](UnstableEvaluatorScope.md) |  | 
**variables** | **Vec<String>** | Variables that can be mapped when creating an evaluation rule.  LLM evaluators require every variable to be mapped exactly once. Code evaluators always expose the fixed runtime payload fields and Langfuse maps them automatically. | 
**evaluation_rule_count** | **i32** | Number of evaluation rules in the project that currently use this evaluator version. | 
**created_at** | **chrono::DateTime<chrono::FixedOffset>** | Timestamp when this evaluator was created. | 
**updated_at** | **chrono::DateTime<chrono::FixedOffset>** | Timestamp when this evaluator was last updated. | 
**source_code** | **String** | Source code executed for each matched observation. | 
**source_code_language** | [**models::UnstableCodeEvaluatorSourceCodeLanguage**](UnstableCodeEvaluatorSourceCodeLanguage.md) |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


