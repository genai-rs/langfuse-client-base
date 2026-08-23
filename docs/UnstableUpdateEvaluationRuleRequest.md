# UnstableUpdateEvaluationRuleRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | Option<**String**> | Updated deployment name. | [optional]
**evaluators** | Option<[**Vec<models::UnstableCreateEvaluationRuleEvaluatorAssignment>**](UnstableCreateEvaluationRuleEvaluatorAssignment.md)> | Full replacement of the rule's evaluator assignments: entries that are not listed are detached.  Mutually exclusive with the deprecated `evaluator` and `mapping` fields. | [optional]
**evaluator** | Option<[**models::UnstableEvaluationRuleEvaluatorReference**](UnstableEvaluationRuleEvaluatorReference.md)> |  | [optional]
**target** | Option<[**models::UnstableEvaluationRuleTarget**](UnstableEvaluationRuleTarget.md)> |  | [optional]
**enabled** | Option<**bool**> | Updated desired enabled state. | [optional]
**sampling** | Option<**f64**> | Updated sampling fraction. | [optional]
**filter** | Option<[**Vec<models::UnstableEvaluationRuleFilter>**](UnstableEvaluationRuleFilter.md)> | Updated filter list.  For `target=experiment`, `column=datasetId` expects dataset `id` values from `GET /api/public/v2/datasets`, not dataset names. | [optional]
**mapping** | Option<[**Vec<models::UnstableEvaluationRuleMapping>**](UnstableEvaluationRuleMapping.md)> | Updated LLM-as-judge variable mappings.  Do not send this field for code evaluator rules. Langfuse stores the fixed code runtime mapping automatically and returns it in the response. | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


