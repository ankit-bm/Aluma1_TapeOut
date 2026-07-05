# Die4_GC.py
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

import gdsfactory as gf
gf.CONF.max_cellname_length = 35
gf.gpdk.PDK.activate()

from AL_Die_Frame import AL_Die_Frame

from ADF_RIO import ADF_RIO
from APF_Pulley import APF_Pulley
from SurpentineLossWg import SurpentineLossWg

###########################################################################################
# Device Configurations
###########################################################################################

ConfigFile        = "Device_Config.xlsx"
APF_10_B1_Config  = pd.read_excel(ConfigFile, sheet_name="APF_10_B1")
APF_25_B1_Config  = pd.read_excel(ConfigFile, sheet_name="APF_25_B1")
APF_75_B1_Config  = pd.read_excel(ConfigFile, sheet_name="APF_75_B1")
APF_100_B1_Config = pd.read_excel(ConfigFile, sheet_name="APF_100_B1")
APF_150_B1_Config = pd.read_excel(ConfigFile, sheet_name="APF_150_B1")
APF_200_B1_Config = pd.read_excel(ConfigFile, sheet_name="APF_200_B1")



###########################################################################################
# Die Outline and Frame
###########################################################################################

@gf.cell
def Die4(
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
    StartX = 30 # grating coupler head 

    die_outline = D << gf.components.rectangle(
                    size=(DieWidth, DieHeight),
                    layer=Layer
                )
    
    FArrayGap_2 = 40
    xl = pd.ExcelFile("Device_Config.xlsx")
    print(xl.sheet_names)
    #----------------------------------------------------------------------
    # Serpentine Loss Wg GC
    #----------------------------------------------------------------------

    TotLengthX_SLW = DieWidth - 168
    SLW_GapY       = 40
    N_LossWg = 1
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
            
    #----------------------------------------------------------------------------------
    # APF10 -25-50-75-100-150-200 B1 W=0.6 WIO=0.6
    #----------------------------------------------------------------------------------

    RowStart     = 0
    RowEnd       = 60
    GC_BufLength = 30
    FArrayGapGC  = 127
    InLengthX    = 50
    NPerRow      = 13
    OffsetX      = 30
    OffsetY      = 20

    RadiusVec = [10, 25, 50, 75,100,150,200]

    APF_GC: dict = {}
    NextRowY =  StartY - 3800 - 100

    for R in RadiusVec:
        Config_GC = pd.read_excel(ConfigFile, sheet_name=f"APF_{R}_B1").iloc[RowStart:RowEnd].reset_index(drop=True)
        NextX     = StartX
        RowStartY = NextRowY + 30
        if R <= 15:
            FArrayGapGC  = 127
            InLengthX    = 50
            BendRadiusIO = 15
            NPerRow      = 20
            OffsetX = 22
        elif R <= 25:
            FArrayGapGC  = 127
            InLengthX    = 85
            BendRadiusIO = 25
            NPerRow      = 20
            OffsetX = 22
        elif R <= 50:
            FArrayGapGC  = 2*127
            InLengthX    = 125
            BendRadiusIO = 50
            NPerRow      = 14
            OffsetX = 25
        elif R <= 75:
            FArrayGapGC  = 2*127
            InLengthX    = 130
            BendRadiusIO = 50
            NPerRow      = 11
            OffsetX = 40
        elif R <= 100:
            FArrayGapGC  = 2*127
            InLengthX    = 130
            BendRadiusIO = 50
            NPerRow      = 10
            OffsetX = 20
        elif R <= 150:
            FArrayGapGC  = 2*127
            InLengthX    = 150
            BendRadiusIO = 75
            NPerRow      = 7
            OffsetX = 50
        else:
            FArrayGapGC  = 3*127
            InLengthX    = 260
            BendRadiusIO = 100
            NPerRow      = 5
            OffsetX      = 80

        for j, row in Config_GC.iterrows():
            key = f"R{R}_D{j+1}"
            APF_GC[key] = D << ADF_RIO(
                                LengthRingX=float(row["LengthRingX"]), 
                                LengthRingY=float(row["LengthRingY"]),
                                WgWidth=float(row["WgWidth"]), 
                                WgWidthIO=WgWidth, Gap=float(row["Gap"]),
                                BendRadius=float(row["BendRadius"]), 
                                BendRadiusIO=BendRadiusIO,
                                InLengthX=InLengthX, 
                                TotLengthX=TotLengthX_GC, 
                                FAGap=FArrayGapGC,
                                TaperOn=False, 
                                OutputIO=False, 
                                Euler=0, 
                                BufLength=GC_BufLength,
                                InIO=2, 
                                OutIO=2, 
                                Layer=AL_Layers.X1P, 
                                LablePosX=-50, 
                                LablePosY=30,
                                DeviceID=f"APF{R}-B1-{j+1}")
            
            if j % NPerRow == 0 and j != 0:
                NextX     = StartX 
                RowStartY = NextRowY
            APF_GC[key].xmin = NextX
            APF_GC[key].ymin = RowStartY
            if R <20:
                NextX    = APF_GC[key].xmax + 50
            else:
                NextX    = APF_GC[key].xmax - InLengthX/2 + OffsetX 
            NextRowY = max(NextRowY, APF_GC[key].ymax+OffsetY)
            
    # ----------------------------------------------------------------------------------
    # ADF 10-25 B1 W=0.6 WIO=0.6
    # ----------------------------------------------------------------------------------

    RowStart      = 0
    RowEnd        = 49
    GC_BufLength  = 30
    NPerRow       = 13
    OffsetX       = 30
    RadiusVec_ADF = [200,150,100,75,50,25,10]
    
    OffsetX = 22
    OffsetY = 30

    ADF_GC: dict = {}
    NextRowY_ADF = StartY - 13500 - 100

    for R in RadiusVec_ADF:
        Config_GC = pd.read_excel(ConfigFile, sheet_name=f"ADF_{R}_B1").iloc[RowStart:RowEnd].reset_index(drop=True)
        
        if R <= 15:
            FArrayGapGC  = 127
            InLengthX    = 50
            BendRadiusIO = 15
            NPerRow      = 25
            OffsetX = 22
        elif R <= 25:
            FArrayGapGC  = 127
            InLengthX    = 85
            BendRadiusIO = 25
            NPerRow      = 17
            OffsetX = 22
        elif R <= 50:
            FArrayGapGC  = 2*127
            InLengthX    = 135
            BendRadiusIO = 50
            NPerRow      = 11
            OffsetX = 25
        elif R <= 75:
            FArrayGapGC  = 2*127
            InLengthX    = 135
            BendRadiusIO = 50
            NPerRow      = 9
            OffsetX = 50
        elif R <= 100:
            FArrayGapGC  = 2*127
            InLengthX    = 135
            BendRadiusIO = 50
            NPerRow      = 8
            OffsetX = 50
        elif R <= 150:
            FArrayGapGC  = 2*127
            InLengthX    = 150
            BendRadiusIO = 100
            NPerRow      = 6
            OffsetX = 70
        else:
            FArrayGapGC  = 3*127
            InLengthX    = 260
            BendRadiusIO = 50
            NPerRow      = 5
            OffsetX      = 70

        NextX     = StartX
        RowStartY = NextRowY_ADF + 30

        for j, row in Config_GC.iterrows():
            key = f"R{R}_D{j+1}"
            ADF_GC[key] = D << ADF_RIO(
                LengthRingX  = float(row["LengthRingX"]),
                LengthRingY  = float(row["LengthRingY"]),
                WgWidth      = float(row["WgWidth"]),
                WgWidthIO    = WgWidth,
                Gap          = float(row["Gap"]),
                BendRadius   = float(row["BendRadius"]),
                BendRadiusIO = BendRadiusIO,
                InLengthX    = InLengthX,
                TotLengthX   = TotLengthX_GC,
                FAGap        = FArrayGapGC,
                TaperOn      = False,
                OutputIO     = True,
                Euler        = 0,
                BufLength    = GC_BufLength,
                InIO         = 2,
                OutIO        = 2,
                Layer        = AL_Layers.X1P,
                LablePosX    = -40,
                LablePosY    = 30,
                DeviceID     = f"ADF{R}-B1-{j+1}")

            if j % NPerRow == 0 and j != 0:
                NextX     = StartX
                RowStartY = NextRowY_ADF

            ADF_GC[key].xmin = NextX
            ADF_GC[key].ymin = RowStartY
            NextX        = ADF_GC[key].xmax + OffsetX 
            NextRowY_ADF = max(NextRowY_ADF, ADF_GC[key].ymax+ OffsetY)
            
    # ----------------------------------------------------------------------------------
    # APF Pulley 10
    # ----------------------------------------------------------------------------------

    RowStart      = 0
    RowEnd        = 60
    GC_BufLength  = 30
    NPerRow       = 25
    OffsetX       = 22
    OffsetY       = 30
    RadiusVec_APF_Pulley = [100,50,25,10]

    APF_Pulley_GC: dict = {}
    NextRowY_APF_Pulley = NextRowY_ADF - 16880
    for R in RadiusVec_APF_Pulley:
        Config_GC = pd.read_excel(ConfigFile, sheet_name=f"APF_Pulley_{R}").iloc[RowStart:RowEnd].reset_index(drop=True)

        if R <= 15:
            FArrayGapGC  = 127
            InLengthX    = 50
            BendRadiusIO = 15
            NPerRow      = 25
            OffsetX      = 20
        elif R <= 25:
            FArrayGapGC  = 127
            InLengthX    = 85
            BendRadiusIO = 25
            NPerRow      = 17
            OffsetX      = 22
        elif R <= 75:
            FArrayGapGC  = 2*127
            InLengthX    = 135
            BendRadiusIO = 50
            NPerRow      = 11
            OffsetX      = 30
        else:
            FArrayGapGC  = 2*127
            InLengthX    = 150
            BendRadiusIO = 50
            NPerRow      = 9
            OffsetX      = -20

        NextX     = StartX
        RowStartY = NextRowY_APF_Pulley + 30

        for j, row in Config_GC.iterrows():
            key = f"R{R}_D{j+1}"
            APF_Pulley_GC[key] = D << ADF_RIO(
                LengthRingX  = 0,
                LengthRingY  = 0,
                WgWidth      = float(row["WgWidth"]),
                WgWidthIO    = WgWidth,
                Gap          = float(row["Gap"]),
                BendRadius   = float(row["BendRadius"]),
                BendRadiusIO = BendRadiusIO,
                InLengthX    = InLengthX,
                TotLengthX   = TotLengthX_GC,
                FAGap        = FArrayGapGC,
                TaperOn      = False,
                OutputIO     = False,
                Euler        = 0,
                BufLength    = GC_BufLength,
                InIO         = 7,
                OutIO        = 2,
                Layer        = AL_Layers.X1P,
                LablePosX    = -40,
                LablePosY    = 30,
                ThetaC       = float(row["ThetaC"]),
                DeviceID     = f"APF_P_{R}-B1-{j+1}")

            if j % NPerRow == 0 and j != 0:
                NextX     = StartX
                RowStartY = NextRowY_APF_Pulley

            APF_Pulley_GC[key].xmin = NextX
            APF_Pulley_GC[key].ymin = RowStartY
            NextX               = APF_Pulley_GC[key].xmax + OffsetX
            NextRowY_APF_Pulley = max(NextRowY_APF_Pulley, APF_Pulley_GC[key].ymax + OffsetY)
    #------------------------------
    # Return
    #------------------------------

    return D

#------------------------------
# Test
#------------------------------
if __name__ == "__main__":
    c = Die4()
    c.write_gds("Die4_test.gds")
    print("Written Die4_test.gds")
    c.show()
    c.plot()
