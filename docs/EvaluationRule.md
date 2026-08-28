# EvaluationRule

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** | Stable evaluation-rule identifier. | 
**name** | **String** | Human-readable rule name. This is independent from evaluator names and does not need to be unique. | 
**created_by** | [**models::Creator**](Creator.md) |  | 
**enabled** | **bool** | Whether live execution is enabled for this rule. | 
**sampling** | **f64** | Fraction of matching observations that should be evaluated.  Must be between `0` and `1`. - `1` evaluates every matching observation. - `0.25` evaluates approximately 25% of matching observations. | 
**filter** | [**Vec<models::EvaluationRuleReadFilter>**](EvaluationRuleReadFilter.md) | List of stored filter conditions returned verbatim. Filters with a `key` use the keyed response shape; all others use the base shape. These response shapes are not broken down by internal filter type. An empty list matches every incoming object. | 
**evaluator_assignments** | [**Vec<models::EvaluatorAssignment>**](EvaluatorAssignment.md) | Evaluators attached to this rule in deterministic assignment order. | 
**created_at** | **chrono::DateTime<chrono::FixedOffset>** | Timestamp when the evaluation rule was created. | 
**updated_at** | **chrono::DateTime<chrono::FixedOffset>** | Timestamp when the evaluation rule was last updated. | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


