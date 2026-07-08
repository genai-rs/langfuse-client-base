# BaseScoreV3

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** |  | 
**project_id** | **String** |  | 
**name** | **String** |  | 
**source** | [**models::ScoreSource**](ScoreSource.md) |  | 
**timestamp** | **chrono::DateTime<chrono::FixedOffset>** |  | 
**environment** | **String** | The environment from which this score originated. | 
**created_at** | **chrono::DateTime<chrono::FixedOffset>** |  | 
**updated_at** | **chrono::DateTime<chrono::FixedOffset>** |  | 
**comment** | Option<**String**> | Optional comment attached to the score. Present when \"details\" is included in the fields parameter. | [optional]
**config_id** | Option<**String**> | The score config ID, if this score was created from a config. Present when \"details\" is included in the fields parameter. | [optional]
**metadata** | Option<**std::collections::HashMap<String, serde_json::Value>**> | Arbitrary metadata attached to the score. Present when \"details\" is included in the fields parameter. | [optional]
**author_user_id** | Option<**String**> | The user who created this score, if available. Present when \"annotation\" is included in the fields parameter. | [optional]
**queue_id** | Option<**String**> | The annotation queue this score belongs to, if any. Present when \"annotation\" is included in the fields parameter. | [optional]
**subject** | Option<[**models::ScoreSubjectV3**](ScoreSubjectV3.md)> |  | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


