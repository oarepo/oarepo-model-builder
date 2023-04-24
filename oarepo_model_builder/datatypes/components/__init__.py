from .facets import RegularFacetsComponent
from .model import (
    FacetsModelComponent,
    InvenioModelComponent,
    ResourceModelComponent,
    SampleModelComponent,
    SavedModelComponent,
    MarshmallowModelComponent,
    UIModelComponent,
)
from .sample import ArraySampleComponent, RegularSampleComponent
from .marshmallow import RegularMarshmallowComponent, ObjectMarshmallowComponent
from .ui import RegularUIComponent, ObjectUIComponent

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
