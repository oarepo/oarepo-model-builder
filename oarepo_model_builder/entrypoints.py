import pkg_resources

from oarepo_model_builder.builder import ModelBuilder


def create_builder_from_entrypoints():
    output_classes = load_entry_points_list('oarepo_model_builder.ouptuts')
    builder_classes = load_entry_points_list('oarepo_model_builder.builders')
    preprocess_classes = load_entry_points_list('oarepo_model_builder.property_preprocessors')
    model_preprocessor_classes = load_entry_points_list('oarepo_model_builder.model_preprocessors')

    builder_types = [x.TYPE for x in builder_classes]
    output_builder_components = {
        builder_type: load_entry_points_list(f'oarepo_model_builder.builder_components.{builder_type}')
        for builder_type in builder_types
    }

    return ModelBuilder(
        output_builders=builder_classes,
        outputs=output_classes,
        property_preprocessors=preprocess_classes,
        model_preprocessors=model_preprocessor_classes,
        output_builder_components=output_builder_components
    )


def load_entry_points_dict(name):
    return {ep.name: ep.load() for ep in pkg_resources.iter_entry_points(group=name)}


def load_entry_points_list(name):
    ret = [(ep.name, ep.load()) for ep in pkg_resources.iter_entry_points(group=name)]
    ret.sort()
    return [x[1] for x in ret]


def load_included_models_from_entry_points():
    return {
        ep.name: lambda schema: ep.load() for ep in pkg_resources.iter_entry_points(group='oarepo_model_builder.models')
    }
