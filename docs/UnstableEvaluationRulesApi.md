# \UnstableEvaluationRulesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**unstable_evaluation_rules_create**](UnstableEvaluationRulesApi.md#unstable_evaluation_rules_create) | **POST** /api/public/unstable/evaluation-rules | 
[**unstable_evaluation_rules_delete**](UnstableEvaluationRulesApi.md#unstable_evaluation_rules_delete) | **DELETE** /api/public/unstable/evaluation-rules/{evaluationRuleId} | 
[**unstable_evaluation_rules_get**](UnstableEvaluationRulesApi.md#unstable_evaluation_rules_get) | **GET** /api/public/unstable/evaluation-rules/{evaluationRuleId} | 
[**unstable_evaluation_rules_list**](UnstableEvaluationRulesApi.md#unstable_evaluation_rules_list) | **GET** /api/public/unstable/evaluation-rules | 
[**unstable_evaluation_rules_update**](UnstableEvaluationRulesApi.md#unstable_evaluation_rules_update) | **PATCH** /api/public/unstable/evaluation-rules/{evaluationRuleId} | 



## unstable_evaluation_rules_create

> models::UnstableEvaluationRule unstable_evaluation_rules_create(unstable_create_evaluation_rule_request)


Create an evaluation rule.  An evaluation rule defines **what** incoming data should be evaluated and **how prompt variables should be populated** from that data.  Use this resource after choosing an evaluator from the evaluator endpoints.  Key rules: - `name` must be unique within the project for public evaluation rules - `target` must be `observation` or `experiment` - `evaluator.name` + `evaluator.scope` must identify an existing evaluator family returned by the evaluator endpoints - Langfuse resolves that family to its latest version before saving the evaluation rule - for `target=experiment`, use dataset `id` values from `GET /api/public/v2/datasets` when filtering by `datasetId` - every evaluator prompt variable must be mapped exactly once - `expected_output` mappings are only valid for `target=experiment` - if `enabled=true`, Langfuse validates that the referenced evaluator can currently run - at most 50 evaluation rules can be effectively active in one project at the same time  If an evaluation rule with the same `name` already exists in the project, the API returns `409`. In that case, update the existing resource with `PATCH /api/public/unstable/evaluation-rules/{evaluationRuleId}` instead of creating a second one.  If enabling this resource would exceed the 50-active limit, the API also returns `409`. In that case, disable or pause another active evaluation rule before enabling a new one.  Current scope: - evaluation rules are live-ingestion rules only - they do not trigger historical backfills  Recovery guidance: - `400 invalid_filter_value`: fix the filter `column` or `value` using `details.column`, `details.invalidValues`, and `details.allowedValues` - `400 invalid_filter_value` with `details.column=datasetId`: call `GET /api/public/v2/datasets`, then retry with dataset `id` values from that response - `400 missing_variable_mapping`: fetch the evaluator again and make sure every variable in `variables` appears exactly once in `mapping` - `400 duplicate_variable_mapping`: remove repeated mappings for the same variable - `400 invalid_variable_mapping`: switch to a valid `source` for the selected `target`, or fix the variable name - `400 invalid_json_path`: remove or correct the `jsonPath` - `422 evaluator_preflight_failed`: the selected evaluator cannot run with the resolved model configuration. Fix the evaluator/default model setup, then retry the create request.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**unstable_create_evaluation_rule_request** | [**UnstableCreateEvaluationRuleRequest**](UnstableCreateEvaluationRuleRequest.md) |  | [required] |

### Return type

[**models::UnstableEvaluationRule**](unstableEvaluationRule.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## unstable_evaluation_rules_delete

> models::UnstableDeleteEvaluationRuleResponse unstable_evaluation_rules_delete(evaluation_rule_id)


Delete an evaluation rule.  This removes the live-ingestion rule only. It does not delete the referenced evaluator.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**evaluation_rule_id** | **String** | Evaluation rule identifier. | [required] |

### Return type

[**models::UnstableDeleteEvaluationRuleResponse**](unstableDeleteEvaluationRuleResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## unstable_evaluation_rules_get

> models::UnstableEvaluationRule unstable_evaluation_rules_get(evaluation_rule_id)


Get one evaluation rule by its identifier.  Use this endpoint to inspect the current evaluator, target, mapping, filters, and effective runtime status.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**evaluation_rule_id** | **String** | Evaluation rule identifier returned by the evaluation rule endpoints. | [required] |

### Return type

[**models::UnstableEvaluationRule**](unstableEvaluationRule.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## unstable_evaluation_rules_list

> models::UnstableEvaluationRules unstable_evaluation_rules_list(page, limit)


List evaluation rules in the authenticated project.  Each item describes one live evaluation rule and its effective runtime status.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**page** | Option<**i32**> | 1-based page number. Defaults to `1`. |  |
**limit** | Option<**i32**> | Maximum number of items per page. Defaults to `50`. |  |

### Return type

[**models::UnstableEvaluationRules**](unstableEvaluationRules.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## unstable_evaluation_rules_update

> models::UnstableEvaluationRule unstable_evaluation_rules_update(evaluation_rule_id, unstable_update_evaluation_rule_request)


Update an evaluation rule.  Typical uses: - enable or disable live execution - switch to another evaluator - adjust sampling - change filters - update variable mappings  Important behavior: - provide only the fields you want to change - if you provide `evaluator`, Langfuse resolves that evaluator family to its latest version before saving - changing `target`, `filter`, or `mapping` must still produce a valid target-specific configuration - if you change `target`, also send a compatible `filter` and `mapping` in the same request unless the existing ones are still valid for the new target - if the resulting config is enabled, Langfuse re-validates that the selected evaluator can run - if the update would move a non-active evaluation rule into the active state and the project already has 50 active evaluation rules, the API returns `409`  Recovery guidance: - if the update fails with `missing_variable_mapping` or `invalid_variable_mapping` after changing `evaluator` or `target`, resend the request with a complete new `mapping` - if the update fails with `invalid_filter_value` after changing `target`, resend the request with a target-compatible `filter`

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**evaluation_rule_id** | **String** | Evaluation rule identifier. | [required] |
**unstable_update_evaluation_rule_request** | [**UnstableUpdateEvaluationRuleRequest**](UnstableUpdateEvaluationRuleRequest.md) |  | [required] |

### Return type

[**models::UnstableEvaluationRule**](unstableEvaluationRule.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

