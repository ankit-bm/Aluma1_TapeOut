import gdsfactory as gf
from Straight import Straight
from Bend import Bend
from AL_Taper import AL_Taper
from AL_GratingCoupler import AL_GratingCoupler

@gf.cell
def IO2( 
    LengthX    = 100,
    LengthY      = 50,
    BendRadius = 10,
    WgWidth    = 1.0,
    Euler      = 0,
    CouplerOn  = 0,   # 0=none, 1=EC, 2=GC
    Layer      = (3,0)
):
    
    IO2 = gf.Component()
    
    ##################################################################################
    #Defined from Bottom to Up
    ##################################################################################
    
    InX    = IO2 << Straight(Length=LengthX-BendRadius, Width=WgWidth, Layer=Layer) 
    Bend1  = IO2 << Bend(Radius=BendRadius, Width=WgWidth, Euler = Euler, Layer=Layer)  
    Y      = IO2 << Straight(Length=LengthY-2*BendRadius, Width=WgWidth, Layer=Layer)   
    Bend2  = IO2 << Bend(Radius=BendRadius, Width=WgWidth, Euler = Euler, Layer=Layer)  
    OutX   = IO2 << Straight(Length=LengthX-BendRadius, Width=WgWidth, Layer=Layer)
    
    ########################################################################################
    # Connections 
    ########################################################################################
    Bend1.connect("o1", InX.ports["o2"])  
    Y.connect("o1", Bend1.ports["o2"])  
    Bend2.connect("o1", Y.ports["o2"])
    OutX.connect("o1", Bend2["o2"])
    
    IO2.ymax = WgWidth/2
    
    IO2.add_port(name="o1", port = InX.ports["o1"])
    IO2.add_port(name="o2", port = OutX.ports["o2"])
    
    
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
        C1 = IO2 << Coupler
        C1.connect(C1.ports[CPort], InX.ports["o1"])
        C2 = IO2 << Coupler
        C2.connect(C2.ports[CPort], OutX.ports["o2"])

    return IO2
