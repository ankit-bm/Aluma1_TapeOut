# Die3.py
from encodings.punycode import T

import gdsfactory as gf
import numpy as np
import pandas as pd
from AFQH_Device import AFQH_Device
from AQH_CB_Device import AQH_CB_Device
from AQH_Device_Rot import AQH_Device_Rot
from OneD_Device import OneD_Device
from DirCoupler_Device import DirCoupler_Device
from IO2 import IO2
from IO3 import IO3

from AL_Layers import AL_Layers
from SurpentineLossWg import SurpentineLossWg

gf.gpdk.PDK.activate()

gf.CONF.max_cellname_length = 35


from AL_Die_Frame import AL_Die_Frame

from ADF_RIO import ADF_RIO
from APF_Pulley import APF_Pulley


###########################################################################################
# Device Configurations
###########################################################################################

ConfigFile        = "Device_Config_2D.xlsx"

###########################################################################################
# Die Outline and Frame
###########################################################################################

@gf.cell
def Die3(
    DieWidth = 4468,
    DieHeight = 20780,
    TaperLength = 400,
    FArrayGap = 50,
    Layer         = AL_Layers.CHS,
):
    D = gf.Component()

    DebugFrame = False

    if DebugFrame:
        die_outline = D << gf.components.rectangle(size=(DieWidth, DieHeight), layer=Layer)    

    xl = pd.ExcelFile("Device_Config_2D.xlsx")
    print(xl.sheet_names)
    
    TotLengthX_EC = DieWidth - 2*TaperLength + 10
    
    StartY = 630
    StartX = TaperLength-5
    
    #----------------------------------------------------------------------
    # IO Params
    #----------------------------------------------------------------------
    
    ECParamsList = [
        dict(Length=395, TaperType=1, MarkerOn=True),   # AQH_CB EC B1
        dict(Length=395, TaperType=2, MarkerOn=True),   # AQH_Rot EC B1
    ]

    GCParamsList = [
        dict(Pitch=0.716, DutyCycle=0.700, NPeriod=25, taper_length=15.0,
            taper_angle=40.0, fiber_angle=10.0, wavelength=1.55,
            LengthGC=100, UniformGrating=True),        # AQH_CB GC B1
        dict(Pitch=0.650, DutyCycle=0.680, NPeriod=25, taper_length=15.0,
            taper_angle=40.0, fiber_angle=10.0, wavelength=1.55,
            LengthGC=100, UniformGrating=True),        # AQH_Rot GC B1
    ]
    
    #----------------------------------------------------------------------
    # AQH_CB EC Block 1
    #----------------------------------------------------------------------

    AQH_CB_Config = pd.read_excel(ConfigFile, sheet_name="AQH_CB").dropna().reset_index(drop=True)
    print(AQH_CB_Config.index.tolist())

    NDevices  = 10
    NPerRow   = 5

    AQH_CB_EC_B1: dict = {}

    InLengthX0  = 100
    PeriodY     = 600
    PeriodVec   = [580, 630, 700, 670, 700, 
                580, 630, 700, 670,720,
                580, 630, 700, 670,720]

    StartY_CB_EC_B1 = StartY
    RowStartY       = StartY_CB_EC_B1
    RowOffset       = 0

    for j, row in AQH_CB_Config.head(NDevices).iterrows():
        RowIdx    = j % NPerRow
        RowOffset = RowIdx
        
        if j < NPerRow:
            ECParams = ECParamsList[0]
        else:
            ECParams = ECParamsList[1]
        AFQH_Period = PeriodVec[j]

        if (RowOffset+1) % 2 == 1:
            InLengthX = InLengthX0 + RowOffset*AFQH_Period
        else:
            InLengthX = TotLengthX_EC - (InLengthX0 + RowOffset*AFQH_Period) - AFQH_Period

        AQH_CB_EC_B1[f"D{j+1}"] = D << AQH_CB_Device(
            Nx           = int(row["Nx"]),
            Ny           = int(row["Ny"]),
            LengthSR     = float(row["LengthRing"]),
            eta          = 0.110,
            Gap          = float(row["Gap"]),
            FCGap        = float(row["FCGap"]),
            BendRadius   = float(row["BendRadius"]),
            WgWidth      = float(row["WgWidth"]),
            FAGap        = FArrayGap,
            InLengthX    = InLengthX,
            TotLengthX   = TotLengthX_EC,
            BendRadiusIO = float(row["BendRadiusIO"]),
            CouplerON    = 1,
            OutputIO     = True,
            Euler        = 1,
            LablePosX    = 80,
            LablePosY    = -18,
            Layer        = AL_Layers.X1P,
            LayerB       = AL_Layers.X1B,
            DeviceID     = f"AQH_CB EC B1 {j+1}",
            ECParams     = ECParams)

        if j == 0:
            AQH_CB_EC_B1[f"D{j+1}"].move((StartX, RowStartY))
        elif RowIdx == 0:
            RowStartY = AQH_CB_EC_B1[f"D{j}"].ports["IN"].center[1] + FArrayGap + PeriodY
            AQH_CB_EC_B1[f"D{j+1}"].move((StartX, RowStartY))
        elif (RowOffset+1) % 2 == 0:
            AQH_CB_EC_B1[f"D{j+1}"].mirror_x(0)
            AQH_CB_EC_B1[f"D{j+1}"].mirror_y(0)
            port_name = "DR" if "DR" in [p.name for p in AQH_CB_EC_B1[f"D{j}"].ports] else "TH"
            Y = AQH_CB_EC_B1[f"D{j}"].ports[port_name].center[1] + FArrayGap
            X = AQH_CB_EC_B1[f"D{j}"].ports[port_name].center[0]
            AQH_CB_EC_B1[f"D{j+1}"].move((X, Y))
        else:
            Y = AQH_CB_EC_B1[f"D{j}"].ports["TH"].center[1] + FArrayGap
            X = StartX
            AQH_CB_EC_B1[f"D{j+1}"].move((X, Y))
            
    #----------------------------------------------------------------------
    # AQH_CB GC Block 1
    #----------------------------------------------------------------------

    FArrayGap_GC = 50

    AQH_CB_GC_B1: dict = {}
    NDevices_GC  = 10
    NPerRow_GC   = 5

    InLengthX0_GC = 120
    PeriodY_GC    = 580

    PeriodVec_GC   = [580, 630, 710, 660, 710, 
                580, 630, 710, 660, 710,
                580, 630, 710, 660, 710]


    StartY_CB_GC_B1 = AQH_CB_EC_B1[f"D{NDevices}"].ports["IN"].center[1] + FArrayGap_GC + 600
    RowStartY_GC    = StartY_CB_GC_B1
    RowOffset_GC    = 0

    for j, row in AQH_CB_Config.head(NDevices_GC).iterrows():
        RowIdx_GC    = j % NPerRow_GC
        RowOffset_GC = RowIdx_GC
        
        if j < NPerRow:
            GCParams = GCParamsList[0]
        else:
            GCParams = GCParamsList[1]

        AFQH_Period = PeriodVec_GC[j]

        if (RowOffset_GC+1) % 2 == 1:
            InLengthX = InLengthX0_GC + RowOffset_GC*AFQH_Period
        else:
            InLengthX = TotLengthX_EC - (InLengthX0_GC + RowOffset_GC*AFQH_Period) - AFQH_Period

        AQH_CB_GC_B1[f"D{j+1}"] = D << AQH_CB_Device(
            Nx           = int(row["Nx"]),
            Ny           = int(row["Ny"]),
            LengthSR     = float(row["LengthRing"]),
            eta          = 0.110,
            Gap          = float(row["Gap"]),
            FCGap        = float(row["FCGap"]),
            BendRadius   = float(row["BendRadius"]),
            WgWidth      = float(row["WgWidth"]),
            FAGap        = FArrayGap_GC,
            InLengthX    = InLengthX,
            TotLengthX   = TotLengthX_EC,
            BendRadiusIO = float(row["BendRadiusIO"]),
            CouplerON    = 2,
            OutputIO     = True,
            Euler        = 1,
            LablePosX    = -100,
            LablePosY    = -18,
            Layer        = AL_Layers.X1P,
            LayerB       = AL_Layers.X1B,
            DeviceID     = f"AQH_CB GC B1 {j+1}",
            GCParams = GCParams)

        if j == 0:
            AQH_CB_GC_B1[f"D{j+1}"].move((StartX, RowStartY_GC))
        elif RowIdx_GC == 0:
            RowStartY_GC = AQH_CB_GC_B1[f"D{j}"].ports["IN"].center[1] + 1.5*FArrayGap_GC + PeriodY_GC
            AQH_CB_GC_B1[f"D{j+1}"].move((StartX, RowStartY_GC))
        elif (RowOffset_GC+1) % 2 == 0:
            AQH_CB_GC_B1[f"D{j+1}"].mirror_x(0)
            AQH_CB_GC_B1[f"D{j+1}"].mirror_y(0)
            port_name = "DR" if "DR" in [p.name for p in AQH_CB_GC_B1[f"D{j}"].ports] else "TH"
            Y = AQH_CB_GC_B1[f"D{j}"].ports[port_name].center[1] + FArrayGap_GC
            X = AQH_CB_GC_B1[f"D{j}"].ports[port_name].center[0]
            AQH_CB_GC_B1[f"D{j+1}"].move((X, Y))
        else:
            Y = AQH_CB_GC_B1[f"D{j}"].ports["TH"].center[1] + FArrayGap_GC
            X = StartX
            AQH_CB_GC_B1[f"D{j+1}"].move((X, Y))
    #----------------------------------------------------------------------
    # AQH_Rot EC Block 1
    #----------------------------------------------------------------------

    AQH_Rot_Config = pd.read_excel(ConfigFile, sheet_name="AQH_Rot").dropna().reset_index(drop=True)

    NDevices_Rot  = 12
    NPerRow_Rot   = 6

    AQH_Rot_EC_B1: dict = {}

    InLengthX0_Rot  = 130
    PeriodY_Rot     = 1260
    PeriodVec_Rot   = [500, 470, 580, 530, 580, 540, 
                    500, 470, 580, 530, 580, 540,
                    500, 470, 580, 530, 580, 540,]
    
    TotLengthX_EC_Rot = TotLengthX_EC + 1

    StartY_Rot_EC_B1 = 5000
    RowStartY_Rot    = StartY_Rot_EC_B1

    for j, row in AQH_Rot_Config.head(NDevices_Rot).iterrows():
        RowIdx_Rot    = j % NPerRow_Rot
        RowOffset_Rot = RowIdx_Rot
        
        if j < NPerRow:
            ECParams = ECParamsList[0]
        else:
            ECParams = ECParamsList[1]
        AFQH_Period = PeriodVec[j]
        
        AFQH_Period   = PeriodVec_Rot[j]

        if (RowOffset_Rot+1) % 2 == 1:
            InLengthX = InLengthX0_Rot + RowOffset_Rot*AFQH_Period
        else:
            InLengthX = TotLengthX_EC_Rot - (InLengthX0_Rot + RowOffset_Rot*AFQH_Period) - AFQH_Period

        AQH_Rot_EC_B1[f"D{j+1}"] = D << AQH_Device_Rot(
            Nx           = int(row["Nx"]),
            Ny           = int(row["Ny"]),
            LengthSR     = float(row["LengthRing"]),
            eta          = 0.110,
            Gap          = float(row["Gap"]),
            FCGap        = float(row["FCGap"]),
            BendRadius   = float(row["BendRadius"]),
            WgWidth      = float(row["WgWidth"]),
            FAGap        = FArrayGap,
            InLengthX    = InLengthX,
            TotLengthX   = TotLengthX_EC_Rot,
            BendRadiusIO = float(row["BendRadiusIO"]),
            CouplerON    = 1,
            OutputIO     = True,
            Euler        = 1,
            LablePosX    = 80,
            LablePosY    = -18,
            Layer        = AL_Layers.X1P,
            LayerB       = AL_Layers.X1B,
            DeviceID     = f"AQH_Rot EC B1 {j+1}",
            ECParams     = ECParams)

        if j == 0:
            AQH_Rot_EC_B1[f"D{j+1}"].move((StartX, RowStartY_Rot))
        elif RowIdx_Rot == 0:
            RowStartY_Rot = AQH_Rot_EC_B1[f"D{j}"].ports["IN"].center[1] + FArrayGap + PeriodY_Rot
            AQH_Rot_EC_B1[f"D{j+1}"].move((StartX, RowStartY_Rot))
        elif (RowOffset_Rot+1) % 2 == 0:
            AQH_Rot_EC_B1[f"D{j+1}"].mirror_x(0)
            AQH_Rot_EC_B1[f"D{j+1}"].mirror_y(0)
            port_name = "DR" if "DR" in [p.name for p in AQH_Rot_EC_B1[f"D{j}"].ports] else "TH"
            Y = AQH_Rot_EC_B1[f"D{j}"].ports[port_name].center[1] + FArrayGap
            X = AQH_Rot_EC_B1[f"D{j}"].ports[port_name].center[0]
            AQH_Rot_EC_B1[f"D{j+1}"].move((X, Y))
        else:
            Y = AQH_Rot_EC_B1[f"D{j}"].ports["TH"].center[1] + FArrayGap
            X = StartX
            AQH_Rot_EC_B1[f"D{j+1}"].move((X, Y))
            
    #----------------------------------------------------------------------
    # AQH_Rot GC Block 1
    #----------------------------------------------------------------------

    NDevices_Rot_GC  = 12
    NPerRow_Rot_GC   = 6

    AQH_Rot_GC_B1: dict = {}

    InLengthX0_Rot_GC  = 130
    PeriodY_Rot_GC     = 640
    FArrayGap_GC       = 50
    PeriodVec_Rot_GC   = [500, 470, 580, 530, 580, 540,
                            500, 470, 580, 530, 580, 540,
                            500, 470, 580, 530, 580, 540]

    TotLengthX_EC_Rot_GC = TotLengthX_EC + 1

    StartY_Rot_GC_B1 = AQH_Rot_EC_B1[f"D{NDevices_Rot}"].ports["IN"].center[1] + FArrayGap_GC + 1250
    RowStartY_Rot_GC = StartY_Rot_GC_B1

    for j, row in AQH_Rot_Config.head(NDevices_Rot_GC).iterrows():
        RowIdx_Rot_GC    = j % NPerRow_Rot_GC
        RowOffset_Rot_GC = RowIdx_Rot_GC
    
        if j < NPerRow:
            GCParams = GCParamsList[0]
        else:
            GCParams = GCParamsList[1]
        AFQH_Period      = PeriodVec_Rot_GC[j]

        if (RowOffset_Rot_GC+1) % 2 == 1:
            InLengthX = InLengthX0_Rot_GC + RowOffset_Rot_GC*AFQH_Period
        else:
            InLengthX = TotLengthX_EC_Rot_GC - (InLengthX0_Rot_GC + RowOffset_Rot_GC*AFQH_Period) - AFQH_Period

        AQH_Rot_GC_B1[f"D{j+1}"] = D << AQH_Device_Rot(
            Nx           = int(row["Nx"]),
            Ny           = int(row["Ny"]),
            LengthSR     = float(row["LengthRing"]),
            eta          = 0.110,
            Gap          = float(row["Gap"]),
            FCGap        = float(row["FCGap"]),
            BendRadius   = float(row["BendRadius"]),
            WgWidth      = float(row["WgWidth"]),
            FAGap        = FArrayGap_GC,
            InLengthX    = InLengthX,
            TotLengthX   = TotLengthX_EC_Rot_GC,
            BendRadiusIO = float(row["BendRadiusIO"]),
            CouplerON    = 2,
            OutputIO     = True,
            Euler        = 1,
            LablePosX    = -100,
            LablePosY    = -18,
            Layer        = AL_Layers.X1P,
            LayerB       = AL_Layers.X1B,
            DeviceID     = f"AQH_Rot GC B1 {j+1}",
            GCParams     = GCParams)

        if j == 0:
            AQH_Rot_GC_B1[f"D{j+1}"].move((StartX, RowStartY_Rot_GC))
        elif RowIdx_Rot_GC == 0:
            RowStartY_Rot_GC = AQH_Rot_GC_B1[f"D{j}"].ports["IN"].center[1] + FArrayGap_GC + 2*PeriodY_Rot_GC
            AQH_Rot_GC_B1[f"D{j+1}"].move((StartX, RowStartY_Rot_GC))
        elif (RowOffset_Rot_GC+1) % 2 == 0:
            AQH_Rot_GC_B1[f"D{j+1}"].mirror_x(0)
            AQH_Rot_GC_B1[f"D{j+1}"].mirror_y(0)
            port_name = "DR" if "DR" in [p.name for p in AQH_Rot_GC_B1[f"D{j}"].ports] else "TH"
            Y = AQH_Rot_GC_B1[f"D{j}"].ports[port_name].center[1] + FArrayGap_GC
            X = AQH_Rot_GC_B1[f"D{j}"].ports[port_name].center[0]
            AQH_Rot_GC_B1[f"D{j+1}"].move((X, Y))
        else:
            Y = AQH_Rot_GC_B1[f"D{j}"].ports["TH"].center[1] + FArrayGap_GC
            X = StartX
            AQH_Rot_GC_B1[f"D{j+1}"].move((X, Y))
            
    #----------------------------------------------------------------------
    # AFQH EC Block 1
    #----------------------------------------------------------------------

    AFQH_Config = pd.read_excel(ConfigFile, sheet_name="AFQH").dropna().reset_index(drop=True)

    NDevices_AFQH  = 18
    NPerRow_AFQH   = 6

    AFQH_EC_B1: dict = {}

    InLengthX0_AFQH  = 130
    PeriodY_AFQH     = 950
    PeriodVec_AFQH   = [500, 470, 580, 530, 580, 540,
                        500, 470, 580, 530, 580, 540,
                        500, 470, 580, 530, 580, 540]

    TotLengthX_EC_AFQH = TotLengthX_EC 

    StartY_AFQH_EC_B1 = AQH_Rot_EC_B1[f"D{NDevices_Rot}"].ports["IN"].center[1] + FArrayGap + 3570
    RowStartY_AFQH    = StartY_AFQH_EC_B1

    for j, row in AFQH_Config.head(NDevices_AFQH).iterrows():
        RowIdx_AFQH    = j % NPerRow_AFQH
        RowOffset_AFQH = RowIdx_AFQH
        
        if j < NPerRow:
            ECParams = ECParamsList[0]
        else:
            ECParams = ECParamsList[1]

        AFQH_Period    = PeriodVec_AFQH[j]

        if (RowOffset_AFQH+1) % 2 == 1:
            InLengthX = InLengthX0_AFQH + RowOffset_AFQH*AFQH_Period
        else:
            InLengthX = TotLengthX_EC_AFQH - (InLengthX0_AFQH + RowOffset_AFQH*AFQH_Period) - AFQH_Period

        AFQH_EC_B1[f"D{j+1}"] = D << AFQH_Device(
            Nx           = int(row["Nx"]),
            Ny           = int(row["Ny"]),
            LengthRing   = int(row["LengthRing"]),
            Gap          = float(row["Gap"]),
            FCGap        = float(row["FCGap"]),
            BendRadius   = float(row["BendRadius"]),
            WgWidth      = float(row["WgWidth"]),
            FAGap        = FArrayGap,
            InLengthX    = InLengthX,
            TotLengthX   = TotLengthX_EC_AFQH,
            BendRadiusIO = float(row["BendRadiusIO"]),
            CouplerON    = 1,
            CouplingM    = False,
            OutputIO     = True,
            Euler        = 1,
            LablePosX    = 80,
            LablePosY    = -18,
            Layer        = AL_Layers.X1P,
            LayerB       = AL_Layers.X1B,
            DeviceID     = f"AFQH EC B1 {j+1}",
            ECParams     = ECParams)

        if j == 0:
            AFQH_EC_B1[f"D{j+1}"].move((StartX, RowStartY_AFQH))
        elif RowIdx_AFQH == 0:
            RowStartY_AFQH = AFQH_EC_B1[f"D{j}"].ports["IN"].center[1] + FArrayGap + PeriodY_AFQH
            AFQH_EC_B1[f"D{j+1}"].move((StartX, RowStartY_AFQH))
        elif (RowOffset_AFQH+1) % 2 == 0:
            AFQH_EC_B1[f"D{j+1}"].mirror_x(0)
            AFQH_EC_B1[f"D{j+1}"].mirror_y(0)
            port_name = "DR" if "DR" in [p.name for p in AFQH_EC_B1[f"D{j}"].ports] else "TH"
            Y = AFQH_EC_B1[f"D{j}"].ports[port_name].center[1] + FArrayGap
            X = AFQH_EC_B1[f"D{j}"].ports[port_name].center[0]
            AFQH_EC_B1[f"D{j+1}"].move((X, Y))
        else:
            Y = AFQH_EC_B1[f"D{j}"].ports["TH"].center[1] + FArrayGap
            X = StartX
            AFQH_EC_B1[f"D{j+1}"].move((X, Y))
    
    #----------------------------------------------------------------------
    # AFQH GC Block 1
    #----------------------------------------------------------------------

    NDevices_AFQH_GC  = 12
    NPerRow_AFQH_GC   = 6

    AFQH_GC_B1: dict = {}

    InLengthX0_AFQH_GC  = 130
    PeriodY_AFQH_GC     = 950
    FArrayGap_AFQH_GC   = 50
    PeriodVec_AFQH_GC   = [500, 470, 580, 530, 580, 540,
                            500, 470, 580, 530, 580, 540,
                            500, 470, 580, 530, 580, 540]

    TotLengthX_GC_AFQH = TotLengthX_EC 

    StartY_AFQH_GC_B1 = AFQH_EC_B1[f"D{NDevices_AFQH}"].ports["IN"].center[1] + FArrayGap + 940
    RowStartY_AFQH_GC = StartY_AFQH_GC_B1

    for j, row in AFQH_Config.head(NDevices_AFQH_GC).iterrows():
        RowIdx_AFQH_GC    = j % NPerRow_AFQH_GC
        RowOffset_AFQH_GC = RowIdx_AFQH_GC
        
        if j < NPerRow:
            GCParams = GCParamsList[0]
        else:
            GCParams = GCParamsList[1]

        
        AFQH_Period       = PeriodVec_AFQH_GC[j]

        if (RowOffset_AFQH_GC+1) % 2 == 1:
            InLengthX = InLengthX0_AFQH_GC + RowOffset_AFQH_GC*AFQH_Period
        else:
            InLengthX = TotLengthX_GC_AFQH - (InLengthX0_AFQH_GC + RowOffset_AFQH_GC*AFQH_Period) - AFQH_Period

        AFQH_GC_B1[f"D{j+1}"] = D << AFQH_Device(
            Nx           = int(row["Nx"]),
            Ny           = int(row["Ny"]),
            LengthRing   = int(row["LengthRing"]),
            Gap          = float(row["Gap"]),
            FCGap        = float(row["FCGap"]),
            BendRadius   = float(row["BendRadius"]),
            WgWidth      = float(row["WgWidth"]),
            FAGap        = FArrayGap_AFQH_GC,
            InLengthX    = InLengthX,
            TotLengthX   = TotLengthX_GC_AFQH,
            BendRadiusIO = float(row["BendRadiusIO"]),
            CouplerON    = 2,
            CouplingM    = False,
            OutputIO     = True,
            Euler        = 1,
            LablePosX    = -100,
            LablePosY    = -18,
            Layer        = AL_Layers.X1P,
            LayerB       = AL_Layers.X1B,
            DeviceID     = f"AFQH GC B1 {j+1}",
            GCParams=GCParams)

        if j == 0:
            AFQH_GC_B1[f"D{j+1}"].move((StartX, RowStartY_AFQH_GC))
        elif RowIdx_AFQH_GC == 0:
            RowStartY_AFQH_GC = AFQH_GC_B1[f"D{j}"].ports["IN"].center[1] + FArrayGap_AFQH_GC + PeriodY_AFQH_GC
            AFQH_GC_B1[f"D{j+1}"].move((StartX, RowStartY_AFQH_GC))
        elif (RowOffset_AFQH_GC+1) % 2 == 0:
            AFQH_GC_B1[f"D{j+1}"].mirror_x(0)
            AFQH_GC_B1[f"D{j+1}"].mirror_y(0)
            port_name = "DR" if "DR" in [p.name for p in AFQH_GC_B1[f"D{j}"].ports] else "TH"
            Y = AFQH_GC_B1[f"D{j}"].ports[port_name].center[1] + FArrayGap_AFQH_GC
            X = AFQH_GC_B1[f"D{j}"].ports[port_name].center[0]
            AFQH_GC_B1[f"D{j+1}"].move((X, Y))
        else:
            Y = AFQH_GC_B1[f"D{j}"].ports["TH"].center[1] + FArrayGap_AFQH_GC
            X = StartX
            AFQH_GC_B1[f"D{j+1}"].move((X, Y))
            
    #----------------------------------------------------------------------
    # OneD EC Block 1
    #----------------------------------------------------------------------

    NDevices_1D  = 10
    NPerRow_1D   = 5
    FArrayGap_1D = 50

    OneD_EC_B1: dict = {}

    InLengthX0_1D  = 130
    PeriodY_1D     = 120
    PeriodVec_1D   = [350, 360, 500, 550,600,
                        350, 360, 500, 550,600]

    NxVec          = [2, 3, 4, 5, 6,
                    2, 3, 4, 5, 6,]

    TotLengthX_1D = TotLengthX_EC

    StartY_1D_EC_B1 = AFQH_GC_B1[f"D{NDevices_AFQH_GC}"].ports["IN"].center[1] + FArrayGap + 600
    RowStartY_1D    = StartY_1D_EC_B1

    for j in range(NDevices_1D):

        RowIdx_1D    = j % NPerRow_1D
        RowOffset_1D = RowIdx_1D

        if j < NPerRow_1D:
            ECParams = ECParamsList[0]
        else:
            ECParams = ECParamsList[1]

        Period_1D = PeriodVec_1D[j]

        if (RowOffset_1D+1) % 2 == 1:
            InLengthX = InLengthX0_1D + RowOffset_1D*Period_1D
        else:
            InLengthX = TotLengthX_1D - (InLengthX0_1D + RowOffset_1D*Period_1D) - Period_1D

        OneD_EC_B1[f"D{j+1}"] = D << OneD_Device(
            Nx           = NxVec[j],
            BendRadius   = 20,
            LengthX      = 12,
            LengthY      = 12,
            LengthXL     = 12.08,
            LengthYL     = 12.08,
            WgWidth      = 1.0,
            Gap          = 0.5,
            FCGap        = 0.6,
            FAGap        = FArrayGap_1D,
            InLengthX    = InLengthX,
            TotLengthX   = TotLengthX_1D,
            BendRadiusIO = 15,
            CouplerON    = 1,
            OutputIO     = True,
            Euler        = 1,
            LablePosX    = 80,
            LablePosY    = -18,
            Layer        = AL_Layers.X1P,
            LayerB       = AL_Layers.X1B,
            DeviceID     = f"1D EC B1 Nx{NxVec[j]}",
            ECParams     = ECParams)

        if j == 0:
            OneD_EC_B1[f"D{j+1}"].move((StartX, RowStartY_1D))
        elif RowIdx_1D == 0:
            RowStartY_1D = OneD_EC_B1[f"D{j}"].ports["IN"].center[1] + FArrayGap_1D + PeriodY_1D
            OneD_EC_B1[f"D{j+1}"].move((StartX, RowStartY_1D))
        elif (RowOffset_1D+1) % 2 == 0:
            OneD_EC_B1[f"D{j+1}"].mirror_x(0)
            OneD_EC_B1[f"D{j+1}"].mirror_y(0)
            port_name = "DR" if "DR" in [p.name for p in OneD_EC_B1[f"D{j}"].ports] else "TH"
            Y = OneD_EC_B1[f"D{j}"].ports[port_name].center[1] + FArrayGap_1D
            X = OneD_EC_B1[f"D{j}"].ports[port_name].center[0]
            OneD_EC_B1[f"D{j+1}"].move((X, Y))
        else:
            Y = OneD_EC_B1[f"D{j}"].ports["TH"].center[1] + FArrayGap_1D
            X = StartX
            OneD_EC_B1[f"D{j+1}"].move((X, Y))

    #----------------------------------------------------------------------
    # OneD GC Block 1
    #----------------------------------------------------------------------

    OneD_GC_B1: dict = {}

    InLengthX0_1D_GC  = 130
    PeriodY_1D_GC     = 140
    FArrayGap_1D_GC   = 50
    PeriodVec_1D_GC   = [350, 360, 500, 550,600,
                        350, 360, 500, 550,600]

    StartY_1D_GC_B1 = OneD_EC_B1[f"D{NDevices_1D}"].ports["IN"].center[1] + FArrayGap_1D + 150
    RowStartY_1D_GC = StartY_1D_GC_B1

    for j in range(NDevices_1D):
        RowIdx_1D_GC    = j % NPerRow_1D
        RowOffset_1D_GC = RowIdx_1D_GC

        if j < NPerRow_1D:
            GCParams = GCParamsList[0]
        else:
            GCParams = GCParamsList[1]

        Period_1D_GC = PeriodVec_1D_GC[j]

        if (RowOffset_1D_GC+1) % 2 == 1:
            InLengthX = InLengthX0_1D_GC + RowOffset_1D_GC*Period_1D_GC
        else:
            InLengthX = TotLengthX_1D - (InLengthX0_1D_GC + RowOffset_1D_GC*Period_1D_GC) - Period_1D_GC

        OneD_GC_B1[f"D{j+1}"] = D << OneD_Device(
            Nx           = NxVec[j],
            BendRadius   = 20,
            LengthX      = 12,
            LengthY      = 12,
            LengthXL     = 12.08,
            LengthYL     = 12.08,
            WgWidth      = 1.0,
            Gap          = 0.5,
            FCGap        = 0.6,
            FAGap        = FArrayGap_1D_GC,
            InLengthX    = InLengthX,
            TotLengthX   = TotLengthX_1D,
            BendRadiusIO = 15,
            CouplerON    = 2,
            OutputIO     = True,
            Euler        = 1,
            LablePosX    = -100,
            LablePosY    = -18,
            Layer        = AL_Layers.X1P,
            LayerB       = AL_Layers.X1B,
            DeviceID     = f"1D GC B1 Nx{NxVec[j]}",
            GCParams     = GCParams)

        if j == 0:
            OneD_GC_B1[f"D{j+1}"].move((StartX, RowStartY_1D_GC))
        elif RowIdx_1D_GC == 0:
            RowStartY_1D_GC = OneD_GC_B1[f"D{j}"].ports["IN"].center[1] + FArrayGap_1D_GC + PeriodY_1D_GC
            OneD_GC_B1[f"D{j+1}"].move((StartX, RowStartY_1D_GC))
        elif (RowOffset_1D_GC+1) % 2 == 0:
            OneD_GC_B1[f"D{j+1}"].mirror_x(0)
            OneD_GC_B1[f"D{j+1}"].mirror_y(0)
            port_name = "DR" if "DR" in [p.name for p in OneD_GC_B1[f"D{j}"].ports] else "TH"
            Y = OneD_GC_B1[f"D{j}"].ports[port_name].center[1] + FArrayGap_1D_GC
            X = OneD_GC_B1[f"D{j}"].ports[port_name].center[0]
            OneD_GC_B1[f"D{j+1}"].move((X, Y))
        else:
            Y = OneD_GC_B1[f"D{j}"].ports["TH"].center[1] + FArrayGap_1D_GC
            X = StartX
            OneD_GC_B1[f"D{j+1}"].move((X, Y))
    
    #----------------------------------------------------------------------
    # DirC EC Block 1
    #----------------------------------------------------------------------

    DirC_Config = pd.read_excel(ConfigFile, sheet_name="DirC").dropna().reset_index(drop=True)

    NDevices_DirC = len(DirC_Config)
    FArrayGap_DirC  = 127
    InLengthX_DirC  = 500

    DirC_EC_B1: dict = {}

    StartY_DirC_EC_B1 = OneD_GC_B1[f"D{NDevices_1D}"].ports["IN"].center[1] + 2*FArrayGap_DirC + 50

    for j, row in DirC_Config.head(NDevices_DirC).iterrows():
        DirC_EC_B1[f"D{j+1}"] = D << DirCoupler_Device(
            WgWidth        = float(row["WgWidth"]),
            Gap            = float(row["Gap"]),
            CouplingLength = float(row["CouplingLength"]),
            BendRadius     = 15,
            InLengthX      = InLengthX_DirC,
            FAGap          = FArrayGap_DirC,
            TaperOn        = True,
            Euler          = 1,
            LablePosX      = 80,
            LablePosY      = -18,
            IOOut          = 5,
            Layer          = AL_Layers.X1P,
            DeviceID       = f"DirC EC {row['Name']}",
            ECParams       = ECParamsList[0])

        if j == 0:
            DirC_EC_B1[f"D{j+1}"].move((StartX, StartY_DirC_EC_B1))
        else:
            Y = DirC_EC_B1[f"D{j}"].ymax + 2*FArrayGap_DirC + 30
            DirC_EC_B1[f"D{j+1}"].move((StartX, Y))
            
    #----------------------------------------------------------------------
    # DirC EC Block 2 (mirror of Block 1, right edge)
    #----------------------------------------------------------------------

    DirC_EC_B2: dict = {}

    for j, row in DirC_Config.head(NDevices_DirC).iterrows():
        DirC_EC_B2[f"D{j+1}"] = D << DirCoupler_Device(
            WgWidth        = float(row["WgWidth"]),
            Gap            = float(row["Gap"]),
            CouplingLength = float(row["CouplingLength"]),
            BendRadius     = 15,
            InLengthX      = InLengthX_DirC,
            FAGap          = FArrayGap_DirC,
            TaperOn        = True,
            Euler          = 1,
            LablePosX      = 80,
            LablePosY      = -18,
            IOOut          = 5,
            Layer          = AL_Layers.X1P,
            DeviceID       = f"DirC EC B2 {row['Name']}",
            ECParams       = ECParamsList[1])

        DirC_EC_B2[f"D{j+1}"].mirror_x(0)
        DirC_EC_B2[f"D{j+1}"].mirror_y(0)

        Y = DirC_EC_B1[f"D{j+1}"].ymin
        DirC_EC_B2[f"D{j+1}"].xmax = DieWidth 
        DirC_EC_B2[f"D{j+1}"].ymin = Y

    #----------------------------------------------------------------------
    # DirC GC Block 1
    #----------------------------------------------------------------------

    StartX_DirC_GC  = 1050
    DirC_GC_B1: dict = {}

    for j, row in DirC_Config.head(NDevices_DirC).iterrows():
        DirC_GC_B1[f"D{j+1}"] = D << DirCoupler_Device(
            WgWidth        = float(row["WgWidth"]),
            Gap            = float(row["Gap"]),
            CouplingLength = float(row["CouplingLength"]),
            BendRadius     = 15,
            InLengthX      = InLengthX_DirC,
            FAGap          = FArrayGap_DirC,
            TaperOn        = False,
            Euler          = 1,
            LablePosX      = 80,
            LablePosY      = -18,
            IOOut          = 5,
            Layer          = AL_Layers.X1P,
            DeviceID       = f"DirC GC {row['Name']}",
            GCParams       = GCParamsList[0])

        Y = DirC_EC_B1[f"D{j+1}"].ymin
        DirC_GC_B1[f"D{j+1}"].xmin = StartX_DirC_GC
        DirC_GC_B1[f"D{j+1}"].ymin = Y
    
    #----------------------------------------------------------------------
    # DirC GC Block 2
    #----------------------------------------------------------------------

    StartX_DirC_GC_B2 = 1900
    DirC_GC_B2: dict = {}

    for j, row in DirC_Config.head(NDevices_DirC).iterrows():
        DirC_GC_B2[f"D{j+1}"] = D << DirCoupler_Device(
            WgWidth        = float(row["WgWidth"]),
            Gap            = float(row["Gap"]),
            CouplingLength = float(row["CouplingLength"]),
            BendRadius     = 20,
            InLengthX      = InLengthX_DirC,
            FAGap          = FArrayGap_DirC,
            TaperOn        = False,
            Euler          = 1,
            LablePosX      = 80,
            LablePosY      = -18,
            IOOut          = 5,
            Layer          = AL_Layers.X1P,
            DeviceID       = f"DirC GC B2 {row['Name']}",
            GCParams       = GCParamsList[1])

        Y = DirC_EC_B1[f"D{j+1}"].ymin
        DirC_GC_B2[f"D{j+1}"].xmin = StartX_DirC_GC_B2
        DirC_GC_B2[f"D{j+1}"].ymin = Y
        
    #----------------------------------------------------------------------
    # DirC GC Block 3
    #----------------------------------------------------------------------

    StartX_DirC_GC_B3 = 2750
    DirC_GC_B3: dict = {}

    for j, row in DirC_Config.head(NDevices_DirC).iterrows():
        DirC_GC_B3[f"D{j+1}"] = D << DirCoupler_Device(
            WgWidth        = float(row["WgWidth"]),
            Gap            = float(row["Gap"]),
            CouplingLength = float(row["CouplingLength"]),
            BendRadius     = 20,
            InLengthX      = InLengthX_DirC,
            FAGap          = FArrayGap_DirC,
            TaperOn        = False,
            Euler          = 1,
            LablePosX      = 80,
            LablePosY      = -18,
            IOOut          = 5,
            Layer          = AL_Layers.X1P,
            DeviceID       = f"DirC GC B3 {row['Name']}",
            GCParams       = GCParamsList[0])

        Y = DirC_EC_B1[f"D{j+1}"].ymin
        DirC_GC_B3[f"D{j+1}"].xmin = StartX_DirC_GC_B3
        DirC_GC_B3[f"D{j+1}"].ymin = Y

    #------------------------------
    # Return
    #------------------------------

    return D

#------------------------------
# Test
#------------------------------
if __name__ == "__main__":
    c = Die3()
    c.write_gds("Die3_test3.gds")
    print("Written Die3_test3.gds")
    c.show()
    c.plot()
