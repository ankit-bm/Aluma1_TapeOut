import gdsfactory as gf
from Straight import Straight
from Bend import Bend

@gf.cell
def IO4( 
    LengthX    = 100,
    LengthY    = 10,
    DY         = 70,
    FAGap      = 50,
    BendRadius = 10,
    WgWidth    = 1.0,
    Euler      = 1,
    Layer      = (3,0)
):
    
    IO4 = gf.Component()
    
    ##################################################################################
    #Defined from Bottom to Up
    ##################################################################################
    LengthX1 = (LengthX - BendRadius)
    LengthY1 = (LengthY - 2*BendRadius)

    LengthY2 = (LengthY - 2*BendRadius - FAGap)
    LengthX2 = LengthX - 3*BendRadius
    
    X1     = IO4 << Straight(Length=LengthX1, Width=WgWidth, Layer=Layer) 
   
    Bend1  = IO4 << Bend(Radius=BendRadius, Width=WgWidth, angle = -90, Layer=Layer,Euler=Euler)  
    
    Y1     = IO4 << Straight(Length=LengthY1, Width=WgWidth, Layer=Layer)   
    
    Bend2  = IO4 << Bend(Radius=BendRadius, Width=WgWidth, angle =  -90, Layer=Layer,Euler=Euler)  
    
    Bend3  = IO4 << Bend(Radius=BendRadius, Width=WgWidth, angle =  -90, Layer=Layer,Euler=Euler) 
    
    Y2     = IO4 << Straight(Length=LengthY2, Width=WgWidth, Layer=Layer)   
    
    Bend4  = IO4 << Bend(Radius=BendRadius, Width=WgWidth, angle =  90, Layer=Layer,Euler=Euler) 
    
    X2     = IO4 << Straight(Length=LengthX2, Width=WgWidth, Layer=Layer) 
    
    
    ########################################################################################
    # Connections 
    ########################################################################################

    Bend1.connect("o1", X1.ports["o2"])  
    
    Y1.connect("o1", Bend1.ports["o2"])  
    
    Bend2.connect("o1", Y1.ports["o2"])
    
    Bend3.connect("o1", Bend2.ports["o2"])
    
    Y2.connect("o1", Bend3.ports["o2"])
    
    Bend4.connect("o1", Y2.ports["o2"])
    
    X2.connect("o1", Bend4["o2"])
    
   
    
    IO4.ymax = WgWidth/2
    
    IO4.add_port(name="o1", port = X1.ports["o1"])
    IO4.add_port(name="o2", port = X2.ports["o2"])
    
    return IO4
