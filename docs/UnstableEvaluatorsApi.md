# \UnstableEvaluatorsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**unstable_evaluators_create**](UnstableEvaluatorsApi.md#unstable_evaluators_create) | **POST** /api/public/unstable/evaluators | 
[**unstable_evaluators_get**](UnstableEvaluatorsApi.md#unstable_evaluators_get) | **GET** /api/public/unstable/evaluators/{evaluatorId} | 
[**unstable_evaluators_list**](UnstableEvaluatorsApi.md#unstable_evaluators_list) | **GET** /api/public/unstable/evaluators | 



## unstable_evaluators_create

> models::UnstableEvaluator unstable_evaluators_create(unstable_create_evaluator_request)


Create an evaluator in the authenticated project.  Use evaluators to define **how** Langfuse should score data: the prompt, the expected structured output, and the optional model configuration.  Naming behavior: - If this is a new evaluator name in your project, Langfuse creates version `1`. - If the name already exists in your project, Langfuse creates the next version and returns it. - When a new project version is created, existing evaluation rules in that project automatically move to the newest version for that evaluator name.  Recommended workflow: 1. Create the evaluator. 2. Read the returned `variables` array. 3. Read the returned `outputDefinition.dataType` so the client knows whether future scores will be numeric, boolean, or categorical. 4. Create one or more evaluation rules that reference the returned evaluator family using `name` and `scope`.  Recovery guidance: - `422` with `code=evaluator_preflight_failed`: the evaluator cannot run with the resolved model configuration. Add a valid explicit `modelConfig`, or configure the project's default evaluation model, then retry the same request. - `400` with `code=invalid_body`: the request shape is malformed. Use the structured `details.issues` array to fix the specific fields and retry. - `400` with `code=invalid_body` on `outputDefinition`: send `dataType`, `reasoning.description`, and `score.description`. Do not send `version`; it is not part of the public request shape.  Unstable API note: - This surface may evolve while the underlying evaluation data model is being redesigned.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**unstable_create_evaluator_request** | [**UnstableCreateEvaluatorRequest**](UnstableCreateEvaluatorRequest.md) |  | [required] |

### Return type

[**models::UnstableEvaluator**](unstableEvaluator.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## unstable_evaluators_get

> models::UnstableEvaluator unstable_evaluators_get(evaluator_id)


Get one evaluator by `id`.  Use this endpoint when you want the prompt, output definition, model configuration, and derived variables for the evaluator you plan to use in an evaluation rule.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**evaluator_id** | **String** | Evaluator identifier returned by the evaluator endpoints. | [required] |

### Return type

[**models::UnstableEvaluator**](unstableEvaluator.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## unstable_evaluators_list

> models::UnstableEvaluators unstable_evaluators_list(page, limit)


List the evaluators available to the authenticated project.  Important behavior: - This endpoint returns the latest version of each available evaluator. - Results can include evaluators from your project and Langfuse-managed evaluators. - If the same evaluator name exists in both places, both are returned as separate items with different `scope` values.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**page** | Option<**i32**> | 1-based page number. Defaults to `1`. |  |
**limit** | Option<**i32**> | Maximum number of items per page. Defaults to `50`. |  |

### Return type

[**models::UnstableEvaluators**](unstableEvaluators.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

