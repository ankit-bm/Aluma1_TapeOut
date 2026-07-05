import gdsfactory as gf
import gdsfactory.components as gc
from Straight import Straight
from Bend import Bend
from Pulley import Pulley

@gf.cell
def IO6_Pulley( 
    InLengthX   = 100,
    TotLengthX  = 300,
    TotLengthY  = 50,
    Radius      = 50,
    BendRadius  = 30,
    WgWidth     = 1.8,
    ThetaC      = 40,
    Gap         = 0.3,
    Euler       = 1,
    Layer       = (3,0)
):
    
    IO6_Pulley = gf.Component()
    
    ##################################################################################
    #Defined from Bottom to Up
    ##################################################################################
        
    P0      = Pulley(Radius = Radius, WgWidth = WgWidth, ThetaC = ThetaC, BendRadius = BendRadius, Gap = Gap, InLengthX = 0, Euler = Euler, Layer= Layer)
    DXP0    = P0.info["DX"]
    DYP0    = P0.info["DY"]

    InLength_Pulley = (TotLengthY- 2*BendRadius - DXP0)/2
    P       = Pulley(Radius = Radius, WgWidth = WgWidth, ThetaC = ThetaC, BendRadius = BendRadius, Gap = Gap, InLengthX = InLength_Pulley, Euler = Euler, Layer= Layer)
    DXP     = P.info["DX"]
    DYP     = P.info["DY"]

    LengthX    = (InLengthX - BendRadius) + DYP - WgWidth
    #LengthY    = TotLengthY - 2*BendRadius
    OutLengthX = TotLengthX - LengthX - 2*BendRadius
    
    InX    = IO6_Pulley << Straight(Length=LengthX, Width=WgWidth, Layer=Layer) 
    Bend1  = IO6_Pulley << Bend(Radius=BendRadius, Width=WgWidth, angle = -90, Layer=Layer)  
    #InY    = IO6_Pulley << Straight(Length=LengthY, Width=WgWidth, Layer=Layer)   
    InY    = IO6_Pulley << P
        
    Bend2  = IO6_Pulley << Bend(Radius=BendRadius, Width=WgWidth, angle = 90, Layer=Layer)  
    OutX   = IO6_Pulley << Straight(Length=OutLengthX, Width=WgWidth, Layer=Layer)
    
    ########################################################################################
    # Connections 
    ########################################################################################
    Bend1.connect("o1", InX.ports["o2"])  
    InY.connect("o1", Bend1.ports["o2"])  
    Bend2.connect("o1", InY.ports["o2"])
    OutX.connect("o1", Bend2["o2"])
    
    IO6_Pulley.ymax = WgWidth/2
    
    IO6_Pulley.add_port(name="o1", port = InX.ports["o1"])
    IO6_Pulley.add_port(name="o2", port = OutX.ports["o2"])
    

    return IO6_Pulley
