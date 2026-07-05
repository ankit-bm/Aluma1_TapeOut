import gdsfactory as gf

from AQH_CB_Lattice import AQH_CB_Lattice
from IO_2D_1 import IO_2D_1
from IO_2D_3 import IO_2D_3
from IO3 import IO3
from AL_Taper import AL_Taper
from AL_GratingCoupler import AL_GratingCoupler

###############################################################################
# Parameters
###############################################################################
@gf.cell(cache=False)
def AQH_CB_Device(
    Nx = 10, 
    Ny = 10, 
    BendRadius = 20,
    LengthSR   = 12,
    eta        = 0.110,
    WgWidth    = 1.0,
    Gap        = 0.5, 
    FCGap      = 0.6,
    InLengthX    = 200,
    TotLengthX   = 500,
    BendRadiusIO = 20,
    FAGap       = 30,
    Euler       = 0,
    CouplerON   = 1, #1 - Taper, #2 GC , #3 for GC with IO3
    BlockBoxOn  = 0,
    OutputIO    = True,
    
    Layer       = (2,0),
    LayerB      = (2,1),
    LablePosX    = 200,
    LablePosY    = 18,
    DeviceID    = "1",
    
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
    
    LengthLR = LengthSR + eta
    
    Lattice =  Device << AQH_CB_Lattice(Nx=Nx, Ny=Ny, Gap=Gap, BendRadius = BendRadius, LengthSR = LengthSR, eta = eta, WgWidth = WgWidth, Euler = Euler, Layer = Layer)


    LatticeLengthX = (Nx-1) * 2*(Gap + WgWidth + 2*BendRadius + LengthSR/2 + LengthLR/2) + 2*(LengthSR/2 + BendRadius)

    LatticeLengthY = (Ny-1) * 2*(Gap + WgWidth + 2*BendRadius + LengthSR/2 + LengthLR/2) + 2*(LengthSR/2 + BendRadius)

    ###########################################################################
    # Input IO
    ###########################################################################
    
    InLengthY    = LatticeLengthY - (BendRadius + LengthSR/2) - (2*BendRadius + LengthLR + Gap + WgWidth)
    #I_TotLengthY = InLengthY + (LengthSR/2 + 3*BendRadiusIO) + (2*BendRadius + LengthLR + Gap + WgWidth) + FAGap
    I_TotLengthY = LatticeLengthY + FAGap

    if CouplerON == 3:
        
        InLengthY    = LatticeLengthY - FAGap
        
        I = Device << IO3(LengthX = InLengthX,MidLengthX = 2*LengthSR, LengthY = LengthSR,TotLengthY=FAGap, BendRadius = BendRadiusIO, WgWidth = WgWidth,
                            Euler=Euler, Layer = Layer)
        
        LatticeOffsetX  = InLengthX + (FCGap + WgWidth + BendRadius + LengthSR/2)
        LatticeOffsetY  = FAGap/2 + WgWidth/2
        Lattice.move((I.xmin + LatticeOffsetX, I.ymin+LatticeOffsetY))

    else:
        I = Device <<IO_2D_1(
                            TotLengthX = TotLengthX,
                            TotLengthY = I_TotLengthY,
                            InLengthX  = InLengthX,
                            InLengthY  = InLengthY,
                            MidLengthX = BendRadius,
                            CouplingLengthY  = LengthSR,  
                            BendRadius   = BendRadiusIO,
                            WgWidth      = WgWidth,
                            Layer        = Layer)

        LatticeOffsetX  = InLengthX + (FCGap + WgWidth + BendRadius + LengthSR/2)
        LatticeOffsetY  = -InLengthY - WgWidth/2
        Lattice.move((I.xmin + LatticeOffsetX, I.ymax + LatticeOffsetY))

    ###########################################################################
    # Output IO
    ###########################################################################

    O_InLengthX  = TotLengthX - (InLengthX + LatticeLengthX + 2*FCGap + 2*WgWidth)

    O_TotLengthY = I_TotLengthY - InLengthY - FAGap

    if OutputIO == True:
        
        if CouplerON == 3:
            
            O = Device << IO3(LengthX = InLengthX, MidLengthX = 2*LengthSR, LengthY = LengthSR,TotLengthY=FAGap, BendRadius = BendRadiusIO, WgWidth = WgWidth,
                    Euler=Euler, Layer = Layer)
            
            O.mirror_x(0)
            OutputIOOffsetX = I.xmax + (InLengthX + LatticeLengthX + 2*FCGap + 2*WgWidth) -WgWidth/2
            OutputIOOffsetY = FAGap + WgWidth/2

            O.move((I.xmin + OutputIOOffsetX , I.ymin + OutputIOOffsetY))
            
        else:
    
            O = Device << IO_2D_3(
                            TotLengthX = O_InLengthX,
                            InLengthY  = O_TotLengthY,
                            MidLengthX = BendRadius, 
                            CouplingLengthY=LengthSR, 
                            FAGap      = FAGap, 
                            BendRadius = BendRadiusIO,
                            WgWidth    = WgWidth,
                            Layer      = Layer)


            O.mirror_x(0)
            OutputIOOffsetX = O_InLengthX + InLengthX + LatticeLengthX + (2*FCGap + 2*WgWidth)
            OutputIOOffsetY = FAGap + WgWidth/2

            O.move((I.xmin + OutputIOOffsetX, I.ymin + OutputIOOffsetY))

    ###########################################################################
    # Grating Couplers
    ###########################################################################
    
    if CouplerON == 1:

        Coupler = AL_Taper(WidthStart=WgWidth, Layer=Layer, **ECParams)
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
    # ports
    ###########################################################################

    Device.add_port(name="IN", port = I.ports["o1"])
    Device.add_port(name="TH", port = I.ports["o2"])
    
    if OutputIO == True:
        Device.add_port(name="BS", port = O.ports["o1"])
        Device.add_port(name="DR", port = O.ports["o2"])

    ###########################################################################
    # Fill Block Layer
    ###########################################################################

    if BlockBoxOn:
        BlockBox =  Device << gf.components.rectangle(size=(LatticeLengthX+20, LatticeLengthY+20), layer = LayerB)
        BlockBox.move((Lattice.xmin - 10, Lattice.ymin - 10))

    ##########################################################################
    #Device Info
    ##########################################################################

    DID = Device << gf.components.text_rectangular(text = DeviceID, size = 1, layer = Layer)
    DID.move((I.xmin - LablePosX, I.ymax-LablePosY))

    return Device