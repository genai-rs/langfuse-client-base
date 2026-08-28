# \EvaluatorsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**evaluators_create**](EvaluatorsApi.md#evaluators_create) | **POST** /api/public/v2/evaluators | 
[**evaluators_delete**](EvaluatorsApi.md#evaluators_delete) | **DELETE** /api/public/v2/evaluators/{evaluatorId} | 
[**evaluators_get**](EvaluatorsApi.md#evaluators_get) | **GET** /api/public/v2/evaluators/{evaluatorId} | 
[**evaluators_list**](EvaluatorsApi.md#evaluators_list) | **GET** /api/public/v2/evaluators | 
[**evaluators_list_versions**](EvaluatorsApi.md#evaluators_list_versions) | **GET** /api/public/v2/evaluators/{evaluatorId}/versions | 
[**evaluators_update**](EvaluatorsApi.md#evaluators_update) | **PATCH** /api/public/v2/evaluators/{evaluatorId} | 



## evaluators_create

> models::Evaluator evaluators_create(create_evaluator_request)


Create an evaluator in the authenticated project.  An evaluator defines **how** Langfuse should score data. LLM-as-a-judge evaluators define a prompt, expected structured output, and optional model configuration. Code evaluators define source code and a runtime language.  This always creates a new evaluator with version `1`. Names are not identifiers and do not need to be unique.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**create_evaluator_request** | [**CreateEvaluatorRequest**](CreateEvaluatorRequest.md) |  | [required] |

### Return type

[**models::Evaluator**](Evaluator.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## evaluators_delete

> models::DeletedEvaluator evaluators_delete(evaluator_id)


Delete an evaluator and all of its stored versions.  Associated evaluation-rule assignments are also removed. Scores already produced by the evaluator are preserved.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**evaluator_id** | **String** | Stable evaluator identifier returned by the evaluator endpoints. | [required] |

### Return type

[**models::DeletedEvaluator**](DeletedEvaluator.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## evaluators_get

> models::Evaluator evaluators_get(evaluator_id)


Get one evaluator by its stable identifier.  The response includes the evaluator's latest definition and version metadata flattened into the evaluator object, plus associated evaluation rules. Use the version-history endpoint when older definitions are needed.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**evaluator_id** | **String** | Stable evaluator identifier returned by the evaluator endpoints. | [required] |

### Return type

[**models::Evaluator**](Evaluator.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## evaluators_list

> models::EvaluatorsPage evaluators_list(limit, cursor)


List evaluators in newest-first creation order.  Every evaluator includes its latest definition and version metadata flattened into the evaluator object, plus associated evaluation rules. Treat the cursor as opaque and return it unchanged.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**limit** | Option<**i32**> | Maximum number of items to return. Defaults to `50` and cannot exceed `100`. |  |
**cursor** | Option<**String**> | Opaque cursor returned by the previous page. |  |

### Return type

[**models::EvaluatorsPage**](EvaluatorsPage.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## evaluators_list_versions

> models::EvaluatorVersionsPage evaluators_list_versions(evaluator_id, limit, cursor)


List an evaluator's version history in newest-first order.  This endpoint is intended for history and audit use cases. Ordinary clients can use the flattened `version` and definition fields on the evaluator response.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**evaluator_id** | **String** | Stable evaluator identifier returned by the evaluator endpoints. | [required] |
**limit** | Option<**i32**> | Maximum number of versions to return. Defaults to `50` and cannot exceed `100`. |  |
**cursor** | Option<**String**> | Opaque cursor returned by the previous page. |  |

### Return type

[**models::EvaluatorVersionsPage**](EvaluatorVersionsPage.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## evaluators_update

> models::Evaluator evaluators_update(evaluator_id, update_evaluator_request)


Update an evaluator by its stable identifier.  Provide only the top-level fields to change. Metadata-only changes do not create a version. Evaluator type cannot change.  Definition fields are flattened into the request. To replace a definition, include `type` and every definition field for that type. Definition fields are replaced as a complete unit rather than merged. For LLM-as-a-judge evaluators, omitting or setting `modelConfig` to `null` selects the project's default evaluation model.  Replacing a definition automatically returns an evaluator paused by an invalid or missing model configuration to `active`, while preserving its id and evaluation-rule assignments. Pauses caused by provider authentication, billing, connectivity, account state, or an unknown legacy reason remain paused until the explicit reactivation check succeeds.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**evaluator_id** | **String** | Stable evaluator identifier returned by the evaluator endpoints. | [required] |
**update_evaluator_request** | [**UpdateEvaluatorRequest**](UpdateEvaluatorRequest.md) |  | [required] |

### Return type

[**models::Evaluator**](Evaluator.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

