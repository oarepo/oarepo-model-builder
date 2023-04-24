from .facets import RegularFacetsComponent
from .model import (
    FacetsModelComponent,
    InvenioModelComponent,
    ResourceModelComponent,
    SampleModelComponent,
    SavedModelComponent,
)
from .sample import ArraySampleComponent, RegularSampleComponent

DEFAULT_COMPONENTS = [
    ResourceModelComponent,
    InvenioModelComponent,
    SavedModelComponent,
    SampleModelComponent,
    RegularFacetsComponent,
    FacetsModelComponent,
    ArraySampleComponent,
    RegularSampleComponent,
]
