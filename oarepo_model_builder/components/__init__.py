from .model import (
    ResourceModelComponent,
    InvenioModelComponent,
    SavedModelComponent,
    FacetsModelComponent,
    SampleModelComponent,
)

from .facets import RegularFacetsComponent
from .sample import RegularSampleComponent, ArraySampleComponent

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
