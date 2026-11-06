/// The error of parsing a string into a generated enum: the string names none of its variants.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ParseEnumError {
    type_name: &'static str,
    value: String,
}

impl ParseEnumError {
    pub(crate) fn new(type_name: &'static str, value: &str) -> Self {
        Self {
            type_name,
            value: value.to_owned(),
        }
    }

    /// The enum that was parsed into.
    pub fn type_name(&self) -> &'static str {
        self.type_name
    }

    /// The string that was rejected.
    pub fn value(&self) -> &str {
        &self.value
    }
}

impl std::fmt::Display for ParseEnumError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "invalid value {:?} for enum {}",
            self.value, self.type_name
        )
    }
}

impl std::error::Error for ParseEnumError {}
