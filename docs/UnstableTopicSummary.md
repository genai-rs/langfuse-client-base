# UnstableTopicSummary

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**trace_id** | **String** |  | 
**trace_name** | **String** |  | 
**environment** | **String** |  | 
**timestamp** | **jiff::Timestamp** | Trace start time. | 
**facet_id** | **String** |  | 
**facet_name** | **String** |  | 
**facet_version** | **i64** |  | 
**state** | [**models::UnstableTopicSummaryState**](UnstableTopicSummaryState.md) |  | 
**summary** | Option<**String**> | Set when `state` is `complete`. | [optional]
**summary_truncated** | **bool** |  | 
**processed_at** | **jiff::Timestamp** |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


