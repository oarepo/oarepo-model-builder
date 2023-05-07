from .enum import EnumComponent
from .facets import RegularFacetsComponent
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
    RecordDumperModelComponent,
    RecordMetadataModelComponent,
    RecordModelComponent,
    ResourceModelComponent,
    SampleModelComponent,
    SavedModelComponent,
    ServiceModelComponent,
    UIMarshmallowModelComponent,
    UIModelComponent,
    ProxyModelComponent
)
from .sample import ArraySampleComponent, RegularSampleComponent
from .ui import ObjectUIComponent, RegularUIComponent

DEFAULT_COMPONENTS = [
    RegularFacetsComponent,
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
    ProxyModelComponent
]
