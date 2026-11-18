# langfuse-client-base 0.25 → 0.26.0: jiff instead of chrono

chrono is unmaintained ([RUSTSEC-2026-0543](https://rustsec.org/advisories/RUSTSEC-2026-0543)). This release
regenerates the client with `timvw-rust` 0.33.0 (openapi-generator 7.27.0) and its option `dateTimeLibrary=jiff`:
dates are [jiff](https://docs.rs/jiff) types, and the crate no longer depends on chrono. The Langfuse spec and
`timvw-rust-runtime` 0.4 are unchanged. The census is `api-diff-0.25.1-to-0.26.0.json`: every change is a date type
(262 model fields, 108 API functions).

## What changes

| | 0.25 (chrono) | 0.26 (jiff) |
| --- | --- | --- |
| `format: date-time` | `chrono::DateTime<chrono::FixedOffset>` | `jiff::Timestamp` |
| `format: date` | `chrono::NaiveDate` | `jiff::civil::Date` |
| Date-time query parameters | `to_rfc3339()`, the offset as given | RFC 3339 in UTC (`2026-01-02T02:04:05Z`) |

Both read any RFC 3339 offset and write RFC 3339 through serde. A `jiff::Timestamp` is an instant: the offset a
date was received with is not kept, and dates are written in UTC.

The crate depends on `jiff` with `default-features = false` and the `std` and `serde` features. It builds for
`wasm32-unknown-unknown` as before; there, `jiff::Timestamp::now()` needs jiff's `js` feature, which your crate can
enable.

## Upgrading

- Replace the types: `chrono::DateTime<chrono::FixedOffset>` → `jiff::Timestamp`, `chrono::NaiveDate` →
  `jiff::civil::Date`.
- `chrono::Utc::now().fixed_offset()` → `jiff::Timestamp::now()`.
- `chrono::DateTime::parse_from_rfc3339(s)?` → `s.parse::<jiff::Timestamp>()?`.
- `t.to_rfc3339()` → `t.to_string()`; with milliseconds, `format!("{t:.3}")`.
- `t + chrono::Duration::seconds(2)` → `t + jiff::SignedDuration::from_secs(2)`.
- Code that still holds chrono values converts through RFC 3339 text: `t.to_rfc3339().parse::<jiff::Timestamp>()?`.
