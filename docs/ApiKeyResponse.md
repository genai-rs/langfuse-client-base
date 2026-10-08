# ApiKeyResponse

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** |  | 
**created_at** | **chrono::DateTime<chrono::FixedOffset>** |  | 
**expires_at** | Option<**chrono::DateTime<chrono::FixedOffset>**> | Expiration timestamp. Null if the key does not expire. | [optional]
**public_key** | **String** |  | 
**secret_key** | **String** |  | 
**display_secret_key** | **String** |  | 
**name** | Option<**String**> | Name of the API key. Contains the same value as note; null if no name was provided. | [optional]
**note** | Option<**String**> | Deprecated alias for name. Contains the same value as name. | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


