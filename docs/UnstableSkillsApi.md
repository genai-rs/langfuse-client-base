# \UnstableSkillsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**unstable_skills_create_version**](UnstableSkillsApi.md#unstable_skills_create_version) | **POST** /api/public/unstable/skills | 
[**unstable_skills_delete_version**](UnstableSkillsApi.md#unstable_skills_delete_version) | **DELETE** /api/public/unstable/skills/{skillName}/versions/{skillVersion} | 
[**unstable_skills_get**](UnstableSkillsApi.md#unstable_skills_get) | **GET** /api/public/unstable/skills/{skillName} | 
[**unstable_skills_get_file_content**](UnstableSkillsApi.md#unstable_skills_get_file_content) | **GET** /api/public/unstable/skills/files/{fileId}/content | 
[**unstable_skills_list**](UnstableSkillsApi.md#unstable_skills_list) | **GET** /api/public/unstable/skills | 
[**unstable_skills_set_labels**](UnstableSkillsApi.md#unstable_skills_set_labels) | **PATCH** /api/public/unstable/skills/{skillName}/versions/{skillVersion} | 
[**unstable_skills_update**](UnstableSkillsApi.md#unstable_skills_update) | **PATCH** /api/public/unstable/skills/{skillName} | 



## unstable_skills_create_version

> models::UnstableSkillVersion unstable_skills_create_version(unstable_create_skill_version_request)


Create skill version

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**unstable_create_skill_version_request** | [**UnstableCreateSkillVersionRequest**](UnstableCreateSkillVersionRequest.md) |  | [required] |

### Return type

[**models::UnstableSkillVersion**](unstableSkillVersion.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## unstable_skills_delete_version

> models::UnstableDeleteSkillVersionResponse unstable_skills_delete_version(skill_name, skill_version)


Delete one immutable skill version. Unreferenced blobs are retained for asynchronous cleanup.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**skill_name** | **String** |  | [required] |
**skill_version** | **i32** |  | [required] |

### Return type

[**models::UnstableDeleteSkillVersionResponse**](unstableDeleteSkillVersionResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## unstable_skills_get

> models::UnstableSkillVersion unstable_skills_get(skill_name, version, label)


Resolve a skill's metadata and file manifest by version or label. Defaults to the production label. Use each file's id with getFileContent to read its text content.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**skill_name** | **String** |  | [required] |
**version** | Option<**i32**> |  |  |
**label** | Option<**String**> |  |  |

### Return type

[**models::UnstableSkillVersion**](unstableSkillVersion.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## unstable_skills_get_file_content

> models::UnstableSkillFileContentResponse unstable_skills_get_file_content(file_id)


Read one text file from a persisted skill version using its file id, not its blob id. Returns JSON containing the text content with Cache-Control no-store.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**file_id** | **String** |  | [required] |

### Return type

[**models::UnstableSkillFileContentResponse**](unstableSkillFileContentResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## unstable_skills_list

> models::UnstableSkillMetaListResponse unstable_skills_list(name, search, tag, page, limit, from_updated_at, to_updated_at)


List skills with metadata and timestamps from their latest version, shared tags, and the version assigned to production when present.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**name** | Option<**String**> | Filter by exact skill name. |  |
**search** | Option<**String**> | Case-insensitive search across skill names and latest-version descriptions. |  |
**tag** | Option<**String**> | Filter by a shared skill tag. |  |
**page** | Option<**i32**> |  |  |
**limit** | Option<**i32**> |  |  |
**from_updated_at** | Option<**chrono::DateTime<chrono::FixedOffset>**> | Include skills whose latest version was updated at or after this timestamp. |  |
**to_updated_at** | Option<**chrono::DateTime<chrono::FixedOffset>**> | Include skills whose latest version was updated before this timestamp. |  |

### Return type

[**models::UnstableSkillMetaListResponse**](unstableSkillMetaListResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## unstable_skills_set_labels

> models::UnstableSkillVersion unstable_skills_set_labels(skill_name, skill_version, unstable_update_skill_labels_request)


Replace the labels on a skill version and atomically move them from other versions.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**skill_name** | **String** |  | [required] |
**skill_version** | **i32** |  | [required] |
**unstable_update_skill_labels_request** | [**UnstableUpdateSkillLabelsRequest**](UnstableUpdateSkillLabelsRequest.md) |  | [required] |

### Return type

[**models::UnstableSkillVersion**](unstableSkillVersion.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## unstable_skills_update

> models::UnstableSkillVersion unstable_skills_update(skill_name, unstable_update_skill_request)


Replace the shared tags across all versions of a skill. An empty tags list clears all tags. Returns the latest skill version with the updated tags.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**skill_name** | **String** |  | [required] |
**unstable_update_skill_request** | [**UnstableUpdateSkillRequest**](UnstableUpdateSkillRequest.md) |  | [required] |

### Return type

[**models::UnstableSkillVersion**](unstableSkillVersion.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

