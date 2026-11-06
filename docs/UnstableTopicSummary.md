# UnstableTopicSummary

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**trace_id** | **String** |  | 
**trace_name** | **String** |  | 
**environment** | **String** |  | 
**timestamp** | **chrono::DateTime<chrono::FixedOffset>** | Trace start time. | 
**facet_id** | **String** |  | 
**facet_name** | **String** |  | 
**facet_version** | **i64** |  | 
**state** | [**models::UnstableTopicSummaryState**](UnstableTopicSummaryState.md) |  | 
**summary** | Option<**String**> | Set when `state` is `complete`. | [optional]
**summary_truncated** | **bool** |  | 
**processed_at** | **chrono::DateTime<chrono::FixedOffset>** |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


