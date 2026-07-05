import gdsfactory as gf

from AFQH_Lattice import AFQH_Lattice
from IO_2D_1 import IO_2D_1
from IO_2D_3 import IO_2D_3
from Taper import Taper

###############################################################################
# Parameters
###############################################################################
@gf.cell
def AFQH_Device( 
    Nx           = 9,
    Ny           = 9,
    LengthRing   = 12,
    BendRadius   = 20,
    WgWidth      = 1.2,
    GapS         = 0.25,
    GapW         = 0.75,
    
    FCGap        = 0.5,
    FAGap        = 20,
    InLengthX    = 100,
    TotLengthX   = 300,
    BendRadiusIO = 20,
    
    TaperOn      = False,
    CouplingM    = True,
    OutputIO     = True,
    Euler        = 0,
    Layer        = (2,0),
    DeviceID     = "1"
    
):

    AFQH_Device = gf.Component()
    
    Lattice = AFQH_Device << AFQH_Lattice(Nx = Nx, Ny = Ny, LengthRing = LengthRing, BendRadius = BendRadius, WgWidth = WgWidth, GapS = GapS, GapW = GapW, Euler = Euler, Layer = Layer)
    
    LatticeLengthX = Nx*(LengthRing + 2*BendRadius) + (Nx-1)*(GapW/2 + GapS/2 + WgWidth)
    LatticeLengthY = Ny*(LengthRing + 2*BendRadius) + (Ny-1)*(GapW/2 + GapS/2 + WgWidth)
    
    ###############################################################################
    # Input IO
    ###############################################################################
    if CouplingM == True:
        DY = (Nx-1)/2*(LengthRing + 2*BendRadius) + (Nx-1)/2*(GapW/2 + GapS/2 + WgWidth)
    else:
        DY = 0
    
    InLengthY      = LatticeLengthY - (BendRadius + LengthRing/2) - DY
    
    I_TotLengthY   = LatticeLengthY - (BendRadius + LengthRing/2) + (LengthRing/2 + 3*BendRadiusIO) + FAGap
    
    LatticeOffsetY = -(LatticeLengthY - (BendRadius + LengthRing/2)) - WgWidth/2
                
            
    I = AFQH_Device <<IO_2D_1(
                    TotLengthX = TotLengthX,
                    TotLengthY = I_TotLengthY,
                    InLengthX  = InLengthX,
                    InLengthY  = InLengthY,
                    MidLengthX = BendRadius,
                    CouplingLengthY  = LengthRing,  
                    BendRadius   = BendRadiusIO,
                    WgWidth      = WgWidth,
                    Layer        = Layer)
        
    
    LatticeOffsetX = InLengthX + (LengthRing/2 + BendRadius + FCGap + WgWidth)    
    Lattice.move((I.xmin + LatticeOffsetX, I.ymax+LatticeOffsetY))

    
    ###############################################################################
    # output IO
    ###############################################################################


    O_InLengthX = TotLengthX - (InLengthX + LatticeLengthX + 2*FCGap + 2*WgWidth)
    
    O_TotLengthY = LengthRing/2 + 3*BendRadiusIO + DY
   
    if OutputIO == True:
        O = AFQH_Device << IO_2D_3(
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
    
    if TaperOn:

        TaperLength = 50
        TaperWidth  = 0.2
        
        Coupler = Taper(Length = TaperLength, WidthStart = TaperWidth, WidthEnd = WgWidth, Layer = Layer)
        CPort   = "o2"
        
        C1 =  AFQH_Device << Coupler  
        C1.connect(C1.ports[CPort], I.ports["o1"])   
            
        C2 =  AFQH_Device << Coupler
        C2.connect(C2.ports[CPort], I.ports["o2"])  
            
        if OutputIO == True:
            C3 =  AFQH_Device << Coupler  
            C3.connect(C3.ports[CPort], O.ports["o1"])   
            
            C4 =  AFQH_Device << Coupler
            C4.connect(C4.ports[CPort], O.ports["o2"])  

   
    ###########################################################################
    # Text
    ###########################################################################
    
    DID = AFQH_Device << gf.components.text(text = DeviceID, size = 10, layer = Layer)
    DID.move((I.xmin + 25, I.ymin+25))

    ###########################################################################
    # Text
    ###########################################################################

    AFQH_Device.add_port(name="IN", port = I.ports["o1"])
    AFQH_Device.add_port(name="TH", port = I.ports["o2"])
    
    if OutputIO == True:
        AFQH_Device.add_port(name="DR", port = O.ports["o1"])
        AFQH_Device.add_port(name="BS", port = O.ports["o2"])

    AFQH_Device.info['center'] = (AFQH_Device.xmin + AFQH_Device.xsize/2, AFQH_Device.ymin + AFQH_Device.ysize/2)

    return AFQH_Device