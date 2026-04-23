# UnstableEvaluator

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** | Identifier of this evaluator. | 
**name** | **String** | Evaluator name. | 
**version** | **i32** | Version number of this evaluator. | 
**scope** | [**models::UnstableEvaluatorScope**](UnstableEvaluatorScope.md) |  | 
**r#type** | [**models::UnstableEvaluatorType**](UnstableEvaluatorType.md) |  | 
**prompt** | **String** | Prompt template used during evaluation. | 
**variables** | **Vec<String>** | Variables extracted from the evaluator prompt.  Every variable in this list must be mapped exactly once when creating an evaluation rule. | 
**output_definition** | [**models::UnstablePublicEvaluatorOutputDefinition**](UnstablePublicEvaluatorOutputDefinition.md) |  | 
**model_config** | Option<[**models::UnstableEvaluatorModelConfig**](UnstableEvaluatorModelConfig.md)> |  | [optional]
**evaluation_rule_count** | **i32** | Number of evaluation rules in the project that currently use this evaluator version. | 
**created_at** | **String** | Timestamp when this evaluator was created. | 
**updated_at** | **String** | Timestamp when this evaluator was last updated. | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


