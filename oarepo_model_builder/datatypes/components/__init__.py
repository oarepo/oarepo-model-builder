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
    FacetsModelComponent,
    InvenioModelComponent,
    MarshmallowModelComponent,
    ResourceModelComponent,
    SampleModelComponent,
    SavedModelComponent,
    UIMarshmallowModelComponent,
    UIModelComponent,
)
from .sample import ArraySampleComponent, RegularSampleComponent
from .ui import ObjectUIComponent, RegularUIComponent

DEFAULT_COMPONENTS = [
    ResourceModelComponent,
    InvenioModelComponent,
    SavedModelComponent,
    SampleModelComponent,
    RegularFacetsComponent,
    FacetsModelComponent,
    ArraySampleComponent,
    RegularSampleComponent,
    MarshmallowModelComponent,
    RegularMarshmallowComponent,
    ObjectMarshmallowComponent,
    RegularUIComponent,
    ObjectUIComponent,
    UIModelComponent,
    ArrayMarshmallowComponent,
    UIMarshmallowComponent,
    UIObjectMarshmallowComponent,
    UIArrayMarshmallowComponent,
    UIMarshmallowModelComponent,
    EnumComponent,
]
