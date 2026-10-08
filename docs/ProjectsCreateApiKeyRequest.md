# ProjectsCreateApiKeyRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | Option<**String**> | Optional name for the API key. Cannot be provided together with note, even if either value is an empty string. | [optional]
**note** | Option<**String**> | Deprecated alias for name. Cannot be provided together with name, even if either value is an empty string. | [optional]
**expires_at** | Option<**chrono::DateTime<chrono::FixedOffset>**> | Optional expiration timestamp in ISO 8601 format. Must be in the future. Omit or set to null for a key that does not expire. | [optional]
**public_key** | Option<**String**> | Optional predefined public key. Must start with 'pk-lf-'. If provided, secretKey must also be provided. | [optional]
**secret_key** | Option<**String**> | Optional predefined secret key. Must start with 'sk-lf-'. If provided, publicKey must also be provided. | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


