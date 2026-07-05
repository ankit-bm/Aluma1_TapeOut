import gdsfactory as gf
from AL_GratingCoupler import AL_GratingCoupler
from IO2 import IO2

@gf.cell
def IO_GC( 
    LengthX    = 100,
    FAGap      = 127,
    BendRadius = 10,
    WgWidth    = 1.0,
    Euler      = 0,
    Layer      = (3,0),
    LablePosX  = 20,
    LablePosY  = -40,
    DeviceID     = "1",
    
    GCParams: dict = dict(
        Pitch          = 0.6,
        DutyCycle      = 0.4,
        UniformGrating = True,
        NPeriod        = 20,
        gaps           = (0.1,)*20,
        widths         = (0.25,)*20,
        polarization   = "te",
        taper_length   = 15.0,
        LengthGC       = 60,
        taper_angle    = 40.0,
        fiber_angle    = 10.0,
        wavelength     = 1.55,
    ),
):
    
    IO_GC = gf.Component()
    
    ##################################################################################
    # U arc
    ##################################################################################
    
    U      = IO_GC << IO2(LengthX=LengthX,LengthY=FAGap,BendRadius=BendRadius,WgWidth=WgWidth,Euler=Euler,CouplerOn=0, Layer=Layer) 
    
    Coupler = AL_GratingCoupler(GCWidthIO=0.6, WgWidthIO=WgWidth, layer=Layer, **GCParams)

    C1 = IO_GC << Coupler
    C2 = IO_GC << Coupler
    
    ##################################################################################
    # Connections
    ##################################################################################

    C1.connect(C1.ports["o1"], U.ports["o1"])
    C2.connect(C2.ports["o1"], U.ports["o2"])

    IO_GC.add_port("IN", port=C1.ports["o2"])
    IO_GC.add_port("OUT", port=C2.ports["o2"])
    
    IO_GC.ymax = WgWidth/2
    
    DID = IO_GC << gf.components.text_rectangular(text = DeviceID, size = 1, layer = Layer)

    DID.move((IO_GC.xmin+LablePosX , IO_GC.ymax + LablePosY))
    
    return IO_GC
