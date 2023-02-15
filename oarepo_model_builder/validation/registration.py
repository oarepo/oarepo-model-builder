from .model import ModelOpenSearchSchema, ModelSchema
from .model_defaults import ModelDefaults
from .model_plugins import PluginConfigSchema, PluginsSchema
from .properties import ArrayItemsSchema, ObjectFieldSchema, PropertiesSchema
from .property import ObjectProperty, Property
from .property_facets import PropertyFacets
from .property_jsonschema import PropertyJSONSchema
from .property_mapping import PropertyMapping
from .property_marshmallow import (ModelMarshmallowSchema,
                                   ObjectPropertyMarshmallowSchema,
                                   PropertyMarshmallowSchema)
from .property_sample_data import ModelSampleConfiguration, PropertySampleData
from .property_sortable import PropertySortable
from .root import RootSchema
from .settings import (SettingsOpenSearchSchema, SettingsPythonSchema,
                       SettingsSchema)

#
# Validators is a dictionary of "points" in model schema mapped to a single ma.Schema class
# or a list of ma.Schema classes. During validation, a new marshmallow class is constructed
# with all those classes as the bases for the class.
#
# To create your own extension point, see for example root.py: RootSchema
#
validators = {
    # Root of the model schema - to extend it with new
    # top-level options, add your schema here
    "root": RootSchema,
    #
    # /settings: To add your own settings key, register it here
    #
    "settings": SettingsSchema,
    #
    # /settings/opensearch: opensearch settings, currently only "version"
    "settings-opensearch": SettingsOpenSearchSchema,
    #
    # /settings/python: use-black, use-isort, ....
    # To add your own schema-wide python options, put
    # them in ma.Schema and register them here
    "settings-python": SettingsPythonSchema,
    #
    # /model: represents the content of the top-level 'model' element.
    # to add model-wide settings, register your schema here
    #
    "model": [
        ModelSchema,
        ModelDefaults,
        ModelSampleConfiguration,
        ModelMarshmallowSchema,
    ],
    #
    # /model/opensearch: defines opensearch index settings (analyzers, etc).
    # You mostly do not want to extend this
    "model-opensearch": ModelOpenSearchSchema,
    #
    # /model/marshmallow: defines marshmallow on the model-level
    "property-marshmallow-model": ModelMarshmallowSchema.ObjectOnlyMarshmallowProps,
    #
    # /model/properties, /model/properties/<element_name>/properties, ...
    # defines content of the properties (any key mapping to object-field).
    # You mostly do not want to modify this.
    "properties": PropertiesSchema,
    #
    # represents a wrapper around one item in properties.
    # You do not want to modify this
    "object-field": ObjectFieldSchema,
    #
    # represents a wrapper around an array "items" field.
    # You do not want to modify this
    "array-items": ArrayItemsSchema,
    #
    # This is the base schema for properties/aaa or array item.
    # Register schema here to add type-independent extensions
    "property": [Property],
    #
    # This is the base schema for properties/aaa
    # Register schema here to add type-independent extensions that are used only on object members
    "object-property": [ObjectProperty],
    #
    # This is the base schema for ...aaa[type=array]/items
    # Register schema here to add type-independent extensions that are used only on array items
    "array-item": [],
    #
    # An extension point for properties/aaa/facets
    "property-facets": PropertyFacets,
    #
    # An extension point for properties/aaa/sample
    "property-sample": PropertySampleData,
    #
    # An extension point for properties/aaa/jsonschema
    "property-jsonschema": PropertyJSONSchema,
    #
    # An extension point for properties/aaa/mapping
    "property-mapping": PropertyMapping,
    #
    # An extension point for properties/aaa/marshmallow
    "property-marshmallow": PropertyMarshmallowSchema,
    #
    # An extension point for properties/aaa/sortable
    "property-sortable": PropertySortable,
    #
    # property-by-type-xxx defines an extension point for schemas
    # that are dependent on property type. The schema is taken automatically
    # from the datatype (DataType.ModelSchema) property, so primarily define
    # your configuration in there.
    #
    # However, if you need to separate concerns and your extension works on
    # just a single data type, add it to this group of extensions
    #
    # This defines extra marshmallow fields for object/nested containers (schema-class, generate, ...)
    "property-by-type-object": [ObjectPropertyMarshmallowSchema],
    "property-by-type-nested": [ObjectPropertyMarshmallowSchema],
    #
    # An extension point for properties/aaa/marshmallow
    "property-marshmallow-object": ObjectPropertyMarshmallowSchema.ObjectMarshmallowProps,
    #
    # /model/plugins schema - defines model builder plugins that
    # are available. Extend this if you add a new "type" of plugins.
    "plugins-schema": PluginsSchema,
    #
    # defines switching on/off plugins of a single "type", for example /model/plugins/builder/enabled
    "plugin-schema": PluginConfigSchema,
}
