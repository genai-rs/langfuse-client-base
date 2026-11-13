# \SkillsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**skills_create_version**](SkillsApi.md#skills_create_version) | **POST** /api/public/skills | 
[**skills_delete_version**](SkillsApi.md#skills_delete_version) | **DELETE** /api/public/skills/{skillName}/versions/{skillVersion} | 
[**skills_get**](SkillsApi.md#skills_get) | **GET** /api/public/skills/{skillName} | 
[**skills_get_file_contents**](SkillsApi.md#skills_get_file_contents) | **GET** /api/public/skills/files/content | 
[**skills_list**](SkillsApi.md#skills_list) | **GET** /api/public/skills | 
[**skills_set_labels**](SkillsApi.md#skills_set_labels) | **PATCH** /api/public/skills/{skillName}/versions/{skillVersion} | 
[**skills_update**](SkillsApi.md#skills_update) | **PATCH** /api/public/skills/{skillName} | 



## skills_create_version

> models::SkillVersion skills_create_version(create_skill_version_request, options)


Create skill version

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**create_skill_version_request** | [**CreateSkillVersionRequest**](CreateSkillVersionRequest.md) |  | [required] |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
skills_create_version().configuration(&configuration).create_skill_version_request(..).options(&options).call().await
```

### Return type

[**models::SkillVersion**](SkillVersion.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## skills_delete_version

> models::DeleteSkillVersionResponse skills_delete_version(skill_name, skill_version, options)


Delete one immutable skill version. Unreferenced blobs are retained for asynchronous cleanup.

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**skill_name** | **String** |  | [required] |
**skill_version** | **i64** |  | [required] |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
skills_delete_version().configuration(&configuration).skill_name(..).skill_version(..).options(&options).call().await
```

### Return type

[**models::DeleteSkillVersionResponse**](DeleteSkillVersionResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## skills_get

> models::SkillVersion skills_get(skill_name, version, label, include_content, options)


Resolve a skill's metadata and file manifest by version or label. Defaults to the production label. Set includeContent to return file contents inline, or use each file's sha256Hash with getFileContents.

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**skill_name** | **String** |  | [required] |
**version** | Option<**i64**> |  |  |
**label** | Option<**String**> |  |  |
**include_content** | Option<**bool**> | Include UTF-8 text content in each file. Defaults to false. |  |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
skills_get().configuration(&configuration).skill_name(..).options(&options).call().await
```

### Return type

[**models::SkillVersion**](SkillVersion.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## skills_get_file_contents

> models::SkillFileContentsResponse skills_get_file_contents(sha256_hashes, options)


Read a batch of text contents by canonical base64-encoded SHA-256 hashes.

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**sha256_hashes** | **String** | Comma-separated list of one to 50 canonical base64-encoded SHA-256 hashes from skill file manifests. URL-encode the value, including +, /, and = characters. | [required] |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
skills_get_file_contents().configuration(&configuration).sha256_hashes(..).options(&options).call().await
```

### Return type

[**models::SkillFileContentsResponse**](SkillFileContentsResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## skills_list

> models::SkillMetaListResponse skills_list(name, search, tag, page, limit, from_updated_at, to_updated_at, options)


List skills with metadata and timestamps from their latest version, shared tags, and the version assigned to production when present.

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**name** | Option<**String**> | Filter by exact skill name. |  |
**search** | Option<**String**> | Case-insensitive search across skill names and latest-version descriptions. |  |
**tag** | Option<**String**> | Filter by a shared skill tag. |  |
**page** | Option<**i64**> |  |  |
**limit** | Option<**i64**> |  |  |
**from_updated_at** | Option<**chrono::DateTime<chrono::FixedOffset>**> | Include skills whose latest version was updated at or after this timestamp. |  |
**to_updated_at** | Option<**chrono::DateTime<chrono::FixedOffset>**> | Include skills whose latest version was updated before this timestamp. |  |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
skills_list().configuration(&configuration).options(&options).call().await
```

### Return type

[**models::SkillMetaListResponse**](SkillMetaListResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## skills_set_labels

> models::SkillVersion skills_set_labels(skill_name, skill_version, update_skill_labels_request, options)


Replace the labels on a skill version and atomically move them from other versions.

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**skill_name** | **String** |  | [required] |
**skill_version** | **i64** |  | [required] |
**update_skill_labels_request** | [**UpdateSkillLabelsRequest**](UpdateSkillLabelsRequest.md) |  | [required] |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
skills_set_labels().configuration(&configuration).skill_name(..).skill_version(..).update_skill_labels_request(..).options(&options).call().await
```

### Return type

[**models::SkillVersion**](SkillVersion.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## skills_update

> models::SkillVersion skills_update(skill_name, update_skill_request, options)


Replace the shared tags across all versions of a skill. An empty tags list clears all tags. Returns the latest skill version with the updated tags.

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**skill_name** | **String** |  | [required] |
**update_skill_request** | [**UpdateSkillRequest**](UpdateSkillRequest.md) |  | [required] |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
skills_update().configuration(&configuration).skill_name(..).update_skill_request(..).options(&options).call().await
```

### Return type

[**models::SkillVersion**](SkillVersion.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

