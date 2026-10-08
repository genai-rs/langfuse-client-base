# StringObjectEvaluationRuleFilter1

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**column** | **String** | Object-valued column to filter on. Currently only `metadata` is supported. | 
**key** | **String** | Top-level key inside the object-valued column to filter on. | 
**operator** | [**models::EvaluationRuleStringObjectFilterOperator**](EvaluationRuleStringObjectFilterOperator.md) |  | 
**value** | **String** | Value to compare against. Ignored for `is set` / `is not set`; send `\"\"`. | 
**r#type** | **Type** |  (enum: stringObject) | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


