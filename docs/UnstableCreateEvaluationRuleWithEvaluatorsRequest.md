# UnstableCreateEvaluationRuleWithEvaluatorsRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **String** | Human-readable deployment name. | 
**evaluators** | [**Vec<models::UnstableCreateEvaluationRuleEvaluatorAssignment>**](UnstableCreateEvaluationRuleEvaluatorAssignment.md) | One or more evaluator assignments. Providing the deprecated top-level `evaluator` or `mapping` fields alongside this is rejected with `400`.  Multiple assignments are supported on writable targets. | 
**target** | [**models::UnstableEvaluationRuleTarget**](UnstableEvaluationRuleTarget.md) |  | 
**enabled** | **bool** |  | 
**sampling** | Option<**f64**> |  | [optional]
**filter** | Option<[**Vec<models::UnstableEvaluationRuleFilter>**](UnstableEvaluationRuleFilter.md)> |  | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


