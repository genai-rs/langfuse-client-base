# \UnstableBillableUnitsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**unstable_billable_units_get**](UnstableBillableUnitsApi.md#unstable_billable_units_get) | **GET** /api/public/unstable/organizations/billable-units | 



## unstable_billable_units_get

> models::UnstableBillableUnitsResponse unstable_billable_units_get(from_timestamp, to_timestamp, granularity, options)


Unstable: the shape may change without notice.  Billable units of the organization's projects, per UTC time bucket and project. These are the numbers of the organization's Usage settings tab. Requires an organization-scoped API key.  Units are counted by ingestion time in `[fromTimestamp, toTimestamp)` as approximate distinct units per bucket (about 0.3% error on large counts, small counts are exact). A unit counts once in every bucket it appears in, so the counts stay close to, but are not exactly, what is billed. Deployments still in the v3 `legacy` write mode count the rows of the traces, observations and scores tables instead.  Buckets start at UTC hour, day, Monday or month boundaries. The first and last bucket cover only the part inside the range, and a `toTimestamp` in the future is cut off at now. Buckets and projects without usage are left out, and so are deleted projects.

### Parameters

Name | Type | Description  | Required | Notes
------------- | ------------- | ------------- | ------------- | -------------
**from_timestamp** | **jiff::Timestamp** | Start of the range (inclusive), ISO 8601 with a time zone. | [required] |
**to_timestamp** | **jiff::Timestamp** | End of the range (exclusive), ISO 8601 with a time zone. At most 31 days after `fromTimestamp` for `hour` granularity, 366 days otherwise. | [required] |
**granularity** | Option<[**UnstableBillableUnitsGranularity**](UnstableBillableUnitsGranularity.md)> | Bucket size. Defaults to `day`. |  |
**options** | Option<&timvw_rust_runtime::RequestOptions> | Per-call extra headers, query parameters and base URL, applied after everything else ([`RequestOptions`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/struct.RequestOptions.html)) |  |

```rust,ignore
unstable_billable_units_get().configuration(&configuration).from_timestamp(..).to_timestamp(..).options(&options).call().await
```

### Return type

[**models::UnstableBillableUnitsResponse**](UnstableBillableUnitsResponse.md)

### Authorization

[BasicAuth](../README.md#BasicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

