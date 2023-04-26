from .facets import RegularFacetsComponent
from .marshmallow import (
    ArrayMarshmallowComponent,
    ObjectMarshmallowComponent,
    RegularMarshmallowComponent,
    UIMarshmallowComponent,
    UIObjectMarshmallowComponent,
    UIArrayMarshmallowComponent,
)
from .model import (
    FacetsModelComponent,
    InvenioModelComponent,
    MarshmallowModelComponent,
    ResourceModelComponent,
    SampleModelComponent,
    SavedModelComponent,
    UIModelComponent,
    UIMarshmallowModelComponent,
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
]
