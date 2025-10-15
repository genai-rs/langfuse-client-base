# ScoreOneOf1

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**value** | Option<**f64**> | Only defined if a config is linked. Represents the numeric category mapping of the stringValue | [optional]
**string_value** | **String** | The string representation of the score value. If no config is linked, can be any string. Otherwise, must map to a config category | 
**id** | **String** |  | 
**trace_id** | Option<**String**> |  | [optional]
**session_id** | Option<**String**> |  | [optional]
**observation_id** | Option<**String**> |  | [optional]
**dataset_run_id** | Option<**String**> |  | [optional]
**name** | **String** |  | 
**source** | [**models::ScoreSource**](ScoreSource.md) |  | 
**timestamp** | **String** |  | 
**created_at** | **String** |  | 
**updated_at** | **String** |  | 
**author_user_id** | Option<**String**> |  | [optional]
**comment** | Option<**String**> |  | [optional]
**metadata** | Option<[**serde_json::Value**](.md)> |  | [optional]
**config_id** | Option<**String**> | Reference a score config on a score. When set, config and score name must be equal and value must comply to optionally defined numerical range | [optional]
**queue_id** | Option<**String**> | The annotation queue referenced by the score. Indicates if score was initially created while processing annotation queue. | [optional]
**environment** | Option<**String**> | The environment from which this score originated. Can be any lowercase alphanumeric string with hyphens and underscores that does not start with 'langfuse'. | [optional]
**data_type** | **String** |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


