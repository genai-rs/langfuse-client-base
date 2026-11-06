# UnstableTopic

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** | Stable topic id, kept across map updates. | 
**version_id** | **String** | Id of this topic version. | 
**name** | **String** |  | 
**description** | **String** |  | 
**facet** | [**models::UnstableTopicFacetRef**](UnstableTopicFacetRef.md) |  | 
**rule_id** | Option<**String**> | The rule whose live map has the topic. Null when the project has no rule. | [optional]
**run_id** | **String** | The run that produced this topic version. | 
**trace_count** | **i32** | Traces in the window whose current result for the facet is this topic. | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


