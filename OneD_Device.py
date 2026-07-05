import gdsfactory as gf
import numpy as np
from OneD_Lattice import OneD_Lattice
from IO_2D_2 import IO_2D_2
from IO_2D_3 import IO_2D_3
from IO3 import IO3
from AL_Taper import AL_Taper
from AL_GratingCoupler import AL_GratingCoupler

###############################################################################
# Parameters
###############################################################################
@gf.cell
def OneD_Device( 
    Nx=4, 
    BendRadius = 20,
    LengthX    = 12,
    LengthY    = 12,
    LengthXL   = 12.08,
    LengthYL   = 12.08,
    WgWidth    = 1.0,
    Gap        = 0.5, 
    FCGap      = 0.6,
    
    FAGap        = 100,
    InLengthX    = 200,
    TotLengthX   = 500,
    BendRadiusIO = 20,
    
    Euler       = 0,
    CouplerON   = 1, #1 - Taper, #2 GC , #3 for GC with IO3
    OutputIO    = True,
    BlockBoxOn  = 0,
    Layer       = (2,0),
    LayerB      = (2,1),
    LablePosX    = 200,
    LablePosY    = 18,
    DeviceID   = "2",
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
    # Lattice
    ###############################################################################
    
    Lattice =  Device << OneD_Lattice(Nx=Nx, Gap=Gap, BendRadius = BendRadius, LengthX = LengthX, LengthY = LengthY, LengthXL = LengthXL, LengthYL = LengthYL, WgWidth = WgWidth, Euler = Euler, Layer = Layer)
        
    LatticeLengthX = (Nx-1) * 2*(Gap + WgWidth + 2*BendRadius + LengthX/2+LengthXL/2) + LengthX + 2*BendRadius
    
    LatticeLengthY = 2*BendRadius + LengthY
        
    ###############################################################################
    # Input IO
    ###############################################################################
    
    BufLength    = 0.1
    
    InLengthY    = BendRadiusIO + LengthY/2
    
    I_TotLengthY = InLengthY + (LengthY/2 + 3*BendRadiusIO) + FAGap + BufLength
    

    if CouplerON == 3:
        I = Device <<IO3(LengthX = InLengthX,MidLengthX = 2*LengthX, LengthY = LengthY,TotLengthY=FAGap, BendRadius = BendRadiusIO, WgWidth = WgWidth,
                            Euler=Euler, Layer = Layer)
        
        LatticeOffsetX  =  InLengthX + FCGap + WgWidth + BendRadius + LengthX/2
        LatticeOffsetY  = -FAGap/2 -WgWidth/2
        Lattice.move((I.xmin + LatticeOffsetX, I.ymax + LatticeOffsetY))
        
    else:
        
        I = Device <<IO_2D_2(
                            TotLengthX = TotLengthX,
                            TotLengthY = I_TotLengthY,
                            InLengthX  = InLengthX,
                            MidLengthX = BendRadius,
                            CouplingLengthY  = LengthX,  
                            BendRadius   = BendRadiusIO,
                            WgWidth      = WgWidth,
                            Layer        = Layer)
        
        LatticeOffsetX  =  InLengthX + FCGap + WgWidth + BendRadius + LengthX/2
        LatticeOffsetY  = -InLengthY - WgWidth/2
        Lattice.move((I.xmin + LatticeOffsetX, I.ymax + LatticeOffsetY))
    
    ###############################################################################
    # Output IO
    ###############################################################################
    
    
    O_InLengthX = TotLengthX - (InLengthX + LatticeLengthX + 2*FCGap + 2*WgWidth)

    O_TotLengthY = I_TotLengthY - InLengthY - FAGap
    
    if OutputIO == True:
    
        if CouplerON == 3:

            O = Device << IO3(LengthX = O_InLengthX,MidLengthX = 2*LengthX, LengthY = LengthY,TotLengthY=FAGap, BendRadius = BendRadiusIO, WgWidth = WgWidth,
                                Euler=Euler, Layer = Layer)


            O.mirror_x(0)
            OutputIOOffsetX = O_InLengthX + InLengthX + LatticeLengthX + 2*FCGap + 2*WgWidth
            OutputIOOffsetY = FAGap + WgWidth/2 

            O.move((I.xmin + OutputIOOffsetX, I.ymin + OutputIOOffsetY))
        
        else:
            
            O = Device << IO_2D_3(
                    TotLengthX = O_InLengthX,
                    InLengthY  = O_TotLengthY,
                    MidLengthX = BendRadius, 
                    CouplingLengthY=LengthX, 
                    FAGap      = FAGap, 
                    BendRadius = BendRadiusIO, 
                    WgWidth    = WgWidth, 
                    Layer      = Layer)


            O.mirror_x(0)
            OutputIOOffsetX = O_InLengthX + InLengthX + LatticeLengthX + 2*FCGap + 2*WgWidth
            OutputIOOffsetY = FAGap + WgWidth/2 

            O.move((I.xmin + OutputIOOffsetX, I.ymin + OutputIOOffsetY))
            
        
    ###############################################################################
    # Output IO
    ###############################################################################

    if CouplerON == 1:

        Coupler = AL_Taper(WidthEnd=WgWidth, Layer=Layer, **ECParams)
        CPort   = "o1"
        
        C1 =  Device << Coupler  
        C1.connect(C1.ports[CPort], I.ports["o1"])   
            
        C2 =  Device << Coupler
        C2.connect(C2.ports[CPort], I.ports["o2"])  
            
        if OutputIO == True:
            C3 =  Device << Coupler  
            C3.connect(C3.ports[CPort], O.ports["o1"])   
            
            C4 =  Device << Coupler
            C4.connect(C4.ports[CPort], O.ports["o2"]) 
    elif CouplerON == 2:
        
        Coupler = AL_GratingCoupler(GCWidthIO=0.6, WgWidthIO=WgWidth, layer=Layer, **GCParams)
        CPort   = "o1"
        
        C1 =  Device << Coupler  
        C1.connect(C1.ports[CPort], I.ports["o1"])   
            
        C2 =  Device << Coupler
        C2.connect(C2.ports[CPort], I.ports["o2"])  
            
        if OutputIO == True:
            C3 =  Device << Coupler  
            C3.connect(C3.ports[CPort], O.ports["o1"])   
            
            C4 =  Device << Coupler
            C4.connect(C4.ports[CPort], O.ports["o2"]) 
        
    elif CouplerON == 3:
        Coupler = AL_GratingCoupler(GCWidthIO=0.6, WgWidthIO=WgWidth, layer=Layer, **GCParams)
        CPort   = "o1"
        C1 =  Device << Coupler
        C1.connect(C1.ports[CPort], I.ports["o1"])
        
        C2 =  Device << Coupler
        C2.connect(C2.ports[CPort], I.ports["o2"])

        if OutputIO == True:
            C3 =  Device << Coupler
            C3.connect(C3.ports[CPort], O.ports["o1"])
            
            C4 =  Device << Coupler
            C4.connect(C4.ports[CPort], O.ports["o2"])
    else:
        pass
        
    ###########################################################################
    # Fill Block Layer
    ###########################################################################
    if BlockBoxOn:
        BlockBox =  Device << gf.components.rectangle(size=(LatticeLengthX+20, LatticeLengthY+20), layer = LayerB)
        BlockBox.move((Lattice.xmin - 10, Lattice.ymin - 10))

    ###########################################################################
    # Text
    ###########################################################################

    Device.add_port(name="IN", port = I.ports["o1"])
    Device.add_port(name="TH", port = I.ports["o2"])
    
    if OutputIO == True:
        Device.add_port(name="BS", port = O.ports["o1"])
        Device.add_port(name="DR", port = O.ports["o2"])
    

    ##########################################################################
    #Device Info
    ##########################################################################

    DID = Device << gf.components.text_rectangular(text = DeviceID, size = 1, layer = Layer)
    DID.move((I.xmin - LablePosX, I.ymax-LablePosY))
        

    return Device


