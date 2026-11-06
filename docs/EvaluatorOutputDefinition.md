# EvaluatorOutputDefinition

## Enum Variants

| Name | Description |
|---- | -----|
| EvaluatorOutputDefinitionPublicEvaluatorBooleanScore | Flat structured output definition used when creating or updating an evaluator.  - &#x60;dataType&#x60; is required. - &#x60;scoreReasoningInstructions&#x60; and &#x60;scoreValueInstructions&#x60; are optional instructions. - &#x60;minValue&#x60; and &#x60;maxValue&#x60; apply only to &#x60;NUMERIC&#x60; outputs. If both are set, &#x60;minValue&#x60; must not exceed &#x60;maxValue&#x60;. - &#x60;categories&#x60; and &#x60;shouldAllowMultipleMatches&#x60; apply only to &#x60;CATEGORICAL&#x60; outputs. - Do not send &#x60;version&#x60;; that is an internal storage detail. |
| EvaluatorOutputDefinitionPublicEvaluatorCategoricalScore | Flat structured output definition used when creating or updating an evaluator.  - &#x60;dataType&#x60; is required. - &#x60;scoreReasoningInstructions&#x60; and &#x60;scoreValueInstructions&#x60; are optional instructions. - &#x60;minValue&#x60; and &#x60;maxValue&#x60; apply only to &#x60;NUMERIC&#x60; outputs. If both are set, &#x60;minValue&#x60; must not exceed &#x60;maxValue&#x60;. - &#x60;categories&#x60; and &#x60;shouldAllowMultipleMatches&#x60; apply only to &#x60;CATEGORICAL&#x60; outputs. - Do not send &#x60;version&#x60;; that is an internal storage detail. |
| EvaluatorOutputDefinitionPublicEvaluatorNumericScore | Flat structured output definition used when creating or updating an evaluator.  - &#x60;dataType&#x60; is required. - &#x60;scoreReasoningInstructions&#x60; and &#x60;scoreValueInstructions&#x60; are optional instructions. - &#x60;minValue&#x60; and &#x60;maxValue&#x60; apply only to &#x60;NUMERIC&#x60; outputs. If both are set, &#x60;minValue&#x60; must not exceed &#x60;maxValue&#x60;. - &#x60;categories&#x60; and &#x60;shouldAllowMultipleMatches&#x60; apply only to &#x60;CATEGORICAL&#x60; outputs. - Do not send &#x60;version&#x60;; that is an internal storage detail. |

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


