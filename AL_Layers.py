import gdsfactory as gf
from gdsfactory.technology import LayerLevel, LayerMap, LayerStack, LayerViews
from gdsfactory.typings import Layer

class AL_Layers(LayerMap):


    CHS: Layer = (100, 0)
    CSL: Layer = (100, 2)

    X1P: Layer  = (2, 0)    # waveguide core
    X1B: Layer  = (2, 1)    # waveguide blocking
    X1BB: Layer = (2, 2)    # waveguide black-box