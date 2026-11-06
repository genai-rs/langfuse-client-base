# UnstableTopicRule

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** |  | 
**name** | **String** |  | 
**filter** | [**Vec<models::EvaluationRuleReadFilter>**](EvaluationRuleReadFilter.md) | Observation filter that selects the rule's traces, returned verbatim. | 
**sampling** | **f64** | Fraction of matching traces that are processed, between `0` and `1`. | 
**facet_ids** | **Vec<String>** | Facets the rule runs. | 
**updated_at** | **chrono::DateTime<chrono::FixedOffset>** |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


