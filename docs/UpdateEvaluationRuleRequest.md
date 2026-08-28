# UpdateEvaluationRuleRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | Option<**String**> | New human-readable rule name. | [optional]
**enabled** | Option<**bool**> | New desired live-execution state. | [optional]
**sampling** | Option<**f64**> | New fraction of matching observations to evaluate. Omit to keep the current value. | [optional]
**filter** | Option<[**Vec<models::EvaluationRuleFilter>**](EvaluationRuleFilter.md)> | Complete replacement filter list. An empty list matches every incoming observation. | [optional]
**evaluator_assignments** | Option<[**Vec<models::EvaluationRuleEvaluatorAssignmentInput>**](EvaluationRuleEvaluatorAssignmentInput.md)> | Complete replacement assignment list. An empty list disables the rule. | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


