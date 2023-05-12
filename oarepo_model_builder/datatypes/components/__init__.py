from .enum import EnumComponent
# from .facets_validation import FacetsValidationModelComponent
from .facets import (RegularFacetsComponent,
                     ObjectFacetsComponent,
                     NestedFacetsComponent,
                     ArrayFacetsComponent
)
from .marshmallow import (
    ArrayMarshmallowComponent,
    ObjectMarshmallowComponent,
    RegularMarshmallowComponent,
    UIArrayMarshmallowComponent,
    UIMarshmallowComponent,
    UIObjectMarshmallowComponent,
)
from .model import (
    AppModelComponent,
    BlueprintsModelComponent,
    DefaultsModelComponent,
    FacetsModelComponent,
    JSONSchemaModelComponent,
    MappingModelComponent,
    MarshmallowModelComponent,
    PermissionsModelComponent,
    PIDModelComponent,
    PluginsModelComponent,
    ProxyModelComponent,
    RecordDumperModelComponent,
    RecordMetadataModelComponent,
    RecordModelComponent,
    ResourceModelComponent,
    SampleModelComponent,
    SavedModelComponent,
    ServiceModelComponent,
    UIMarshmallowModelComponent,
    UIModelComponent,
)
from .sample import ArraySampleComponent, RegularSampleComponent
from .ui import ObjectUIComponent, RegularUIComponent

DEFAULT_COMPONENTS = [
    # FacetsValidationModelComponent,
    ArraySampleComponent,
    RegularSampleComponent,
    RegularMarshmallowComponent,
    ObjectMarshmallowComponent,
    RegularUIComponent,
    ObjectUIComponent,
    ArrayMarshmallowComponent,
    UIMarshmallowComponent,
    UIObjectMarshmallowComponent,
    UIArrayMarshmallowComponent,
    EnumComponent,
    AppModelComponent,
    BlueprintsModelComponent,
    FacetsModelComponent,
    JSONSchemaModelComponent,
    MappingModelComponent,
    MarshmallowModelComponent,
    PIDModelComponent,
    PermissionsModelComponent,
    RecordDumperModelComponent,
    RecordMetadataModelComponent,
    RecordModelComponent,
    ResourceModelComponent,
    SampleModelComponent,
    SavedModelComponent,
    ServiceModelComponent,
    UIMarshmallowModelComponent,
    UIModelComponent,
    DefaultsModelComponent,
    ProxyModelComponent,
    PluginsModelComponent,
    ObjectFacetsComponent,

    NestedFacetsComponent,
    RegularFacetsComponent,
    ArrayFacetsComponent
]
