# UnstableCreateEvaluatorRequest

## Enum Variants

| Name | Description |
|---- | -----|
| UnstableCreateCodeEvaluatorRequest | Request body for creating an evaluator.  If the same &#x60;name&#x60; already exists in your project, Langfuse creates the next version and returns it. Existing evaluation rules automatically use the latest evaluator version. If &#x60;type&#x60; is omitted, Langfuse defaults it to &#x60;llm_as_judge&#x60; for backwards compatibility. |
| UnstableCreateLlmAsJudgeEvaluatorRequest | Request body for creating an evaluator.  If the same &#x60;name&#x60; already exists in your project, Langfuse creates the next version and returns it. Existing evaluation rules automatically use the latest evaluator version. If &#x60;type&#x60; is omitted, Langfuse defaults it to &#x60;llm_as_judge&#x60; for backwards compatibility. |

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


