# Die4.py
import gdsfactory as gf
import numpy as np
import pandas as pd
import os

from AL_Layers import AL_Layers
from SurpentineLossWg import SurpentineLossWg
from Single_Ring_Block_GC import Single_Ring_Block_GC
from IO_GC import IO_GC

gf.gpdk.PDK.activate()
gf.CONF.max_cellname_length = 35

@gf.cell
def Die4(DieWidth = 3468, DieHeight = 20780, TaperLength = 400,
        WgWidth = 0.6, Layer = AL_Layers.CHS,):

    D       = gf.Component()
    
    StartX  = 100
    StartY  = 50
    
    FAGap   = 127
    
    BlockGapY = 75
    
    TotLengthX_GC = 3200

    Debug = False
    DebugFrame = False

    if DebugFrame:
        die_outline = D << gf.components.rectangle(size=(DieWidth, DieHeight), layer=Layer)    

    ConfigFile        = "Device_Config_Rings.xlsx"
    
    # How many GC Ring block?
    GC_RowStart = 0
    GC_RowEnd   = 5

    #----------------------------------------------------------------------------------
    # GC Characterization
    #----------------------------------------------------------------------------------

    NPerRow  = 31
    OffsetX  = 23
    OffsetY  = 40
    BendRadiusIO_GC = 15

    GC_Devs: dict = {}
    
    NextRowY = StartY + OffsetY

    Config_GC = pd.read_excel(ConfigFile, sheet_name="IO_GC").dropna().reset_index(drop=True)
    NextX     = StartX
    RowStartY = NextRowY + OffsetY

    for j, row in Config_GC.iterrows():
        key = f"GC_D{j+1}"
        GC_Devs[key] = D << IO_GC(
                            LengthX        = float(row["LengthX"]),
                            FAGap          = FAGap,
                            BendRadius     = BendRadiusIO_GC,
                            WgWidth        = WgWidth,
                            Layer          = AL_Layers.X1P,
                            GCParams     = dict(
                                Pitch          = float(row["GC_Pitch"]),
                                DutyCycle      = float(row["GC_DutyCycle"]),
                                UniformGrating = True,
                                NPeriod        = int(row["GC_NPeriod"]),
                                taper_length   = float(row["GC_TaperLength"]),
                                taper_angle    = float(row["GC_TaperAngle"]),
                                LengthGC       = 100,
                                wavelength     = 1.55,
                                fiber_angle    = 10.0,
                                ),
                            DeviceID       = f"{j+1}"
                        )

        if j % NPerRow == 0 and j != 0:
            NextX     = StartX
            RowStartY = NextRowY

        GC_Devs[key].xmin = NextX
        GC_Devs[key].ymin = RowStartY
        NextX    = GC_Devs[key].xmax + OffsetX
        NextRowY = max(NextRowY, GC_Devs[key].ymax + OffsetY)

        RingBlockStartY = GC_Devs[key].ymax
    
    #---------------------------------------------------------------------------
    # Blocks
    #---------------------------------------------------------------------------

    BlockParams = dict(
        ConfigFile   = ConfigFile,
        InLengthX    = 50,
        TotLengthX   = 500,
        FAGap        = FAGap,
        BendRadiusIO = 15,
        BufLength    = 15,
        OffsetX_APF  = {"15": 13, "20": 12, "30": 13, "40": 13},
        OffsetY_APF  = {"15": 20, "20": 20, "30": 20, "40": 20},
        OffsetX_APFP = {"15": 13, "20": 12, "30": 13, "40": 13},
        OffsetY_APFP = {"15": 20, "20": 20, "30": 20, "40": 20},
        OffsetX_ADF  = {"15": 14, "20": 12, "30": 12, "40": 11 },
        OffsetY_ADF  = {"15": 20, "20": 20, "30": 20, "40": 20},
        Layer        = AL_Layers.X1P,
        NPerRowAPF   = {"15": 26, "20": 24, "30": 21, "40": 18},
        NPerRowAPFP  = {"15": 26, "20": 24, "30": 21, "40": 18},
        NPerRowADF   = {"15": 26, "20": 25, "30": 27, "40": 21},
    )
    
    GC_Config_Blocks = pd.read_excel(ConfigFile, sheet_name="GCParams").dropna().reset_index(drop=True).iloc[GC_RowStart:GC_RowEnd]

    NextY     = RingBlockStartY + BlockGapY

    for j, row in GC_Config_Blocks.iterrows():
        BlockNo  = int(row["BlockNo"])
        GCParams = dict(
            Pitch          = float(row["GC_Pitch"]),
            DutyCycle      = float(row["GC_DutyCycle"]),
            NPeriod        = int(row["GC_NPeriod"]),
            taper_length   = float(row["GC_TaperLength"]),
            taper_angle    = float(row["GC_TaperAngle"]),
            LengthGC       = 50,
            wavelength     = 1.55,
            fiber_angle    = 10.0,
            UniformGrating = True,
        )

        RadiusVec = (15, 20, 30, 40)                 # default — override per block below
        # if BlockNo == 13: RadiusVec = (15, 20)
        # if BlockNo == 11: RadiusVec = (15, 20, 30) # example

        Path = f"GC_RingBlock_B{BlockNo}.gds"

        if not Debug and os.path.exists(Path):
            print(f"B{BlockNo} loaded from saved gds")
            B = D << gf.import_gds(Path)
        else:
            print(f"B{BlockNo} computing...")
            Block = Single_Ring_Block_GC(GCParams=GCParams, BlockID=f"B{BlockNo}", RadiusVec=RadiusVec, **BlockParams)
            Block.write_gds(Path)
            B = D << Block

        B.xmin = StartX
        B.ymin = NextY
        NextY  = B.ymax + BlockGapY
        
    #------------------------------
    # Loss Characterization Wg GC
    #------------------------------

    GC_Loss_Config = pd.read_excel(ConfigFile, sheet_name="GCParams").dropna(subset=["BlockNo"]).reset_index(drop=True)

    NCurveVec     = [(0,2), (2,1), (4,1)] # (NCurves, NRepeat)
    LossWgGapY    = 25
    WgWidthLoss   = 0.6
    LossInLengthX = TotLengthX_GC - 10
    MaxY          = DieHeight - 100

    LossNextY = NextY + BlockGapY - 250

    for j, row in GC_Loss_Config.iterrows():
        GCParamsLoss = dict(
            Pitch          = float(row["GC_Pitch"]),
            DutyCycle      = float(row["GC_DutyCycle"]),
            NPeriod        = int(row["GC_NPeriod"]),
            taper_length   = float(row["GC_TaperLength"]),
            taper_angle    = float(row["GC_TaperAngle"]),
            fiber_angle    = 10.0,
            wavelength     = 1.55,
            LengthGC       = 100,
            UniformGrating = True,
        )

        for N, NRepeat in NCurveVec:
            for k in range(NRepeat):
                if LossNextY >= MaxY:
                    break
                LossLength = (N + 1) * LossInLengthX
                LW = D << SurpentineLossWg(
                    WgWidth      = WgWidthLoss,
                    InLengthX    = LossInLengthX,
                    BendRadiusIO = 15,
                    NCurves      = N,
                    TaperOn      = False,
                    Euler        = 0,
                    LabelX       = 0,
                    LabelY       = 10,
                    Layer        = AL_Layers.X1P,
                    GCParams     = GCParamsLoss,
                    DeviceID     = f"L{LossLength}GC{int(row['BlockNo'])}",
                )
                LW.xmin   = StartX
                LW.ymin   = LossNextY
                LossNextY = LW.ymax + LossWgGapY

    NextY = LossNextY   

    #---------------------------------------------------------------------------
    # Return
    #---------------------------------------------------------------------------
        
    return D

if __name__ == "__main__":
    c = Die4()
    c.write_gds("Die4_test3.gds")
    print("Written Die4_test3.gds")
    c.show()
    c.plot()