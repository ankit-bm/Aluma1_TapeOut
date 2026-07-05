import gdsfactory as gf
import numpy as np
from Racetrack import Racetrack
from Ring import Ring
from IO1 import IO1
from IO2 import IO2
from IO3 import IO3
from IO4 import IO4
from IO5 import IO5
from IO6_Pulley import IO6_Pulley
from IO7_Pulley import IO7_Pulley
from AL_Taper import AL_Taper
from AL_GratingCoupler import AL_GratingCoupler

###############################################################################
# Parameters
###############################################################################
@gf.cell
def APF_Pulley( 
    
    WgWidth      = 1.6,
    WgWidthIO    = 1.0,
    BendRadius   = 12,
    BendRadiusIO = 20,
    Gap          = 0.5,
    
    CouplingLength = 4,
    
    InLengthX    = 200,
    TotLengthX   = 500,

    TaperOn      = True,
    InIO         = 6,   
    Euler        = 1,
        
    Layer        = (2,0),
    DeviceID     = "1",
    LableX       = 10,
    LableY       = 15
):

    APF = gf.Component()

###############################################################################
# Input IO
###############################################################################
    ThetaC = np.degrees(CouplingLength/BendRadius)

    TotLengthY = 2*BendRadius + 1*BendRadiusIO 
    if InIO == 6:
        I =  APF << IO6_Pulley(InLengthX = InLengthX, TotLengthX = TotLengthX, TotLengthY = TotLengthY, Radius = BendRadius, BendRadius = BendRadiusIO, ThetaC = -ThetaC, Gap = Gap, WgWidth = WgWidthIO, Euler = Euler, Layer = Layer)
    elif InIO == 7:
        I =  APF << IO7_Pulley(InLengthX = InLengthX, TotLengthX = TotLengthX, TotLengthY = TotLengthY, Radius = BendRadius, BendRadius = BendRadiusIO, ThetaC = -ThetaC, Gap = Gap, WgWidth = WgWidthIO, Euler = Euler, Layer = Layer)
        
###############################################################################
# Ring Resonator
###############################################################################
    R =  APF << Ring(BendRadius=BendRadius, WgWidth=WgWidth, Layer = Layer)
    
    RingOffsetX = InLengthX + (BendRadius + Gap + WgWidth/2 + WgWidthIO/2)
    RingOffsetY = -(I.ymax - I.ymin)/2
    
    R.move((I.xmin + RingOffsetX, I.ymax + RingOffsetY))

    
########################################################################################
# Tapers / Grating
########################################################################################
    
    if TaperOn:
        
        Coupler = AL_Taper(WgWidth = WgWidthIO, Layer = Layer)
        CPort   = "o1"
        
        C1 =  APF << Coupler  
        C1.connect(C1.ports[CPort], I.ports["o1"])   
            
        C2 =  APF << Coupler
        C2.connect(C2.ports[CPort], I.ports["o2"])  
    
    else:
        
        Coupler = AL_GratingCoupler(polarization = "te", taper_length = 20.0, WgWidthIO = WgWidthIO , taper_angle = 40.0, fiber_angle = 10.0,
                    grating_line_width = 0.343, nperiods = 30, wavelength = 1.55, )
        CPort   = "o1"
        C1 =  APF << Coupler
        C1.connect(C1.ports[CPort], I.ports["o1"])
        
        C2 =  APF << Coupler
        C2.connect(C2.ports[CPort], I.ports["o2"])

        
###############################################################################
# Output Ports
###############################################################################
                    
    APF.add_port(name="IN", port = I.ports["o1"])
    APF.add_port(name="TH", port = I.ports["o2"])

###########################################################################
# Device Info
###########################################################################

    DID = APF << gf.components.text_rectangular(text = DeviceID, size = 1, layer = Layer)
    DID.move((I.xmin - LableX, I.ymax-LableY))

    return APF
