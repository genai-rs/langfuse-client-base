# \FeedbackApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**feedback_submit**](FeedbackApi.md#feedback_submit) | **POST** /api/public/feedback | 



## feedback_submit

> models::SubmitFeedbackResponse feedback_submit(submit_feedback_request)


Submit explicit user-approved feedback about Langfuse skills, MCP tools, CLI, docs, or public API. Do not include secrets, credentials, customer data, trace payloads, or unrelated use-case details.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**submit_feedback_request** | [**SubmitFeedbackRequest**](SubmitFeedbackRequest.md) |  | [required] |

### Return type

[**models::SubmitFeedbackResponse**](SubmitFeedbackResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

