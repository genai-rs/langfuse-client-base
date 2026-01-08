# BaseScoreV1

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** |  | 
**trace_id** | **String** |  | 
**name** | **String** |  | 
**source** | [**models::ScoreSource**](ScoreSource.md) |  | 
**observation_id** | Option<**String**> | The observation ID associated with the score | [optional]
**timestamp** | **String** |  | 
**created_at** | **String** |  | 
**updated_at** | **String** |  | 
**author_user_id** | Option<**String**> | The user ID of the author | [optional]
**comment** | Option<**String**> | Comment on the score | [optional]
**metadata** | Option<[**serde_json::Value**](.md)> | Metadata associated with the score | 
**config_id** | Option<**String**> | Reference a score config on a score. When set, config and score name must be equal and value must comply to optionally defined numerical range | [optional]
**queue_id** | Option<**String**> | The annotation queue referenced by the score. Indicates if score was initially created while processing annotation queue. | [optional]
**environment** | **String** | The environment from which this score originated. Can be any lowercase alphanumeric string with hyphens and underscores that does not start with 'langfuse'. | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


