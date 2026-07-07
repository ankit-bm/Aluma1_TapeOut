import gdsfactory as gf
from numpy import size
from IO8_Pulley import IO8_Pulley
from Racetrack import Racetrack
from Ring import Ring
from IO1 import IO1
from IO2 import IO2
from IO3 import IO3
from IO4 import IO4
from IO5 import IO5
from IO6_Pulley import IO6_Pulley
from IO7_Pulley import IO7_Pulley
from IO8_Pulley import IO8_Pulley

from AL_Taper import AL_Taper
from AL_GratingCoupler import AL_GratingCoupler
from ModulatedRing import ModulatedRing

###############################################################################
# Parameters
###############################################################################
@gf.cell
def ADF_PhC(         
    A       = [0.2],
    M       = [250],
    NPoints = 36000,
    
    LengthRingX = 0,
    LengthRingY = 0,

    BendRadius   = 20.0,
    BendRadiusIO = 20.0,
    
    WgWidth      = 1.6,
    WgWidthIO    = 1.0,
    
    Gap          = 0.5,
    
    FAGap        = 100.0,
    InLengthX    = 200.0,
    TotLengthX   = 500.0,
    
    ThetaC       = 60,
    
    InIO         = 1,
    OutIO        = 2,
    
    TaperOn     = True,   # 1: Grating, 0: Edge
    OutputIO    = True,

    Euler       = 0,
    BufLength   = 0.1,
        
    Layer        = (2,0),
    DeviceID     = "1",
    
    LablePosX       = 10,
    LablePosY       = 15,
    
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

    ADF_IO = gf.Component()
    # BufLength = 0.1
    
    PulleyBufY = 0
    
###############################################################################
# Input IO
###############################################################################
    if InIO == 1:
        #TotLengthY = 2*BendRadius + 2*BendRadiusIO + LengthRingY + (OutputIO==True)*FAGap
        TotLengthY = 3*BendRadius + LengthRingY + BufLength + (OutputIO==True)*FAGap
        I =  ADF_IO << IO1(InLengthX = InLengthX, TotLengthX = TotLengthX, TotLengthY = TotLengthY, BendRadius = BendRadiusIO, WgWidth = WgWidthIO, Layer = Layer,Euler=1)
    elif InIO == 2:
        I =  ADF_IO << IO2(LengthX = InLengthX, LengthY = FAGap, BendRadius = BendRadiusIO, WgWidth = WgWidthIO, Layer = Layer, Euler=1)
    elif InIO == 3:
        I =  ADF_IO << IO3(LengthX = InLengthX, LengthY = LengthRingY, TotLengthY = FAGap, BendRadius = BendRadiusIO, WgWidth = WgWidthIO, Layer = Layer,Euler=1)
    elif InIO == 6:
        TotLengthY = 2*BendRadius + 2*BendRadiusIO + LengthRingY + FAGap
        I =  ADF_IO << IO6_Pulley(InLengthX = InLengthX, TotLengthX = TotLengthX, TotLengthY = TotLengthY, Radius = BendRadius, BendRadius = BendRadiusIO, ThetaC = -ThetaC, Gap = Gap, WgWidth = WgWidthIO, Layer = Layer)
    elif InIO == 7:
        TotLengthY = 2*BendRadius + 2*BendRadiusIO + LengthRingY + FAGap
        I =  ADF_IO << IO7_Pulley(InLengthX = InLengthX, TotLengthX = TotLengthX, TotLengthY = TotLengthY, Radius = BendRadius, BendRadius = BendRadiusIO, ThetaC = ThetaC, Gap = Gap, WgWidth = WgWidthIO, Layer = Layer)

    
###############################################################################
# Ring Resonator
###############################################################################
    # if LengthRingX == 0 and LengthRingY == 0:
    #     R =  ADF_IO << Ring(BendRadius=BendRadius, WgWidth=WgWidth, Layer = Layer)
    # else:
    #     R =  ADF_IO << Racetrack(LengthX=LengthRingX, LengthY=LengthRingY, BendRadius=BendRadius, WgWidth=WgWidth,  Euler = Euler, Layer = Layer)

    R = ADF_IO << ModulatedRing(
            Radius  = BendRadius,
            WgWidth = WgWidth,
            Layer   = Layer,
            A = A,
            M = M,
            NPoints=NPoints
        )

    RingOffsetX = InLengthX + (LengthRingX/2 + BendRadius + Gap + WgWidthIO/2)
    
    if InIO == 1:
        #RingOffsetY = -BendRadiusIO - BendRadius - LengthRingY/2 - WgWidthIO/2
        RingOffsetY = - 1.5*BendRadius - LengthRingY/2 - WgWidthIO/2 - BufLength/2
    elif InIO == 6:
        # RingOffsetX = InLengthX + (LengthRingX/2 + BendRadius + Gap + WgWidth/2 + WgWidthIO/2)
        RingOffsetX = InLengthX + (LengthRingX/2 + BendRadius + Gap + WgWidthIO/2) #Special case for PhC, tracking outer radius
        RingOffsetY = -(I.ymax - I.ymin)/2
    elif InIO == 7:
        # RingOffsetX = InLengthX + (LengthRingX/2 + BendRadius + Gap + WgWidth/2 + WgWidthIO/2)
        RingOffsetX = InLengthX + (LengthRingX/2 + BendRadius + Gap + WgWidthIO/2) #Special case for PhC, tracking outer radius
        RingOffsetY = -(I.ymax - I.ymin)/2
    else:
        RingOffsetY = -FAGap/2 - WgWidthIO/2

    R.move((I.xmin + RingOffsetX, I.ymax + RingOffsetY))

###############################################################################
# Output IO
###############################################################################
    
    if OutputIO:

        if OutIO == 2 and InIO == 2:
            
            LengthOX = InLengthX + 2*BendRadius + LengthRingX + 2*Gap + 0*WgWidth + WgWidthIO
            
            O = ADF_IO << IO2(LengthX = LengthOX, LengthY = 3*FAGap, BendRadius = BendRadiusIO, WgWidth = WgWidthIO, Layer = Layer, Euler=1)
                
            OutputIOOffsetX = 0 
            OutputIOOffsetY = - WgWidthIO/2 + FAGap
            
        elif OutIO == 2:
                
            LengthOX = TotLengthX - InLengthX - (LengthRingX + 2*BendRadius + 2*Gap + 0*WgWidth + WgWidthIO)
            
            O = ADF_IO << IO2(LengthX = LengthOX, LengthY = FAGap, BendRadius = BendRadiusIO, WgWidth = WgWidthIO, Layer = Layer,Euler=1)
                
            O.mirror_x(0)
            OutputIOOffsetX = TotLengthX 
            OutputIOOffsetY = - WgWidthIO/2
            
        
        elif OutIO == 3:
            
            LengthOX = TotLengthX - InLengthX - (LengthRingX + 2*BendRadius + 2*Gap + 0*WgWidth + WgWidthIO)
            
            O = ADF_IO << IO3(LengthX = LengthOX, LengthY = LengthRingY, TotLengthY = FAGap, BendRadius = BendRadiusIO, WgWidth = WgWidthIO, Layer = Layer,Euler=1)
                
            O.mirror_x(0)
            OutputIOOffsetX = TotLengthX 
            OutputIOOffsetY = - WgWidthIO/2
            
            
        elif OutIO == 4:
                
            LengthOX = TotLengthX - InLengthX - (LengthRingX + 2*BendRadius + 2*Gap + 0*WgWidth + WgWidthIO)
            LengthY  = 3*BendRadius + LengthRingY + BufLength
            
            O = ADF_IO << IO4(LengthX = LengthOX, FAGap = FAGap, LengthY = LengthY, BendRadius = BendRadiusIO, WgWidth = WgWidthIO, Layer = Layer,Euler=1)
            O.mirror_x(0)
            O.mirror_y(0)
            OutputIOOffsetX = TotLengthX
            OutputIOOffsetY = -LengthY - WgWidthIO/2 
            
            
        elif OutIO == 5:
            
            LengthOX = TotLengthX - InLengthX - (LengthRingX + 2*BendRadius + 2*Gap + 0*WgWidth + WgWidthIO) - 2*BendRadiusIO
        
            O = ADF_IO << IO5(TotLengthX = TotLengthX, LengthX = LengthOX, LengthY = FAGap, TotLengthY = 3*FAGap, BendRadius = BendRadiusIO, WgWidth = WgWidthIO, Layer = Layer,Euler=1)
            
            OutputIOOffsetX = 0
            OutputIOOffsetY = FAGap - WgWidthIO/2
            
        elif OutIO == 8:
            PulleyBufY = FAGap
            TotLengthY_IO8 = 2*BendRadiusIO + 2*BendRadius + 2*FAGap 

            LengthOX = TotLengthX - InLengthX - (LengthRingX + 2*BendRadius + 2*Gap + WgWidthIO) - 2*BendRadiusIO

            O = ADF_IO << IO8_Pulley(
                InLengthX  = InLengthX,
                TotLengthX = TotLengthX,
                TotLengthY = TotLengthY_IO8,
                Radius     = BendRadius,
                BendRadius = BendRadiusIO,
                ThetaC     = ThetaC,
                Gap        = Gap,
                WgWidth    = WgWidthIO,
                BufY       = PulleyBufY,
                Layer      = Layer,
            )

            O.mirror_x(0)
            O.mirror_y(0)

            OutputIOOffsetX = TotLengthX
            OutputIOOffsetY = -(I.ymax - I.ymin) / 2

        O.move((I.xmin + OutputIOOffsetX, I.ymax + OutputIOOffsetY))
    
########################################################################################
# Tapers / Grating
########################################################################################

    if TaperOn:
        Coupler = AL_Taper(WidthEnd=WgWidthIO, Layer=Layer, **ECParams)
        CPort   = "o1"
        
        C1 =  ADF_IO << Coupler  
        C1.connect(C1.ports[CPort], I.ports["o1"])   
            
        C2 =  ADF_IO << Coupler
        C2.connect(C2.ports[CPort], I.ports["o2"])  
            
        if OutputIO == True:
            C3 =  ADF_IO << Coupler  
            C3.connect(C3.ports[CPort], O.ports["o1"])   
            
            C4 =  ADF_IO << Coupler
            C4.connect(C4.ports[CPort], O.ports["o2"]) 
    else:
        
        Coupler = AL_GratingCoupler(
                    GCWidthIO = 0.6,
                    WgWidthIO = WgWidthIO,
                    layer     = Layer,
                    **GCParams)
        CPort   = "o1"
        C1 =  ADF_IO << Coupler
        C1.connect(C1.ports[CPort], I.ports["o1"])
        
        C2 =  ADF_IO << Coupler
        C2.connect(C2.ports[CPort], I.ports["o2"])
        
        if OutputIO == True:
            C3 =  ADF_IO << Coupler
            C3.connect(C3.ports[CPort], O.ports["o1"])
            
            C4 =  ADF_IO << Coupler
            C4.connect(C4.ports[CPort], O.ports["o2"])

        
###############################################################################
# Output Ports
###############################################################################
                    
    ADF_IO.add_port(name="IN", port = I.ports["o1"])
    ADF_IO.add_port(name="TH", port = I.ports["o2"])
    
    if(OutputIO == True):
        ADF_IO.add_port(name="BS", port = O.ports["o1"])
        ADF_IO.add_port(name="DR", port = O.ports["o2"])

###########################################################################
# Device Info
###########################################################################

    DID = ADF_IO << gf.components.text_rectangular(text = DeviceID, size = 1, layer = Layer)

    DID.move((I.xmin+LablePosX , I.ymax + LablePosY))

    return ADF_IO





if __name__ == "__main__":
    c = gf.Component()

    D = ADF_PhC(
        Gap        = 0.26,
        FAGap      = 25,
        InIO       = 6,
        OutIO      = 8,
        OutputIO   = True,
        TaperOn    = True,
        BufLength  = 25,
        BendRadius = 20,
        BendRadiusIO = 20,
    )

    c << D

    c.show()
    c.plot()
    c.write_gds("ADF_PhC_In6_Out8_test.gds")
    print("Written ADF_PhC_In6_Out8_test.gds")