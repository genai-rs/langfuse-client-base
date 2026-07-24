# SubmitFeedbackRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**target_type** | [**models::FeedbackTargetType**](FeedbackTargetType.md) |  | 
**target** | **String** | The specific instance within targetType: the skill name, MCP tool name, CLI command, API endpoint path, or docs page path (e.g. 'queryMetrics', '/docs/mcp'). An identifier, not a sentence. Must be between 1 and 200 characters. | 
**feedback** | **String** | Concise feedback text approved by the user. Must be between 1 and 3000 characters. | 
**goal** | Option<**String**> | Optional user-approved goal or use case they were trying to achieve. Must be between 1 and 1500 characters when provided. Do not include secrets, customer data, trace payloads, or broad unrelated context. | [optional]
**reference_url** | Option<**String**> | Optional HTTP(S) reference URL. Langfuse stores it as text for triage and does not fetch it. | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


