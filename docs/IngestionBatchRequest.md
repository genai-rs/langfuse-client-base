# IngestionBatchRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**batch** | [**Vec<models::IngestionEvent>**](IngestionEvent.md) | Batch of events to be ingested, discriminated by attribute `type`. From November 16, 2026 on Langfuse Cloud, only `score-create` events are accepted; all other event types are rejected. | 
**metadata** | Option<**serde_json::Value**> | Optional. Metadata field used by the Langfuse SDKs for debugging. | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


