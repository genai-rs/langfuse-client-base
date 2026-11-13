# \ScimApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**scim_create_user**](ScimApi.md#scim_create_user) | **POST** /api/public/scim/Users | 
[**scim_delete_user**](ScimApi.md#scim_delete_user) | **DELETE** /api/public/scim/Users/{userId} | 
[**scim_get_resource_types**](ScimApi.md#scim_get_resource_types) | **GET** /api/public/scim/ResourceTypes | 
[**scim_get_schemas**](ScimApi.md#scim_get_schemas) | **GET** /api/public/scim/Schemas | 
[**scim_get_service_provider_config**](ScimApi.md#scim_get_service_provider_config) | **GET** /api/public/scim/ServiceProviderConfig | 
[**scim_get_user**](ScimApi.md#scim_get_user) | **GET** /api/public/scim/Users/{userId} | 
[**scim_list_users**](ScimApi.md#scim_list_users) | **GET** /api/public/scim/Users | 



## scim_create_user

> models::ScimUser scim_create_user(scim_create_user_request, options)


Create a new user in the organization (requires organization-scoped API key)

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**scim_create_user_request** | [**ScimCreateUserRequest**](ScimCreateUserRequest.md) |  | [required] |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
scim_create_user().configuration(&configuration).scim_create_user_request(..).options(&options).call().await
```

### Return type

[**models::ScimUser**](ScimUser.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## scim_delete_user

> serde_json::Value scim_delete_user(user_id, options)


Remove a user from the organization (requires organization-scoped API key). Note that this only removes the user from the organization but does not delete the user entity itself.

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**user_id** | **String** |  | [required] |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
scim_delete_user().configuration(&configuration).user_id(..).options(&options).call().await
```

### Return type

**serde_json::Value**

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## scim_get_resource_types

> models::ResourceTypesResponse scim_get_resource_types(options)


Get SCIM Resource Types (requires organization-scoped API key)

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
scim_get_resource_types().configuration(&configuration).options(&options).call().await
```

### Return type

[**models::ResourceTypesResponse**](ResourceTypesResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## scim_get_schemas

> models::SchemasResponse scim_get_schemas(options)


Get SCIM Schemas (requires organization-scoped API key)

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
scim_get_schemas().configuration(&configuration).options(&options).call().await
```

### Return type

[**models::SchemasResponse**](SchemasResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## scim_get_service_provider_config

> models::ServiceProviderConfig scim_get_service_provider_config(options)


Get SCIM Service Provider Configuration (requires organization-scoped API key)

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
scim_get_service_provider_config().configuration(&configuration).options(&options).call().await
```

### Return type

[**models::ServiceProviderConfig**](ServiceProviderConfig.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## scim_get_user

> models::ScimUser scim_get_user(user_id, options)


Get a specific user by ID (requires organization-scoped API key)

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**user_id** | **String** |  | [required] |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
scim_get_user().configuration(&configuration).user_id(..).options(&options).call().await
```

### Return type

[**models::ScimUser**](ScimUser.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## scim_list_users

> models::ScimUsersListResponse scim_list_users(filter, start_index, count, options)


List users in the organization (requires organization-scoped API key)

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**filter** | Option<**String**> | Filter expression (e.g. userName eq \"value\") |  |
**start_index** | Option<**i64**> | 1-based index of the first result to return (default 1) |  |
**count** | Option<**i64**> | Maximum number of results to return (default 100) |  |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
scim_list_users().configuration(&configuration).options(&options).call().await
```

### Return type

[**models::ScimUsersListResponse**](ScimUsersListResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

