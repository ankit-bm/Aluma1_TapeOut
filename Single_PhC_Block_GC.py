# Single_PhC_Block_GC.py
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
def Single_PhC_Block_GC(
    ConfigFile   = ConfigFile,
    GCParams: dict = dict(
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
    InLengthX    = 75,
    TotLengthX   = 500,
    FAGap        = 127,
    BendRadiusIO = 15,
    BufLength    = 30,

    OffsetX_APF:  dict = {"20": 25, "30": 25},
    OffsetY_APF:  dict = {"20": 20, "30": 20},
    OffsetX_APFP: dict = {"20": 25, "30": 25},
    OffsetY_APFP: dict = {"20": 20, "30": 20},

    RadiusVec    = (20, 30),

    NPerRowAPF:  dict = {"20": 25, "30": 25},
    NPerRowAPFP: dict = {"20": 25, "30": 25},

    NCapAPF:  dict = {"20": 25, "30": 25},
    NCapAPFP: dict = {"20": 25, "30": 25},

    Layer        = AL_Layers.X1P,
    BlockID      = "B1",
):

    SRB      = gf.Component()
    NextRowY = 0

    #----------------------------------------------------------------------------------
    # APF
    #----------------------------------------------------------------------------------

    APF_Config_GC  = LoadSheet(ConfigFile, "PhC_APF_GC")

    print(f"Sheet load: {time.time()-T0:.2f}s")

    for R in RadiusVec:

        Config_R  = APF_Config_GC[APF_Config_GC["BendRadius"] == R].reset_index(drop=True)
        Config_R  = Config_R.head(NCapAPF.get(str(R), len(Config_R)))
        if Config_R.empty:
            continue

        NPerRow   = NPerRowAPF[str(R)]
        OX        = OffsetX_APF[str(R)]
        OY        = OffsetY_APF[str(R)]
        NextX     = 0
        RowStartY = NextRowY + OY

        for j, row in Config_R.iterrows():
            if j % NPerRow == 0 and j != 0:
                NextX     = 0
                RowStartY = NextRowY + OY

            Dev = SRB << ADF_PhC(
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
                TaperOn      = False,
                OutputIO     = False,
                LablePosX    = -30,
                LablePosY    = -60,
                Euler        = 0,
                BufLength    = BufLength,
                InIO         = 2,
                OutIO        = 2,
                Layer        = Layer,
                GCParams     = GCParams,
                DeviceID     = f"{BlockID} PhC R{R} {j+1}",
            )
            Dev.xmin = NextX
            Dev.ymin = RowStartY
            NextX    = Dev.xmax + OX
            NextRowY = max(NextRowY, Dev.ymax + OY)

    print(f"APF loop done: {time.time()-T0:.2f}s")

    #----------------------------------------------------------------------------------
    # APF Pulley
    #----------------------------------------------------------------------------------

    APFP_Config_GC = LoadSheet(ConfigFile, "PhC_APFP_GC")

    for R in RadiusVec:
        Config_R  = APFP_Config_GC[APFP_Config_GC["BendRadius"] == R].reset_index(drop=True)
        Config_R  = Config_R.head(NCapAPFP.get(str(R), len(Config_R)))
        if Config_R.empty:
            continue

        NPerRow   = NPerRowAPFP[str(R)]
        OX        = OffsetX_APFP[str(R)]
        OY        = OffsetY_APFP[str(R)]
        NextX     = 0
        RowStartY = NextRowY + OY

        for j, row in Config_R.iterrows():
            if j % NPerRow == 0 and j != 0:
                NextX     = 0
                RowStartY = NextRowY + OY

            Dev = SRB << ADF_PhC(
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
                TaperOn      = False,
                OutputIO     = False,
                LablePosX    = -30,
                LablePosY    = -60,
                Euler        = 0,
                BufLength    = BufLength,
                InIO         = 7,
                OutIO        = 2,
                Layer        = Layer,
                GCParams     = GCParams,
                DeviceID     = f"{BlockID} PhC P R{R} {j+1}",
            )
            Dev.xmin = NextX
            Dev.ymin = RowStartY
            NextX    = Dev.xmax + OX
            NextRowY = max(NextRowY, Dev.ymax + OY)

    print(f"APFP loop done: {time.time()-T0:.2f}s")

    return SRB


if __name__ == "__main__":
    c = Single_PhC_Block_GC()
    c.show()
    c.plot()
    c.write_gds("Single_PhC_Block_GC_test.gds")
    print("Written Single_PhC_Block_GC_test.gds")