from oarepo_model_builder.outputs.json_stack import JSONStack


def test_json_stack():
    st = JSONStack()
    st.push(None, {})
    st.push("a", 1)
    st.pop()
    st.push("b", {})
    st.push("c", 2)
    st.pop()
    st.pop()
    st.push("d", [])
    st.push(0, 3)
    st.pop()
    st.push(1, 4)
    st.pop()
    st.pop()
    st.pop()
    st.pop()
    assert st.value == {"a": 1, "b": {"c": 2}, "d": [3, 4]}
