# UnstableCreateEvaluationRuleRequest

## Enum Variants

| Name | Description |
|---- | -----|
| UnstableCreateCodeEvaluationRuleRequest | Request body for creating an evaluation rule.  Checklist for agents and SDK clients: - reference an existing evaluator family by &#x60;evaluator.name&#x60; and &#x60;evaluator.scope&#x60; - choose &#x60;target&#x3D;observation&#x60; or &#x60;target&#x3D;experiment&#x60; - if &#x60;target&#x3D;experiment&#x60; and you want a dataset filter, call &#x60;GET /api/public/v2/datasets&#x60; first and use dataset &#x60;id&#x60; values in &#x60;filter[].value&#x60; - for &#x60;llm_as_judge&#x60;, fetch or inspect the evaluator first and provide a complete variable mapping for every evaluator variable - for &#x60;code&#x60;, do not send variables or mappings; Langfuse stores the fixed code runtime mapping automatically - optionally narrow execution with &#x60;filter&#x60; - set &#x60;enabled&#x3D;true&#x60; only when you want live execution immediately |
| UnstableCreateLlmAsJudgeEvaluationRuleRequest | Request body for creating an evaluation rule.  Checklist for agents and SDK clients: - reference an existing evaluator family by &#x60;evaluator.name&#x60; and &#x60;evaluator.scope&#x60; - choose &#x60;target&#x3D;observation&#x60; or &#x60;target&#x3D;experiment&#x60; - if &#x60;target&#x3D;experiment&#x60; and you want a dataset filter, call &#x60;GET /api/public/v2/datasets&#x60; first and use dataset &#x60;id&#x60; values in &#x60;filter[].value&#x60; - for &#x60;llm_as_judge&#x60;, fetch or inspect the evaluator first and provide a complete variable mapping for every evaluator variable - for &#x60;code&#x60;, do not send variables or mappings; Langfuse stores the fixed code runtime mapping automatically - optionally narrow execution with &#x60;filter&#x60; - set &#x60;enabled&#x3D;true&#x60; only when you want live execution immediately |

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


