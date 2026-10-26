use langfuse_client_base::apis::parse_deep_object;
use serde_json::json;

#[test]
fn scalar_values_do_not_panic() {
    assert_eq!(
        parse_deep_object("filter", &json!("abc")),
        vec![("filter".to_string(), "abc".to_string())]
    );
    assert_eq!(
        parse_deep_object("filter", &json!(42)),
        vec![("filter".to_string(), "42".to_string())]
    );
    assert_eq!(
        parse_deep_object("filter", &json!(true)),
        vec![("filter".to_string(), "true".to_string())]
    );
}

#[test]
fn array_items_inside_objects_are_indexed() {
    let params = parse_deep_object("filter", &json!({"tags": ["a", "b"]}));
    assert_eq!(
        params,
        vec![
            ("filter[tags][0]".to_string(), "a".to_string()),
            ("filter[tags][1]".to_string(), "b".to_string()),
        ]
    );
}
