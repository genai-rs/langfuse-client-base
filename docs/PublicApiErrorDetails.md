# PublicApiErrorDetails

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**issues** | Option<[**Vec<models::PublicApiValidationIssue>**](PublicApiValidationIssue.md)> | Validation issues for an invalid request body or query. | [optional]
**retry_after_seconds** | Option<**i32**> | Number of seconds to wait before retrying a rate-limited request. | [optional]
**limit** | Option<**i32**> | Rate-limit request allowance. | [optional]
**remaining** | Option<**i32**> | Remaining requests in the current rate-limit window. | [optional]
**reset_at** | Option<**chrono::DateTime<chrono::FixedOffset>**> | Time when the current rate-limit window resets. | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


