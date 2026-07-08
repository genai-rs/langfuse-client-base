# ExperimentItem

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** |  | 
**trace_id** | **String** |  | 
**start_time** | **chrono::DateTime<chrono::FixedOffset>** |  | 
**end_time** | Option<**chrono::DateTime<chrono::FixedOffset>**> |  | 
**level** | [**models::ObservationLevel**](ObservationLevel.md) |  | 
**environment** | **String** |  | 
**experiment_id** | **String** |  | 
**experiment_name** | **String** |  | 
**experiment_item_id** | **String** |  | 
**experiment_dataset_id** | Option<**String**> | Included when `fields=dataset` is requested. | [optional]
**experiment_item_version** | Option<**chrono::DateTime<chrono::FixedOffset>**> | Included when `fields=dataset` is requested. | [optional]
**input** | Option<**serde_json::Value**> | Included when `fields=io` is requested. | [optional]
**output** | Option<**serde_json::Value**> | Included when `fields=io` is requested. | [optional]
**expected_output** | Option<**serde_json::Value**> | Included when `fields=io` is requested. | [optional]
**metadata** | Option<**std::collections::HashMap<String, serde_json::Value>**> | Included when `fields=metadata` is requested. | [optional]
**experiment_item_metadata** | Option<**std::collections::HashMap<String, serde_json::Value>**> | Included when `fields=itemMetadata` is requested. | [optional]
**experiment_metadata** | Option<**std::collections::HashMap<String, serde_json::Value>**> | Included when `fields=experimentMetadata` is requested. | [optional]
**experiment_description** | Option<**String**> | Included when `fields=experimentMetadata` is requested. | [optional]
**scores** | Option<[**Vec<models::ScoreV3>**](ScoreV3.md)> | Included only when `fields=scores` is requested. Contains item and trace scores only; experiment-level scores are returned by the experiments endpoint. | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


