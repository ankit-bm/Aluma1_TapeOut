import gdsfactory as gf
from Straight import Straight
from Bend import Bend

@gf.cell
def Ring(
    BendRadius = 30,
    WgWidth = 1.0,
    Layer = (2,0),
):
    
    
    R = gf.Component() 

    ####################################################################################
    # Racetrack Parameters
    ####################################################################################
    BendR  = Bend(Radius=BendRadius, Width=WgWidth, Euler = 0, Layer=Layer)
    
    Bend_1 = R << BendR
    
    Bend_2 = R << BendR
    
    Bend_3 = R << BendR
    
    Bend_4 = R << BendR
    
    ########################################################################################
    #Connections
    #######################################################################################
    
    
    Bend_2.connect("o1", Bend_1.ports["o2"])
    
    Bend_3.connect("o1", Bend_2.ports["o2"])
   
    Bend_4.connect("o1", Bend_3.ports["o2"])

    Bend_1.connect("o1", Bend_4.ports["o2"])
    
    
    R.center = (0, 0)  
    
    return R
