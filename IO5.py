import gdsfactory as gf
from Straight import Straight
from Bend import Bend

@gf.cell
def IO5( 
    TotLengthX = 100,
    LengthX    = 10,
    LengthY    = 10,
    TotLengthY      = 50,
    BendRadius = 10,
    WgWidth    = 1.0,
    Euler      = 0,
    Layer      = (3,0)
):
    
    IO5 = gf.Component()
    
    ##################################################################################
    #Defined from Bottom to Up
    ##################################################################################
    LengthX1 = (TotLengthX - BendRadius)
    LengthY1 = (TotLengthY - 4*BendRadius - LengthY)/2
    
    InX1   = IO5 << Straight(Length=LengthX1, Width=WgWidth, Layer=Layer) 
   
    Bend1  = IO5 << Bend(Radius=BendRadius, Width=WgWidth, angle = 90, Euler = Euler, Layer=Layer)  
    
    InY1   = IO5 << Straight(Length=LengthY1, Width=WgWidth, Layer=Layer)   
    
    Bend2  = IO5 << Bend(Radius=BendRadius, Width=WgWidth, angle =  90, Euler = Euler, Layer=Layer)  
    
    InX2   = IO5 << Straight(Length=LengthX, Width=WgWidth, Layer=Layer) 

    Bend3  = IO5 << Bend(Radius=BendRadius, Width=WgWidth, angle =  -90, Euler = Euler, Layer=Layer) 
    
    Y      = IO5 << Straight(Length=LengthY-2*BendRadius, Width=WgWidth, Layer=Layer)   
    
    Bend4  = IO5 << Bend(Radius=BendRadius, Width=WgWidth, angle =  -90, Euler = Euler, Layer=Layer) 
    
    OutX2  = IO5 << Straight(Length=LengthX, Width=WgWidth, Layer=Layer) 
    
    Bend5  = IO5 << Bend(Radius=BendRadius, Width=WgWidth, angle = 90, Euler = Euler, Layer=Layer)  
    
    OutY1  = IO5 << Straight(Length=LengthY1, Width=WgWidth, Layer=Layer)   
    
    Bend6  = IO5 << Bend(Radius=BendRadius, Width=WgWidth, angle =  90, Euler = Euler, Layer=Layer)  
    
    OutX1  = IO5 << Straight(Length=LengthX1, Width=WgWidth, Layer=Layer) 
    
    ########################################################################################
    # Connections 
    ########################################################################################
    Bend1.connect("o1", InX1.ports["o2"])  
    
    InY1.connect("o1", Bend1.ports["o2"])  
    
    Bend2.connect("o1", InY1.ports["o2"])
    
    InX2.connect("o1", Bend2.ports["o2"])  
    
    Bend3.connect("o1", InX2.ports["o2"])
    
    Y.connect("o1", Bend3.ports["o2"])
    
    Bend4.connect("o1", Y.ports["o2"])
    
    OutX2.connect("o1", Bend4["o2"])
    
    Bend5.connect("o1", OutX2.ports["o2"])
    
    OutY1.connect("o1", Bend5["o2"])
    
    Bend6.connect("o1", OutY1.ports["o2"])
    
    OutX1.connect("o1", Bend6["o2"])
    
    
    IO5.ymax = WgWidth/2
    
    IO5.add_port(name="o1", port = InX1.ports["o1"])
    IO5.add_port(name="o2", port = OutX1.ports["o2"])
    
    return IO5
