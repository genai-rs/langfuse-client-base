# UnstableLegacyEvaluationRule

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** | Stable evaluation rule identifier. | 
**name** | **String** | Human-readable deployment name. This is independent from the evaluator name. | 
**evaluator** | [**models::UnstableEvaluationRuleEvaluator**](UnstableEvaluationRuleEvaluator.md) |  | 
**enabled** | **bool** | Desired enabled state configured by the client. | 
**status** | [**models::UnstableEvaluationRuleStatus**](UnstableEvaluationRuleStatus.md) |  | 
**paused_reason** | Option<**String**> | Machine-readable reason when `status=paused`, otherwise `null`. | 
**paused_message** | Option<**String**> | Human-readable explanation when `status=paused`, otherwise `null`. | 
**sampling** | **f64** | Fraction of matching target objects that should be evaluated.  Must be greater than `0` and less than or equal to `1`. - `1` means evaluate every matching target. - `0.25` means evaluate approximately 25% of matching targets. | 
**created_at** | **chrono::DateTime<chrono::FixedOffset>** | Timestamp when the evaluation rule was created. | 
**updated_at** | **chrono::DateTime<chrono::FixedOffset>** | Timestamp when the evaluation rule was last updated. | 
**target** | [**models::UnstableLegacyEvaluationRuleTarget**](UnstableLegacyEvaluationRuleTarget.md) |  | 
**delay** | **i32** | Delay in milliseconds before the legacy evaluation job runs. | 
**time_scope** | [**Vec<models::UnstableEvaluationRuleTimeScope>**](UnstableEvaluationRuleTimeScope.md) | Whether the legacy rule evaluates newly ingested data, existing data, or both. | 
**filter** | [**Vec<models::UnstableEvaluationRuleFilter>**](UnstableEvaluationRuleFilter.md) | Stored filters used by the legacy trace or dataset rule. | 
**mapping** | [**Vec<models::UnstableLegacyEvaluationRuleMapping>**](UnstableLegacyEvaluationRuleMapping.md) | Stored variable mappings, including the trace, dataset item, or named observation selected for each variable. | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


