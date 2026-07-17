# \UnstableDashboardWidgetsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**unstable_dashboard_widgets_create**](UnstableDashboardWidgetsApi.md#unstable_dashboard_widgets_create) | **POST** /api/public/unstable/dashboard-widgets | 
[**unstable_dashboard_widgets_delete**](UnstableDashboardWidgetsApi.md#unstable_dashboard_widgets_delete) | **DELETE** /api/public/unstable/dashboard-widgets/{widgetId} | 
[**unstable_dashboard_widgets_get**](UnstableDashboardWidgetsApi.md#unstable_dashboard_widgets_get) | **GET** /api/public/unstable/dashboard-widgets/{widgetId} | 
[**unstable_dashboard_widgets_list**](UnstableDashboardWidgetsApi.md#unstable_dashboard_widgets_list) | **GET** /api/public/unstable/dashboard-widgets | 
[**unstable_dashboard_widgets_update**](UnstableDashboardWidgetsApi.md#unstable_dashboard_widgets_update) | **PATCH** /api/public/unstable/dashboard-widgets/{widgetId} | 



## unstable_dashboard_widgets_create

> models::UnstableDashboardWidget unstable_dashboard_widgets_create(unstable_create_dashboard_widget_request)


Create a dashboard widget (a standalone chart definition you place on any dashboard).  This endpoint creates the widget only; place it on a dashboard via `POST /dashboards/{dashboardId}/placements`.  Supported views are `observations`, `scores-numeric`, and `scores-categorical`. The legacy `traces` view is not supported by this unstable API. Widgets are created as v2 internally.  `chartConfig` is optional and defaults to the plain config for `chartType`; when `chartConfig.type` is given it must match `chartType`.  Unstable API note: - This surface may evolve while dashboard/widget APIs are being finalized.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**unstable_create_dashboard_widget_request** | [**UnstableCreateDashboardWidgetRequest**](UnstableCreateDashboardWidgetRequest.md) |  | [required] |

### Return type

[**models::UnstableDashboardWidget**](unstableDashboardWidget.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## unstable_dashboard_widgets_delete

> models::UnstableDeleteDashboardWidgetResponse unstable_dashboard_widgets_delete(widget_id)


Delete a dashboard widget.  The API returns `409` while the widget is still placed on a dashboard. Remove those placements first.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**widget_id** | **String** |  | [required] |

### Return type

[**models::UnstableDeleteDashboardWidgetResponse**](unstableDeleteDashboardWidgetResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## unstable_dashboard_widgets_get

> models::UnstableDashboardWidget unstable_dashboard_widgets_get(widget_id)


Get a dashboard widget by id.  The response may use `view: traces` for legacy widgets.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**widget_id** | **String** |  | [required] |

### Return type

[**models::UnstableDashboardWidget**](unstableDashboardWidget.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## unstable_dashboard_widgets_list

> models::UnstableDashboardWidgetList unstable_dashboard_widgets_list(page, limit)


List dashboard widgets in the project, ordered by most recently updated first.  Responses may include legacy `traces` widgets created before this API existed. New widgets cannot be created with `view: traces`.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**page** | Option<**i32**> | 1-based page number. Defaults to `1`. |  |
**limit** | Option<**i32**> | Maximum number of items per page. Defaults to `50`. |  |

### Return type

[**models::UnstableDashboardWidgetList**](unstableDashboardWidgetList.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## unstable_dashboard_widgets_update

> models::UnstableDashboardWidget unstable_dashboard_widgets_update(widget_id, unstable_update_dashboard_widget_request)


Update a dashboard widget.  All fields are optional; at least one field is required. Changing `chartType` without sending `chartConfig` resets the config to the new chart type's defaults. When `chartConfig.type` is given it must match the widget's (possibly updated) `chartType`.  `view` cannot be changed to the legacy `traces` value. Existing `traces` widgets may be updated on other fields.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**widget_id** | **String** |  | [required] |
**unstable_update_dashboard_widget_request** | [**UnstableUpdateDashboardWidgetRequest**](UnstableUpdateDashboardWidgetRequest.md) |  | [required] |

### Return type

[**models::UnstableDashboardWidget**](unstableDashboardWidget.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

