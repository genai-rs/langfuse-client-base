# UnstableEvaluator

## Enum Variants

| Name | Description |
|---- | -----|
| UnstableEvaluatorOneOf | One evaluator that can be used for scoring.  An evaluator describes **how** to score data.  It does not define **which** live objects are evaluated. That is the job of &#x60;evaluation-rules&#x60;.  For agent clients, the most important fields are: - &#x60;type&#x60;: determines which evaluator fields are present - &#x60;variables&#x60;: for LLM evaluators, use these exact names when building the evaluation-rule &#x60;mapping&#x60; array. LLM evaluators require every variable to be mapped. Code evaluators always expose the fixed runtime payload fields and Langfuse maps them automatically.  Versioning behavior: - &#x60;GET /evaluators&#x60; returns the latest version of each available evaluator. - &#x60;GET /evaluators/{id}&#x60; can return an older version. - Evaluation rules always run against the latest version for the selected evaluator name within the same source (&#x60;project&#x60; or &#x60;managed&#x60;). |
| UnstableEvaluatorOneOf1 | One evaluator that can be used for scoring.  An evaluator describes **how** to score data.  It does not define **which** live objects are evaluated. That is the job of &#x60;evaluation-rules&#x60;.  For agent clients, the most important fields are: - &#x60;type&#x60;: determines which evaluator fields are present - &#x60;variables&#x60;: for LLM evaluators, use these exact names when building the evaluation-rule &#x60;mapping&#x60; array. LLM evaluators require every variable to be mapped. Code evaluators always expose the fixed runtime payload fields and Langfuse maps them automatically.  Versioning behavior: - &#x60;GET /evaluators&#x60; returns the latest version of each available evaluator. - &#x60;GET /evaluators/{id}&#x60; can return an older version. - Evaluation rules always run against the latest version for the selected evaluator name within the same source (&#x60;project&#x60; or &#x60;managed&#x60;). |

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


