from oarepo_model_builder.stack import ModelBuilderStack


class SchemaPathValidator:
    valid = False

    def get(self, path_el):
        raise NotImplementedError()


class Invalid(SchemaPathValidator):
    def get(self, path_el):
        return self


invalid = Invalid()


class PrimitiveValidator(SchemaPathValidator):
    valid = True

    def get(self, path_el):
        return invalid


primitive = PrimitiveValidator()


class DictValidator(SchemaPathValidator):
    valid = True

    def __init__(self, dict=None, primitives=None):
        self.dict = dict or {}
        if primitives:
            for p in primitives.split(','):
                p = p.strip()
                if not p:
                    continue
                self.dict[p] = primitive

    def get(self, path_el):
        if path_el in self.dict:
            return self.dict[path_el]
        return invalid


class AnyKeyDictValidator(SchemaPathValidator):
    valid = True

    def __init__(self, _next):
        self._next = _next

    def get(self, path_el):
        return self._next


class Ref(SchemaPathValidator):
    refs = {}
    valid = True

    def __init__(self, refstr):
        self.refstr = refstr

    def get(self, path_el):
        return self.refs[self.refstr].get(path_el)


Ref.refs['type'] = DictValidator({
    "properties": Ref('property'),
    "patternProperties": Ref('property'),
    "additionalProperties": DictValidator(primitives='type'),
    "propertyNames": DictValidator(primitives='pattern'),
    "items": Ref('type'),
    "prefixItems": Ref('type'),
    "contains": Ref('type'),
},
    primitives="type,"
               "enum,const,"  # enums and consts
               "required,minProperties,maxProperties,"  # object
               "minItems,maxItems,uniqueItems,minContains,maxContains,"  # array
               "minLength,maxLength,pattern,format,"  # string
               "minimum,exclusiveMinimum,maximum,exclusiveMaximum,multipleOf"  # numbers
)

Ref.refs['property'] = AnyKeyDictValidator(Ref('type'))

schema_paths = DictValidator(
    {
        "$vocabulary": AnyKeyDictValidator(primitive),
        "properties": Ref('property')
    }, primitives='$schema,$id,type'
)

model_paths = DictValidator(
    {
        'model': schema_paths
    }
)


def is_schema_element(stack: ModelBuilderStack):
    sc = model_paths
    for entry in stack.stack:
        key = entry.key
        if key is None:
            continue
        if isinstance(key, int):
            continue
        sc = sc.get(key)
        if not sc.valid:
            return False
    return True
