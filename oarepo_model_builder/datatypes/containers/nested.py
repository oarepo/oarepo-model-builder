from .object import ObjectDataType


class NestedDataType(ObjectDataType):
    mapping_type = "nested"
    # marshmallow_field = "ma_fields.Nested"
    # ui_marshmallow_field = "ma_fields.Nested"
    model_type = "nested"
    # default_facet_class = "NestedLabeledFacet"
    # default_facet_imports = [
    #     {"import": "oarepo_runtime.facets.nested_facet.NestedLabeledFacet"}
    # ]

    # def get_facet(self, stack, parent_path, path_suffix=None):
    #     if not stack:
    #         return None
    #     return super().get_facet(stack, parent_path, path_suffix)

    # def _get_facet_definition(
    #     self, stack, facet_class, facet_name, path, path_suffix, label, serialized_args
    # ):
    #     nested_arr = []
    #     facet_obj = stack[0].get_facet(stack[1:], path)

    #     for f in facet_obj:
    #         nested_arr.append(
    #             {
    #                 "facet": f'{facet_class}(path="{path}{path_suffix}", nested_facet = {f["facet"]}{serialized_args})',
    #                 "path": f["path"],
    #             }
    #         )
    #     return nested_arr
