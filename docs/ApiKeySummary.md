# ApiKeySummary

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** |  | 
**created_at** | **chrono::DateTime<chrono::FixedOffset>** |  | 
**expires_at** | Option<**chrono::DateTime<chrono::FixedOffset>**> | Expiration timestamp. Null if the key does not expire. | [optional]
**last_used_at** | Option<**chrono::DateTime<chrono::FixedOffset>**> |  | [optional]
**name** | Option<**String**> | Name of the API key. Contains the same value as note; null if no name was provided. | [optional]
**note** | Option<**String**> | Deprecated alias for name. Contains the same value as name. | [optional]
**public_key** | **String** |  | 
**display_secret_key** | **String** |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


