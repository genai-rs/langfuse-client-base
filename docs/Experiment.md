# Experiment

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** |  | 
**name** | **String** |  | 
**description** | Option<**String**> |  | 
**start_time** | **chrono::DateTime<chrono::FixedOffset>** | Start of the experiment, i.e. the earliest event within the requested time range. Clipped to `fromStartTime` when the experiment started before the requested range. | 
**end_time** | **chrono::DateTime<chrono::FixedOffset>** | End of the experiment, i.e. the latest event end within the requested time range. | 
**item_count** | **i32** | Number of experiment items within the requested time range. | 
**dataset_id** | Option<**String**> | Null when the experiment is not associated with a dataset. | 
**metadata** | Option<**std::collections::HashMap<String, serde_json::Value>**> | Included only when `fields=metadata` is requested. | [optional]
**scores** | Option<[**Vec<models::ScoreV3>**](ScoreV3.md)> | Included only when `fields=scores` is requested. Contains scores directly attached to the experiment. | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


