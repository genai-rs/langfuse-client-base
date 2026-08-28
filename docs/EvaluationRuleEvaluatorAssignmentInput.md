# EvaluationRuleEvaluatorAssignmentInput

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**evaluator_id** | **String** | Stable evaluator identifier. The rule automatically uses that evaluator's latest version. | 
**variable_mapping** | Option<[**Vec<models::PromptVariableMappingInput>**](PromptVariableMappingInput.md)> | Rule-specific prompt-variable mapping.  Set to `null` or omit to inherit the evaluator's latest default mapping. Code evaluators use the fixed runtime mapping and should use `null`. | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


