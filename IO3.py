import gdsfactory as gf
from Straight import Straight
from Bend import Bend
from AL_Taper import AL_Taper
from AL_GratingCoupler import AL_GratingCoupler

@gf.cell
def IO3( 
    LengthX    = 100,
    MidLengthX = 20,
    LengthY    = 10,
    TotLengthY = 50,
    BendRadius = 10,
    WgWidth    = 1.0,
    CouplerOn  = 0,   # 0=none, 1=EC, 2=GC
    Euler      = 0,
    Layer      = (3,0)
):
    
    IO3 = gf.Component()
    
    ##################################################################################
    #Defined from Bottom to Up
    ##################################################################################
    LengthX1 = (LengthX - MidLengthX - 3*BendRadius)
    LengthY1 = (TotLengthY - 6*BendRadius - LengthY)/2
    
    InX1   = IO3 << Straight(Length=LengthX1, Width=WgWidth, Layer=Layer) 
   
    Bend1  = IO3 << Bend(Radius=BendRadius, Width=WgWidth, angle = -90, Euler = Euler, Layer=Layer)  
    
    InY1   = IO3 << Straight(Length=LengthY1, Width=WgWidth, Layer=Layer)   
    
    Bend2  = IO3 << Bend(Radius=BendRadius, Width=WgWidth, angle =  90, Euler = Euler, Layer=Layer)  
    
    InX2   = IO3 << Straight(Length=MidLengthX, Width=WgWidth, Layer=Layer) 
    
    Bend3  = IO3 << Bend(Radius=BendRadius, Width=WgWidth, angle =  -90, Euler = Euler, Layer=Layer) 
    
    Y      = IO3 << Straight(Length=LengthY, Width=WgWidth, Layer=Layer)   
    
    Bend4  = IO3 << Bend(Radius=BendRadius, Width=WgWidth, angle =  -90, Euler = Euler, Layer=Layer) 
    
    OutX2  = IO3 << Straight(Length=MidLengthX, Width=WgWidth, Layer=Layer) 
    
    Bend5  = IO3 << Bend(Radius=BendRadius, Width=WgWidth, angle = 90, Euler = Euler, Layer=Layer)  
    
    OutY1  = IO3 << Straight(Length=LengthY1, Width=WgWidth, Layer=Layer)   
    
    Bend6  = IO3 << Bend(Radius=BendRadius, Width=WgWidth, angle =  -90, Euler = Euler, Layer=Layer)  
    
    OutX1  = IO3 << Straight(Length=LengthX1, Width=WgWidth, Layer=Layer) 
    
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
    
    
    IO3.ymax = WgWidth/2
    
    IO3.add_port(name="o1", port = InX1.ports["o1"])
    IO3.add_port(name="o2", port = OutX1.ports["o2"])
    
        ########################################################################################
    # Couplers
    ########################################################################################

    if CouplerOn == 1:
        Coupler = AL_Taper(WgWidth=WgWidth, Layer=Layer)
        CPort   = "o1"
    elif CouplerOn == 2:
        Coupler = AL_GratingCoupler(polarization="te", taper_length=20.0, WgWidthIO=WgWidth,
                    taper_angle=40.0, fiber_angle=10.0, grating_line_width=0.343,
                    nperiods=30, wavelength=1.55,layer=Layer)
        CPort   = "o1"

    if CouplerOn > 0:
        C1 = IO3 << Coupler
        C1.connect(C1.ports[CPort], InX1.ports["o1"])
        C2 = IO3 << Coupler
        C2.connect(C2.ports[CPort], OutX1.ports["o2"])

    return IO3
