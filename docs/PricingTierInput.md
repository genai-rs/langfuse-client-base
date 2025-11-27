# PricingTierInput

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **String** | Name of the pricing tier for display and identification purposes.  Must be unique within the model. Common patterns: \"Standard Pricing\", \"High Volume Tier\", \"Extended Context\" | 
**is_default** | **bool** | Whether this is the default tier. Exactly one tier per model must be marked as default.  Requirements for default tier: - Must have isDefault=true - Must have priority=0 - Must have empty conditions array (conditions=[])  The default tier acts as a fallback when no conditional tiers match. | 
**priority** | **i32** | Priority for tier matching evaluation. Lower numbers = higher priority (evaluated first).  Must be unique within the model. The default tier must have priority=0. Conditional tiers should use priority 1, 2, 3, etc. based on their specificity. | 
**conditions** | [**Vec<models::PricingTierCondition>**](PricingTierCondition.md) | Array of conditions that must ALL be met for this tier to match (AND logic).  The default tier must have an empty array (conditions=[]). Conditional tiers should define one or more conditions that specify when this tier's pricing applies.  Each condition specifies a regex pattern, operator, and threshold value for matching against usage details. | 
**prices** | **std::collections::HashMap<String, f64>** | Prices (USD) by usage type for this tier. At least one price must be defined.  Common usage types: \"input\", \"output\", \"total\", \"request\", \"image\" Prices are in USD per unit (e.g., per token).  Example: {\"input\": 0.000003, \"output\": 0.000015} represents $3 per million input tokens and $15 per million output tokens. | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


