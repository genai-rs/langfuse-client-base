# UnstableCreateEvaluationRuleRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **String** | Human-readable deployment name. | 
**evaluator** | [**models::UnstableEvaluationRuleEvaluatorReference**](UnstableEvaluationRuleEvaluatorReference.md) |  | 
**target** | [**models::UnstableEvaluationRuleTarget**](UnstableEvaluationRuleTarget.md) |  | 
**enabled** | **bool** | Whether the deployment should be active immediately after creation. | 
**sampling** | Option<**f64**> | Optional sampling fraction. Defaults to `1`. | [optional]
**filter** | Option<[**Vec<models::UnstableEvaluationRuleFilter>**](UnstableEvaluationRuleFilter.md)> | Optional filter list.  Omit or pass an empty list to evaluate all matching targets for the selected `target`. Each filter object must use a column that is valid for that `target`. For `target=experiment`, `column=datasetId` expects dataset `id` values from `GET /api/public/v2/datasets`, not dataset names. | [optional]
**mapping** | [**Vec<models::UnstableEvaluationRuleMapping>**](UnstableEvaluationRuleMapping.md) | Required variable mappings.  Every evaluator variable must appear exactly once. Build this list from the evaluator `variables` array returned by the evaluator endpoints. | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


