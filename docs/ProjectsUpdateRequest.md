# ProjectsUpdateRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **String** |  | 
**metadata** | Option<[**std::collections::HashMap<String, serde_json::Value>**](serde_json::Value.md)> | Optional metadata for the project | [optional]
**retention** | Option<**i32**> | Number of days to retain data. Must be 0 or at least 3 days. Requires data-retention entitlement for non-zero values. Optional. Will retain existing retention setting if omitted. | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


