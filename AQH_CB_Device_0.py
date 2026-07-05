import gdsfactory as gf

from AQH_CB_Lattice import AQH_CB_Lattice
from IO_2D_1 import IO_2D_1
from IO_2D_3 import IO_2D_3
from LT_Taper import LT_Taper

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
    TaperOn     = False,
    OutputIO    = True,
    
    Layer       = (2,0),
    DeviceID    = "1"
):

    Device = gf.Component()
    
    LengthLR = LengthSR + eta
    
    Lattice =  Device << AQH_CB_Lattice(Nx=Nx, Ny=Ny, Gap=Gap, BendRadius = BendRadius, LengthSR = LengthSR, eta = eta, WgWidth = WgWidth, Euler = Euler, Layer = Layer)


    LatticeLengthX = (Nx-1) * 2*(Gap + WgWidth + 2*BendRadius + LengthSR/2 + LengthLR/2) + 2*(LengthSR/2 + BendRadius)

    LatticeLengthY = (Ny-2) * 2*(Gap + WgWidth + 2*BendRadius + LengthSR/2 + LengthLR/2) + 2*(LengthSR/2 + BendRadius)

    ###########################################################################
    # Input IO
    ###########################################################################
    
    InLengthY    = LatticeLengthY - (BendRadius + LengthSR/2)
    I_TotLengthY = InLengthY + (LengthSR/2 + 3*BendRadiusIO) + FAGap
   

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
    
    if TaperOn:

        Coupler = LT_Taper(WgWidth = WgWidth)
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
    
    
    ###########################################################################
    # ports
    ###########################################################################
   
    Device.add_port(name="IN", port = I.ports["o1"])
    Device.add_port(name="TH", port = I.ports["o2"])
    
    if OutputIO == True:
       Device.add_port(name="BS", port = O.ports["o1"])
       Device.add_port(name="DR", port = O.ports["o2"])


    ###########################################################################
    # Device Info
    ###########################################################################

    # DID = Device << gf.components.text(text = DeviceID, size = 10, layer = Layer)
    # DID.move((I.xmin + 25, I.ymin+25))



    return Device