from .facets import RegularFacetsComponent
from .marshmallow import ObjectMarshmallowComponent, RegularMarshmallowComponent
from .model import (
    FacetsModelComponent,
    InvenioModelComponent,
    MarshmallowModelComponent,
    ResourceModelComponent,
    SampleModelComponent,
    SavedModelComponent,
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
]
