# UnstableCreateEvaluatorRequestOneOf

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **String** | Evaluator name within the authenticated project. | 
**prompt** | **String** | Prompt template used by the evaluator. | 
**output_definition** | [**models::UnstableEvaluatorOutputDefinition**](UnstableEvaluatorOutputDefinition.md) |  | 
**model_config** | Option<[**models::UnstableEvaluatorModelConfig**](UnstableEvaluatorModelConfig.md)> |  | [optional]
**mapping** | Option<[**Vec<models::UnstableEvaluationRuleMapping>**](UnstableEvaluationRuleMapping.md)> | Optional default variable mapping inherited by rule assignments that do not provide an override. | [optional]
**r#type** | **Type** |  (enum: llm_as_judge) | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


