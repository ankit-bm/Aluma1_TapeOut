import gdsfactory as gf
import numpy as np
from AQH_Lattice_Rot import AQH_Lattice_Rot
from IO_AQH_1 import IO_AQH_1
from IO_AQH_2 import IO_AQH_2
from AL_Taper import AL_Taper
from AL_GratingCoupler import AL_GratingCoupler
from Straight import Straight
from Straight import Straight

###############################################################################
# Parameters
###############################################################################
@gf.cell(check_instances=False)
def AQH_Device_Rot( 
    Nx = 10, 
    Ny = 10, 
    BendRadius = 20,
    LengthSR   = 12,
    eta        = 0.11,
    WgWidth    = 1.0,
    Gap        = 0.5, 
    FCGap      = 0.6,
    InLengthX    = 200,
    TotLengthX   = 1500,
    BendRadiusIO = 20,
    FAGap       = 30,
    Euler       = 0,
    CouplerON   = 1, #1 - Taper, #2 GC 
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

    BufLength = 1
    
    Projection = np.cos(np.pi/4)
    
    LengthLR = LengthSR + eta
    
    Lattice =  Device << AQH_Lattice_Rot(Nx=Nx, Ny=Ny, Gap=Gap, BendRadius = BendRadius, LengthSR = LengthSR, eta = eta, WgWidth = WgWidth, Euler = Euler, Layer = Layer)
    
    LatticeLengthX = (Nx) * Projection * 2*(Gap + WgWidth + 2*BendRadius + LengthSR/2 + LengthLR/2) + 2*(WgWidth/2 + BendRadius + LengthLR/2)/Projection
    LatticeLengthY = (Ny) * Projection * 2*(Gap + WgWidth + 2*BendRadius + LengthSR/2 + LengthLR/2) + 2*(WgWidth/2 + BendRadius + LengthLR/2)/Projection 
        
    TotLengthX0 = TotLengthX - BufLength

    ###########################################################################
    # Input IO
    ###########################################################################
    
    InLengthY    = LatticeLengthY - (WgWidth/2 + BendRadius + LengthLR/2)/Projection
    I_TotLengthY = LatticeLengthY + 3*FAGap

    I = Device <<IO_AQH_1(TotLengthX = TotLengthX0,
                        TotLengthY = I_TotLengthY,
                        InLengthX  = InLengthX,
                        InLengthY  = InLengthY,
                        MidLengthX = BendRadius,
                        CouplingLength  = LengthSR,  
                        BendRadius   = BendRadiusIO,
                        WgWidth      = WgWidth,
                        Layer        = Layer)

    LatticeOffsetX  =  InLengthX + (FCGap + WgWidth + BendRadius + LengthSR/2)*np.cos(np.deg2rad(45))
    LatticeOffsetY  = -InLengthY - WgWidth/2 + (FCGap + WgWidth + BendRadius + LengthSR/2)*Projection
    Lattice.move((I.xmin + LatticeOffsetX, I.ymax + LatticeOffsetY))

    ###########################################################################
    # Output IO
    ###########################################################################

    O_InLengthX = TotLengthX0 - (InLengthX +  Projection*2*(LengthSR/2+BendRadius+FCGap+WgWidth) + Projection*(Nx-1)*2*(Gap + WgWidth + 2*BendRadius + LengthSR/2 + LengthLR/2)) 

    O_TotLengthY = I_TotLengthY - InLengthY - FAGap

    if OutputIO == True:
        O = Device << IO_AQH_2(
                        InLengthX  = O_InLengthX,
                        InLengthY  = O_TotLengthY,
                        CouplingLength=LengthSR, 
                        FAGap      = FAGap, 
                        BendRadius = BendRadiusIO,
                        WgWidth    = WgWidth,
                        Layer      = Layer)


        O.mirror_x(0)
        OutputIOOffsetX = O_InLengthX + InLengthX + LatticeLengthX + 2*FCGap + 2*WgWidth
        OutputIOOffsetY = FAGap + WgWidth/2

        O.move((I.xmin + TotLengthX0, I.ymin + OutputIOOffsetY))


    ###########################################################################
    # Create Buffer Straight Elements to Fix Grid Snapping Issues
    ###########################################################################
    BufThLength = I.xmax - I.xmin
    BufDrLength = O.ports["o1"].center[0] - I.xmin 
    BufBSLength = O.ports["o2"].center[0] - I.xmin 

    BF_TH  = Device << Straight(Length=BufLength + (TotLengthX0 - BufThLength), Width = WgWidth, Layer=Layer)
    BF_DR  = Device << Straight(Length=BufLength + (TotLengthX0 - BufDrLength), Width = WgWidth, Layer=Layer)
    BF_BS  = Device << Straight(Length=BufLength + (TotLengthX0 - BufBSLength), Width = WgWidth, Layer=Layer)

    BF_TH.connect(BF_TH.ports["o2"], I.ports["o2"])  
    BF_DR.connect(BF_DR.ports["o2"], O.ports["o1"])         
    BF_BS.connect(BF_BS.ports["o2"], O.ports["o2"])  
    
    ###########################################################################
    # Coupler
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

    ##########################################################################
    #Device Info
    ##########################################################################

    DID = Device << gf.components.text_rectangular(text = DeviceID, size = 1, layer = Layer)
    DID.move((I.xmin - LablePosX, I.ymax-LablePosY))
        
    return Device