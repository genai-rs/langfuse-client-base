# \UnstableDashboardWidgetsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**unstable_dashboard_widgets_create**](UnstableDashboardWidgetsApi.md#unstable_dashboard_widgets_create) | **POST** /api/public/unstable/dashboard-widgets | 



## unstable_dashboard_widgets_create

> models::UnstableDashboardWidget unstable_dashboard_widgets_create(unstable_create_dashboard_widget_request)


Create a reusable dashboard widget.  This endpoint creates the widget. It does not place the widget on a dashboard grid, this has to be done in the UI.  Supported views are `observations`, `scores-numeric`, and `scores-categorical`. The legacy `traces` view is not supported by this unstable API, `minVersion` defaults to `2`; values below `2` are rejected.  Unstable API note: - This surface may evolve while dashboard/widget APIs are being finalized.

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

