# PricingTier

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** | Unique identifier for the pricing tier | 
**name** | **String** | Name of the pricing tier for display and identification purposes.  Examples: \"Standard\", \"High Volume Tier\", \"Large Context\", \"Extended Context Tier\" | 
**is_default** | **bool** | Whether this is the default tier. Every model must have exactly one default tier with priority 0 and no conditions.  The default tier serves as a fallback when no conditional tiers match, ensuring cost calculation always succeeds. It typically represents the base pricing for standard usage patterns. | 
**priority** | **i32** | Priority for tier matching evaluation. Lower numbers = higher priority (evaluated first).  The default tier must always have priority 0. Conditional tiers should have priority 1, 2, 3, etc.  Example ordering: - Priority 0: Default tier (no conditions, always matches as fallback) - Priority 1: High usage tier (e.g., >200K tokens) - Priority 2: Medium usage tier (e.g., >100K tokens)  This ensures more specific conditions are checked before general ones. | 
**conditions** | [**Vec<models::PricingTierCondition>**](PricingTierCondition.md) | Array of conditions that must ALL be met for this tier to match (AND logic).  The default tier must have an empty conditions array. Conditional tiers should have one or more conditions that define when this tier's pricing applies.  Multiple conditions enable complex matching scenarios (e.g., \"high input tokens AND low output tokens\"). | 
**prices** | **std::collections::HashMap<String, f64>** | Prices (USD) by usage type for this tier.  Common usage types: \"input\", \"output\", \"total\", \"request\", \"image\" Prices are specified in USD per unit (e.g., per token, per request, per second).  Example: {\"input\": 0.000003, \"output\": 0.000015} means $3 per million input tokens and $15 per million output tokens. | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


