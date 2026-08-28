# PublicEvaluatorCategoricalScore

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**score_reasoning_instructions** | Option<**String**> | Optional instructions for deriving the reasoning returned with the score. | [optional]
**score_value_instructions** | Option<**String**> | Optional instructions for deriving the score value. | [optional]
**data_type** | **String** | Categorical score output. | 
**categories** | **Vec<String>** | Allowed category values. At least two unique values are required. | 
**should_allow_multiple_matches** | **bool** | Whether the evaluator may return more than one category. | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


