# UnstableEvaluationRuleMapping

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**variable** | **String** | Prompt variable name without braces.  Example: for the prompt `Judge {{input}} against {{output}}`, use `input` and `output`. | 
**source** | [**models::UnstableEvaluationRuleMappingSource**](UnstableEvaluationRuleMappingSource.md) |  | 
**json_path** | Option<**String**> | Optional JSONPath selector applied to the selected source before it is passed to the evaluator prompt.  Requirements: - Must start with `$` - Must be a syntactically valid JSONPath expression - Most useful with `source=metadata` | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


