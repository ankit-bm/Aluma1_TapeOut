import gdsfactory as gf
from Straight import Straight
from Bend import Bend

@gf.cell
def Racetrack(
    LengthX = 12,
    LengthY = 18,
    BendRadius = 30,
    WgWidth = 1.0,
    Euler = 0,
    Layer = (2,0),
):
    
    
    R = gf.Component() 

    ####################################################################################
    # Racetrack Components
    ####################################################################################
    BendR     = Bend(Radius=BendRadius, Width=WgWidth, Euler =Euler, Layer=Layer)
    StraightX = Straight(Length=LengthX, Width=WgWidth, Layer=Layer)
    StraightY = Straight(Length=LengthY, Width=WgWidth, Layer=Layer)
    
    Bend_1 = R << BendR
    Y1     = R << StraightY
    Bend_2 = R << BendR
    X1     = R << StraightX
    Bend_3 = R << BendR
    Y2     = R << StraightY
    Bend_4 = R << BendR
    X2     = R << StraightX

    ########################################################################################
    #Connections
    #######################################################################################
    
    Y1.connect("o1", Bend_1.ports["o2"])
    Bend_2.connect("o1", Y1.ports["o2"])
    X1.connect("o1", Bend_2.ports["o2"])
    Bend_3.connect("o1", X1.ports["o2"])
    Y2.connect("o1", Bend_3.ports["o2"])
    Bend_4.connect("o1", Y2.ports["o2"])
    X2.connect("o1", Bend_4.ports["o2"])
    
    R.center = (0, 0)  
    
    return R
