# \EvaluationRulesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**evaluation_rules_create**](EvaluationRulesApi.md#evaluation_rules_create) | **POST** /api/public/v2/evaluation-rules | 
[**evaluation_rules_delete**](EvaluationRulesApi.md#evaluation_rules_delete) | **DELETE** /api/public/v2/evaluation-rules/{evaluationRuleId} | 
[**evaluation_rules_get**](EvaluationRulesApi.md#evaluation_rules_get) | **GET** /api/public/v2/evaluation-rules/{evaluationRuleId} | 
[**evaluation_rules_list**](EvaluationRulesApi.md#evaluation_rules_list) | **GET** /api/public/v2/evaluation-rules | 
[**evaluation_rules_update**](EvaluationRulesApi.md#evaluation_rules_update) | **PATCH** /api/public/v2/evaluation-rules/{evaluationRuleId} | 



## evaluation_rules_create

> models::EvaluationRule evaluation_rules_create(create_evaluation_rule_request)


Create an evaluation rule using stable evaluator identifiers.  An evaluation rule defines **which** incoming observations should be evaluated and how prompt variables should be populated.  Key behavior: - rule names are not identifiers and do not need to be unique - rules always use the latest version of each associated evaluator - an enabled rule requires at least one evaluator assignment - omit `sampling` to evaluate every matching observation - omit `filter` to match every incoming observation - `datasetId` is the public filter name for selecting experiment datasets

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**create_evaluation_rule_request** | [**CreateEvaluationRuleRequest**](CreateEvaluationRuleRequest.md) |  | [required] |

### Return type

[**models::EvaluationRule**](EvaluationRule.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## evaluation_rules_delete

> models::DeletedEvaluationRule evaluation_rules_delete(evaluation_rule_id)


Delete an evaluation rule.  This removes the live-ingestion rule only. It does not delete associated evaluators or scores already produced by them.  Legacy trace and dataset rules can also be deleted. Their evaluators and previously produced scores are preserved.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**evaluation_rule_id** | **String** | Stable evaluation-rule identifier returned by the evaluation-rule endpoints. | [required] |

### Return type

[**models::DeletedEvaluationRule**](DeletedEvaluationRule.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## evaluation_rules_get

> models::EvaluationRule evaluation_rules_get(evaluation_rule_id)


Get one evaluation rule, including a legacy trace or dataset rule, by its stable identifier.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**evaluation_rule_id** | **String** | Stable evaluation-rule identifier returned by the evaluation-rule endpoints. | [required] |

### Return type

[**models::EvaluationRule**](EvaluationRule.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## evaluation_rules_list

> models::EvaluationRulesPage evaluation_rules_list(limit, cursor)


List evaluation rules in newest-first creation order.  This includes legacy trace and dataset rules so they can be inspected and migrated. Treat the cursor as opaque and return it unchanged.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**limit** | Option<**i32**> | Maximum number of items to return. Defaults to `50` and cannot exceed `100`. |  |
**cursor** | Option<**String**> | Opaque cursor returned by the previous page. |  |

### Return type

[**models::EvaluationRulesPage**](EvaluationRulesPage.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


## evaluation_rules_update

> models::EvaluationRule evaluation_rules_update(evaluation_rule_id, update_evaluation_rule_request)


Update an evaluation rule by its stable identifier.  Provide only the fields to change. Providing `evaluatorAssignments` replaces the complete assignment list. Replacing the list with an empty array disables the rule. Setting `enabled=true` is rejected when the resulting assignment list is empty, including when both fields are sent in the same request.  Legacy trace and dataset rules follow the existing lifecycle restrictions: they can be deactivated with `enabled=false`, but their name, filters, sampling, and evaluator assignments cannot be changed.

### Parameters


Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**evaluation_rule_id** | **String** | Stable evaluation-rule identifier returned by the evaluation-rule endpoints. | [required] |
**update_evaluation_rule_request** | [**UpdateEvaluationRuleRequest**](UpdateEvaluationRuleRequest.md) |  | [required] |

### Return type

[**models::EvaluationRule**](EvaluationRule.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

