# ObservationsView

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** | The unique identifier of the observation | 
**trace_id** | Option<**String**> | The trace ID associated with the observation | 
**r#type** | **String** | The type of the observation | 
**name** | Option<**String**> | The name of the observation | 
**start_time** | **chrono::DateTime<chrono::FixedOffset>** | The start time of the observation | 
**end_time** | Option<**chrono::DateTime<chrono::FixedOffset>**> | The end time of the observation. | 
**completion_start_time** | Option<**chrono::DateTime<chrono::FixedOffset>**> | The completion start time of the observation | 
**model** | Option<**String**> | The model used for the observation | 
**model_parameters** | Option<**serde_json::Value**> | The parameters of the model used for the observation | 
**input** | Option<**serde_json::Value**> | The input data of the observation | 
**version** | Option<**String**> | The version of the observation | 
**metadata** | Option<**serde_json::Value**> | Additional metadata of the observation | 
**output** | Option<**serde_json::Value**> | The output data of the observation | 
**usage** | [**models::Usage**](Usage.md) |  | 
**level** | [**models::ObservationLevel**](ObservationLevel.md) |  | 
**status_message** | Option<**String**> | The status message of the observation | 
**parent_observation_id** | Option<**String**> | The parent observation ID | 
**prompt_id** | Option<**String**> | The prompt ID associated with the observation | 
**usage_details** | **std::collections::HashMap<String, i32>** | The usage details of the observation. Key is the name of the usage metric, value is the number of units consumed. The total key is the sum of all (non-total) usage metrics or the total value ingested. | 
**cost_details** | **std::collections::HashMap<String, f64>** | The cost details of the observation. Key is the name of the cost metric, value is the cost in USD. The total key is the sum of all (non-total) cost metrics or the total value ingested. | 
**environment** | **String** | The environment from which this observation originated. Can be any lowercase alphanumeric string with hyphens and underscores that does not start with 'langfuse'. | 
**prompt_name** | Option<**String**> | The name of the prompt associated with the observation | 
**prompt_version** | Option<**i32**> | The version of the prompt associated with the observation | 
**model_id** | Option<**String**> | The unique identifier of the model | 
**input_price** | Option<**f64**> | The price of the input in USD | 
**output_price** | Option<**f64**> | The price of the output in USD. | 
**total_price** | Option<**f64**> | The total price in USD. | 
**calculated_input_cost** | Option<**f64**> | (Deprecated. Use usageDetails and costDetails instead.) The calculated cost of the input in USD | 
**calculated_output_cost** | Option<**f64**> | (Deprecated. Use usageDetails and costDetails instead.) The calculated cost of the output in USD | 
**calculated_total_cost** | Option<**f64**> | (Deprecated. Use usageDetails and costDetails instead.) The calculated total cost in USD | 
**latency** | Option<**f64**> | The latency in seconds. | 
**time_to_first_token** | Option<**f64**> | The time to the first token in seconds | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


