# UnstablePublicApiErrorDetails

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**issues** | Option<[**Vec<models::UnstablePublicApiValidationIssue>**](UnstablePublicApiValidationIssue.md)> | Validation issues for malformed request bodies or query parameters. | [optional]
**field** | Option<**String**> | Path-like reference to the failing field, for example `mapping[1].jsonPath`. | [optional]
**column** | Option<**String**> | Filter column that failed validation. | [optional]
**invalid_values** | Option<**Vec<String>**> | Unsupported values supplied by the caller. | [optional]
**allowed_values** | Option<**Vec<String>**> | Allowed values for the failing filter column. | [optional]
**variable** | Option<**String**> | Evaluator variable involved in the failure. | [optional]
**variables** | Option<**Vec<String>**> | Multiple evaluator variables involved in the failure, for example missing mappings. | [optional]
**value** | Option<**String**> | Raw invalid value supplied by the caller. | [optional]
**evaluator_name** | Option<**String**> | Evaluator name used during preflight validation. | [optional]
**provider** | Option<**String**> | Provider resolved during evaluator preflight, if any. | [optional]
**model** | Option<**String**> | Model resolved during evaluator preflight, if any. | [optional]
**retry_after_seconds** | Option<**i32**> | Suggested retry delay for rate-limited requests. | [optional]
**limit** | Option<**i32**> | Numeric limit associated with the failure, for example the active evaluation-rule cap or the current rate-limit window. | [optional]
**remaining** | Option<**i32**> | Remaining requests in the current rate-limit window. | [optional]
**reset_at** | Option<**String**> | ISO-8601 timestamp when the current rate-limit window resets. | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


