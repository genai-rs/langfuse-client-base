# Deprecation

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **String** | Human- and agent-readable summary of the deprecation and its replacement. | 
**replacement** | Option<**String**> | The replacement endpoint, e.g. \"GET /api/public/v2/observations\". Omitted when the endpoint is being removed without a direct replacement. | [optional]
**docs_url** | Option<**String**> | Link to the migration documentation (markdown), when available. | [optional]
**sunset_at** | Option<**String**> | ISO date after which the endpoint may stop working, when a removal date is committed. | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


