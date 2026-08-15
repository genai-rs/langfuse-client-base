# ScimCreateUserRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_name** | **String** | User's email address (required) | 
**name** | [**models::ScimName**](ScimName.md) |  | 
**emails** | Option<[**Vec<models::ScimEmail>**](ScimEmail.md)> | User's email addresses | [optional]
**active** | Option<**bool**> | Whether the user is active | [optional]
**password** | Option<**String**> | Ignored. Accepted only for compatibility with identity providers that always send a password on user creation (Okta sends a placeholder value even when password sync is disabled). No credential is created for the user; provisioned users authenticate via SSO or set a password themselves through the password reset flow. | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


