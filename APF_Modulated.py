import gdsfactory as gf
from Ring import Ring
from ModulatedRing import ModulatedRing
from IO2 import IO2
from LT_Taper import LT_Taper

###############################################################################
# Parameters
###############################################################################
@gf.cell
def APF_Modulated( 
    BendRadius   = 12.0,
    BendRadiusIO = 20.0,
    WgWidth      = 1.6,
    WgWidthIO    = 1.0,
    Gap          = 0.5,
    FAGap        = 100.0,
    InLengthX    = 200.0,
    Modulation   = True,
    NPoints      = 360*10,
    ModPeriod    = [250, 251, 252, 253],
    DW           = 0.2,
    FlipRing     = True,        
    TaperOn      = True,    
    Layer        = (2,0),
    DeviceID     = "1"
):

    APF = gf.Component()
   
###############################################################################
# Input IO
###############################################################################
    
    I =  APF << IO2(LengthX = InLengthX, LengthY = FAGap, BendRadius = BendRadiusIO, WgWidth = WgWidthIO, Layer = Layer)
    
###############################################################################
# Ring Resonator
###############################################################################
    
    if Modulation == True:
        R =  APF << ModulatedRing(NPoints = NPoints, Radius=BendRadius, WgWidth=WgWidth, A = DW, M = ModPeriod, Layer = Layer)
    else:
        R =  APF << Ring(BendRadius=BendRadius, WgWidth=WgWidth, Layer = Layer)
    
    
    if FlipRing == True:
        RingOffsetX  = InLengthX - (BendRadius + Gap + WgWidth/2 + WgWidthIO/2) + (Modulation == True) * WgWidth/2
    else:
        RingOffsetX  = InLengthX + (BendRadius + Gap + WgWidth/2 + WgWidthIO/2)

    RingOffsetY = -FAGap/2 - WgWidthIO/2
    
    R.move((I.xmin + RingOffsetX, I.ymax + RingOffsetY))

    
########################################################################################
# Tapers / Grating
########################################################################################
    
    if TaperOn:

        Coupler = LT_Taper(WgWidth = WgWidthIO)
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
    DID.move((I.xmin - 200, I.ymax-16))

    return APF
