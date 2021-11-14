from oarepo_model_builder.stack import ModelBuilderStack


def is_schema_element(stack: ModelBuilderStack):
    key = stack.top.key
    if not isinstance(key, str):
        return True
    if not key.startswith('oarepo:'):
        return True
    # if the key starts with oarepo:, it still might be in properties section
    if stack[-2].key == 'properties':
        return True
    return False
