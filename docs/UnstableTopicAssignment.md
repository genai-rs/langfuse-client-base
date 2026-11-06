# UnstableTopicAssignment

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**trace_id** | **String** |  | 
**timestamp** | **chrono::DateTime<chrono::FixedOffset>** | Trace start time. | 
**facet_id** | **String** |  | 
**facet_name** | **String** |  | 
**facet_version** | **i32** |  | 
**rule_id** | Option<**String**> | The rule whose map assigned the trace. Null when the project has no rule. | [optional]
**status** | [**models::UnstableTopicAssignmentStatus**](UnstableTopicAssignmentStatus.md) |  | 
**topic** | Option<[**models::UnstableTopicAssignmentTopic**](UnstableTopicAssignmentTopic.md)> |  | [optional]
**run_id** | Option<**String**> | The run that assigned the trace. Null for assignments made as traces arrive. | [optional]
**assigned_at** | **chrono::DateTime<chrono::FixedOffset>** |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


