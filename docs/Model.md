# Model

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** |  | 
**model_name** | **String** | Name of the model definition. If multiple with the same name exist, they are applied in the following order: (1) custom over built-in, (2) newest according to startTime where model.startTime<observation.startTime | 
**match_pattern** | **String** | Regex pattern which matches this model definition to generation.model. Useful in case of fine-tuned models. If you want to exact match, use `(?i)^modelname$` | 
**start_date** | Option<**String**> | Apply only to generations which are newer than this ISO date. | [optional]
**unit** | Option<[**models::ModelUsageUnit**](ModelUsageUnit.md)> |  | [optional]
**input_price** | Option<**f64**> | Deprecated. See 'prices' instead. Price (USD) per input unit | [optional]
**output_price** | Option<**f64**> | Deprecated. See 'prices' instead. Price (USD) per output unit | [optional]
**total_price** | Option<**f64**> | Deprecated. See 'prices' instead. Price (USD) per total unit. Cannot be set if input or output price is set. | [optional]
**tokenizer_id** | Option<**String**> | Optional. Tokenizer to be applied to observations which match to this model. See docs for more details. | [optional]
**tokenizer_config** | Option<[**serde_json::Value**](.md)> | Optional. Configuration for the selected tokenizer. Needs to be JSON. See docs for more details. | 
**is_langfuse_managed** | **bool** |  | 
**created_at** | **String** | Timestamp when the model was created | 
**prices** | [**std::collections::HashMap<String, models::ModelPrice>**](ModelPrice.md) | Deprecated. Use 'pricingTiers' instead for models with usage-based pricing variations.  This field shows prices by usage type from the default pricing tier. Maintained for backward compatibility. If the model uses tiered pricing, this field will be populated from the default tier's prices. | 
**pricing_tiers** | [**Vec<models::PricingTier>**](PricingTier.md) | Array of pricing tiers with conditional pricing based on usage thresholds.  Pricing tiers enable accurate cost tracking for models that charge different rates based on usage patterns (e.g., different rates for high-volume usage, large context windows, or cached tokens).  Each model must have exactly one default tier (isDefault=true, priority=0) that serves as a fallback. Additional conditional tiers can be defined with specific matching criteria.  If this array is empty, the model uses legacy flat pricing from the inputPrice/outputPrice/totalPrice fields. | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


