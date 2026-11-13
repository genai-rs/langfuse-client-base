# \UnstableDashboardsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**unstable_dashboards_add_placement**](UnstableDashboardsApi.md#unstable_dashboards_add_placement) | **POST** /api/public/unstable/dashboards/{dashboardId}/placements | 
[**unstable_dashboards_create**](UnstableDashboardsApi.md#unstable_dashboards_create) | **POST** /api/public/unstable/dashboards | 
[**unstable_dashboards_delete**](UnstableDashboardsApi.md#unstable_dashboards_delete) | **DELETE** /api/public/unstable/dashboards/{dashboardId} | 
[**unstable_dashboards_delete_placement**](UnstableDashboardsApi.md#unstable_dashboards_delete_placement) | **DELETE** /api/public/unstable/dashboards/{dashboardId}/placements/{placementId} | 
[**unstable_dashboards_get**](UnstableDashboardsApi.md#unstable_dashboards_get) | **GET** /api/public/unstable/dashboards/{dashboardId} | 
[**unstable_dashboards_list**](UnstableDashboardsApi.md#unstable_dashboards_list) | **GET** /api/public/unstable/dashboards | 
[**unstable_dashboards_update**](UnstableDashboardsApi.md#unstable_dashboards_update) | **PATCH** /api/public/unstable/dashboards/{dashboardId} | 
[**unstable_dashboards_update_placement**](UnstableDashboardsApi.md#unstable_dashboards_update_placement) | **PATCH** /api/public/unstable/dashboards/{dashboardId}/placements/{placementId} | 



## unstable_dashboards_add_placement

> models::UnstableDashboardPlacement unstable_dashboards_add_placement(dashboard_id, unstable_create_dashboard_placement_request, options)


Add a placement to a dashboard grid (see `DashboardPlacement` for grid semantics).  `id` and the position fields are optional: when omitted, the placement gets a server-generated id and is appended below all existing tiles as a 6x6 tile. Returns the created placement.  The referenced widget must exist in the same project or be a Langfuse-managed widget. The API returns `409` if a placement with the same `id` already exists on the dashboard.

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**dashboard_id** | **String** |  | [required] |
**unstable_create_dashboard_placement_request** | [**UnstableCreateDashboardPlacementRequest**](UnstableCreateDashboardPlacementRequest.md) |  | [required] |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
unstable_dashboards_add_placement().configuration(&configuration).dashboard_id(..).unstable_create_dashboard_placement_request(..).options(&options).call().await
```

### Return type

[**models::UnstableDashboardPlacement**](UnstableDashboardPlacement.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## unstable_dashboards_create

> models::UnstableDashboard unstable_dashboards_create(unstable_create_dashboard_request, options)


Create a dashboard.

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**unstable_create_dashboard_request** | [**UnstableCreateDashboardRequest**](UnstableCreateDashboardRequest.md) |  | [required] |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
unstable_dashboards_create().configuration(&configuration).unstable_create_dashboard_request(..).options(&options).call().await
```

### Return type

[**models::UnstableDashboard**](UnstableDashboard.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## unstable_dashboards_delete

> models::UnstableDeleteDashboardResponse unstable_dashboards_delete(dashboard_id, options)


Delete a dashboard.

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**dashboard_id** | **String** |  | [required] |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
unstable_dashboards_delete().configuration(&configuration).dashboard_id(..).options(&options).call().await
```

### Return type

[**models::UnstableDeleteDashboardResponse**](UnstableDeleteDashboardResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## unstable_dashboards_delete_placement

> models::UnstableDeleteDashboardPlacementResponse unstable_dashboards_delete_placement(dashboard_id, placement_id, options)


Remove a placement from a dashboard grid without deleting the referenced widget.

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**dashboard_id** | **String** |  | [required] |
**placement_id** | **String** |  | [required] |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
unstable_dashboards_delete_placement().configuration(&configuration).dashboard_id(..).placement_id(..).options(&options).call().await
```

### Return type

[**models::UnstableDeleteDashboardPlacementResponse**](UnstableDeleteDashboardPlacementResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## unstable_dashboards_get

> models::UnstableDashboard unstable_dashboards_get(dashboard_id, options)


Get a dashboard by id.

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**dashboard_id** | **String** |  | [required] |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
unstable_dashboards_get().configuration(&configuration).dashboard_id(..).options(&options).call().await
```

### Return type

[**models::UnstableDashboard**](UnstableDashboard.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## unstable_dashboards_list

> models::UnstableDashboardList unstable_dashboards_list(page, limit, options)


List dashboards in the project, ordered by most recently updated first.

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**page** | Option<**i64**> | 1-based page number. Defaults to `1`. |  |
**limit** | Option<**i64**> | Maximum number of items per page. Defaults to `50`. |  |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
unstable_dashboards_list().configuration(&configuration).options(&options).call().await
```

### Return type

[**models::UnstableDashboardList**](UnstableDashboardList.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## unstable_dashboards_update

> models::UnstableDashboard unstable_dashboards_update(dashboard_id, unstable_update_dashboard_request, options)


Update a dashboard's name, description, definition, or filters.

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**dashboard_id** | **String** |  | [required] |
**unstable_update_dashboard_request** | [**UnstableUpdateDashboardRequest**](UnstableUpdateDashboardRequest.md) |  | [required] |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
unstable_dashboards_update().configuration(&configuration).dashboard_id(..).unstable_update_dashboard_request(..).options(&options).call().await
```

### Return type

[**models::UnstableDashboard**](UnstableDashboard.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## unstable_dashboards_update_placement

> models::UnstableDashboardPlacement unstable_dashboards_update_placement(dashboard_id, placement_id, unstable_update_dashboard_placement_request, options)


Move or resize a placement. All fields are optional; at least one is required. Omitted fields keep their current value. The placement's content (widget/preset reference) and id cannot change — delete and re-add the placement to swap content. Returns the updated placement.

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**dashboard_id** | **String** |  | [required] |
**placement_id** | **String** |  | [required] |
**unstable_update_dashboard_placement_request** | [**UnstableUpdateDashboardPlacementRequest**](UnstableUpdateDashboardPlacementRequest.md) |  | [required] |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
unstable_dashboards_update_placement().configuration(&configuration).dashboard_id(..).placement_id(..).unstable_update_dashboard_placement_request(..).options(&options).call().await
```

### Return type

[**models::UnstableDashboardPlacement**](UnstableDashboardPlacement.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

