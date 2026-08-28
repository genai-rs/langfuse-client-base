# \UnstableEvaluatorsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**unstable_evaluators_create**](UnstableEvaluatorsApi.md#unstable_evaluators_create) | **POST** /api/public/unstable/evaluators | 
[**unstable_evaluators_delete**](UnstableEvaluatorsApi.md#unstable_evaluators_delete) | **DELETE** /api/public/unstable/evaluators/{evaluatorId} | 
[**unstable_evaluators_get**](UnstableEvaluatorsApi.md#unstable_evaluators_get) | **GET** /api/public/unstable/evaluators/{evaluatorId} | 
[**unstable_evaluators_list**](UnstableEvaluatorsApi.md#unstable_evaluators_list) | **GET** /api/public/unstable/evaluators | 



## unstable_evaluators_create

> models::UnstableEvaluator unstable_evaluators_create(unstable_create_evaluator_request)


**Deprecated:** On Langfuse Cloud, this unstable endpoint is deprecated and will be removed on September 4, 2026. Use the stable `/api/public/v2/evaluators` API instead. Self-hosted deployments are unaffected by this date; the endpoint becomes unavailable when they upgrade to Langfuse v4. See the [Langfuse v3 to v4 upgrade guide](https://langfuse.com/self-hosting/upgrade/upgrade-guides/upgrade-v3-to-v4).  Create an evaluator in the authenticated project.  Use evaluators to define **how** Langfuse should score data. LLM-as-a-judge evaluators define a prompt, expected structured output, and optional model configuration. Code evaluators define source code and a runtime language.  Naming behavior: - If this is a new evaluator name in your project, Langfuse creates version `1`. - If the name already exists in your project, Langfuse creates the next version and returns it. - The evaluator `id` remains stable across versions. - Existing evaluation rules automatically use the latest evaluator version; no rule update is required.  Recommended workflow: 1. Create the evaluator. 2. Read the returned `variables` array. 3. Read the returned `outputDefinition.dataType` so the client knows whether future scores will be numeric, boolean, or categorical. 4. Create one or more evaluation rules that reference the returned evaluator family using `name` and `type`.  Code evaluator validation: - At creation, Langfuse only validates the request shape - The `sourceCode` itself is not executed here. It is first run (preflight-tested against a sample observation) when you link the evaluator to an evaluation rule, so runtime errors in the code surface at evaluation-rule creation, not at evaluator creation.  Recovery guidance: - `422` with `code=evaluator_preflight_failed`: the evaluator cannot run with the resolved model configuration. Add a valid explicit `modelConfig`, or configure the project's default evaluation model, then retry the same request. - `400` with `code=invalid_body`: the request shape is malformed. Use the structured `details.issues` array to fix the specific fields and retry. - `400` with `code=invalid_body` on `outputDefinition`: for `type=llm_as_judge`, send `dataType`, `reasoning.description`, and `score.description`. Do not send `version`; it is not part of the public request shape. - If `type` is omitted, Langfuse treats the request as `type=llm_as_judge` for backwards compatibility. New clients should send `type` explicitly.  Unstable API note: - This surface may evolve while the underlying evaluation data model is being redesigned.

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


## unstable_evaluators_delete

> models::UnstableDeleteEvaluatorResponse unstable_evaluators_delete(evaluator_id)


**Deprecated:** On Langfuse Cloud, this unstable endpoint is deprecated and will be removed on September 4, 2026. Use the stable `/api/public/v2/evaluators` API instead. Self-hosted deployments are unaffected by this date; the endpoint becomes unavailable when they upgrade to Langfuse v4. See the [Langfuse v3 to v4 upgrade guide](https://langfuse.com/self-hosting/upgrade/upgrade-guides/upgrade-v3-to-v4).  Delete an evaluator.  Important behavior: - This deletes the evaluator including all of its stored versions. - Evaluation rule assignments referencing the evaluator are also deleted. - Scores already produced by the evaluator are not deleted.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**evaluator_id** | **String** | Evaluator identifier returned by the evaluator endpoints. | [required] |

### Return type

[**models::UnstableDeleteEvaluatorResponse**](unstableDeleteEvaluatorResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## unstable_evaluators_get

> models::UnstableEvaluator unstable_evaluators_get(evaluator_id)


**Deprecated:** On Langfuse Cloud, this unstable endpoint is deprecated and will be removed on September 4, 2026. Use the stable `/api/public/v2/evaluators` API instead. Self-hosted deployments are unaffected by this date; the endpoint becomes unavailable when they upgrade to Langfuse v4. See the [Langfuse v3 to v4 upgrade guide](https://langfuse.com/self-hosting/upgrade/upgrade-guides/upgrade-v3-to-v4).  Get one evaluator by `id`.  This endpoint always returns the evaluator's latest version. Use it when you want the current prompt, output definition, model configuration, and derived variables for the evaluator you plan to use in an evaluation rule.

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


**Deprecated:** On Langfuse Cloud, this unstable endpoint is deprecated and will be removed on September 4, 2026. Use the stable `/api/public/v2/evaluators` API instead. Self-hosted deployments are unaffected by this date; the endpoint becomes unavailable when they upgrade to Langfuse v4. See the [Langfuse v3 to v4 upgrade guide](https://langfuse.com/self-hosting/upgrade/upgrade-guides/upgrade-v3-to-v4).  List the evaluators available to the authenticated project.  Important behavior: - This endpoint returns the latest version of each available evaluator. - Every evaluator is owned by the authenticated project.

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

