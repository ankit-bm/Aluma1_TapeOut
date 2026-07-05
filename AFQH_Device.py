import gdsfactory as gf

from AFQH_Lattice import AFQH_Lattice
from IO_2D_1 import IO_2D_1
from IO_2D_3 import IO_2D_3
from IO3 import IO3
from AL_Taper import AL_Taper
from AL_GratingCoupler import AL_GratingCoupler

###############################################################################
# Parameters
###############################################################################
@gf.cell
def AFQH_Device( 
    Nx           = 9,
    Ny           = 9,
    LengthRing   = 15,
    BendRadius   = 25,
    WgWidth      = 1.2,
    Gap          = 0.25,
    FCGap        = 0.5,
    FAGap        = 20,
    InLengthX    = 100,
    TotLengthX   = 850,
    BendRadiusIO = 20,
    
    CouplerON   = 1, #1 - Taper, #2 GC , #3 for GC with IO3
    BlockBoxOn  = 0,
    CouplingM    = False,
    OutputIO     = True,

    Euler        = 0,
    Layer        = (2,0),
    LayerB       = (2,1),
    LablePosX    = 200,
    LablePosY    = 18,
    DeviceID     = "1",
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
    
    Lattice = Device << AFQH_Lattice(Nx = Nx, Ny = Ny, LengthRing = LengthRing, BendRadius = BendRadius, WgWidth = WgWidth, Gap = Gap, Euler = Euler, Layer = Layer)
    
    LatticeLengthX = Nx*(LengthRing + 2*BendRadius) + (Nx-1)*(Gap + WgWidth)
    LatticeLengthY = Ny*(LengthRing + 2*BendRadius) + (Ny-1)*(Gap + WgWidth)
    
    ###############################################################################
    # Input IO
    ###############################################################################
    if CouplingM == True:
        DY = (Nx-1)/2*(LengthRing + 2*BendRadius) + (Nx-1)/2*(Gap + WgWidth)
    else:
        DY = 0
    
    BufLength = 0.1

    InLengthY      = LatticeLengthY - (BendRadius + LengthRing/2) - DY
    
    I_TotLengthY   = LatticeLengthY - (BendRadius + LengthRing/2) + (LengthRing/2 + 3*BendRadiusIO) + FAGap + BufLength

    if CouplerON == 3:
        
        LatticeOffsetY = -(LatticeLengthY-FAGap-WgWidth)
        I = Device << IO3(LengthX = InLengthX,MidLengthX = 2*LengthRing, LengthY = LengthRing,TotLengthY=FAGap, BendRadius = BendRadiusIO, WgWidth = WgWidth,
                        Euler=Euler, Layer = Layer)
        
        LatticeOffsetX = InLengthX + (LengthRing/2 + BendRadius + FCGap + WgWidth)    
        # Lattice.move((I.xmin + LatticeOffsetX, I.ymin+LatticeOffsetY))
        Lattice.move((I.xmin + LatticeOffsetX,-FAGap/2))
    else:
        
        LatticeOffsetY = -(LatticeLengthY - (BendRadius + LengthRing/2)) - WgWidth/2
        
        I = Device <<IO_2D_1(
                        TotLengthX = TotLengthX,
                        TotLengthY = I_TotLengthY,
                        InLengthX  = InLengthX,
                        InLengthY  = InLengthY,
                        MidLengthX = BendRadius,
                        CouplingLengthY  = LengthRing,  
                        BendRadius = BendRadiusIO,
                        WgWidth      = WgWidth,
                        Layer        = Layer)
        
        LatticeOffsetX = InLengthX + (LengthRing/2 + BendRadius + FCGap + WgWidth)    
        Lattice.move((I.xmin + LatticeOffsetX, I.ymax+LatticeOffsetY))
    
    ###############################################################################
    # output IO
    ###############################################################################

    O_InLengthX = TotLengthX - (InLengthX + LatticeLengthX + 2*FCGap + 2*WgWidth)
    
    O_TotLengthY = LengthRing/2 + 3*BendRadiusIO + DY + BufLength

    if OutputIO == True:
        if CouplerON == 3:
            
            O_InLengthX = TotLengthX - (InLengthX + LatticeLengthX + 2*FCGap + 2*WgWidth)
            
            O = Device << IO3(LengthX = InLengthX, MidLengthX = 2*LengthRing, LengthY = LengthRing,TotLengthY=FAGap, BendRadius = BendRadiusIO, WgWidth = WgWidth,
                        Euler=Euler, Layer = Layer)
            
            O.mirror_x(0)

            OutputIOOffsetX = InLengthX +WgWidth + 2*FCGap + LatticeLengthX +WgWidth/2
            OutputIOOffsetY = FAGap + WgWidth/2

            O.move((I.xmax + OutputIOOffsetX, I.ymin + OutputIOOffsetY))

        else:
            
            O_InLengthX = TotLengthX - (InLengthX + LatticeLengthX + 2*FCGap + 2*WgWidth)
            
            O = Device << IO_2D_3(
                            TotLengthX      = O_InLengthX, 
                            InLengthY       = O_TotLengthY, 
                            CouplingLengthY = LengthRing, 
                            MidLengthX      = BendRadius,    
                            FAGap           = FAGap, 
                            BendRadius      = BendRadiusIO,
                            WgWidth         = WgWidth,
                            Layer           = Layer)

            O.mirror_x(0)

            OutputIOOffsetX = TotLengthX 
            OutputIOOffsetY = FAGap + WgWidth/2

            O.move((I.xmin + OutputIOOffsetX, I.ymin + OutputIOOffsetY))

    ########################################################################################
    # Grating Couplers
    ########################################################################################
    
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
    # Ports
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
        
    ###########################################################################
    # Text
    ###########################################################################
    
    DID = Device << gf.components.text_rectangular(text = DeviceID, size = 1, layer = Layer)

    DID.move((I.xmin - LablePosX, I.ymax-LablePosY))
    
    return Device