//! Decoding of tagged unions: read the JSON value, look at the tag, decode only what it selects. A union
//! calls these from the `dispatch` function next to its `Deserialize`.
//!
//! Decoding goes through `serde_json::Value`, like `serde(untagged)`, whose buffer holds numbers the same
//! way: an integer up to 64 bits stays that integer, anything larger and every float is an `f64`.
//! A key that appears twice in an object is the last one, where a struct alone would reject it.

use serde::de::DeserializeOwned;
use serde_json::Value;

/// What a union finds where it looks for its tag.
pub(crate) enum Tag<'a> {
    /// The tag's value.
    Value(&'a str),
    /// An object without the tag, or with `null` for it.
    Missing,
    /// Not an object at all.
    NotObject,
}

/// Looks at the tag. A tag of another kind than a string is an error here, whatever the variants say.
pub(crate) fn tag<'a>(value: &'a Value, union: &str, tag: &str) -> Result<Tag<'a>, String> {
    let Value::Object(fields) = value else {
        return Ok(Tag::NotObject);
    };
    match fields.get(tag) {
        None | Some(Value::Null) => Ok(Tag::Missing),
        Some(Value::String(found)) => Ok(Tag::Value(found)),
        Some(other) => Err(format!(
            "{union}: tag `{tag}` must be a string, got {}",
            kind(other)
        )),
    }
}

/// Decodes the one variant selected, and keeps its error.
pub(crate) fn decode<T: DeserializeOwned>(
    value: Value,
    union: &str,
    variant: &str,
) -> Result<T, String> {
    serde_json::from_value(value).map_err(|e| format!("{union}::{variant}: {e}"))
}

/// A variant to try: its name, and how to decode it.
pub(crate) type Attempt<U> = (&'static str, fn(Value) -> Result<U, serde_json::Error>);

/// Tries the variants selected in order, and keeps the error of each when none decodes.
pub(crate) fn first_of<U>(
    mut value: Value,
    union: &str,
    tag: &str,
    attempts: &[Attempt<U>],
) -> Result<U, String> {
    let found = match value.get(tag) {
        Some(Value::String(found)) => format!("`{tag}` {found:?}"),
        _ if value.is_object() => format!("no `{tag}`"),
        _ => kind(&value).to_owned(),
    };
    let mut errors = Vec::with_capacity(attempts.len());
    for (index, (variant, decode)) in attempts.iter().enumerate() {
        let input = if index + 1 == attempts.len() {
            std::mem::take(&mut value)
        } else {
            value.clone()
        };
        match decode(input) {
            Ok(decoded) => return Ok(decoded),
            Err(e) => errors.push(format!("{variant}: {e}")),
        }
    }
    Err(format!(
        "{union}: no variant decodes {found}: {}",
        errors.join("; ")
    ))
}

/// The error of a tag no variant has.
#[allow(dead_code)]
pub(crate) fn unknown_tag(union: &str, tag: &str, value: &str) -> String {
    format!("{union}: unknown `{tag}` value {value:?}")
}

/// The error of no tag, when every variant requires it.
pub(crate) fn missing_tag(union: &str, tag: &str) -> String {
    format!("{union}: tag `{tag}` is missing or null")
}

/// The error of something other than an object, when every variant is one.
pub(crate) fn not_an_object(value: &Value, union: &str, tag: &str) -> String {
    format!(
        "{union}: expected an object with tag `{tag}`, got {}",
        kind(value)
    )
}

fn kind(value: &Value) -> &'static str {
    match value {
        Value::Null => "null",
        Value::Bool(_) => "a boolean",
        Value::Number(_) => "a number",
        Value::String(_) => "a string",
        Value::Array(_) => "an array",
        Value::Object(_) => "an object",
    }
}
