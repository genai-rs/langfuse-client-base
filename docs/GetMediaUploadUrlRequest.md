# GetMediaUploadUrlRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**trace_id** | Option<**String**> | The trace the media is associated with. Null for dataset item media uploads. | [optional]
**observation_id** | Option<**String**> | The observation ID associated with the media record. If the media record is associated directly with a trace, this will be null. | [optional]
**dataset_id** | Option<**String**> | The dataset the media belongs to. Null for trace/observation media uploads. | [optional]
**dataset_item_id** | Option<**String**> | The dataset item the media is associated with (need not exist yet). Null for trace/observation media uploads. | [optional]
**content_type** | [**models::MediaContentType**](MediaContentType.md) |  | 
**content_length** | **i32** | The size of the media record in bytes | 
**sha256_hash** | **String** | The SHA-256 hash of the media record | 
**field** | **String** | The item field the media is in: `input`/`output`/`metadata` (trace) or `input`/`expectedOutput`/`metadata` (dataset item). | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


