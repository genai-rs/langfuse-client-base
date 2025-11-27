# PricingTierCondition

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**usage_detail_pattern** | **String** | Regex pattern to match against usage detail keys. All matching keys' values are summed for threshold comparison.  Examples: - \"^input\" matches \"input\", \"input_tokens\", \"input_cached\", etc. - \"^(input|prompt)\" matches both \"input_tokens\" and \"prompt_tokens\" - \"_cache$\" matches \"input_cache\", \"output_cache\", etc.  The pattern is case-insensitive by default. If no keys match, the sum is treated as zero. | 
**operator** | [**models::PricingTierOperator**](PricingTierOperator.md) |  | 
**value** | **f64** | Threshold value for comparison. For token-based pricing, this is typically the token count threshold (e.g., 200000 for a 200K token threshold). | 
**case_sensitive** | **bool** | Whether the regex pattern matching is case-sensitive. Default is false (case-insensitive matching). | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


