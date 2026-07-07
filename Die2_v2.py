# Die2_v2.py
import gdsfactory as gf
import numpy as np
import pandas as pd
import os

from AL_Layers import AL_Layers
from SurpentineLossWg import SurpentineLossWg
from Single_Ring_Block_EC import Single_Ring_Block_EC
from Single_PhC_Block_EC import Single_PhC_Block_EC

gf.gpdk.PDK.activate()
gf.CONF.max_cellname_length = 35

ConfigFile = "Device_Config_Rings.xlsx"

@gf.cell
def Die2(DieWidth = 4468, DieHeight = 20780, TaperLength = 400, Layer = AL_Layers.CHS,):

    D      = gf.Component()
    StartX = 0
    StartY = 75
    FAGap  = 25
    Debug  = False

    TotLengthX_EC = DieWidth - 2*TaperLength + 10
    
    Debug = False
    DebugFrame = True
    
    MaxY = DieHeight - 80

    if DebugFrame:
        die_outline = D << gf.components.rectangle(size=(DieWidth, DieHeight), layer=Layer)

    #---------------------------------------------------------------------------
    # EC Ring Blocks
    #---------------------------------------------------------------------------

    BlockParams = dict(
        ConfigFile   = ConfigFile,
        InLengthX0   = 1000,
        TotLengthX   = TotLengthX_EC,
        FAGap        = FAGap,
        BendRadiusIO = 15,
        BufLength    = 30,
        OffsetX_APF  = {"30": 30, "40": 30},
        OffsetY_APF  = {"30": 60, "40": 100},
        OffsetX_APFP = {"30": 50, "40": 30},
        OffsetY_APFP = {"30": 30, "40": 115},
        OffsetX_ADF  = {"30": 60, "40": 30},
        OffsetY_ADF  = {"30": 50, "40": 150},
        Layer        = AL_Layers.X1P,
        # NPerRowAPF   = {"30": 6,  "40": 5},
        # NPerRowAPFP  = {"30": 5,  "40": 4},
        # NPerRowADF   = {"30": 4,  "40": 3},
    )
    
    EC_Config_Blocks = pd.read_excel(ConfigFile, sheet_name="ECParams")
    print(EC_Config_Blocks)
    print(EC_Config_Blocks.columns.tolist())
    
    EC_RowStart = 2
    EC_RowEnd   = 3
    EC_Config_Blocks = EC_Config_Blocks.iloc[EC_RowStart:EC_RowEnd]

    BlockGapY = 50
    NextY     = StartY

    row = EC_Config_Blocks.iloc[0]
    BlockNo  = int(row["BlockNo"])
    ECParams = dict(
        WidthStart = float(row["WidthStart"]),
        TaperType  = int(row["Type"]),
        BezierP1   = 0.2,
        BezierP2   = 0.8,
        MarkerOn   = True,
    )
    RadiusVec = (30, 40)          # remaining part from Die1
    Path      = f"EC_RingBlock_B{BlockNo}.gds"

    if not Debug and os.path.exists(Path):
        print(f"B{BlockNo} loaded from saved gds")
        B = D << gf.import_gds(Path)
    else:
        print(f"B{BlockNo} computing...")
        Block = Single_Ring_Block_EC(ECParams=ECParams, BlockID=f"B{BlockNo}", RadiusVec=RadiusVec, **BlockParams)
        Block.write_gds(Path)
        B = D << Block

    B.xmin = StartX
    B.ymin = NextY
    NextY  = B.ymax + BlockGapY
    
    #---------------------------------------------------------------------------
    # EC PhC Block
    #---------------------------------------------------------------------------

    PhC_EC_RowStart = 0
    PhC_EC_RowEnd   = 3

    BlockParamsPhC = dict(
        ConfigFile   = ConfigFile,
        InLengthX0   = 200,
        TotLengthX   = TotLengthX_EC,
        NPoints      = 4*36000,
        FAGap        = FAGap,
        BendRadiusIO = 15,
        BufLength    = 30,

        OffsetX_APF  = {"20": 20, "30": 20},
        OffsetY_APF  = {"20": 50, "30": 75},
        OffsetX_APFP = {"20": 20, "30": 20},
        OffsetY_APFP = {"20": 30, "30": 95},
        
        OffsetX_ADF = {"20": 20, "30": 20},
        OffsetY_ADF = {"20": 40, "30": 135},

        NPerRowAPF   = {"20": 30, "30":20},
        NPerRowAPFP  = {"20": 25, "30": 25},
        NPerRowADF   = {"20": 20, "30":30},

        NCapAPF      = {"20": 30, "30": 20},
        NCapAPFP     = {"20": 25, "30": 25},
        NCapADF      = {"20": 20, "30": 30},

        Layer        = AL_Layers.X1P,
    )

    PhC_EC_Config_Blocks = pd.read_excel(ConfigFile, sheet_name="ECParams")
    PhC_EC_Config_Blocks = PhC_EC_Config_Blocks.iloc[PhC_EC_RowStart:PhC_EC_RowEnd]

    for j, row in PhC_EC_Config_Blocks.iterrows():

        if NextY >= MaxY:
            break

        BlockNo = int(row["BlockNo"])

        ECParams = dict(
            WidthStart = float(row["WidthStart"]),
            TaperType  = int(row["Type"]),
            BezierP1   = 0.2,
            BezierP2   = 0.8,
            MarkerOn   = True,
        )

        RadiusVec = (20, 30)
        Path      = f"EC_PhC_Block_B{BlockNo}.gds"

        if not Debug and os.path.exists(Path):
            print(f"PhC B{BlockNo} loaded from saved gds")
            B = D << gf.import_gds(Path)
        else:
            print(f"PhC B{BlockNo} computing...")
            Block = Single_PhC_Block_EC(
                ECParams  = ECParams,
                BlockID   = f"B{BlockNo}",
                RadiusVec = RadiusVec,
                **BlockParamsPhC,
            )
            Block.write_gds(Path)
            B = D << Block

        B.xmin = StartX
        B.ymin = NextY
        NextY = B.ymax + BlockGapY
        
    #------------------------------
    # Loss Characterization Wg
    #------------------------------

    LossWgParams = [
        dict(TaperType=1, MarkerOn=True),
        dict(TaperType=2, MarkerOn=True),
        # dict(TaperType=3, MarkerOn=True),
    ]

    NCurveVec   = [(0,1),(4,1),(6,1),]  # (NCurves, NRepeat)
    LossWgGapY  = 25
    WgWidthLoss = 0.6
    LossInLengthX = TotLengthX_EC - 10
    MaxY        = DieHeight - 100

    LossNextY = NextY + BlockGapY -80

    for ECParams in LossWgParams:
        for N, NRepeat in NCurveVec:
            for _ in range(NRepeat):
                if LossNextY >= MaxY:
                    break
                LossLength = (N + 1) * LossInLengthX
                LW = D << SurpentineLossWg(
                    WgWidth      = WgWidthLoss,
                    InLengthX    = LossInLengthX,
                    BendRadiusIO = 15,
                    NCurves      = N,
                    TaperOn      = True,
                    Euler        = 0,
                    LabelX       = 0,
                    LabelY       = 8,
                    Layer        = AL_Layers.X1P,
                    ECParams     = dict(Length=400, **ECParams),
                    DeviceID     = f"L{LossLength}T{ECParams['TaperType']}",
                )
                LW.xmin   = StartX
                LW.ymin   = LossNextY
                LossNextY = LW.ymax + LossWgGapY

    NextY = LossNextY

        
    #------------------------------
    # Return
    #------------------------------

    return D

if __name__ == "__main__":
    c = Die2()
    c.write_gds("Die2_test5.gds")
    print("Written Die2_test5.gds")
    c.show()
    c.plot()