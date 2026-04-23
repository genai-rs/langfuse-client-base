# UnstableEvaluationRule

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** | Stable evaluation rule identifier. | 
**name** | **String** | Human-readable deployment name. This is independent from the evaluator name. | 
**evaluator** | [**models::UnstableEvaluationRuleEvaluator**](UnstableEvaluationRuleEvaluator.md) |  | 
**target** | [**models::UnstableEvaluationRuleTarget**](UnstableEvaluationRuleTarget.md) |  | 
**enabled** | **bool** | Desired enabled state configured by the client. | 
**status** | [**models::UnstableEvaluationRuleStatus**](UnstableEvaluationRuleStatus.md) |  | 
**paused_reason** | Option<**String**> | Machine-readable reason when `status=paused`, otherwise `null`. | [optional]
**paused_message** | Option<**String**> | Human-readable explanation when `status=paused`, otherwise `null`. | [optional]
**sampling** | **f64** | Fraction of matching target objects that should be evaluated.  Must be greater than `0` and less than or equal to `1`. - `1` means evaluate every matching target. - `0.25` means evaluate approximately 25% of matching targets. | 
**filter** | [**Vec<models::UnstableEvaluationRuleFilter>**](UnstableEvaluationRuleFilter.md) | List of filter conditions used to decide whether a target should be evaluated. | 
**mapping** | [**Vec<models::UnstableEvaluationRuleMapping>**](UnstableEvaluationRuleMapping.md) | Variable mappings used to populate the evaluator prompt from the live target object. | 
**created_at** | **String** | Timestamp when the evaluation rule was created. | 
**updated_at** | **String** | Timestamp when the evaluation rule was last updated. | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


