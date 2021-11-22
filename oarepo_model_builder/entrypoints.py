import pkg_resources

from oarepo_model_builder.builder import ModelBuilder


def create_builder_from_entrypoints():
    output_classes = load_entry_points_list('oarepo_model_builder.ouptuts')
    builder_classes = load_entry_points_list('oarepo_model_builder.builders')
    preprocess_classes = load_entry_points_list('oarepo_model_builder.property_preprocessors')
    model_preprocessor_classes = load_entry_points_list('oarepo_model_builder.model_preprocessors')

    return ModelBuilder(
        output_builders=builder_classes,
        outputs=output_classes,
        property_preprocessors=preprocess_classes,
        model_preprocessors=model_preprocessor_classes
    )


def load_entry_points_dict(name):
    return {ep.name: ep.load() for ep in pkg_resources.iter_entry_points(group=name)}


def load_entry_points_list(name):
    ret = [(ep.name, ep.load()) for ep in pkg_resources.iter_entry_points(group=name)]
    ret.sort()
    return [x[1] for x in ret]
