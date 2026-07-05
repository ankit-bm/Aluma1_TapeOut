import gdsfactory as gf
from IO3 import IO3
from IO5 import IO5
from AL_Taper import AL_Taper
from AL_GratingCoupler import AL_GratingCoupler

###############################################################################
# Parameters
###############################################################################
@gf.cell
def DirCoupler_Device( 
        WgWidth        = 1.8,
        Gap            = 0.5,
        CouplingLength = 20,
        BendRadius     = 12,
        InLengthX      = 100,
        FAGap          = 100,

        TaperOn     = True,   # 0: Grating, 1: Edge
        Euler       = 0,
        Layer       = (2,0),
        LablePosX   = 10,
        LablePosY   =-20,
        IOIn        = 3,
        IOOut       = 3,
        DeviceID    = "1",
        FlipText    = False,
        GCParams : dict = dict(
            Pitch          = 0.716,
            DutyCycle      = 0.700,
            NPeriod        = 25,
            taper_length   = 15.0,
            taper_angle    = 40.0,
            fiber_angle    = 10.0,
            wavelength     = 1.55,
            LengthGC       = 100,
            UniformGrating = True,
        ),
        ECParams : dict = dict(
            Length     = 395,
            TaperType  = 1,
            MarkerOn   = True,
    ),
):

    Device = gf.Component()

###############################################################################
# Input
###############################################################################
    BufLengthX = 0.1

    MidLengthX = BufLengthX
    I =  Device << IO3(LengthX = InLengthX, MidLengthX = MidLengthX, LengthY = CouplingLength, TotLengthY = FAGap, BendRadius = BendRadius, WgWidth = WgWidth, Euler = Euler, Layer = Layer)
    

###############################################################################
# Output
###############################################################################
            
    TotLengthX =  InLengthX + (Gap + WgWidth) + MidLengthX + 2*BendRadius 
    LengthOX   = MidLengthX
    
    if IOOut == 3:
        O = Device << IO3(LengthX = LengthOX , MidLengthX = MidLengthX, LengthY = CouplingLength, TotLengthY = FAGap, BendRadius = BendRadius, WgWidth = WgWidth, Euler = Euler, Layer = Layer)
    
    else:
        O = Device << IO5(TotLengthX = TotLengthX, LengthX = LengthOX, LengthY = CouplingLength+2*BendRadius, TotLengthY = 3*FAGap, BendRadius = BendRadius, WgWidth = WgWidth, Euler = Euler, Layer = Layer)
    
    OutputIOOffsetX = 0
    OutputIOOffsetY = FAGap - WgWidth/2
            
            
    O.move((I.xmin + OutputIOOffsetX, I.ymax + OutputIOOffsetY))
    
########################################################################################
# Tapers / Grating
########################################################################################
    
    if TaperOn:
        Coupler = AL_Taper(WidthEnd=WgWidth, Layer=Layer, **ECParams)
        CPort   = "o1"
    else:
        Coupler = AL_GratingCoupler(GCWidthIO=0.6, WgWidthIO=WgWidth, layer=Layer, **GCParams)
        CPort   = "o1"

    C1 = Device << Coupler
    C1.connect(C1.ports[CPort], I.ports["o1"])
    C2 = Device << Coupler
    C2.connect(C2.ports[CPort], I.ports["o2"])
    C3 = Device << Coupler
    C3.connect(C3.ports[CPort], O.ports["o1"])
    C4 = Device << Coupler
    C4.connect(C4.ports[CPort], O.ports["o2"])
        
###############################################################################
# Output Ports
###############################################################################
                    
    Device.add_port(name="IN", port = I.ports["o1"])
    Device.add_port(name="TH", port = I.ports["o2"])
    
    Device.add_port(name="BS", port = O.ports["o1"])
    Device.add_port(name="DR", port = O.ports["o2"])

###########################################################################
# Device Info
###########################################################################

    DID = Device << gf.components.text_rectangular(text = DeviceID, size = 1, layer = Layer)
    
    if FlipText == True:
        DID.mirror_x()
        
    DID.move((I.xmin - LablePosX, I.ymax-LablePosY))


    return Device
