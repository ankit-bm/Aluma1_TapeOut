import gdsfactory as gf

gf.clear_cache()


from AFQH_Device   import AFQH_Device

from AQH_Device_Rot    import AQH_Device_Rot
from AQH_Lattice_Rot import AQH_Lattice_Rot

from AFQH_Device   import AFQH_Device
from AQH_Device    import AQH_Device
from AQH_CB_Device import AQH_CB_Device
from IQH_Device    import IQH_Device
from ADF_RIO import ADF_RIO
from APF_Pulley import APF_Pulley
from OneD_Device import OneD_Device

#from DirCoupler import DirCoupler
from DirCoupler_Device import DirCoupler_Device

#from IO_AQH_2 import IO_AQH_2

#from IO_2D_3 import IO_2D_3

#from AQH_Device import AQH_Device
#from AQH_Lattice import AQH_Lattice
from APF_Modulated import APF_Modulated

gf.gpdk.PDK.activate()
 
Top = gf.Component()

#Device =  AQH_Device(Nx=10, Ny=10, Gap=0.5, BendRadius = 20, LengthSR = 12, LengthLR = 16, WgWidth  = 1.0, FCGap = 0.6,
# FAGap        = 127,
# InLengthX    = 150,
# TotLengthX   = 1300,
# BendRadiusIO = 20,

# Coupler     = 0,
# TaperLength = 50,
# TaperWidth  = 0.5,
# Euler = 1,
# Layer = (1,0))


# Device =  IO_AQH_2(TotLengthX  = 1000,
#         TotLengthY   = 500,
#         InLengthX    = 200,
#         InLengthY    = 400,
#         MidLengthX   = 20,
#         CouplingLength = 10,
#         BendRadius  = 30,
#         WgWidth     = 1.8,
#         Layer       = (3,0)
# )
    
    
# Device = IQH_Lattice(
#         Nx = 8, 
#         Ny = 8, 
#         BendRadius = 20,
#         LengthSRX  = 12,
#         LengthSRY  = 10,
#         eta        = 2,
#         alpha      = 2,
#         Gap        = 0.5, 
#         WgWidth    = 1.2, 
#         Euler      = 1,
#         Layer      = (2,0) )
    
    
# Device =  IO13(TotLengthX  = 1000,
#         TotLengthY   = 400,
#         InLengthX    = 400,
#         InLengthY    = 200,
#         CouplingLengthY = 20,
#         BendRadius  = 30,
#         WgWidth     = 1.8,
#         Layer       = (3,0)
# )
    

# Device = IO11(TotLengthX  = 300, 
#         InLengthY       = 250,
#         MidLengthX      = 100,
#         CouplingLengthY = 25,
#         IOSepration     = 50,
#         BendRadius      = 10,
#         WgWidth         = 1.8,
#         Layer           = (3,0)
# )


# Device = AFQH_Device( 
#     Nx          = 9,
#     Ny          = 9,
#     LengthRing  = 12,
#     BendRadius  = 20,
#     WgWidth     = 1.4,
#     Gap         = 0.25,    
#     FCGap       = 0.5,
#     FAGap       = 30,
#     InLengthX   = 200,
#     TotLengthX  = 1000,
#     BendRadiusIO = 20,
#     CouplingM    = False,
#     OutputIO     = True,
#     Euler        = 0,
#     TaperOn      = False,
#     Layer        = (2,0),
#     DeviceID     = "1"
    
# )

# Device =  OneD_Device( 
#     Nx=4, 
#     BendRadius = 20,
#     LengthX    = 12,
#     LengthY    = 12,
#     LengthXL   = 12,
#     LengthYL   = 12,
#     WgWidth    = 1.2,
#     Gap        = 0.5, 
#     FCGap      = 0.6,
    
#     FAGap        = 30,
#     InLengthX    = 200,
#     TotLengthX   = 1000,
#     BendRadiusIO = 25,
     
#     Euler       = 0,
    
#     Layer       = (2,0),
#     OCoupler    = 2,
#     DeviceID   = "2"
# )
    

# Device =  DirCoupler(
#         TotLengthX   = 150,
#         TotLengthY   = 100,
#         CouplingGap  = 0.2,
#         CouplingLength = 20,
#         BendRadius  = 20,
#         WgWidth     = 1.8,
#         Layer       = (3,0)
# )

# Device = AQH_Device_Rot( 
#     Nx = 10, 
#     Ny = 10, 
#     BendRadius = 20,
#     LengthSR   = 12,
#     eta        = 0.11,
#     WgWidth    = 1.0,
#     Gap        = 0.5, 
#     FCGap      = 0.2,
#     InLengthX    = 200,
#     TotLengthX   = 1800,
#     BendRadiusIO = 20,
#     FAGap       = 30,
#     Euler       = 0,
#     TaperOn     = False,
#     OutputIO    = True,
#     Layer       = (2,0),
#     DeviceID    = "1"
# )

# Device =  IO_2D_3(TotLengthX     = 300, 
#         InLengthY       = 250,
#         MidLengthX      = 100,
#         CouplingLengthY = 25,
#         FAGap           = 50,
#         BendRadius      = 10,
#         WgWidth         = 1.8,
#         Layer           = (3,0)
# )



# Device = AQH_Lattice_Rot(
#         Nx = 8, 
#         Ny = 8, 
#         BendRadius = 20,
#         LengthSR   = 12,
#         eta        = 0.110,
#         Gap        = 0.5, 
#         WgWidth    = 1.8, 
#         Euler      = 1,
#         Layer      = (2,0) )

#Device.rotate(45)
# Device = AQH_CB_Device( 
#     Nx = 10, 
#     Ny = 10, 
#     BendRadius = 20,
#     LengthSR   = 12,
#     eta        = 0.11,
#     WgWidth    = 1.0,
#     Gap        = 0.5, 
#     FCGap      = 0.6,
#     InLengthX    = 200,
#     TotLengthX   = 1800,
#     BendRadiusIO = 25,
#     FAGap       = 30,
#     Euler       = 0,
#     TaperOn     = False,
#     OutputIO    = True,
#     Layer       = (2,0),
#     DeviceID    = "1"
# )

# Device =  ADF_RIO( 
#     LengthRingX = 0,
#     LengthRingY = 0,
#     WgWidth     = 1.6,
#     WgWidthIO   = 1,
#     BendRadius  = 25,
#     BendRadiusIO = 20,
#     Gap          = 0.5,
#     FAGap        = 30,
#     InLengthX    = 200,
#     TotLengthX   = 500,
#     InIO         = 1,
#     OutIO        = 4,
#     TaperOn      = False,   # 1: Grating, 0: Edge
#     OutputIO     = True,
#     Euler        = 0,
#     Layer        = (2,0)
# )


# Device = APF_Pulley( 
#     BendRadius  = 25,
#     WgWidth     = 1.6,
#     WgWidthIO   = 1.0,
#     Gap         = 0.5,
#     ThetaC       = 40,
#     BendRadiusIO = 20,
#     InLengthX    = 200,
#     TotLengthX   = 500,
#     TaperOn      = False,   # 1: Grating, 0: Edg
#     Euler        = 0,    
#     Layer        = (2,0)
# )
    
    

# Device =  DirCoupler_Device( 
#         WgWidth        = 1.2,
#         Gap            = 0.5,
#         CouplingLength = 12,
#         BendRadius     = 20,
#         InLengthX      = 120,
#         TotLengthX     = 500,
#         FAGap        = 127,

#         TaperOn     = False,   # 1: Grating, 0: Edge
#         Euler       = 0,
        
#         Layer        = (2,0)
# )
    
# Device = Pulley(
#         Radius  = 50,
#         WgWidth = 1.0,
#         ThetaC  = 70,
#         BendRadius = 15.0,
#         Euler = 0,
#         Layer = (2, 0),
#     )
        
        
# Device =  IO4( 
#     LengthX    = 200,
#     LengthY    = 100,
#     FAGap      = 30,
#     BendRadius = 20,
#     WgWidth    = 1.0,
#     Layer      = (2,0)
# )


# Device = IO6( 
#     LengthX    = 100,
#     LengthY    = 10,
#     DY         = 70,
#     FAGap      = 50,
#     BendRadius = 10,
#     WgWidth    = 1.0,
#     Layer      = (3,0)
# )

# Device = IQH_Device( 
#     Nx = 10, 
#     Ny = 10, 
#     BendRadius  = 20,
#     LengthSRX   = 12,
#     LengthSRY   = 10,
#     eta         = 0.08,
#     alpha       = 0.08,
#     WgWidth     = 1.0,
#     Gap         = 0.5, 
#     FCGap       = 0.6,
#     InLengthX    = 200,
#     TotLengthX   = 1800,
#     BendRadiusIO = 25,
#     FAGap        = 30,
#     Euler        = 0,
#     TaperOn      = False,
#     OutputIO     = True,
#     Layer        = (2,0),
#     DeviceID     = "1"
# )

# Device =  AQH_CB_Lattice(
#        Nx = 8, 
#        Ny = 8, 
#        BendRadius = 20,
#        LengthSR   = 12,
#        LengthLR   = 24,
#        Gap        = 0.5, 
#        WgWidth    = 1.8, 
#        Euler      = 1,
#        Layer      = (2,0) )


# Device = IQH_Device_Bot( 
#     Nx          = 8,
#     Ny          = 8,
#     LengthSRX   = 12,
#     LengthSRY   = 10,
#     eta         = 0.08,
#     alpha       = 0.08,
#     Gap         = 0.5,
    
#     WgWidth     = 1.2,
#     BendRadius  = 20,

#     FCGap       = 0.5,
#     FAGap       = 20,
#     InLengthX   = 200,
#     TotLengthX  = 1000,
#     BendRadiusIO = 20,
#     IOSepration  = 30,

#     IOFlip     = True,
    
#     Euler        = 0,

#     TaperOn      = False,

#     Layer        = (2,0),
#     DeviceID     = "1"
    
# )
    

# Device =  AQH_CB_Device_Bot( 
#     Nx          = 8,
#     Ny          = 8,
#     LengthSR    = 12,
#     LengthLR    = 10,
#     Gap         = 0.5,
    
#     WgWidth     = 1.2,
#     BendRadius  = 20,

#     FCGap       = 0.5,
#     FAGap       = 20,
#     InLengthX   = 100,
#     TotLengthX  = 300,
#     BendRadiusIO = 20,
#     IOSepration  = 30,

#     IOFlip     = True,
    
#     Euler        = 0,

#     TaperOn      = False,

#     Layer        = (2,0),
#     DeviceID     = "1"
    
# )
    
# Device =  AQH_Lattice_Rot(
#         Nx = 8, 
#         Ny = 8, 
#         BendRadius = 20,
#         LengthSR   = 12,
#         eta        = 0.110,
#         Gap        = 0.5, 
#         WgWidth    = 1.8, 
#         Euler      = 1,
#         Layer      = (2,0) )
    
# Device = AQH_Lattice_2(
#         Ny=8, 
#         Nx=8, 
#         BendRadius = 10,
#         LengthX    = 12,
#         LengthY    = 12,
#         LengthXL   = 12.08,
#         LengthYL   = 12.08,
#         Gap        = 0.5, 
#         WgWidth    = 0.5, 
#         Euler      = 0,
#         Layer      = (2,0) )


Device =  APF_Modulated(NPoints = 360*12, WgWidth = 1.2, WgWidthIO = 1.0, Gap = 0.3, BendRadius = 50.0, BendRadiusIO = 20, Modulation = True, ModPeriod = (358, 362), DW = (0.01, 0.02), FlipRing = True, 
                            InLengthX = 100, FAGap = 200, TaperOn = False, Layer = (2,0), DeviceID = "" )
      


Device_Ref = Top << Device


Top.write_gds("APF_M_R50_M358_362_DW020_G300.gds")
Top.plot()
Top.show()