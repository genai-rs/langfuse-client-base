# UnstableTopicFacet

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** |  | 
**name** | **String** |  | 
**description** | **String** |  | 
**is_built_in** | **bool** |  | 
**active** | **bool** | Whether a Topics rule runs the facet. True for all facets if the project has no rule. | 
**rule_ids** | **Vec<String>** | The rules that run the facet. | 
**version** | **i64** | Latest facet version. | 
**prompt** | **String** | Prompt of the latest facet version. | 
**published_run** | Option<[**models::UnstableTopicFacetPublishedRun**](UnstableTopicFacetPublishedRun.md)> |  | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


