# Single_PhC_Block_EC.py
import gdsfactory as gf
import pandas as pd
from AL_Layers import AL_Layers
from ADF_PhC import ADF_PhC

import time
T0 = time.time()

gf.gpdk.PDK.activate()
gf.CONF.max_cellname_length = 35

ConfigFile = "Device_Config_Rings.xlsx"

#----------------------------------------------------------------------------------------------------
# Loading all device before the gf cell
#----------------------------------------------------------------------------------------------------

AllDevices = dict()

def LoadSheet(ConfigFile, Sheet):
    Key = f"{ConfigFile}_{Sheet}"
    if Key not in AllDevices:
        AllDevices[Key] = pd.read_excel(ConfigFile, sheet_name=Sheet).dropna().reset_index(drop=True)
    return AllDevices[Key]


def ReadList(x, dtype=float):
    return [dtype(v.strip()) for v in str(x).split(",")]


#----------------------------------------------------------------------------------------------------
# gf cell
#----------------------------------------------------------------------------------------------------

@gf.cell
def Single_PhC_Block_EC(
    ConfigFile   = ConfigFile,
    ECParams: dict = dict(
        WidthStart = 0.2,
        TaperType  = 1,
        BezierP1   = 0.2,
        BezierP2   = 0.8,
        MarkerOn   = True,
    ),
    InLengthX0   = 1000,
    TotLengthX   = 4000,
    FAGap        = 30,
    BendRadiusIO = 15,
    BufLength    = 30,

    OffsetX_APF:  dict = {"20": 12, "30": 12},
    OffsetY_APF:  dict = {"20": 60, "30": 80},
    OffsetX_APFP: dict = {"20": 12, "30": 12},
    OffsetY_APFP: dict = {"20": 70, "30": 80},
    
    OffsetX_ADF: dict = {"20": 12, "30": 12},
    OffsetY_ADF: dict = {"20": 70, "30": 80},

    RadiusVec    = (20, 30),

    NPerRowAPF:  dict = {"20": 8, "30": 6},
    NPerRowAPFP: dict = {"20": 6, "30": 5},
    NPerRowADF: dict = {"20": 6, "30": 5},
    
    NCapAPF:  dict = {},
    NCapAPFP: dict = {},
    NCapADF: dict = {},

    Layer        = AL_Layers.X1P,
    BlockID      = "B1",
):

    SRB      = gf.Component()
    NextRowY = 0

    StartX    = 0
    LabelPosX = -30
    LabelPosY = 12

    #----------------------------------------------------------------------------------
    # APF
    #----------------------------------------------------------------------------------

    APF_Config_EC = LoadSheet(ConfigFile, "PhC_APF_EC")
    print(f"Sheet load: {time.time()-T0:.2f}s")

    APFs = {}

    for R in RadiusVec:

        Config_R = APF_Config_EC[APF_Config_EC["BendRadius"] == R].reset_index(drop=True)
        Config_R = Config_R.head(NCapAPF.get(str(R), len(Config_R)))
        if Config_R.empty:
            continue

        NPerRow   = NPerRowAPF[str(R)]
        OX        = OffsetX_APF[str(R)]
        OY        = OffsetY_APF[str(R)]
        RowStartY = NextRowY + OY

        for j, row in Config_R.iterrows():

            if j % NPerRow == 0 and j != 0:
                RowStartY = NextRowY + OY

            InLengthX = InLengthX0 + j * (2 * float(row["BendRadius"]) + OX)

            APFs[f"D{j+1}"] = SRB << ADF_PhC(
                A            = ReadList(row["A"], float),
                M            = ReadList(row["M"], int),
                NPoints      = 36000,
                LengthRingX  = 0,
                LengthRingY  = 0,
                WgWidth      = float(row["WgWidth"]),
                WgWidthIO    = float(row["WgWidthIO"]),
                Gap          = float(row["Gap"]),
                BendRadius   = float(row["BendRadius"]),
                BendRadiusIO = BendRadiusIO,
                InLengthX    = InLengthX,
                TotLengthX   = TotLengthX,
                FAGap        = FAGap,
                TaperOn      = True,
                OutputIO     = False,
                LablePosX    = LabelPosX,
                LablePosY    = LabelPosY,
                Euler        = 0,
                BufLength    = BufLength,
                InIO         = 1,
                OutIO        = 2,
                Layer        = Layer,
                ECParams     = ECParams,
                DeviceID     = f"{BlockID} PhC R{R} {j+1}",
            )

            if j == 0:
                APFs[f"D{j+1}"].move((StartX, RowStartY))
            else:
                Y = APFs[f"D{j}"].ports["IN"].center[1] + FAGap
                APFs[f"D{j+1}"].move((StartX, Y))

            NextRowY = max(NextRowY, APFs[f"D{j+1}"].ymax + OY)

    print(f"APF loop done: {time.time()-T0:.2f}s")

    #----------------------------------------------------------------------------------
    # APF Pulley
    #----------------------------------------------------------------------------------

    APFP_Config_EC = LoadSheet(ConfigFile, "PhC_APFP_EC")

    APFPs = {}

    for R in RadiusVec:

        Config_R = APFP_Config_EC[APFP_Config_EC["BendRadius"] == R].reset_index(drop=True)
        Config_R = Config_R.head(NCapAPFP.get(str(R), len(Config_R)))
        if Config_R.empty:
            continue

        NPerRow   = NPerRowAPFP[str(R)]
        OX        = OffsetX_APFP[str(R)]
        OY        = OffsetY_APFP[str(R)]
        RowStartY = NextRowY + OY

        for j, row in Config_R.iterrows():

            if j % NPerRow == 0 and j != 0:
                RowStartY = NextRowY + OY

            InLengthX = InLengthX0 + j * (2 * float(row["BendRadius"]) + OX)
            InLengthX = max(InLengthX0, InLengthX)

            if InLengthX >= TotLengthX:
                InLengthX = InLengthX0

            APFPs[f"D{j+1}"] = SRB << ADF_PhC(
                A            = ReadList(row["A"], float),
                M            = ReadList(row["M"], int),
                LengthRingX  = 0,
                LengthRingY  = 0,
                WgWidth      = float(row["WgWidth"]),
                WgWidthIO    = float(row["WgWidthIO"]),
                Gap          = float(row["Gap"]),
                BendRadius   = float(row["BendRadius"]),
                BendRadiusIO = BendRadiusIO,
                InLengthX    = InLengthX,
                TotLengthX   = TotLengthX,
                FAGap        = FAGap,
                TaperOn      = True,
                OutputIO     = False,
                LablePosX    = LabelPosX,
                LablePosY    = LabelPosY,
                Euler        = 0,
                BufLength    = BufLength,
                InIO         = 6,
                OutIO        = 2,
                Layer        = Layer,
                ECParams     = ECParams,
                DeviceID     = f"{BlockID} PhC P R{R} {j+1}",
            )

            if j == 0:
                APFPs[f"D{j+1}"].move((StartX, RowStartY))
            else:
                Y = APFPs[f"D{j}"].ports["IN"].center[1] + FAGap
                APFPs[f"D{j+1}"].move((StartX, Y))

            NextRowY = max(NextRowY, APFPs[f"D{j+1}"].ymax + OY)

    print(f"APFP loop done: {time.time()-T0:.2f}s")
    
    #----------------------------------------------------------------------------------
    # ADF
    #----------------------------------------------------------------------------------

    ADF_Config_EC = LoadSheet(ConfigFile, "PhC_ADF_EC")

    ADFs = {}
    
    for R in RadiusVec:
        Config_R = ADF_Config_EC[ADF_Config_EC["BendRadius"] == R].reset_index(drop=True)
        Config_R = Config_R.head(NCapADF.get(str(R), len(Config_R)))
        if Config_R.empty:
            continue
        OY   = OffsetY_ADF[str(R)]
        OX   = OffsetX_ADF[str(R)]

        RowStartY = NextRowY + OY
        InLengthX0_R = InLengthX0

        for j, row in Config_R.iterrows():
            if j % 2 == 0:
                InLengthX = InLengthX0_R
            else:
                InLengthX = TotLengthX - InLengthX0_R - 2*float(row["BendRadius"])-32

            ADFs[f"D{j+1}"] = SRB << ADF_PhC(
                A            = ReadList(row["A"], float),
                M            = ReadList(row["M"], int),
                LengthRingX  = 0,
                LengthRingY  = 0,
                WgWidth      = float(row["WgWidth"]),
                WgWidthIO    = float(row["WgWidthIO"]),
                Gap          = float(row["Gap"]),
                BendRadius   = float(row["BendRadius"]),
                BendRadiusIO = BendRadiusIO,
                InLengthX    = InLengthX,
                TotLengthX   = TotLengthX,
                FAGap        = FAGap,
                TaperOn      = True,
                OutputIO     = True,
                LablePosX    = LabelPosX,
                LablePosY    = LabelPosY,
                Euler        = 0,
                BufLength    = BufLength,
                InIO         = 1,
                OutIO        = 4,
                Layer        = Layer,
                ECParams     = ECParams,
                DeviceID     = f"{BlockID} PhC ADF R{R} {j+1}",
            )
            
            if j == 0:
                ADFs[f"D{j+1}"].move((StartX, RowStartY))
            elif j % 2 == 1:
                ADFs[f"D{j+1}"].mirror_x(0)
                ADFs[f"D{j+1}"].mirror_y(0)
                Y = ADFs[f"D{j}"].ports["TH"].center[1] + 3*FAGap
                X = ADFs[f"D{j}"].ports["TH"].center[0]
                ADFs[f"D{j+1}"].move((X, Y))
            else:
                Y = ADFs[f"D{j}"].ports["TH"].center[1] + 1*FAGap
                ADFs[f"D{j+1}"].move((StartX, Y))
                
            InLengthX0_R = InLengthX0_R + 2*float(row["BendRadius"]) + 0*OX +50
            
            NextRowY   =  ADFs[f"D{j+1}"].ymax + OY 

    print(f"ADF loop done: {time.time()-T0:.2f}s")

    return SRB


if __name__ == "__main__":
    c = Single_PhC_Block_EC()
    c.show()
    c.plot()
    c.write_gds("Single_PhC_Block_EC_test.gds")
    print("Written Single_PhC_Block_EC_test.gds")