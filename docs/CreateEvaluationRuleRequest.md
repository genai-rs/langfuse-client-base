# CreateEvaluationRuleRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **String** | Human-readable rule name. Names are not identifiers and do not need to be unique. | 
**enabled** | **bool** | Whether live execution should start immediately. Enabled rules require at least one evaluator assignment. | 
**sampling** | Option<**f64**> | Fraction of matching observations to evaluate. Omit this field to use the default of `1`, which evaluates every match. `null` is not accepted. | [optional]
**filter** | Option<[**Vec<models::EvaluationRuleFilter>**](EvaluationRuleFilter.md)> | Conditions used to select observations. Defaults to an empty list, which matches every incoming observation. | [optional]
**evaluator_assignments** | [**Vec<models::EvaluationRuleEvaluatorAssignmentInput>**](EvaluationRuleEvaluatorAssignmentInput.md) | Evaluators to attach to this rule. Disabled rules may use an empty list as a draft. | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


