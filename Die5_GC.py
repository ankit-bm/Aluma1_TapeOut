# Die5_GC.py
import gdsfactory as gf
import numpy as np
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

@gf.cell
def Die5(
    DieWidth = 3468,
    DieHeight = 20780,
    TotLengthX_GC = 1000,
    InLengthX0    = 180,
    BendRadius    = 25,
    WgWidth       = 0.6,
    FArrayGap     = 2*127,
    Layer         = AL_Layers.CHS,
):
    D = gf.Component()
    StartY = DieHeight - 40
    StartX = 50 # grating coupler head 

    die_outline = D << gf.components.rectangle(
                    size=(DieWidth, DieHeight),
                    layer=Layer
                )
    
    FArrayGap_2 = 40
    
    #----------------------------------------------------------------------
    # Serpentine Loss Wg GC
    #----------------------------------------------------------------------

    TotLengthX_SLW = DieWidth - 168
    SLW_GapY       = 40
    N_LossWg = 11
    SLW_GC: dict   = {}

    for i in range(N_LossWg):
        Length = TotLengthX_SLW - i * 300

        SLW_GC[f"D{i+1}"] = D << SurpentineLossWg(
            WgWidth      = WgWidth,
            TotLengthX   = Length,
            InLengthX    = Length,
            NCurves      = 0,
            OutIOOn      = False,
            BendRadiusIO = BendRadius,
            DeviceID     = f"L {Length:.0f}",
            TaperOn      = False,
            Layer        = AL_Layers.X1P)

        SLW_GC[f"D{i+1}"].xmin = StartX
        if i == 0:
            SLW_GC[f"D{i+1}"].ymin = StartY
        else:
            SLW_GC[f"D{i+1}"].ymin = SLW_GC[f"D{i}"].ymin - SLW_GapY

    #----------------------------------------------------------------------
    # AFQH Block 1
    #----------------------------------------------------------------------
    
    AFQH_GC_B1: dict = {}
    
    AFQH_NDevices_1 = 4
    AFQH_NxVec_1  = np.array([7, 7,  7,  7])
    AFQH_NyVec_1  = np.array([7, 7,  7,  7])
    LRingVec_1    = np.array([20, 20, 30, 30])
    GapVec_1      = np.array([0.30, 0.30, 0.30, 0.30])
    FCGapVec_1    = np.array([0.50, 0.65, 0.55, 0.65])
    
    StartY_B1 = StartY - N_LossWg*SLW_GapY -330

    for j in range(AFQH_NDevices_1):
        AFQH_GC_B1[f"D{j+1}"] = D << AFQH_Device(
            Nx=AFQH_NxVec_1[j], Ny=AFQH_NyVec_1[j],
            LengthRing=int(LRingVec_1[j]), Gap=GapVec_1[j],
            FCGap=FCGapVec_1[j], BendRadius=BendRadius,
            WgWidth=WgWidth, FAGap=FArrayGap,
            InLengthX=InLengthX0, TotLengthX=TotLengthX_GC,
            BendRadiusIO=BendRadius, CouplerON=3,
            CouplingM=False, OutputIO=True, Euler=1,
            LablePosX=0, LablePosY=-50,
            Layer=AL_Layers.X1P, LayerB=AL_Layers.X1B,
            DeviceID=f"AFQH B1 {j+1}")

        if (j+1) % 2 == 0:
            AFQH_GC_B1[f"D{j+1}"].mirror_y(0)

        if j == 0:
            AFQH_GC_B1[f"D{j+1}"].move((StartX, StartY_B1))
        else:
            AFQH_GC_B1[f"D{j+1}"].ymin = StartY_B1 - FArrayGap
            AFQH_GC_B1[f"D{j+1}"].xmin = AFQH_GC_B1[f"D{j}"].ports["DR"].center[0] - InLengthX0 + 1.5*BendRadius

    #----------------------------------------------------------------------
    # AFQH Block 2 (9x9)
    #----------------------------------------------------------------------

    AFQH_GC_B2: dict = {}

    AFQH_NDevices_2 = 3
    AFQH_NxVec_2  = np.array([9, 9,  9,  5])
    AFQH_NyVec_2  = np.array([9, 9,  9,  5])
    LRingVec_2    = np.array([20, 20, 30, 30])
    GapVec_2      = np.array([0.30, 0.30, 0.30, 0.30])
    FCGapVec_2    = np.array([0.50, 0.65, 0.55, 0.65])

    # StartY_B2 = AFQH_GC_B1[f"D{AFQH_NDevices_1}"].ymin - FArrayGap
    StartY_B2 = StartY_B1 - 900
    
    for j in range(AFQH_NDevices_2):
        AFQH_GC_B2[f"D{j+1}"] = D << AFQH_Device(
            Nx=AFQH_NxVec_2[j], Ny=AFQH_NyVec_2[j],
            LengthRing=int(LRingVec_2[j]), Gap=GapVec_2[j],
            FCGap=FCGapVec_2[j], BendRadius=BendRadius,
            WgWidth=WgWidth, FAGap=FArrayGap,
            InLengthX=InLengthX0, TotLengthX=TotLengthX_GC,
            BendRadiusIO=BendRadius, CouplerON=3,
            CouplingM=False, OutputIO=True, Euler=1,
            LablePosX=0, LablePosY=-50,
            Layer=AL_Layers.X1P, LayerB=AL_Layers.X1B,
            DeviceID=f"AFQH B2 {j+1}")

        if (j+1) % 2 == 0:
            AFQH_GC_B2[f"D{j+1}"].mirror_y(0)

        if j == 0:
            AFQH_GC_B2[f"D{j+1}"].move((StartX, StartY_B2))
        else:
            AFQH_GC_B2[f"D{j+1}"].ymin = StartY_B2 - FArrayGap
            AFQH_GC_B2[f"D{j+1}"].xmin = AFQH_GC_B2[f"D{j}"].ports["DR"].center[0] - InLengthX0 + 1.5*BendRadius

    #----------------------------------------------------------------------
    # AFQH Block 3 (5x5)
    #----------------------------------------------------------------------

    AFQH_GC_B3: dict = {}

    AFQH_NDevices_3 = 5
    AFQH_NxVec_3  = np.array([5, 5, 5, 5,5])
    AFQH_NyVec_3  = np.array([5, 5, 5, 5,5])
    LRingVec_3    = np.array([20, 30, 20, 30, 20])
    GapVec_3      = np.array([0.30, 0.30, 0.30, 0.30, 0.30])
    FCGapVec_3    = np.array([0.50, 0.65, 0.55, 0.65, 0.65])

    StartY_B3 = StartY_B2 - 600

    for j in range(AFQH_NDevices_3):
        AFQH_GC_B3[f"D{j+1}"] = D << AFQH_Device(
            Nx=AFQH_NxVec_3[j], Ny=AFQH_NyVec_3[j],
            LengthRing=int(LRingVec_3[j]), Gap=GapVec_3[j],
            FCGap=FCGapVec_3[j], BendRadius=BendRadius,
            WgWidth=WgWidth, FAGap=FArrayGap,
            InLengthX=InLengthX0, TotLengthX=TotLengthX_GC,
            BendRadiusIO=BendRadius, CouplerON=3,
            CouplingM=False, OutputIO=True, Euler=1,
            LablePosX=0, LablePosY=-50,
            Layer=AL_Layers.X1P, LayerB=AL_Layers.X1B,
            DeviceID=f"AFQH B3 {j+1}")

        if (j+1) % 2 == 0:
            AFQH_GC_B3[f"D{j+1}"].mirror_y(0)

        if j == 0:
            AFQH_GC_B3[f"D{j+1}"].move((StartX, StartY_B3))
        elif (j+1) % 2 == 0:
            AFQH_GC_B3[f"D{j+1}"].ymin = StartY_B3 - 200
            AFQH_GC_B3[f"D{j+1}"].xmin = AFQH_GC_B3[f"D{j}"].ports["DR"].center[0] - InLengthX0 + 1.5*BendRadius
        else:
            AFQH_GC_B3[f"D{j+1}"].ymin = StartY_B3 -275 
            AFQH_GC_B3[f"D{j+1}"].xmin = AFQH_GC_B3[f"D{j}"].ports["DR"].center[0] - InLengthX0 + 1.5*BendRadius

        #----------------------------------------------------------------------
        # AFQH Block 4 (CouplerON=2)
        #----------------------------------------------------------------------

        AFQH_GC_B4: dict = {}
        
        InLengthX0 = 150
        TotLengthX_GC = 900

        AFQH_NDevices_4 = 4
        AFQH_NxVec_4  = np.array([7, 7, 7, 7])
        AFQH_NyVec_4  = np.array([7, 7, 7, 7])
        LRingVec_4    = np.array([20, 30, 20, 30])
        GapVec_4      = np.array([0.30, 0.30, 0.30, 0.30])
        FCGapVec_4    = np.array([0.50, 0.65, 0.55, 0.65])

        StartY_B4 = StartY_B3 - 600

        for j in range(AFQH_NDevices_4):
            AFQH_GC_B4[f"D{j+1}"] = D << AFQH_Device(
                Nx=AFQH_NxVec_4[j], Ny=AFQH_NyVec_4[j],
                LengthRing=int(LRingVec_4[j]), Gap=GapVec_4[j],
                FCGap=FCGapVec_4[j], BendRadius=BendRadius,
                WgWidth=WgWidth, FAGap=FArrayGap_2,
                InLengthX=InLengthX0, TotLengthX=TotLengthX_GC,
                BendRadiusIO=BendRadius, CouplerON=2,
                CouplingM=False, OutputIO=True, Euler=1,
                LablePosX=0, LablePosY=-50,
                Layer=AL_Layers.X1P, LayerB=AL_Layers.X1B,
                DeviceID=f"AFQH B4 {j+1}")
            
            if j == 0:
                AFQH_GC_B4[f"D{j+1}"].move((StartX, StartY_B4))
            elif (j+1) % 2 == 0:
                AFQH_GC_B4[f"D{j+1}"].mirror_y(0)   # mirror first
                AFQH_GC_B4[f"D{j+1}"].ymin = StartY_B4 - 440
                AFQH_GC_B4[f"D{j+1}"].xmin = AFQH_GC_B4[f"D{j}"].ports["DR"].center[0] - InLengthX0 + 0.0*BendRadius
            else:
                AFQH_GC_B4[f"D{j+1}"].ymin = StartY_B4 - 620
                AFQH_GC_B4[f"D{j+1}"].xmin = AFQH_GC_B4[f"D{j}"].ports["DR"].center[0] - InLengthX0 + 0.0*BendRadius
                
        #----------------------------------------------------------------------
        # AFQH Block 5 (9x9)
        #----------------------------------------------------------------------

        AFQH_GC_B5: dict = {}
        
        TotLengthX_GC = 1100

        AFQH_NDevices_5 = 3
        AFQH_NxVec_5  = np.array([9, 9, 9,])
        AFQH_NyVec_5  = np.array([9, 9, 9, ])
        LRingVec_5    = np.array([20, 20, 30, 30])
        GapVec_5      = np.array([0.30, 0.30, 0.30, 0.30])
        FCGapVec_5    = np.array([0.50, 0.65, 0.55, 0.65])

        StartY_B5 = StartY_B4 - 1000

        for j in range(AFQH_NDevices_5):
            AFQH_GC_B5[f"D{j+1}"] = D << AFQH_Device(
                Nx=AFQH_NxVec_5[j], Ny=AFQH_NyVec_5[j],
                LengthRing=int(LRingVec_5[j]), Gap=GapVec_5[j],
                FCGap=FCGapVec_5[j], BendRadius=BendRadius,
                WgWidth=WgWidth, FAGap=FArrayGap_2,
                InLengthX=InLengthX0, TotLengthX=TotLengthX_GC,
                BendRadiusIO=BendRadius, CouplerON=2,
                CouplingM=False, OutputIO=True, Euler=1,
                LablePosX=0, LablePosY=-50,
                Layer=AL_Layers.X1P, LayerB=AL_Layers.X1B,
                DeviceID=f"AFQH B5 {j+1}")

            if j == 0:
                AFQH_GC_B5[f"D{j+1}"].move((StartX, StartY_B5))
            elif (j+1) % 2 == 0:
                AFQH_GC_B5[f"D{j+1}"].mirror_y(0)
                AFQH_GC_B5[f"D{j+1}"].ymin = StartY_B5 - 500
                AFQH_GC_B5[f"D{j+1}"].xmin = AFQH_GC_B5[f"D{j}"].ports["DR"].center[0] - 1*InLengthX0 - 3.0*BendRadius
            else:
                AFQH_GC_B5[f"D{j+1}"].ymin = StartY_B5 - 770
                AFQH_GC_B5[f"D{j+1}"].xmin = AFQH_GC_B5[f"D{j}"].ports["DR"].center[0] - 1*InLengthX0 - 3.0*BendRadius
                
        #----------------------------------------------------------------------
        # AFQH Block 6 (5x5)
        #----------------------------------------------------------------------

        AFQH_GC_B6: dict = {}
        
        TotLengthX_GC = 700

        AFQH_NDevices_6 = 5
        AFQH_NxVec_6  = np.array([5, 5, 5, 5,5])
        AFQH_NyVec_6  = np.array([5, 5, 5, 5,5])
        LRingVec_6    = np.array([20, 30, 20, 30,20])
        GapVec_6      = np.array([0.30, 0.30, 0.30, 0.30,0.30])
        FCGapVec_6    = np.array([0.50, 0.65, 0.55, 0.65,0.55])

        StartY_B6 = StartY_B5 - 1100

        for j in range(AFQH_NDevices_6):
            AFQH_GC_B6[f"D{j+1}"] = D << AFQH_Device(
                Nx=AFQH_NxVec_6[j], Ny=AFQH_NyVec_6[j],
                LengthRing=int(LRingVec_6[j]), Gap=GapVec_6[j],
                FCGap=FCGapVec_6[j], BendRadius=BendRadius,
                WgWidth=WgWidth, FAGap=FArrayGap_2,
                InLengthX=InLengthX0, TotLengthX=TotLengthX_GC,
                BendRadiusIO=BendRadius, CouplerON=2,
                CouplingM=False, OutputIO=True, Euler=1,
                LablePosX=0, LablePosY=-50,
                Layer=AL_Layers.X1P, LayerB=AL_Layers.X1B,
                DeviceID=f"AFQH B6 {j+1}")

            if j == 0:
                AFQH_GC_B6[f"D{j+1}"].move((StartX, StartY_B6))
            elif (j+1) % 2 == 0:
                AFQH_GC_B6[f"D{j+1}"].mirror_y(0)
                AFQH_GC_B6[f"D{j+1}"].ymin = StartY_B6 - 300
                AFQH_GC_B6[f"D{j+1}"].xmin = AFQH_GC_B6[f"D{j}"].ports["DR"].center[0] - InLengthX0 + 2.0*BendRadius
            else:
                AFQH_GC_B6[f"D{j+1}"].ymin = StartY_B6 - 500
                AFQH_GC_B6[f"D{j+1}"].xmin = AFQH_GC_B6[f"D{j}"].ports["DR"].center[0] - InLengthX0 + 2.0*BendRadius
        
        #----------------------------------------------------------------------
        # Serpentine Loss Wg GC #2
        #----------------------------------------------------------------------
        
        TotLengthX = DieWidth - 168
        MidLengthX = TotLengthX
        InLengthX  = MidLengthX
        
        StartY_SLW_GC_2 = StartY_B6 - 525

        SLW_GC["D2"] = D << SurpentineLossWg(WgWidth=WgWidth,TotLengthX=TotLengthX, MidLengthX=MidLengthX,
                                            InLengthX=InLengthX, BendRadiusIO=BendRadius,DeviceID=f"L {3*TotLengthX} + 2pi x R")
        SLW_GC["D2"].move((StartX, StartY_SLW_GC_2))
        
        #----------------------------------------------------------------------
        # AQH_CB Block 1
        #----------------------------------------------------------------------

        AQH_CB_B1: dict = {}

        AQH_CB_NDevices_1 = 3
        AQH_CB_NxVec_1   = np.array([7, 7, 5, 7])
        AQH_CB_NyVec_1   = np.array([7, 7, 7, 7])
        LengthSRVec_CB1  = np.array([20, 30, 20, 30])
        GapVec_CB1       = np.array([0.30, 0.30, 0.30, 0.30])
        FCGapVec_CB1     = np.array([0.50, 0.65, 0.55, 0.65])
        eta              = 0.110

        StartY_CB1 = StartY_SLW_GC_2 - 830

        for j in range(AQH_CB_NDevices_1):
            AQH_CB_B1[f"D{j+1}"] = D << AQH_CB_Device(
                Nx=AQH_CB_NxVec_1[j], Ny=AQH_CB_NyVec_1[j],
                LengthSR=float(LengthSRVec_CB1[j]), eta=eta,
                Gap=GapVec_CB1[j], FCGap=FCGapVec_CB1[j],
                BendRadius=BendRadius, WgWidth=WgWidth,
                FAGap=FArrayGap, InLengthX=InLengthX0, TotLengthX=TotLengthX_GC,
                BendRadiusIO=BendRadius, CouplerON=3,
                OutputIO=True, Euler=1,
                LablePosX=0, LablePosY=-50,
                Layer=AL_Layers.X1P, LayerB=AL_Layers.X1B,
                DeviceID=f"AQH_CB B1 {j+1}")

            if j == 0:
                AQH_CB_B1[f"D{j+1}"].move((StartX, StartY_CB1))
            elif (j+1) % 2 == 0:
                AQH_CB_B1[f"D{j+1}"].mirror_y(0)
                AQH_CB_B1[f"D{j+1}"].ymin = StartY_CB1 - 440
                AQH_CB_B1[f"D{j+1}"].xmin = AQH_CB_B1[f"D{j}"].ports["DR"].center[0] - InLengthX0 + 2.0*BendRadius
            else:
                AQH_CB_B1[f"D{j+1}"].ymin = StartY_CB1 - 800
                AQH_CB_B1[f"D{j+1}"].xmin = AQH_CB_B1[f"D{j}"].ports["DR"].center[0] - InLengthX0 - 2.25*BendRadius

        #----------------------------------------------------------------------
        # AQH_CB Block 2
        #----------------------------------------------------------------------

        AQH_CB_B2: dict = {}

        AQH_CB_NDevices_2 = 3
        AQH_CB_NxVec_2   = np.array([5, 5, 5, 7])
        AQH_CB_NyVec_2   = np.array([5, 5, 5, 7])
        LengthSRVec_CB2  = np.array([20, 30, 20, 30])
        GapVec_CB2       = np.array([0.30, 0.30, 0.30, 0.30])
        FCGapVec_CB2     = np.array([0.50, 0.65, 0.55, 0.65])

        StartY_CB2 = StartY_CB1 - 800

        for j in range(AQH_CB_NDevices_2):
            AQH_CB_B2[f"D{j+1}"] = D << AQH_CB_Device(
                Nx=AQH_CB_NxVec_2[j], Ny=AQH_CB_NyVec_2[j],
                LengthSR=float(LengthSRVec_CB2[j]), eta=eta,
                Gap=GapVec_CB2[j], FCGap=FCGapVec_CB2[j],
                BendRadius=BendRadius, WgWidth=WgWidth,
                FAGap=FArrayGap, InLengthX=InLengthX0, TotLengthX=TotLengthX_GC,
                BendRadiusIO=BendRadius, CouplerON=3,
                OutputIO=True, Euler=1,
                LablePosX=0, LablePosY=-50,
                Layer=AL_Layers.X1P, LayerB=AL_Layers.X1B,
                DeviceID=f"AQH_CB B2 {j+1}")

            if j == 0:
                AQH_CB_B2[f"D{j+1}"].move((StartX, StartY_CB2))
            elif (j+1) % 2 == 0:
                AQH_CB_B2[f"D{j+1}"].mirror_y(0)
                AQH_CB_B2[f"D{j+1}"].ymin = StartY_CB2 - 440
                AQH_CB_B2[f"D{j+1}"].xmin = AQH_CB_B2[f"D{j}"].ports["DR"].center[0] - InLengthX0 + 2.0*BendRadius
            else:
                AQH_CB_B2[f"D{j+1}"].ymin = StartY_CB2 - 800
                AQH_CB_B2[f"D{j+1}"].xmin = AQH_CB_B2[f"D{j}"].ports["DR"].center[0] - InLengthX0 - 2.25*BendRadius

        #----------------------------------------------------------------------
        # AQH_CB Block 3 (CouplerON=2)
        #----------------------------------------------------------------------

        AQH_CB_B3: dict = {}

        AQH_CB_NDevices_3 = 2
        AQH_CB_NxVec_3   = np.array([7, 7, 5, 7])
        AQH_CB_NyVec_3   = np.array([7, 7, 5, 7])
        LengthSRVec_CB3  = np.array([20, 30, 20, 30])
        GapVec_CB3       = np.array([0.30, 0.30, 0.30, 0.30])
        FCGapVec_CB3     = np.array([0.50, 0.65, 0.55, 0.65])

        StartY_CB3   = StartY_CB2 - 1200
        TotLengthX_GC = 1400

        for j in range(AQH_CB_NDevices_3):
            AQH_CB_B3[f"D{j+1}"] = D << AQH_CB_Device(
                Nx=AQH_CB_NxVec_3[j], Ny=AQH_CB_NyVec_3[j],
                LengthSR=float(LengthSRVec_CB3[j]), eta=eta,
                Gap=GapVec_CB3[j], FCGap=FCGapVec_CB3[j],
                BendRadius=BendRadius, WgWidth=WgWidth,
                FAGap=FArrayGap_2, InLengthX=InLengthX0, TotLengthX=TotLengthX_GC,
                BendRadiusIO=BendRadius, CouplerON=2,
                OutputIO=True, Euler=1,
                LablePosX=0, LablePosY=-50,
                Layer=AL_Layers.X1P, LayerB=AL_Layers.X1B,
                DeviceID=f"AQH_CB B3 {j+1}")

            if j == 0:
                AQH_CB_B3[f"D{j+1}"].move((StartX, StartY_CB3))
            elif (j+1) % 2 == 0:
                AQH_CB_B3[f"D{j+1}"].mirror_y(0)
                AQH_CB_B3[f"D{j+1}"].ymin = StartY_CB3 - 800
                AQH_CB_B3[f"D{j+1}"].xmin = AQH_CB_B3[f"D{j}"].ports["DR"].center[0] - InLengthX0 - 4.0*BendRadius
            else:
                AQH_CB_B3[f"D{j+1}"].ymin = StartY_CB3 - 800
                AQH_CB_B3[f"D{j+1}"].xmin = AQH_CB_B3[f"D{j}"].ports["DR"].center[0] - InLengthX0 - 2.25*BendRadius
    
        #----------------------------------------------------------------------
        # AQH_CB Block 4 (5x5)
        #----------------------------------------------------------------------

        AQH_CB_B4: dict = {}

        AQH_CB_NDevices_4 = 3
        AQH_CB_NxVec_4   = np.array([5, 5, 5, 5])
        AQH_CB_NyVec_4   = np.array([5, 5, 5, 5])
        LengthSRVec_CB4  = np.array([20, 30, 20, 30])
        GapVec_CB4       = np.array([0.30, 0.30, 0.30, 0.30])
        FCGapVec_CB4     = np.array([0.50, 0.65, 0.55, 0.65])

        StartY_CB4 = StartY_CB3 - 1400
        TotLengthX_GC = 1100

        for j in range(AQH_CB_NDevices_4):
            AQH_CB_B4[f"D{j+1}"] = D << AQH_CB_Device(
                Nx=AQH_CB_NxVec_4[j], Ny=AQH_CB_NyVec_4[j],
                LengthSR=float(LengthSRVec_CB4[j]), eta=eta,
                Gap=GapVec_CB4[j], FCGap=FCGapVec_CB4[j],
                BendRadius=BendRadius, WgWidth=WgWidth,
                FAGap=FArrayGap_2, InLengthX=InLengthX0, TotLengthX=TotLengthX_GC,
                BendRadiusIO=BendRadius, CouplerON=2,
                OutputIO=True, Euler=1,
                LablePosX=10, LablePosY=40,
                Layer=AL_Layers.X1P, LayerB=AL_Layers.X1B,
                DeviceID=f"AQH_CB B4 {j+1}")

            if j == 0:
                AQH_CB_B4[f"D{j+1}"].move((StartX, StartY_CB4))
            elif (j+1) % 2 == 0:
                AQH_CB_B4[f"D{j+1}"].mirror_y(0)
                AQH_CB_B4[f"D{j+1}"].ymin = StartY_CB4 - 480
                AQH_CB_B4[f"D{j+1}"].xmin = AQH_CB_B4[f"D{j}"].ports["DR"].center[0] - InLengthX0 -4.5*BendRadius
            else:
                AQH_CB_B4[f"D{j+1}"].ymin = StartY_CB4 - 620
                AQH_CB_B4[f"D{j+1}"].xmin = AQH_CB_B4[f"D{j}"].ports["DR"].center[0] - InLengthX0 - 1.5*BendRadius
                
        #----------------------------------------------------------------------
        # AQH_CB Block 5 (7x7, CouplerON=2)
        #----------------------------------------------------------------------

        AQH_CB_B5: dict = {}

        AQH_CB_NDevices_5 = 3
        AQH_CB_NxVec_5   = np.array([7, 7, 5, 7])
        AQH_CB_NyVec_5   = np.array([7, 7, 7, 7])
        LengthSRVec_CB5  = np.array([20, 20, 20, 30])
        GapVec_CB5       = np.array([0.30, 0.30, 0.30, 0.30])
        FCGapVec_CB5     = np.array([0.50, 0.65, 0.55, 0.65])

        StartY_CB5 = StartY_CB4 - 880
        TotLengthX_GC = 1200

        for j in range(AQH_CB_NDevices_5):
            if (j+1)==3: #special case for this block
                TotLengthX_GC = 1000
            AQH_CB_B5[f"D{j+1}"] = D << AQH_CB_Device(
                Nx=AQH_CB_NxVec_5[j], Ny=AQH_CB_NyVec_5[j],
                LengthSR=float(LengthSRVec_CB5[j]), eta=eta,
                Gap=GapVec_CB5[j], FCGap=FCGapVec_CB5[j],
                BendRadius=BendRadius, WgWidth=WgWidth,
                FAGap=FArrayGap_2, InLengthX=InLengthX0, TotLengthX=TotLengthX_GC,
                BendRadiusIO=BendRadius, CouplerON=2,
                OutputIO=True, Euler=1,
                LablePosX=10, LablePosY=30,
                Layer=AL_Layers.X1P, LayerB=AL_Layers.X1B,
                DeviceID=f"AQH_CB B5 {j+1}")

            if j == 0:
                AQH_CB_B5[f"D{j+1}"].move((StartX, StartY_CB5))
            elif (j+1) % 2 == 0:
                AQH_CB_B5[f"D{j+1}"].mirror_y(0)
                AQH_CB_B5[f"D{j+1}"].ymin = StartY_CB5 - 760
                AQH_CB_B5[f"D{j+1}"].xmin = AQH_CB_B5[f"D{j}"].ports["DR"].center[0] - InLengthX0 + 2*BendRadius
            else:
                AQH_CB_B5[f"D{j+1}"].ymin = StartY_CB5 - 1000
                AQH_CB_B5[f"D{j+1}"].xmin = AQH_CB_B5[f"D{j}"].ports["DR"].center[0] - InLengthX0 + 3.0*BendRadius
                
        #----------------------------------------------------------------------
        # Serpentine Loss Wg GC #3
        #----------------------------------------------------------------------
        
        TotLengthX = DieWidth - 168
        MidLengthX = TotLengthX
        InLengthX  = MidLengthX
        
        StartY_SLW_GC_3 = StartY_CB5 - 1020

        SLW_GC["D3"] = D << SurpentineLossWg(WgWidth=WgWidth,TotLengthX=TotLengthX, MidLengthX=MidLengthX,
                                            InLengthX=InLengthX, BendRadiusIO=BendRadius,DeviceID=f"L {3*TotLengthX} + 2pi x R")
        SLW_GC["D3"].move((StartX, StartY_SLW_GC_3))
        
        #----------------------------------------------------------------------
        # AQH_Rot Block 1
        #----------------------------------------------------------------------

        AQH_Rot_B1: dict = {}

        AQH_Rot_NDevices_1 = 3
        AQH_Rot_NxVec_1   = np.array([7, 7, 7, 7])
        AQH_Rot_NyVec_1   = np.array([7, 7, 7, 7])
        LengthSRVec_Rot1  = np.array([20, 30, 20, 30])
        GapVec_Rot1       = np.array([0.30, 0.30, 0.30, 0.30])
        FCGapVec_Rot1     = np.array([0.50, 0.65, 0.55, 0.65])

        StartY_Rot1 = StartY_SLW_GC_3 - 350

        for j in range(AQH_Rot_NDevices_1):
            if (j+1)==3: #special case for this block
                TotLengthX_GC = 1000
            
            AQH_Rot_B1[f"D{j+1}"] = D << AQH_Device_Rot(
                Nx=AQH_Rot_NxVec_1[j], Ny=AQH_Rot_NyVec_1[j],
                LengthSR=float(LengthSRVec_Rot1[j]), eta=eta,
                Gap=GapVec_Rot1[j], FCGap=FCGapVec_Rot1[j],
                BendRadius=BendRadius, WgWidth=WgWidth,
                FAGap=FArrayGap_2, InLengthX=InLengthX0, TotLengthX=TotLengthX_GC,
                BendRadiusIO=BendRadius, CouplerON=2,
                OutputIO=True, Euler=1,
                LablePosX=50, LablePosY=40,
                Layer=AL_Layers.X1P, LayerB=AL_Layers.X1B,
                DeviceID=f"AQH_Rot B1 {j+1}")

            if j == 0:
                AQH_Rot_B1[f"D{j+1}"].move((StartX, StartY_Rot1))
            elif (j+1) % 2 == 0:
                AQH_Rot_B1[f"D{j+1}"].mirror_y(0)
                AQH_Rot_B1[f"D{j+1}"].ymin = StartY_Rot1 - 830
                AQH_Rot_B1[f"D{j+1}"].xmin = AQH_Rot_B1[f"D{j}"].ports["DR"].center[0] - InLengthX0 + 3.0*BendRadius
            else:
                AQH_Rot_B1[f"D{j+1}"].ymin = StartY_Rot1 - 930
                AQH_Rot_B1[f"D{j+1}"].xmin = AQH_Rot_B1[f"D{j}"].ports["DR"].center[0] - InLengthX0 + 7.0*BendRadius
                
        #----------------------------------------------------------------------
        # AQH_Rot Block 2
        #----------------------------------------------------------------------

        AQH_Rot_B2: dict = {}

        AQH_Rot_NDevices_2 = 2
        AQH_Rot_NxVec_2   = np.array([9, 9, 5, 7])
        AQH_Rot_NyVec_2   = np.array([9, 9, 5, 7])
        LengthSRVec_Rot2  = np.array([20, 20, 30, 30])
        GapVec_Rot2       = np.array([0.30, 0.30, 0.30, 0.30])
        FCGapVec_Rot2     = np.array([0.50, 0.65, 0.55, 0.65])

        StartY_Rot2 = StartY_Rot1 - 1100
        TotLengthX_GC = 1180

        for j in range(AQH_Rot_NDevices_2):
            AQH_Rot_B2[f"D{j+1}"] = D << AQH_Device_Rot(
                Nx=AQH_Rot_NxVec_2[j], Ny=AQH_Rot_NyVec_2[j],
                LengthSR=float(LengthSRVec_Rot2[j]), eta=eta,
                Gap=GapVec_Rot2[j], FCGap=FCGapVec_Rot2[j],
                BendRadius=BendRadius, WgWidth=WgWidth,
                FAGap=FArrayGap_2, InLengthX=InLengthX0, TotLengthX=TotLengthX_GC,
                BendRadiusIO=BendRadius, CouplerON=2,
                OutputIO=True, Euler=1,
                LablePosX=80, LablePosY=40,
                Layer=AL_Layers.X1P, LayerB=AL_Layers.X1B,
                DeviceID=f"AQH_Rot B2 {j+1}")

            if j == 0:
                AQH_Rot_B2[f"D{j+1}"].move((StartX, StartY_Rot2))
            elif (j+1) % 2 == 0:
                AQH_Rot_B2[f"D{j+1}"].mirror_y(0)
                AQH_Rot_B2[f"D{j+1}"].ymin = StartY_Rot2 - 1000
                AQH_Rot_B2[f"D{j+1}"].xmin = AQH_Rot_B2[f"D{j}"].ports["DR"].center[0] - InLengthX0 + 4.0*BendRadius
            else:
                AQH_Rot_B2[f"D{j+1}"].ymin = StartY_Rot2 - 830
                AQH_Rot_B2[f"D{j+1}"].xmin = AQH_Rot_B2[f"D{j}"].ports["DR"].center[0] - InLengthX0 + 3.0*BendRadius
                
        #----------------------------------------------------------------------
        # AQH_Rot Block 3
        #----------------------------------------------------------------------

        AQH_Rot_B3: dict = {}

        AQH_Rot_NDevices_3 = 4
        AQH_Rot_NxVec_3   = np.array([5, 5, 5, 5])
        AQH_Rot_NyVec_3   = np.array([5, 5, 5, 5])
        LengthSRVec_Rot3  = np.array([30, 20, 30, 20])
        GapVec_Rot3       = np.array([0.30, 0.30, 0.30, 0.30])
        FCGapVec_Rot3     = np.array([0.50, 0.65, 0.55, 0.65])

        StartY_Rot3 = StartY_Rot2 - 1250
        TotLengthX_GC = 870

        for j in range(AQH_Rot_NDevices_3):
            AQH_Rot_B3[f"D{j+1}"] = D << AQH_Device_Rot(
                Nx=AQH_Rot_NxVec_3[j], Ny=AQH_Rot_NyVec_3[j],
                LengthSR=float(LengthSRVec_Rot3[j]), eta=eta,
                Gap=GapVec_Rot3[j], FCGap=FCGapVec_Rot3[j],
                BendRadius=BendRadius, WgWidth=WgWidth,
                FAGap=FArrayGap_2, InLengthX=InLengthX0, TotLengthX=TotLengthX_GC,
                BendRadiusIO=BendRadius, CouplerON=2,
                OutputIO=True, Euler=1,
                LablePosX=0, LablePosY=-20,
                Layer=AL_Layers.X1P, LayerB=AL_Layers.X1B,
                DeviceID=f"AQH_Rot B3 {j+1}")

            if j == 0:
                AQH_Rot_B3[f"D{j+1}"].move((StartX, StartY_Rot3))
            elif (j+1) % 2 == 0:
                AQH_Rot_B3[f"D{j+1}"].mirror_y(0)
                if j == 3:
                    AQH_Rot_B3[f"D{j+1}"].ymin = StartY_Rot3 - 780 
                else: 
                    AQH_Rot_B3[f"D{j+1}"].ymin = StartY_Rot3 - 680
                AQH_Rot_B3[f"D{j+1}"].xmin = AQH_Rot_B3[f"D{j}"].ports["DR"].center[0] - InLengthX0 + 2.5*BendRadius
            else:
                AQH_Rot_B3[f"D{j+1}"].ymin = StartY_Rot3 - 900 
                AQH_Rot_B3[f"D{j+1}"].xmin = AQH_Rot_B3[f"D{j}"].ports["DR"].center[0] - InLengthX0 + 1.0*BendRadius
            
        #----------------------------------------------------------------------
        # AQH_Rot Block 4
        #----------------------------------------------------------------------

        AQH_Rot_B4: dict = {}

        AQH_Rot_NDevices_4 = 3
        AQH_Rot_NxVec_4   = np.array([7, 7, 7, 7])
        AQH_Rot_NyVec_4   = np.array([7, 7, 7, 7])
        LengthSRVec_Rot4  = np.array([20, 30, 20, 30])
        GapVec_Rot4       = np.array([0.30, 0.30, 0.30, 0.30])
        FCGapVec_Rot4     = np.array([0.50, 0.65, 0.55, 0.65])

        StartY_Rot4 = StartY_Rot3 - 1150
        InLengthX0 = 200
        TotLengthX_GC = 1130

        for j in range(AQH_Rot_NDevices_4):
            AQH_Rot_B4[f"D{j+1}"] = D << AQH_Device_Rot(
                Nx=AQH_Rot_NxVec_4[j], Ny=AQH_Rot_NyVec_4[j],
                LengthSR=float(LengthSRVec_Rot4[j]), eta=eta,
                Gap=GapVec_Rot4[j], FCGap=FCGapVec_Rot4[j],
                BendRadius=BendRadius, WgWidth=WgWidth,
                FAGap=FArrayGap_2, InLengthX=InLengthX0, TotLengthX=TotLengthX_GC,
                BendRadiusIO=BendRadius, CouplerON=2,
                OutputIO=True, Euler=1,
                LablePosX=0, LablePosY=20,
                Layer=AL_Layers.X1P, LayerB=AL_Layers.X1B,
                DeviceID=f"AQH_Rot B4 {j+1}")

            if j == 0:
                AQH_Rot_B4[f"D{j+1}"].move((StartX, StartY_Rot4))
            elif (j+1) % 2 == 0:
                AQH_Rot_B4[f"D{j+1}"].mirror_y(0)
                AQH_Rot_B4[f"D{j+1}"].ymin = StartY_Rot4 - 820
                AQH_Rot_B4[f"D{j+1}"].xmin = AQH_Rot_B4[f"D{j}"].ports["DR"].center[0] - InLengthX0 + 2.0*BendRadius
            else:
                AQH_Rot_B4[f"D{j+1}"].ymin = StartY_Rot4 - 830
                AQH_Rot_B4[f"D{j+1}"].xmin = AQH_Rot_B4[f"D{j}"].ports["DR"].center[0] - InLengthX0 + 6.0*BendRadius
                
        #----------------------------------------------------------------------
        # Serpentine Loss Wg GC - NCurves sweep (D13 onward)
        #----------------------------------------------------------------------

        TotLengthX_SLW = DieWidth - 168
        SLW_GapY       = 30
        NCurves_vec    = [1, 2, 3, 4, 5, 6, 7, 8]   # tune as needed
        
        StartY_LossWg_2 =StartY_Rot4 - 1040

        for i, NC in enumerate(NCurves_vec):
            key = f"D{13+i}"
            TotalLength = (NC + 1) * TotLengthX_SLW + NC * np.pi * BendRadius

            SLW_GC[key] = D << SurpentineLossWg(
                WgWidth      = WgWidth,
                TotLengthX   = TotLengthX_SLW,
                InLengthX    = TotLengthX_SLW,
                MidLengthX   = TotLengthX_SLW,
                NCurves      = NC,
                OutIOOn      = False,
                BendRadiusIO = BendRadius,
                TaperOn      = False,
                DeviceID     = f"L {TotalLength:.0f}",
                Layer        = AL_Layers.X1P)

            SLW_GC[key].xmin = StartX
            if i == 0:
                SLW_GC[key].ymax = StartY_LossWg_2
            else:
                SLW_GC[key].ymax = SLW_GC[f"D{13+i-1}"].ymin - SLW_GapY
                
        #----------------------------------------------------------------------
        # Bend Loss GC - BendRadius sweep
        #----------------------------------------------------------------------

        BendRadius_vec = list(reversed([100,125,150,175,200]))
        BendLoss_GapX   = 30
        
        StartY_BendLoss = StartY_LossWg_2 - 2670

        BendLoss_GC: dict = {}

        for i, BR in enumerate(BendRadius_vec):
            key = f"D{i+1}"

            BendLoss_GC[key] = D << IO2(
                LengthX    = 4*BR,
                LengthY    = 2*BR,
                BendRadius = BR,
                WgWidth    = WgWidth,
                CouplerOn  = 2,
                Euler= 0,
                Layer      = AL_Layers.X1P)

            BendLoss_GC[key].ymin = StartY_BendLoss
            if i == 0:
                BendLoss_GC[key].xmin = StartX
            else:
                BendLoss_GC[key].xmin = BendLoss_GC[f"D{i}"].xmax + BendLoss_GapX
                
        #----------------------------------------------------------------------
        # Serpentine Loss Wg GC - BendRadius sweep (NCurves=1)
        #----------------------------------------------------------------------

        TotLengthX_SLW2 = DieWidth - 268 + 50
        SLW_GapY2       = 30
        BendRadius_SLW  = [10, 15, 20, 40, 50, 80]

        StartY_LossWg_3 = StartY_BendLoss - 30

        SLW_BR_GC: dict = {}

        for i, BR in enumerate(BendRadius_SLW):
            key = f"D{i+1}"
            TotalLength = 2 * TotLengthX_SLW2 + np.pi * BR

            SLW_BR_GC[key] = D << SurpentineLossWg(
                WgWidth      = WgWidth,
                TotLengthX   = TotLengthX_SLW2,
                InLengthX    = TotLengthX_SLW2,
                MidLengthX   = TotLengthX_SLW2,
                NCurves      = 2,
                OutIOOn      = False,
                BendRadiusIO = float(BR),
                TaperOn      = False,
                DeviceID     = f"L {TotalLength:.0f} R{BR}",
                Layer        = AL_Layers.X1P)

            SLW_BR_GC[key].move((StartX + SLW_BR_GC[key].ports["IN"].center[0]+50, 0))
            if i == 0:
                SLW_BR_GC[key].ymax = StartY_LossWg_3
            else:
                SLW_BR_GC[key].ymax = SLW_BR_GC[f"D{i}"].ymin - SLW_GapY2
        
        #----------------------------------------------------------------------
        # OneD devices
        #----------------------------------------------------------------------

        N_OneD_Device   = 4
        OneD_NxVec      = [2,    3,    4,    5  ]
        OneD_LXVec      = [20,   20,   30,   30  ]
        OneD_LYVec      = [20,   20,   30,   30  ]
        OneD_GapVec     = [0.30, 0.30, 0.30, 0.30]
        OneD_FCGapVec   = [0.50, 0.65, 0.55, 0.65]
        OneD_StartXVec  = [100,  630,  1360,  2300 ]
        OneD_StartYVec  = [280, 330, 280, 330]
        OneD_TotLenXVec = [500, 700, 900, 1050]
        OneD_InLenXVec  = [150,200,200,150]

        OneD_B1: dict = {}

        for i in range(N_OneD_Device):
            key = f"D{i+1}"
            OneD_B1[key] = D << OneD_Device(
                Nx          = OneD_NxVec[i],
                LengthX     = OneD_LXVec[i],
                LengthY     = OneD_LYVec[i],
                BendRadius  = BendRadius,
                WgWidth     = WgWidth,
                Gap         = OneD_GapVec[i],
                FCGap       = OneD_FCGapVec[i],
                FAGap       = FArrayGap,
                InLengthX   = OneD_InLenXVec[i],
                TotLengthX  = OneD_TotLenXVec[i],
                BendRadiusIO= BendRadius,
                CouplerON   = 3,
                OutputIO    = True,
                Euler       = 1,
                LablePosX   = -300,
                LablePosY   = 200,
                Layer       = AL_Layers.X1P,
                LayerB      = AL_Layers.X1B,
                DeviceID    = f"1D B1 {key}")

            OneD_B1[key].move((OneD_StartXVec[i], OneD_StartYVec[i]))

        #----------------------------------------------------------------------
        # Directional Coupler Block 1
        #----------------------------------------------------------------------

        DirC_NDevices    = 5
        DirC_GapVec      = [0.150, 0.20, 0.250, 0.300, 0.350]
        DirC_CLenVec     = [20,   20,   20,   20, 20]
        DirC_InLenXVec   = [100,  100,  100,  100, 100 ]
        DirC_StartXVec   = [3400,  3400, 3180,  3410, 3380]
        DirC_StartYVec   = [5100, 5960, 8500, 8500, 9870]

        DirC_B1: dict = {}

        for i in range(DirC_NDevices):
            key = f"D{i+1}"
            DirC_B1[key] = D << DirCoupler_Device(
                WgWidth        = WgWidth,
                Gap            = DirC_GapVec[i],
                CouplingLength = DirC_CLenVec[i],
                InLengthX      = DirC_InLenXVec[i],
                BendRadius     = BendRadius,
                FAGap          = FArrayGap,
                TaperOn        = False,
                Euler          = 1,
                Layer          = AL_Layers.X1P,
                DeviceID       = f"DirC B1 {key}")
            DirC_B1[key].mirror_x(0)
            DirC_B1[key].move((DirC_StartXVec[i], DirC_StartYVec[i]))
            
        #----------------------------------------------------------------------
        # Characterization Ring
        #----------------------------------------------------------------------
        
        
                
        
        #------------------------------
        # Return
        #------------------------------

    return D

#------------------------------
# Test
#------------------------------
if __name__ == "__main__":
    c = Die5()
    c.write_gds("Die5_test.gds")
    print("Written Die5_test.gds")
    c.show()
    c.plot()
