import gdsfactory as gf

from IQH_Lattice import IQH_Lattice
from IO_2D_1 import IO_2D_1
from IO_2D_3 import IO_2D_3

from LT_Taper import LT_Taper

###############################################################################
# Parameters
###############################################################################
@gf.cell
def IQH_Device( 
    Nx = 10, 
    Ny = 10, 
    BendRadius  = 20,
    LengthSRX   = 12,
    LengthSRY   = 10,
    eta         = 0.08,
    alpha       = 0.08,
    WgWidth     = 1.0,
    Gap         = 0.5, 
    FCGap       = 0.6,
    InLengthX    = 200,
    TotLengthX   = 500,
    BendRadiusIO = 20,
    FAGap        = 30,
    Euler        = 0,
    TaperOn      = False,
    OutputIO     = True,
    Layer        = (2,0),
    DeviceID     = "1"
):

    IQH_Device = gf.Component()
    

    Lattice =  IQH_Device << IQH_Lattice(Nx=Nx, Ny=Ny, Gap=Gap, BendRadius = BendRadius, LengthSRX  = LengthSRX, LengthSRY  = LengthSRY, eta = eta, alpha = alpha, WgWidth = WgWidth, Euler = Euler, Layer = Layer)

    LengthLRX = LengthSRY
    LengthLRY = LengthSRX + 2*eta
    
    LatticeLengthX = (Nx - 1) * 2 * (Gap + WgWidth + 2*BendRadius + LengthSRX/2 + LengthLRX/2) + 2*(BendRadius + LengthSRX/2) 
    LatticeLengthY = (Ny - 1) * 2 * (Gap + WgWidth + 2*BendRadius + LengthSRY/2 + LengthLRY/2) + 2*(BendRadius + LengthSRY/2) 
        
    ###########################################################################
    # Input IO
    ###########################################################################
    
    InLengthY    = LatticeLengthY - (BendRadius + LengthSRY/2)
    I_TotLengthY = InLengthY + (LengthSRY/2 + 3*BendRadiusIO) + FAGap
    

    I = IQH_Device <<IO_2D_1(
                          TotLengthX = TotLengthX,
                          TotLengthY = I_TotLengthY,
                          InLengthX  = InLengthX,
                          InLengthY  = InLengthY,
                          MidLengthX = BendRadius,
                          CouplingLengthY  = LengthSRY,  
                          BendRadius   = BendRadiusIO,
                          WgWidth      = WgWidth,
                          Layer        = Layer)
    


    LatticeOffsetX  = InLengthX + (FCGap + WgWidth + BendRadius + LengthSRX/2)
    LatticeOffsetY  = -InLengthY - WgWidth/2
    Lattice.move((I.xmin + LatticeOffsetX, I.ymax + LatticeOffsetY))

    ###########################################################################
    # Output IO
    ###########################################################################

    O_InLengthX  = TotLengthX - (InLengthX + LatticeLengthX + 2*FCGap + 2*WgWidth)

    O_TotLengthY = I_TotLengthY - InLengthY - FAGap

    if OutputIO == True:
        O = IQH_Device << IO_2D_3(
                        TotLengthX = O_InLengthX,
                        InLengthY  = O_TotLengthY,
                        MidLengthX = BendRadius, 
                        CouplingLengthY=LengthSRY, 
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
    
    if TaperOn:

        Coupler = LT_Taper(WgWidth = WgWidth)
        CPort   = "o1"
    
        C1 =  IQH_Device << Coupler
        C1.connect(C1.ports[CPort], I.ports["o1"])   
            
        C2 =  IQH_Device << Coupler
        C2.connect(C2.ports[CPort], I.ports["o2"])  
        
        if OutputIO ==- True:
            C3 =  IQH_Device << Coupler  
            C3.connect(C3.ports[CPort], O.ports["o1"])   
            
            C4 =  IQH_Device << Coupler
            C4.connect(C4.ports[CPort], O.ports["o2"])  
    
    # Label placed at block level (IQH_BlockLayout) using absolute IN port coords
    # — do NOT place label here inside @gf.cell; position would be in local/pre-move space

    ###########################################################################
    # Output Ports
    ###########################################################################

    IQH_Device.add_port(name="IN", port = I.ports["o1"])
    IQH_Device.add_port(name="TH", port = I.ports["o2"])
    
    if OutputIO == True:
        IQH_Device.add_port(name="DR", port = O.ports["o1"])
        IQH_Device.add_port(name="BS", port = O.ports["o2"])
        
    return IQH_Device