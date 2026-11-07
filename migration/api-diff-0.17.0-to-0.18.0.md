# langfuse-client-base 0.17.0 → 0.18.0: role-based auth for blob storage integrations

This release is regenerated from the latest Langfuse OpenAPI spec (genai-rs/langfuse-client-base#275) with the same
generator, `timvw-rust` 0.17.0 on openapi-generator 7.27.0, and the same options. The machine-readable census is
`api-diff-0.17.0-to-0.18.0.json` in this folder (`compare_public_api.py` against 0.17.0).

## What stays the same

- Every operation keeps its module, function name and parameters.
- Every other model, field and enum is unchanged. `Model`, `CreateModelRequest` and `ModelTokenizerId` only get new doc
  comments: the tokenizer fields are kept for compatibility, and ingestion no longer uses them to infer usage.

## What changes

Langfuse blob storage integrations can authenticate with an assumed IAM role instead of access keys.

- **New enum `BlobStorageIntegrationAuthType`**: `AccessKeys` (`"ACCESS_KEYS"`), `RoleArn` (`"ROLE_ARN"`) and the
  catch-all `Unknown` for a value this crate does not know. It derives `Clone`, `Copy`, `Debug`, `Eq`, `Hash`, `Ord`,
  `PartialEq`, `PartialOrd`, `Serialize`, `Deserialize`.
- **`BlobStorageIntegrationResponse` gains four fields**, all of which the spec marks required:

  | Field | Type | JSON |
  | --- | --- | --- |
  | `auth_type` | `models::BlobStorageIntegrationAuthType` | `authType` |
  | `role_arn` | `Option<String>` | `roleArn` (key required, may be `null`) |
  | `external_id` | `Option<String>` | `externalId` (key required, may be `null`) |
  | `cross_account_role_arn` | `Option<String>` | `crossAccountRoleArn` (key required, may be `null`) |

  `BlobStorageIntegrationResponse::new` takes them, after `region` and around `access_key_id`. A response from a Langfuse
  server that does not send these keys yet no longer decodes; upgrade the server or stay on 0.17.
- **`CreateBlobStorageIntegrationRequest` gains two optional fields**: `auth_type: Option<BlobStorageIntegrationAuthType>`
  (`authType`, left out when `None`) and `role_arn: Option<Option<String>>` (`roleArn`; `Some(None)` sends `null`).
  `new()` is unchanged.

## Migrating

- Code that builds `BlobStorageIntegrationResponse` with `new()` or a struct literal passes the four new values, for
  example `BlobStorageIntegrationAuthType::AccessKeys, None, None, None` for an access-key integration.
- Code that builds `CreateBlobStorageIntegrationRequest` with a struct literal adds `auth_type: None, role_arn: None`, or
  uses `new()` and sets them afterwards. To use a role: `auth_type = Some(BlobStorageIntegrationAuthType::RoleArn)` and
  `role_arn = Some(Some(arn))`.
- A `match` on `BlobStorageIntegrationAuthType` needs an `Unknown` arm.
