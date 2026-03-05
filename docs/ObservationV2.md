# ObservationV2

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** | The unique identifier of the observation | 
**trace_id** | Option<**String**> | The trace ID associated with the observation | [optional]
**start_time** | **String** | The start time of the observation | 
**end_time** | Option<**String**> | The end time of the observation | [optional]
**project_id** | **String** | The project ID this observation belongs to | 
**parent_observation_id** | Option<**String**> | The parent observation ID | [optional]
**r#type** | **String** | The type of the observation (e.g. GENERATION, SPAN, EVENT) | 
**name** | Option<**String**> | The name of the observation | [optional]
**level** | Option<[**models::ObservationLevel**](ObservationLevel.md)> |  | [optional]
**status_message** | Option<**String**> | The status message of the observation | [optional]
**version** | Option<**String**> | The version of the observation | [optional]
**environment** | Option<**String**> | The environment from which this observation originated | [optional]
**bookmarked** | Option<**bool**> | Whether the observation is bookmarked | [optional]
**public** | Option<**bool**> | Whether the observation is public | [optional]
**user_id** | Option<**String**> | The user ID associated with the observation | [optional]
**session_id** | Option<**String**> | The session ID associated with the observation | [optional]
**completion_start_time** | Option<**String**> | The completion start time of the observation | [optional]
**created_at** | Option<**String**> | The creation timestamp of the observation | [optional]
**updated_at** | Option<**String**> | The last update timestamp of the observation | [optional]
**input** | Option<**serde_json::Value**> | The input data of the observation | [optional]
**output** | Option<**serde_json::Value**> | The output data of the observation | [optional]
**metadata** | Option<**serde_json::Value**> | Additional metadata of the observation | [optional]
**provided_model_name** | Option<**String**> | The model name as provided by the user | [optional]
**internal_model_id** | Option<**String**> | The internal model ID matched by Langfuse | [optional]
**model_parameters** | Option<**serde_json::Value**> | The parameters of the model used for the observation | [optional]
**usage_details** | Option<**std::collections::HashMap<String, i32>**> | The usage details of the observation. Key is the usage metric name, value is the number of units consumed. | [optional]
**cost_details** | Option<**std::collections::HashMap<String, f64>**> | The cost details of the observation. Key is the cost metric name, value is the cost in USD. | [optional]
**total_cost** | Option<**f64**> | The total cost of the observation in USD | [optional]
**prompt_id** | Option<**String**> | The prompt ID associated with the observation | [optional]
**prompt_name** | Option<**String**> | The prompt name associated with the observation | [optional]
**prompt_version** | Option<**i32**> | The prompt version associated with the observation | [optional]
**latency** | Option<**f64**> | The latency in seconds | [optional]
**time_to_first_token** | Option<**f64**> | The time to first token in seconds | [optional]
**model_id** | Option<**String**> | The matched model ID | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


