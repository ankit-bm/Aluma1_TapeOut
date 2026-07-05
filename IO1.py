import gdsfactory as gf
import gdsfactory.components as gc
from Straight import Straight
from Bend import Bend

@gf.cell
def IO1( 
    InLengthX   = 100,
    TotLengthX  = 300,
    TotLengthY  = 50,
    BendRadius  = 30,
    WgWidth     = 1.8,
    Euler       = 1,
    Layer       = (3,0)
):
    
    IO1 = gf.Component()
    
    ##################################################################################
    #Defined from Bottom to Up
    ##################################################################################
    
    
    LengthX    = (InLengthX - BendRadius)
    LengthY    = TotLengthY - 2*BendRadius
    OutLengthX = TotLengthX - (InLengthX + BendRadius)
    
    InX    = IO1 << Straight(Length=LengthX, Width=WgWidth, Layer=Layer) 
    Bend1  = IO1 << Bend(Radius=BendRadius, Width=WgWidth, angle = -90, Layer=Layer, Euler=Euler)  
    InY    = IO1 << Straight(Length=LengthY, Width=WgWidth, Layer=Layer)   
    Bend2  = IO1 << Bend(Radius=BendRadius, Width=WgWidth, angle = 90, Layer=Layer, Euler=Euler)  
    OutX   = IO1 << Straight(Length=OutLengthX, Width=WgWidth, Layer=Layer)
    
    ########################################################################################
    # Connections 
    ########################################################################################
    Bend1.connect("o1", InX.ports["o2"])  
    InY.connect("o1", Bend1.ports["o2"])  
    Bend2.connect("o1", InY.ports["o2"])
    OutX.connect("o1", Bend2["o2"])
    
    IO1.ymax = WgWidth/2
    
    IO1.add_port(name="o1", port = InX.ports["o1"])
    IO1.add_port(name="o2", port = OutX.ports["o2"])
    

    return IO1
